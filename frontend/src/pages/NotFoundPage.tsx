import { Link } from 'react-router-dom';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-6xl font-bold text-red-500">404</h1>
      <p className="text-xl text-gray-600 dark:text-gray-400">Page not found</p>
      <Link to="/" className="text-brand hover:underline">
        Go back home
      </Link>
    </div>
  );
}
