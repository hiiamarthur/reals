from typing import Optional, Type
import uuid
from http.client import HTTPException
from app.core.gpt import client, asyncClient
from app.models.gpt_model import (
    APIRequestLog,
    APIUsage,
    Message,
    MessageFilter,
    Session,
    SessionFilter,
)
from app.schemas.gpt_schema import OpenAIHeaders, OpenAIRequest, OpenAIResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from datetime import datetime
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log,
)
import logging
from circuitbreaker import circuit
from openai import RateLimitError, APIError, APIConnectionError
from fastapi import Depends, HTTPException

from app.repositories.gpt_repository import GPTRepository
from app.repositories.base_repository import BaseRepository
from app.models.user_model import User
from app.core.database import get_async_db
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )


class GPTCircuitBreaker:
    FAILURE_THRESHOLD = 5  # Number of failures before opening circuit
    RECOVERY_TIMEOUT = 60  # Seconds to wait before attempting recovery
    EXPECTED_EXCEPTIONS = (RateLimitError, APIError, APIConnectionError)


# @retry(
#     stop=stop_after_attempt(3),
#     wait=wait_exponential(multiplier=1, min=4, max=10),
#     retry=retry_if_exception_type((RateLimitError, APIError, APIConnectionError)),
#     before=before_log(logger, logging.INFO),
#     after=after_log(logger, logging.INFO),
# )
# @circuit(
#     failure_threshold=GPTCircuitBreaker.FAILURE_THRESHOLD,
#     recovery_timeout=GPTCircuitBreaker.RECOVERY_TIMEOUT,
#     expected_exception=GPTCircuitBreaker.EXPECTED_EXCEPTIONS,
# )
# async def call_gpt_api(
#     messages: list, model: str = "gpt-4", **kwargs
# ) -> Dict[str, Any]:
#     """
#     Make API call to GPT with retry and circuit breaker patterns.
#     """
#     try:
#         response = await client.chat.completions.create(
#             model=model, messages=messages, **kwargs
#         )
#         return response
#     except Exception as e:
#         logger.error(f"Error calling GPT API: {str(e)}")
#         raise


class GPTService:

    def __init__(self, db: AsyncSession):
        self.gpt_repository = GPTRepository(db)
        self.session_repo = BaseRepository(Session, db)
        self.message_repo = BaseRepository(Message, db)
        self.user_repo = BaseRepository(User, db)
        self.api_usage_repository = BaseRepository(APIUsage, db)
        self.api_request_log_repository = BaseRepository(APIRequestLog, db)
        self.system_messages = {
            "role": "system",
            "content": (
                "You are an expert dating itinerary planner in Hong Kong. Here is the provided first prompt format:  "
                '{"location": "string", "date": "YYYY-MM-DD","budget": float,"preferences": "string","transportation": "string"}'
                "There may be additional changes in the prompt, change the result accordingly."
                "If the user additional prompt isn't related to the itinerary, just return normal text, otherwise, follow the format below."
                "Response in JSON format:"
                '{"date": "YYYY-MM-DD", '
                '"weather": {"description": "string", "temperature": "string", "conditions": "string"}, '
                '"activities": [{"name": "string", "description": "string", "price": "string", '
                '"place": "string", "transit": {"from": "string", "method": "string", '
                '"estimated_time": "string", "price": "string"}}], '
                '"budget": {"total_activity_cost": "string", "total_transit_cost": "string", '
                '"grand_total": "string"}}. '
                # "Ensure the response adheres strictly to this format."
            ),
        }

    # system_messages = {
    #     "role": "system",
    #     "content": (
    #         "You are an expert dating itinerary planner. Create a romantic and engaging "
    #         "itinerary that maximizes the experience while respecting the budget and preferences. "
    #         "Provide the response in JSON format with the following structure:\n"
    #         "{\n"
    #         '  "date": "YYYY-MM-DD",\n'
    #         '  "weather": {\n'
    #         '    "description": "Brief weather description",\n'
    #         '    "temperature": "Temperature in Celsius",\n'
    #         '    "conditions": "Weather conditions"\n'
    #         "  },\n"
    #         '  "activities": [\n'
    #         "    {\n"
    #         '      "time": "HH:MM",\n'
    #         '      "name": "Activity name",\n'
    #         '      "description": "Detailed description",\n'
    #         '      "price": "Estimated cost",\n'
    #         '      "place": "Location name",\n'
    #         '      "address": "Full address",\n'
    #         '      "transit": {\n'
    #         '        "from": "Previous location",\n'
    #         '        "method": "Transportation method",\n'
    #         '        "estimated_time": "Duration in minutes",\n'
    #         '        "price": "Transit cost"\n'
    #         "      }\n"
    #         "    }\n"
    #         "  ],\n"
    #         '  "budget": {\n'
    #         '    "total_activity_cost": "Total activities cost",\n'
    #         '    "total_transit_cost": "Total transportation cost",\n'
    #         '    "grand_total": "Total cost"\n'
    #         "  },\n"
    #         '  "tips": ["Romantic tip 1", "Romantic tip 2"]\n'
    #         "}"
    #     ),
    # }
    async def check_gpt_avalibility(self):
        """Pre-check for API availability"""
        try:
            # Check model rate limits
            # if model in self.rate_limits:
            #     if self.rate_limits[model]["remaining"] <= 0:
            #         raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # result = await self.gpt_repository.get(APIRequestLog)
            result = await self.api_request_log_repository.get_first()
            if result is None:
                return True
            if (
                result.rate_limit_remaining_tokens <= 0
                or result.rate_limit_remaining_requests <= 0
            ):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Check API key validity
            # This could be a lightweight API call or config check
            if not settings.OPENAI_API_KEY:
                raise HTTPException(status_code=503, detail="API configuration error")

            return True
        except Exception as e:
            logger.error(f"Availability check failed: {e}")
            return False

    async def handle_gpt_user_session(
        self, request: OpenAIRequest, db: AsyncSession = Depends(get_async_db)
    ):
        self.user_repo = BaseRepository(User, db)
        self.session_repo = BaseRepository(Session, db)
        print("handle_gpt_user_session", request)
        if not request.user_id:
            raise HTTPException(status_code=400, detail="Invalid session or user ID")
        if request.session_id:

            result = await self.session_repo.get_first(
                filters={"uuid": request.session_id}, include=["messages"]
            )
            print("result", result.to_dict(), result.messages)
            if result.messages:
                if len(result.messages) <= 10:
                    return result
                else:
                    raise HTTPException(
                        status_code=400, detail="Session messages limit exceeded"
                    )

        else:
            print(
                "create new session",
                request.user_id,
                # request.content,
                # Session(
                #     user_id=request.user_id,
                #     # messages=[Message(role="user", content=request.content)],
                #     # api_usage=APIUsage(
                #     #     total_requests=0,
                #     #     total_tokens=0,
                #     # ),
                # ).to_dict()
                type(db),
            )
            # result = await self.user_repo.create(
            #     {
            #         "email": "test@example.com",
            #         "username": "test",
            #         "hashed_password": "securepassword123",
            #         "is_active": True,
            #         "is_superuser": False,
            #         "profile": {},
            #         "sessions": [],
            #     }
            # )

            result = await self.session_repo.create(
                {
                    "user_id": request.user_id,
                    "messages": [
                        {
                            "role": "user",
                            "content": request.content,
                        }
                    ],
                    "api_usage": {
                        "total_requests": 0,
                        "total_tokens": 0,
                    },
                }
            )
            # with self.user_repo.session() as session:
            # result = await self.user_repo.get_all()
            # result = await self.session_repo.get_all()
            # result = await self.user_repo.get_by_id(6)
            # result = await self.user_repo.get_first(filters={"uuid": request.user_id})

            print("user is", result)
            # result.sessions.append(
            #     Session(
            #         # user_id=request.user_id,
            #         messages=[Message(role="user", content=request.content)],
            #         api_usage=APIUsage(
            #             total_requests=0,
            #             total_tokens=0,
            #         ),
            #     )
            # )
            # await self.user_repo.update(request.user_id, user.to_dict())
            # print("result xd", result.to_dict())
        return result
        return None

    async def post_process(
        self,
        request: OpenAIRequest,
        response: Optional[OpenAIResponse],
        headers: Optional[OpenAIHeaders],
        session: Optional[Session],
        response_code: int,
        log: str,
    ):
        try:
            # Create API request log if we have response and headers
            print("post_process", response, headers, session)
            request_log = await self.api_request_log_repository.create(
                APIRequestLog(
                    session_uuid=request.session_id or session.uuid,
                    response_code=response_code,
                    request_id=response.id if response else None,
                    processing_time_ms=(
                        headers.openai_processing_ms if headers else None
                    ),
                    prompt_tokens=(
                        response.usage.prompt_tokens
                        if response and response.usage
                        else None
                    ),
                    completion_tokens=(
                        response.usage.completion_tokens
                        if response and response.usage
                        else None
                    ),
                    total_tokens=(
                        response.usage.total_tokens
                        if response and response.usage
                        else None
                    ),
                    rate_limit_remaining_requests=(
                        headers.x_ratelimit_remaining_requests if headers else None
                    ),
                    rate_limit_remaining_tokens=(
                        headers.x_ratelimit_remaining_tokens if headers else None
                    ),
                    rate_limit_reset_requests=(
                        headers.x_ratelimit_reset_requests if headers else None
                    ),
                    rate_limit_reset_tokens=(
                        headers.x_ratelimit_reset_tokens if headers else None
                    ),
                    log=log,
                ).to_dict()
            )
            print("request_log xd", request_log)
            # Update session messages if we have a session and response
            # if session and response:
            current_session = await self.session_repo.get_first(
                {"filter_by[uuid][equals]": session.uuid},
                include=["api_usage", "messages", "request_logs"],
            )
            if current_session:
                print("current_session 1")
                # Add user message if this is a new session
                if not request.session_id:
                    current_session.messages.append(
                        Message(
                            session_uuid=session.uuid,
                            role="user",
                            content=request.content,
                        )
                    )
                print("current_session 2")
                # Add assistant message if we have a valid response
                if response and response.choices and len(response.choices) > 0:
                    current_session.messages.append(
                        Message(
                            session_uuid=session.uuid,
                            role=response.choices[0].message.role,
                            content=response.choices[0].message.content,
                        )
                    )

                    current_session.api_usage.total_requests += 1
                    current_session.api_usage.total_tokens += (
                        response.usage.total_tokens
                    )

                    # self.api_usage_repository.update(
                    #     current_session.api_usage.id,
                    #     {
                    #         "total_requests": current_session.api_usage.total_requests
                    #         + 1,
                    #         "total_tokens": current_session.api_usage.total_tokens
                    #         + response.usage.total_tokens,
                    #     },
                    # )
                print("current_session 3")
                current_session.request_logs.append(request_log)
                print("current_session 4")
                # Update the session
                await self.session_repo.update(
                    session.id,
                    {
                        "messages": current_session.messages,
                        "request_logs": current_session.request_logs,
                        "api_usage": current_session.api_usage,
                    },
                )
                print("current_session 5")
        except Exception as e:
            logger.error(f"Error in post_process: {str(e)} ${str(e.__traceback__)}")
            # Don't raise here as this is post-processing
            # Just log the error and continue

    def update_chat_to_table():
        return

    async def insert_table_and_update_tables(
        session: AsyncSession,
        session_id: str,
        role: str,
        content: str,
        request_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        response_code: int,
        processing_time_ms: int,
    ):
        async with session.begin():
            try:
                new_message = Message(
                    session_id=session_id,
                    role=role,
                    content=content,
                    created_at=datetime.utcnow(),
                )
                session.add(new_message)

                new_request_log = APIRequestLog(
                    session_id=session_id,
                    request_id=request_id,
                    response_code=response_code,
                    processing_time_ms=processing_time_ms,
                    request_timestamp=datetime.utcnow(),
                )

                session.add(new_request_log)

                # Calculate total tokens
                total_tokens = prompt_tokens + completion_tokens

                # Insert APIUsage for tracking token usage
                new_api_usage = APIUsage(
                    session_id=session_id,
                    request_id=request_id,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    timestamp=datetime.utcnow(),
                )
                session.add(new_api_usage)

                # Commit the transaction
                await session.commit()
            except Exception as e:
                # Rollback happens automatically in case of an exception
                raise HTTPException(status_code=400, detail=str(e))
            finally:
                session.close()

    def send_command():
        return

    @retry(
        stop=stop_after_attempt(2),  # Strictly 1 retry (2 attempts total)
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(RateLimitError),
        before_sleep=before_sleep_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True,
    )
    async def streamed_request(self, usr_input: str):
        try:
            response_content = ""
            async for chunk in client.chat.completions.with_raw_response.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_messages["content"]},
                    {"role": "user", "content": usr_input},
                ],
                stream=True,
                temperature=0.7,
                max_tokens=1000,
            ):
                if "choices" in chunk:
                    for choice in chunk["choices"]:
                        if "delta" in choice and "content" in choice["delta"]:
                            response_content += choice["delta"]["content"]
            return response_content
        except RateLimitError as e:
            logger.error(f"Rate limit hit, attempt {e}")
            raise HTTPException(
                status_code=500, detail="Service temporarily unavailable after retries"
            )
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @retry(
        stop=stop_after_attempt(1),  # Strictly 1 retry (2 attempts total)
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(RateLimitError),
        before_sleep=before_sleep_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True,
    )
    @circuit(
        failure_threshold=GPTCircuitBreaker.FAILURE_THRESHOLD,
        recovery_timeout=GPTCircuitBreaker.RECOVERY_TIMEOUT,
        expected_exception=GPTCircuitBreaker.EXPECTED_EXCEPTIONS,
    )
    async def async_request(self, request: OpenAIRequest, db):
        try:
            print("async_request")
            await self.check_gpt_avalibility()
            session = await self.handle_gpt_user_session(request, db)
            print("session xd", session.to_dict())
            legacy_response = (
                await asyncClient.chat.completions.with_raw_response.create(
                    model="gpt-4o-mini",
                    messages=[
                        self.system_messages,
                        *[
                            {"role": message.role, "content": message.content}
                            for message in session.messages
                        ],
                        {"role": "user", "content": request.content},
                    ],
                    max_tokens=500,
                )
            )
            # legacy_response = (
            #     await asyncClient.chat.completions.with_raw_response.create(
            #         model="gpt-4o-mini",
            #         messages=[
            #             {"role": "user", "content": "Hello"},
            #         ],
            #         max_tokens=5,
            #     )
            # )

            chat_completetion_response = legacy_response.parse()
            response_dict = {
                "id": chat_completetion_response.id,
                "choices": [
                    {
                        "finish_reason": choice.finish_reason,
                        "index": choice.index,
                        "logprobs": choice.logprobs,
                        "message": {
                            "content": choice.message.content,
                            "role": choice.message.role,
                            "refusal": choice.message.refusal,
                            "function_call": choice.message.function_call,
                            "tool_calls": choice.message.tool_calls,
                        },
                    }
                    for choice in chat_completetion_response.choices
                ],
                "created": chat_completetion_response.created,
                "model": chat_completetion_response.model,
                "object": chat_completetion_response.object,
                "service_tier": chat_completetion_response.service_tier,
                "system_fingerprint": chat_completetion_response.system_fingerprint,
                "usage": {
                    "completion_tokens": chat_completetion_response.usage.completion_tokens,
                    "prompt_tokens": chat_completetion_response.usage.prompt_tokens,
                    "total_tokens": chat_completetion_response.usage.total_tokens,
                    "prompt_tokens_details": chat_completetion_response.usage.prompt_tokens_details,
                    "completion_tokens_details": chat_completetion_response.usage.completion_tokens_details,
                },
            }

            print("response xd", response_dict, legacy_response.headers)
            # res_data = await asyncClient.chat.completions.create(
            #     model="gpt-3.5-turbo",
            #     messages=[self.system_messages, {"role": "user", "content": usr_input}],
            #     stream=False,
            #     temperature=0.7,
            #     # max_tokens=1000,
            #     top_p=0.9,
            #     presence_penalty=0,
            #     frequency_penalty=0,
            # )
            # parsed_response = await self.handle_gpt_request(usr_input)
            response = OpenAIResponse.from_dict(response_dict)
            print("openaiResponse", response)
            headers = OpenAIHeaders.from_headers(legacy_response.headers)
            print("headers", headers)
            await self.post_process(
                request,
                response,
                headers,
                session,
                legacy_response.status_code,
                "Success",
            )
            return response
        except RateLimitError as e:
            logger.error("Rate limit exceeded")
            # await self.post_process(request, None, None, None, 429, str(e))
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            # await self.post_process(request, None, None, None, 500, str(e))
            raise HTTPException(status_code=500, detail=str(e))

    # Function to handle GPT API request and store the response
    async def handle_gpt_request(
        user_id: int, session_id: uuid.UUID, user_input: str, client
    ):
        # Fetch previous messages in session
        messages = fetch_session_messages(session_id)

        # Add current user input to message stack
        messages.append({"role": "user", "content": user_input})

        # Call GPT API
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.9,
            presence_penalty=0,
            frequency_penalty=0,
        )

        # Parse response
        assistant_message = response["choices"][0]["message"]["content"]
        prompt_tokens = response["usage"]["prompt_tokens"]
        completion_tokens = response["usage"]["completion_tokens"]
        total_tokens = response["usage"]["total_tokens"]

        # Add assistant message to session
        add_message_to_session(session_id, "assistant", assistant_message)

        # Track API usage
        rate_limit_reset = datetime.utcfromtimestamp(
            response["headers"]["x-ratelimit-reset-requests"]
        )
        track_api_usage(user_id, prompt_tokens, completion_tokens, rate_limit_reset)

        # Log API request
        log_api_request(
            session_id=session_id,
            request_id=response["id"],
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            rate_limit_remaining_requests=response["headers"][
                "x-ratelimit-remaining-requests"
            ],
            rate_limit_remaining_tokens=response["headers"][
                "x-ratelimit-remaining-tokens"
            ],
        )

        return assistant_message

    async def _handle_gpt_response(self, response):
        """Process GPT response and log usage"""
        parsed_response = response.parse()
        try:
            await self.gpt_repository.log_api_usage(
                usage=parsed_response.usage.model_dump(), headers=response.headers
            )
        except Exception as e:
            # Log but don't fail the request
            logger.error(f"Failed to log GPT usage: {e}")

        return parsed_response

    # async def get_circuit_status():
    #     """
    #     Get the current status of the circuit breaker.
    #     """
    #     return {
    #         "status": self.async_request.circuit_breaker.state,
    #         "failure_count": async_request.circuit_breaker.failure_count,
    #         "last_failure": async_request.circuit_breaker.last_failure,
    #         "last_success": async_request.circuit_breaker.last_success,
    #     }
