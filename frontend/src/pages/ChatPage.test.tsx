import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithProviders } from '../tests/test-utils';
import ChatPage from './ChatPage';

vi.mock('../services/chatService', () => ({
  sendMessage: vi.fn(),
}));

vi.mock('../assets/images/avatar.png', () => ({ default: 'avatar.png' }));

import { sendMessage } from '../services/chatService';
const mockSendMessage = vi.mocked(sendMessage);

beforeEach(() => {
  vi.clearAllMocks();
});

describe('ChatPage', () => {
  it('renders the empty state with heading and avatar', () => {
    renderWithProviders(<ChatPage />);
    expect(screen.getByText("Chat with Hugo's AI")).toBeInTheDocument();
    expect(screen.getByAltText('Hugo')).toBeInTheDocument();
  });

  it('renders suggestion cards', () => {
    renderWithProviders(<ChatPage />);
    expect(screen.getByText('Work experience')).toBeInTheDocument();
    expect(screen.getByText('Tech stack')).toBeInTheDocument();
    expect(screen.getByText('Background')).toBeInTheDocument();
  });

  it('renders the input field with placeholder', () => {
    renderWithProviders(<ChatPage />);
    expect(screen.getByPlaceholderText('Ask a question...')).toBeInTheDocument();
  });

  it('sets the page title', () => {
    renderWithProviders(<ChatPage />);
    expect(document.title).toBe('Chat — Hugo Carrasco');
  });

  it('does not show the clear button when there are no messages', () => {
    renderWithProviders(<ChatPage />);
    expect(screen.queryByTitle('Clear chat')).not.toBeInTheDocument();
  });

  it('sends a message and shows the response', async () => {
    mockSendMessage.mockResolvedValueOnce({
      question: 'Hello',
      answer: 'Hi there!',
    });

    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    const input = screen.getByPlaceholderText('Ask a question...');
    await user.type(input, 'Hello');
    await user.keyboard('{Enter}');

    expect(screen.getByText('Hello')).toBeInTheDocument();
    expect(mockSendMessage).toHaveBeenCalledWith('Hello');

    await waitFor(() => {
      expect(screen.getByText('Hi there!')).toBeInTheDocument();
    });
  });

  it('shows error message when API call fails', async () => {
    mockSendMessage.mockRejectedValueOnce(new Error('Network error'));

    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    const input = screen.getByPlaceholderText('Ask a question...');
    await user.type(input, 'Hello');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(
        screen.getByText('Sorry, something went wrong. Please try again.')
      ).toBeInTheDocument();
    });
  });

  it('shows clear button after sending a message', async () => {
    mockSendMessage.mockResolvedValueOnce({
      question: 'Hi',
      answer: 'Hello!',
    });

    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    const input = screen.getByPlaceholderText('Ask a question...');
    await user.type(input, 'Hi');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByTitle('Clear chat')).toBeInTheDocument();
    });
  });

  it('clears chat when clear button is clicked', async () => {
    mockSendMessage.mockResolvedValueOnce({
      question: 'Hi',
      answer: 'Hello!',
    });

    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    const input = screen.getByPlaceholderText('Ask a question...');
    await user.type(input, 'Hi');
    await user.keyboard('{Enter}');

    await waitFor(() => {
      expect(screen.getByText('Hello!')).toBeInTheDocument();
    });

    await user.click(screen.getByTitle('Clear chat'));

    expect(screen.queryByText('Hello!')).not.toBeInTheDocument();
    expect(screen.getByText("Chat with Hugo's AI")).toBeInTheDocument();
  });

  it('sends message when clicking a suggestion card', async () => {
    mockSendMessage.mockResolvedValueOnce({
      question: "What is Hugo's professional experience?",
      answer: 'Hugo worked at Euronext.',
    });

    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    await user.click(screen.getByText('Work experience'));

    expect(mockSendMessage).toHaveBeenCalledWith("What is Hugo's professional experience?");

    await waitFor(() => {
      expect(screen.getByText('Hugo worked at Euronext.')).toBeInTheDocument();
    });
  });

  it('does not send empty messages', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ChatPage />);

    const input = screen.getByPlaceholderText('Ask a question...');
    await user.type(input, '   ');
    await user.keyboard('{Enter}');

    expect(mockSendMessage).not.toHaveBeenCalled();
  });
});
