interface ChatCompletionResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    usage: {
      prompt_tokens: number;
      completion_tokens: number;
      total_tokens: number;
    };
    choices: Array<{
      message: {
        role: string;
        content: string;
      };
      logprobs: null | Record<string, unknown>; // Adjust based on actual logprobs structure if needed
      finish_reason: string;
      index: number;
    }>;
  }