import { useEffect, useState } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  FileText,
  Loader2,
  AlertCircle,
  BookOpen,
  Code,
  Wrench,
  Layers,
  RefreshCw,
} from 'lucide-react';
import { fetchProjects, generateDocs } from '../services/docsService';
import { useDocs } from '../contexts/DocsContext';
import PageTransition from '../components/PageTransition';
import { SkeletonCard } from '../components/Skeleton';

const TAB_ICONS: Record<string, React.ReactNode> = {
  overview: <BookOpen className="size-4" />,
  architecture: <Layers className="size-4" />,
  api: <Code className="size-4" />,
  setup: <Wrench className="size-4" />,
};

export default function DocsPage() {
  const {
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
  } = useDocs();
  const [isLoadingProjects, setIsLoadingProjects] = useState(!projects.length);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    document.title = 'Docs — Hugo Carrasco';
  }, []);

  // Load projects on mount (only if not already loaded)
  useEffect(() => {
    if (projects.length > 0) {
      setIsLoadingProjects(false);
      return;
    }
    fetchProjects()
      .then((data) => setProjects(data.projects))
      .catch(() => setError('Failed to load projects.'))
      .finally(() => setIsLoadingProjects(false));
  }, [projects.length, setProjects]);

  const handleGenerate = async (repo: string, forceRegenerate: boolean = false) => {
    setSelectedRepo(repo);
    setDocs(null);
    setError('');
    setIsCached(false);
    setIsGenerating(true);

    try {
      const data = await generateDocs(repo, forceRegenerate);
      setDocs(data);
      setIsCached(data.cached);
      const firstTab = Object.keys(data.documentation)[0];
      if (firstTab) setActiveTab(firstTab);
    } catch {
      setError('Failed to generate documentation. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <PageTransition>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="size-8 text-brand" />
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Documentation Generator
            </h1>
          </div>
          <p className="text-gray-600 dark:text-gray-400">
            Auto-generate documentation for my GitHub repositories using AI.
          </p>
        </div>

        {/* Error */}
        {error && (
          <div className="mb-6 flex items-center gap-2 p-4 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400">
            <AlertCircle className="size-5 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {/* Projects list */}
        {isLoadingProjects ? (
          <div className="grid gap-4 sm:grid-cols-2 mb-8">
            <SkeletonCard />
            <SkeletonCard />
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 mb-8">
            {projects.map((project) => (
              <div
                key={project.repo}
                className={`p-5 rounded-xl border transition-all duration-300 hover:scale-[1.02] hover:shadow-lg ${
                  selectedRepo === project.repo
                    ? 'border-brand bg-brand/5 dark:bg-brand/10'
                    : 'border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800'
                }`}
              >
                <h3 className="font-semibold text-gray-900 dark:text-white mb-1">{project.name}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-3">
                  {project.description}
                </p>
                <div className="flex flex-wrap gap-1.5 mb-4">
                  {project.doc_types.map((type) => (
                    <span
                      key={type}
                      className="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                    >
                      {type}
                    </span>
                  ))}
                </div>
                <button
                  onClick={() => handleGenerate(project.repo)}
                  disabled={isGenerating}
                  className="w-full px-4 py-2 bg-brand text-white rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 text-sm font-medium"
                >
                  {isGenerating && selectedRepo === project.repo
                    ? 'Generating...'
                    : 'Generate Docs'}
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Generating spinner */}
        {isGenerating && (
          <div className="flex flex-col items-center justify-center py-16 gap-3">
            <Loader2 className="size-8 animate-spin text-brand" />
            <p className="text-gray-500 dark:text-gray-400">
              Generating documentation... This may take a minute.
            </p>
          </div>
        )}

        {/* Documentation output */}
        {docs && !isGenerating && (
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Documentation for <span className="text-brand">{docs.repo}</span>
            </h2>

            {isCached && (
              <div className="mb-4 flex items-center gap-2">
                <span className="text-xs px-2 py-1 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                  Served from cache
                </span>
                <button
                  onClick={() => handleGenerate(docs.repo, true)}
                  disabled={isGenerating}
                  className="flex items-center gap-1.5 text-xs px-3 py-1 rounded-full border border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className="size-3" />
                  Regenerate
                </button>
              </div>
            )}

            {/* Tabs */}
            <div className="flex gap-1 border-b border-gray-200 dark:border-gray-700 mb-6">
              {Object.keys(docs.documentation).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`flex items-center gap-1.5 px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab
                      ? 'border-brand text-brand'
                      : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                  }`}
                >
                  {TAB_ICONS[tab] || <FileText className="size-4" />}
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>

            {/* Tab content */}
            <div className="prose prose-gray dark:prose-invert max-w-none rounded-xl bg-gray-50 dark:bg-gray-800 p-6">
              <Markdown remarkPlugins={[remarkGfm]}>{docs.documentation[activeTab]}</Markdown>
            </div>
          </div>
        )}
      </div>
    </PageTransition>
  );
}
