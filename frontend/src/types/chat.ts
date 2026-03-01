export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  question: string;
  answer: string;
}
