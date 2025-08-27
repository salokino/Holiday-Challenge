"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react";
import { Spinner } from '@/components/ui/spinner';
import CheapestHotelOffer from "@/components/CheapestOffer";
import { CheapestOffer } from "@/components/CheapestOffer";

export default function Hotels() {
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [cheapestOffers, setCheapestOffers] = useState([]);

  useEffect(() => {
    const fetchResults = async () => {
      setIsLoading(true);
      const results = await fetch(`http://127.0.0.1:8000/hotels?${searchParams.toString()}`)
      const data = await results.json();
      setCheapestOffers(data);
      setIsLoading(false);
    }

    if (!isLoading) {
      fetchResults();
    }

  }, [searchParams])

  return (
    isLoading ? (
      <div className="flex h-screen">
        <div className="m-auto">
          <Spinner className="text-sky-800" size="large" />
        </div>
      </div>
    ) : (
      cheapestOffers.map((offer: CheapestOffer) => (
        <div className="flex justify-center" key={offer.hotel_id}>
          <CheapestHotelOffer key={offer.hotel_id} offer={offer} />
        </div>
      ))
    )
  )
}