import { Link } from 'react-router-dom';
import { useEffect } from 'react';

export default function NotFoundPage() {
  useEffect(() => {
    document.title = 'Not Found — Hugo Carrasco';
  }, []);

  return (
    <div className="flex flex-col items-center justify-center gap-4 py-32">
      <h1 className="text-6xl font-bold text-red-500">404</h1>
      <p className="text-xl text-gray-600 dark:text-gray-400">Page not found</p>
      <Link to="/" className="text-brand hover:underline">
        Go back home
      </Link>
    </div>
  );
}
