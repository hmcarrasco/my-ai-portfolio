import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithProviders } from '../tests/test-utils';
import DocsPage from './DocsPage';

vi.mock('../services/docsService', () => ({
  fetchProjects: vi.fn(),
  generateDocs: vi.fn(),
}));

import { fetchProjects, generateDocs } from '../services/docsService';
const mockFetchProjects = vi.mocked(fetchProjects);
const mockGenerateDocs = vi.mocked(generateDocs);

beforeEach(() => {
  vi.clearAllMocks();
});

const mockProjects = {
  projects: [
    {
      name: 'Test Project',
      repo: 'user/test-project',
      description: 'A test project',
      doc_types: ['overview', 'api'],
    },
    {
      name: 'Another Project',
      repo: 'user/another-project',
      description: 'Another project',
      doc_types: ['setup'],
    },
  ],
};

describe('DocsPage', () => {
  it('renders the page header', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    renderWithProviders(<DocsPage />);

    expect(screen.getByText('Documentation Generator')).toBeInTheDocument();
    expect(
      screen.getByText('Auto-generate documentation for my GitHub repositories using AI.')
    ).toBeInTheDocument();
  });

  it('sets the page title', () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    renderWithProviders(<DocsPage />);
    expect(document.title).toBe('Docs — Hugo Carrasco');
  });

  it('loads and displays projects', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Project')).toBeInTheDocument();
      expect(screen.getByText('Another Project')).toBeInTheDocument();
    });
  });

  it('displays doc type badges for each project', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('overview')).toBeInTheDocument();
      expect(screen.getByText('api')).toBeInTheDocument();
      expect(screen.getByText('setup')).toBeInTheDocument();
    });
  });

  it('shows error when projects fail to load', async () => {
    mockFetchProjects.mockRejectedValueOnce(new Error('Network error'));
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('Failed to load projects.')).toBeInTheDocument();
    });
  });

  it('generates docs when clicking Generate button', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    mockGenerateDocs.mockResolvedValueOnce({
      repo: 'user/test-project',
      documentation: { overview: '# Overview\nThis is the overview.' },
      cached: false,
    });

    const user = userEvent.setup();
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Project')).toBeInTheDocument();
    });

    const generateButtons = screen.getAllByText('Generate Docs');
    await user.click(generateButtons[0]);

    expect(mockGenerateDocs).toHaveBeenCalledWith('user/test-project', false);

    await waitFor(() => {
      expect(screen.getByText(/Documentation for/)).toBeInTheDocument();
    });
  });

  it('shows cached badge and regenerate button when docs are cached', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    mockGenerateDocs.mockResolvedValueOnce({
      repo: 'user/test-project',
      documentation: { overview: '# Cached docs' },
      cached: true,
    });

    const user = userEvent.setup();
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Project')).toBeInTheDocument();
    });

    const generateButtons = screen.getAllByText('Generate Docs');
    await user.click(generateButtons[0]);

    await waitFor(() => {
      expect(screen.getByText('Served from cache')).toBeInTheDocument();
      expect(screen.getByText('Regenerate')).toBeInTheDocument();
    });
  });

  it('shows error when doc generation fails', async () => {
    mockFetchProjects.mockResolvedValueOnce(mockProjects);
    mockGenerateDocs.mockRejectedValueOnce(new Error('Generation failed'));

    const user = userEvent.setup();
    renderWithProviders(<DocsPage />);

    await waitFor(() => {
      expect(screen.getByText('Test Project')).toBeInTheDocument();
    });

    const generateButtons = screen.getAllByText('Generate Docs');
    await user.click(generateButtons[0]);

    await waitFor(() => {
      expect(
        screen.getByText('Failed to generate documentation. Please try again.')
      ).toBeInTheDocument();
    });
  });
});
