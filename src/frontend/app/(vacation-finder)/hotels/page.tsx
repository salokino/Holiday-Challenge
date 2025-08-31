"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react";
import { Spinner } from '@/components/ui/spinner';
import CheapestHotelOffer from "@/components/CheapestOffer";
import { CheapestOffer } from "@/components/CheapestOffer";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const sortOptions = [
  { value: "hotel_name", label: "Hotel Name: Alphabetically" },
  { value: "price_asc", label: "Price: Low to High" },
  { value: "price_desc", label: "Price: High to Low" },
];

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

  const handleSorting = (type: string) => {
    if (type === "hotel_name") {
      const sorted = [...cheapestOffers].sort((a, b) => a.hotel_name.localeCompare(b.hotel_name));
      setCheapestOffers(sorted);
    } else if (type === "price_asc") {
      const sorted = [...cheapestOffers].sort((a, b) => a.price - b.price);
      setCheapestOffers(sorted);
    } else if (type === "price_desc") {
      const sorted = [...cheapestOffers].sort((a, b) => b.price - a.price);
      setCheapestOffers(sorted);
    }
  }

  return (
    isLoading ? (
      <div className="flex h-screen">
        <div className="m-auto">
          <Spinner className="text-sky-800" size="large" />
        </div>
      </div>
    ) : (
      <div>
        <div className="flex justify-end pr-16 pb-16">
          <Select onValueChange={(v) => handleSorting(v)}>
            <SelectTrigger className="w-[240px]">
              <SelectValue placeholder="Sort By" />
            </SelectTrigger>
            <SelectContent>
              {sortOptions.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        {cheapestOffers.map((offer: CheapestOffer) => (
          <div className="flex justify-center" key={offer.hotel_id}>
            <CheapestHotelOffer key={offer.hotel_id} offer={offer} />
          </div>
        ))}
      </div>
    )
  )
}