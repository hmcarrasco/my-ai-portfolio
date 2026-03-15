import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { ThemeProvider, useTheme } from './ThemeContext';

beforeEach(() => {
  localStorage.clear();
  document.documentElement.classList.remove('dark');
});

describe('ThemeContext', () => {
  it('defaults to light theme', () => {
    const { result } = renderHook(() => useTheme(), { wrapper: ThemeProvider });
    expect(result.current.theme).toBe('light');
  });

  it('toggles from light to dark', () => {
    const { result } = renderHook(() => useTheme(), { wrapper: ThemeProvider });

    act(() => result.current.toggleTheme());

    expect(result.current.theme).toBe('dark');
    expect(document.documentElement.classList.contains('dark')).toBe(true);
  });

  it('toggles from dark back to light', () => {
    const { result } = renderHook(() => useTheme(), { wrapper: ThemeProvider });

    act(() => result.current.toggleTheme());
    act(() => result.current.toggleTheme());

    expect(result.current.theme).toBe('light');
    expect(document.documentElement.classList.contains('dark')).toBe(false);
  });

  it('persists theme to localStorage', () => {
    const { result } = renderHook(() => useTheme(), { wrapper: ThemeProvider });

    act(() => result.current.toggleTheme());

    expect(localStorage.getItem('theme')).toBe('dark');
  });

  it('reads theme from localStorage on mount', () => {
    localStorage.setItem('theme', 'dark');

    const { result } = renderHook(() => useTheme(), { wrapper: ThemeProvider });
    expect(result.current.theme).toBe('dark');
  });

  it('throws when used outside provider', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => {});
    expect(() => renderHook(() => useTheme())).toThrow(
      'useTheme must be used within ThemeProvider'
    );
    spy.mockRestore();
  });
});
