
import { Suspense } from 'react';
import HotelsList from '@/components/hotelsList';
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
      <HotelsList />
    </Suspense>
  )
}