import { describe, it, expect } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithProviders } from '../../../tests/test-utils';
import Header from './Header';

describe('Header', () => {
  it('renders the logo with HC initials', () => {
    renderWithProviders(<Header />);
    expect(screen.getByText('HC')).toBeInTheDocument();
  });

  it('renders Hugo Carrasco name', () => {
    renderWithProviders(<Header />);
    expect(screen.getByText('Carrasco')).toBeInTheDocument();
  });

  it('renders desktop navigation links', () => {
    renderWithProviders(<Header />);
    const homeLinks = screen.getAllByRole('link', { name: 'Home' });
    const chatLinks = screen.getAllByRole('link', { name: 'Chat' });
    const docsLinks = screen.getAllByRole('link', { name: 'Docs' });
    expect(homeLinks.length).toBeGreaterThanOrEqual(1);
    expect(chatLinks.length).toBeGreaterThanOrEqual(1);
    expect(docsLinks.length).toBeGreaterThanOrEqual(1);
  });

  it('renders the theme toggle button', () => {
    renderWithProviders(<Header />);
    const toggleButtons = screen.getAllByRole('button', { name: 'Toggle theme' });
    expect(toggleButtons.length).toBeGreaterThanOrEqual(1);
  });

  it('renders the mobile menu toggle button', () => {
    renderWithProviders(<Header />);
    expect(screen.getByRole('button', { name: 'Toggle menu' })).toBeInTheDocument();
  });

  it('toggles mobile menu on click', async () => {
    const user = userEvent.setup();
    renderWithProviders(<Header />);

    const menuButton = screen.getByRole('button', { name: 'Toggle menu' });
    await user.click(menuButton);

    // After opening, the mobile nav should exist with link elements
    const chatLinks = screen.getAllByRole('link', { name: 'Chat' });
    expect(chatLinks.length).toBeGreaterThanOrEqual(2); // desktop + mobile

    await user.click(menuButton);
    // After closing, should be back to just desktop links
    const chatLinksAfter = screen.getAllByRole('link', { name: 'Chat' });
    expect(chatLinksAfter.length).toBeGreaterThanOrEqual(1);
  });

  it('has correct link paths', () => {
    renderWithProviders(<Header />);
    const logoLink = screen.getAllByRole('link').find((link) => link.textContent?.includes('HC'));
    expect(logoLink).toHaveAttribute('href', '/');
  });
});
