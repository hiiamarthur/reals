import axios from "axios";
import OpenAI from "openai";
import { openai } from "src/config/gpt";

const systemMessages: OpenAI.Chat.Completions.ChatCompletionMessageParam = {
  role: "system",
  content:
    'You are an expert dating itinerary planner. Provide the response in JSON format with the following structure: {"date": "YYYY-MM-DD", "weather": {"description": "string", "temperature": "string", "conditions": "string"}, "activities": [{"name": "string", "description": "string", "price": "string", "place": "string", "transit": {"from": "string", "method": "string", "estimated_time": "string", "price": "string"}}], "budget": {"total_activity_cost": "string", "total_transit_cost": "string", "grand_total": "string"}. Ensure the response adheres strictly to this format.',
};

export function checkGPTAvaliability(input: any) {}

export function udpateGPTMonitorTable() {}

export function checkGPTUserSession() {}

export async function sendCommand() {
  //   streamedResponse.then((A) => {
  //   })
  // const data: = {
  //     model: 'gpt-4-o',
  //     messages: [{ role: 'user', content: 'Hello' }],
  //     temperature: 0.7
  //   };
  // axios.post(process.env.GPT_API_URL,)
}

async function streamedRequest() {
  const streamedResponse = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      systemMessages,
      {
        role: "user",
        content:
          "In the context of Hong Kong, please plan a date for a couple and produce a detailed itinerary, using the web browsing function to access the latest information, including weather, available activities, trending events, etc. The route should be conveniently located within the same direction. The date should follow the requirements in the below: 1. Date - 31/08/2024 2. Time - whole day 3. Type of date - artistic, music, entertainment, nightlife, adventure 4. Preferred cuisine - decided for me 5. Transit method - public transport 6. Total Budget - 1000 7. Number of activities, excluding meal - 3 8. Location of date - New Territories",
      },
    ],
    stream: true,
    temperature: 0.7,
    max_tokens: 400,
    top_p: 0.9,
    presence_penalty: 0,
    frequency_penalty: 0,
  });

  for await (const chunk of streamedResponse) {
    process.stdout.write(chunk.choices[0]?.delta?.content || "");
  }
}

async function asyncRequest(
  message: OpenAI.Chat.Completions.ChatCompletionMessageParam
) {
  const reponse = await openai.chat.completions.create({
    model: "gpt-4o",

    messages: [
      {
        role: "user",
        content:
          "In the context of Hong Kong, please plan a date for a couple and produce a detailed itinerary, using the web browsing function to access the latest information, including weather, available activities, trending events, etc. The route should be conveniently located within the same direction. The date should follow the requirements in the below: 1. Date - 31/08/2024 2. Time - whole day 3. Type of date - artistic, music, entertainment, nightlife, adventure 4. Preferred cuisine - decided for me 5. Transit method - public transport 6. Total Budget - 1000 7. Number of activities, excluding meal - 3 8. Location of date - New Territories",
      },
    ],
    stream: false,
    temperature: 0.7,
    max_tokens: 400,
    top_p: 0.9,
    presence_penalty: 0,
    frequency_penalty: 0,
  });

  reponse.choices;
}
