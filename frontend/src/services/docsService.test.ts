import { describe, it, expect, vi, beforeEach } from 'vitest';
import { fetchProjects, generateDocs } from './docsService';

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

beforeEach(() => {
  vi.clearAllMocks();
});

describe('docsService', () => {
  describe('fetchProjects', () => {
    it('sends a GET request', async () => {
      const mockData = {
        projects: [{ name: 'Test', repo: 'user/test', description: 'desc', doc_types: [] }],
      };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockData),
      });

      const result = await fetchProjects();

      expect(mockFetch).toHaveBeenCalledWith(expect.stringContaining('/docs/projects'));
      expect(result).toEqual(mockData);
    });

    it('throws on non-ok response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        text: () => Promise.resolve('Server error'),
      });

      await expect(fetchProjects()).rejects.toThrow('Server error');
    });
  });

  describe('generateDocs', () => {
    it('sends a POST request with repo', async () => {
      const mockData = { repo: 'user/test', documentation: {}, cached: false };
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockData),
      });

      const result = await generateDocs('user/test');

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/docs/generate'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ repo: 'user/test', force_regenerate: false }),
        })
      );
      expect(result).toEqual(mockData);
    });

    it('sends force_regenerate=true when specified', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve({ repo: 'user/test', documentation: {}, cached: false }),
      });

      await generateDocs('user/test', true);

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/docs/generate'),
        expect.objectContaining({
          body: JSON.stringify({ repo: 'user/test', force_regenerate: true }),
        })
      );
    });

    it('throws on non-ok response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        text: () => Promise.resolve(''),
      });

      await expect(generateDocs('user/test')).rejects.toThrow('Failed to generate documentation');
    });
  });
});
