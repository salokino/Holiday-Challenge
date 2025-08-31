"use client";

import { Navbar } from "@/components/navbar";
import { Button } from "@/components/ui/button";
import { useRouter } from 'next/navigation'

export default function Home() {
  const router = useRouter();

  return (
    <>
      <Navbar />
      <main>
        <div className="flex h-screen">
          <div className="m-auto">
            <div className="text-center pb-8">
              <p className="text-4xl font-bold text-sky-800 pb-4">
                Welcome to the Holiday Challenge! - Check24 TechUp
              </p>
              <p className="text-lg text-gray-700">
                Discover our vacation finder and find the best deals on hotels and flights for <strong> your </strong> trip to Mallorca!
              </p>
            </div>
            <div className="text-center">
              <Button
                variant="outline"
                className="mt-4 w-xl bg-gray-200 cursor-pointer hover:bg-gray-300 text-gray-800 hover:text-gray-900 mb-2"
                onClick={() => {
                  router.push('/vacation-finder');
                }}
              >
                Go to Vacation Finder
              </Button>
            </div>
          </div>
        </div>
      </main >
    </>
  );
}
