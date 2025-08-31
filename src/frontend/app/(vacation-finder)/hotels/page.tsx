
import { Suspense } from 'react';
import Hotels from '@/components/hotels';
import { Spinner } from '@/components/ui/spinner';

export default function AvailableHotelsPage() {

  const loadingFallback = (
    <div className="flex h-screen">
      <div className="m-auto">
        <Spinner className="text-sky-800" size="large" />
      </div>
    </div>
  );

  return (
    <Suspense fallback={loadingFallback}>
      <Hotels />
    </Suspense>
  )
}