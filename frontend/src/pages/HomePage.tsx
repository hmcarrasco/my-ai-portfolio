import { Link } from 'react-router-dom';
import { MessageSquare, FileText } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 sm:py-32">
        <div className="max-w-7xl mx-auto text-center">
          {/* Badge */}
          <span className="inline-block px-4 py-2 rounded-full bg-brand/10 text-brand text-sm font-medium mb-8">
            AI Engineer | Systems Engineer
          </span>

          {/* Heading */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6">
            Know Me Better
            <br />
            <span className="text-brand">with AI</span>
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-10">
            Chat with my AI assistant and discover automated documentation generation.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              to="/chat"
              className="px-8 py-4 bg-brand text-white rounded-xl font-medium hover:bg-brand/90 transition-colors"
            >
              Chat with AI
            </Link>
            <Link
              to="/projects"
              className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-xl font-medium border border-gray-200 dark:border-gray-700 hover:border-brand transition-colors"
            >
              View Projects
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 sm:px-6 lg:px-8 py-20 bg-gray-50 dark:bg-gray-800/50">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white text-center mb-12">
            How it works
          </h2>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {[
              {
                title: 'AI Chat Assistant',
                description:
                  'Get instant answers about my work and experience through an intelligent chatbot.',
                icon: <MessageSquare className="size-8 text-brand" />,
              },
              {
                title: 'Auto Documentation',
                description:
                  'Generate comprehensive docs from my GitHub repositories automatically.',
                icon: <FileText className="size-8 text-brand" />,
              },
            ].map((feature, index) => (
              <div
                key={index}
                className="p-8 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-brand/50 transition-colors"
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
