import { describe, it, expect, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { ChatProvider, useChat } from './ChatContext';
import type { Message } from '../types/chat';

describe('ChatContext', () => {
  it('starts with empty messages', () => {
    const { result } = renderHook(() => useChat(), { wrapper: ChatProvider });
    expect(result.current.messages).toEqual([]);
  });

  it('can add messages via setMessages', () => {
    const { result } = renderHook(() => useChat(), { wrapper: ChatProvider });

    const msg: Message = { id: '1', role: 'user', content: 'Hello' };
    act(() => result.current.setMessages([msg]));

    expect(result.current.messages).toEqual([msg]);
  });

  it('clears all messages with clearChat', () => {
    const { result } = renderHook(() => useChat(), { wrapper: ChatProvider });

    const msg: Message = { id: '1', role: 'user', content: 'Hello' };
    act(() => result.current.setMessages([msg]));
    act(() => result.current.clearChat());

    expect(result.current.messages).toEqual([]);
  });

  it('throws when used outside provider', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => renderHook(() => useChat())).toThrow('useChat must be used within ChatProvider');
    spy.mockRestore();
  });
});
