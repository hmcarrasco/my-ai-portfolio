import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../tests/test-utils';
import NotFoundPage from './NotFoundPage';

describe('NotFoundPage', () => {
  it('renders 404 heading', () => {
    renderWithProviders(<NotFoundPage />);
    expect(screen.getByText('404')).toBeInTheDocument();
  });

  it('renders "Page not found" message', () => {
    renderWithProviders(<NotFoundPage />);
    expect(screen.getByText('Page not found')).toBeInTheDocument();
  });

  it('renders a link back to home', () => {
    renderWithProviders(<NotFoundPage />);
    const link = screen.getByRole('link', { name: 'Go back home' });
    expect(link).toHaveAttribute('href', '/');
  });

  it('sets the page title', () => {
    renderWithProviders(<NotFoundPage />);
    expect(document.title).toBe('Not Found — Hugo Carrasco');
  });
});
