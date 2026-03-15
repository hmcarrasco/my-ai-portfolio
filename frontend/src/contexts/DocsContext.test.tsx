import { describe, it, expect, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { DocsProvider, useDocs } from './DocsContext';
import type { GenerateDocsResponse } from '../types/docs';

describe('DocsContext', () => {
  it('starts with empty state', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });
    expect(result.current.projects).toEqual([]);
    expect(result.current.selectedRepo).toBeNull();
    expect(result.current.docs).toBeNull();
    expect(result.current.activeTab).toBe('');
    expect(result.current.isCached).toBe(false);
  });

  it('can set projects', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });

    const projects = [
      { name: 'Test', repo: 'user/test', description: 'desc', doc_types: ['overview'] },
    ];
    act(() => result.current.setProjects(projects));

    expect(result.current.projects).toEqual(projects);
  });

  it('can set selected repo', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });

    act(() => result.current.setSelectedRepo('user/test'));
    expect(result.current.selectedRepo).toBe('user/test');
  });

  it('can set docs', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });

    const docs: GenerateDocsResponse = {
      repo: 'user/test',
      documentation: { overview: '# Overview' },
      cached: false,
    };
    act(() => result.current.setDocs(docs));

    expect(result.current.docs).toEqual(docs);
  });

  it('can set active tab', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });

    act(() => result.current.setActiveTab('api'));
    expect(result.current.activeTab).toBe('api');
  });

  it('can set cached status', () => {
    const { result } = renderHook(() => useDocs(), { wrapper: DocsProvider });

    act(() => result.current.setIsCached(true));
    expect(result.current.isCached).toBe(true);
  });

  it('throws when used outside provider', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => renderHook(() => useDocs())).toThrow('useDocs must be used within DocsProvider');
    spy.mockRestore();
  });
});
