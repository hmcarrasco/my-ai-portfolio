import { Link } from 'react-router-dom';
import { useEffect } from 'react';
import { MessageSquare, FileText } from 'lucide-react';
import PageTransition from '../components/PageTransition';

export default function HomePage() {
  useEffect(() => {
    document.title = 'Hugo Carrasco — AI Engineer Portfolio';
  }, []);
  return (
    <PageTransition>
      <div className="min-h-screen">
        {/* Hero Section */}
        <section className="px-4 sm:px-6 lg:px-8 py-20 sm:py-32">
          <div className="max-w-7xl mx-auto text-center">
            {/* Badge */}
            <span className="inline-block px-4 py-2 rounded-full bg-brand/10 text-brand text-sm font-medium mb-8 animate-fade-in-up">
              AI Engineer | Systems Engineer
            </span>

            {/* Heading */}
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 animate-fade-in-up [animation-delay:0.1s]">
              Know Me Better
              <br />
              <span className="text-brand">with AI</span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto mb-10 animate-fade-in-up [animation-delay:0.2s]">
              Chat with my AI assistant and discover automated documentation generation about my
              projects.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-wrap justify-center gap-4 animate-fade-in-up [animation-delay:0.3s]">
              <Link
                to="/chat"
                className="px-8 py-4 bg-brand text-white rounded-xl font-medium hover:bg-brand/90 transition-colors"
              >
                Chat with AI
              </Link>
              <Link
                to="/docs"
                className="px-8 py-4 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-xl font-medium border border-gray-200 dark:border-gray-700 hover:border-brand transition-colors"
              >
                Explore Docs
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
                  key={feature.title}
                  className="p-8 rounded-2xl bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-brand/50 hover:scale-[1.02] hover:shadow-lg transition-all duration-300 animate-fade-in-up"
                  style={{ animationDelay: `${0.1 * index + 0.4}s` }}
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
    </PageTransition>
  );
}
