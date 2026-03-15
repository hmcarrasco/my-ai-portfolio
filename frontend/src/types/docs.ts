export interface Project {
  name: string;
  repo: string;
  description: string;
  doc_types: string[];
}

export interface ProjectsResponse {
  projects: Project[];
}

export interface GenerateDocsRequest {
  repo: string;
  force_regenerate?: boolean;
}

export interface GenerateDocsResponse {
  repo: string;
  documentation: Record<string, string>;
  cached: boolean;
}
