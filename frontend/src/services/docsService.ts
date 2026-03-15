import { API_BASE_URL } from '../constants/config';
import type { ProjectsResponse, GenerateDocsResponse } from '../types/docs';

export async function fetchProjects(): Promise<ProjectsResponse> {
  const res = await fetch(`${API_BASE_URL}/docs/projects`);

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || 'Failed to fetch projects');
  }

  return res.json();
}

export async function generateDocs(
  repo: string,
  forceRegenerate: boolean = false
): Promise<GenerateDocsResponse> {
  const res = await fetch(`${API_BASE_URL}/docs/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo, force_regenerate: forceRegenerate }),
  });

  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || 'Failed to generate documentation');
  }

  return res.json();
}
