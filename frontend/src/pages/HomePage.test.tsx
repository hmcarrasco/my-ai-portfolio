import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../tests/test-utils';
import HomePage from './HomePage';

describe('HomePage', () => {
  it('renders the hero heading', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('Know Me Better')).toBeInTheDocument();
    expect(screen.getByText('with AI')).toBeInTheDocument();
  });

  it('renders the badge', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('AI Engineer | Systems Engineer')).toBeInTheDocument();
  });

  it('renders CTA links with correct routes', () => {
    renderWithProviders(<HomePage />);
    const chatLink = screen.getByRole('link', { name: 'Chat with AI' });
    const docsLink = screen.getByRole('link', { name: 'Explore Docs' });
    expect(chatLink).toHaveAttribute('href', '/chat');
    expect(docsLink).toHaveAttribute('href', '/docs');
  });

  it('renders feature cards', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('AI Chat Assistant')).toBeInTheDocument();
    expect(screen.getByText('Auto Documentation')).toBeInTheDocument();
  });

  it('renders the "How it works" section heading', () => {
    renderWithProviders(<HomePage />);
    expect(screen.getByText('How it works')).toBeInTheDocument();
  });

  it('sets the page title', () => {
    renderWithProviders(<HomePage />);
    expect(document.title).toBe('Hugo Carrasco — AI Engineer Portfolio');
  });
});
