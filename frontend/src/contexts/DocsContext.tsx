import { createContext, useContext, useState } from 'react';
import type { Project, GenerateDocsResponse } from '../types/docs';

interface DocsContextType {
  projects: Project[];
  setProjects: React.Dispatch<React.SetStateAction<Project[]>>;
  selectedRepo: string | null;
  setSelectedRepo: React.Dispatch<React.SetStateAction<string | null>>;
  docs: GenerateDocsResponse | null;
  setDocs: React.Dispatch<React.SetStateAction<GenerateDocsResponse | null>>;
  activeTab: string;
  setActiveTab: React.Dispatch<React.SetStateAction<string>>;
  isCached: boolean;
  setIsCached: React.Dispatch<React.SetStateAction<boolean>>;
}

const DocsContext = createContext<DocsContextType | null>(null);

export function DocsProvider({ children }: { children: React.ReactNode }) {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedRepo, setSelectedRepo] = useState<string | null>(null);
  const [docs, setDocs] = useState<GenerateDocsResponse | null>(null);
  const [activeTab, setActiveTab] = useState('');
  const [isCached, setIsCached] = useState(false);

  return (
    <DocsContext.Provider
      value={{
        projects,
        setProjects,
        selectedRepo,
        setSelectedRepo,
        docs,
        setDocs,
        activeTab,
        setActiveTab,
        isCached,
        setIsCached,
      }}
    >
      {children}
    </DocsContext.Provider>
  );
}

export function useDocs(): DocsContextType {
  const ctx = useContext(DocsContext);
  if (!ctx) throw new Error('useDocs must be used within DocsProvider');
  return ctx;
}
