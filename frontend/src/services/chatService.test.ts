import { describe, it, expect, vi, beforeEach } from 'vitest';
import { sendMessage } from './chatService';

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

beforeEach(() => {
  vi.clearAllMocks();
});

describe('chatService', () => {
  it('sends a POST request with the question', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ question: 'Hi', answer: 'Hello!' }),
    });

    const result = await sendMessage('Hi');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/chat/ask'),
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: 'Hi' }),
      })
    );
    expect(result).toEqual({ question: 'Hi', answer: 'Hello!' });
  });

  it('throws on non-ok response', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      text: () => Promise.resolve('Bad request'),
    });

    await expect(sendMessage('Hi')).rejects.toThrow('Bad request');
  });

  it('throws with default message when response has no body', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      text: () => Promise.resolve(''),
    });

    await expect(sendMessage('Hi')).rejects.toThrow('Failed to get response');
  });
});
