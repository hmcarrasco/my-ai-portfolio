import { API_BASE_URL, API_KEY } from '../constants/config';
import type { ChatRequest, ChatResponse } from '../types/chat';

export async function sendMessage(question: string): Promise<ChatResponse> {
  const body: ChatRequest = { question };

  const res = await fetch(`${API_BASE_URL}/chat/ask`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || 'Failed to get response');
  }

  return res.json();
}
