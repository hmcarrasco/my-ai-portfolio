export function SkeletonBlock({ className = '' }: { className?: string }) {
  return <div className={`skeleton ${className}`} />;
}

export function SkeletonCard() {
  return (
    <div className="p-5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
      <SkeletonBlock className="h-5 w-1/2 mb-3" />
      <SkeletonBlock className="h-4 w-full mb-2" />
      <SkeletonBlock className="h-4 w-3/4 mb-4" />
      <div className="flex gap-1.5 mb-4">
        <SkeletonBlock className="h-5 w-14 rounded-full" />
        <SkeletonBlock className="h-5 w-16 rounded-full" />
        <SkeletonBlock className="h-5 w-12 rounded-full" />
      </div>
      <SkeletonBlock className="h-9 w-full rounded-lg" />
    </div>
  );
}

export function SkeletonLine({ className = '' }: { className?: string }) {
  return <SkeletonBlock className={`h-4 ${className}`} />;
}
