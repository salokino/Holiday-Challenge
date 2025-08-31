"use client"

import { Spinner } from '@/components/ui/spinner';
import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import OffsetPagination from "@/components/OffsetPagination";
import Icon from "@/components/Icon";


import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"


type Hotel = { hotel_id: number, hotel_name: string, hotel_stars: number }

const filterOptions = [
  { value: "all", label: "All Hotels" },
  { value: "1", label: "1 star" },
  { value: "2", label: "2 stars" },
  { value: "3", label: "3 stars" },
  { value: "4", label: "4 stars" },
  { value: "5", label: "5 stars" }
];

export default function AvailableHotelsPage() {
  const router = useRouter();
  const isBrowser = () => typeof window !== 'undefined';
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [hotels, setHotels] = useState<Hotel[]>([]);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    const fetchResults = async () => {
      setIsLoading(true);
      const results = await fetch(`http://localhost:8000/available-hotels?${searchParams.toString()}&offset=${offset}&limit=${limit}`)
      const data = await results.json();
      setHotels(data);
      setIsLoading(false);
    }

    if (!isLoading) {
      fetchResults();
    }

  }, [searchParams, offset])


  function scrollToTop() {
    if (!isBrowser()) return;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const handleChange = (direction: string) => {
    if (direction === "plus" && hotels.length === limit) {
      setOffset(offset + limit)
    }

    if (direction === "minus" && offset >= limit) {
      setOffset(offset - limit)
    }

    scrollToTop()
  }

  const handleFiltering = (value: string) => {
    const params = new URLSearchParams(searchParams.toString());

    if (value === "all") {
      params.delete("stars");
    } else {
      params.set('stars', value);
    }
    setOffset(0);
    params.delete('offset');

    router.push(`${window.location.pathname}?${params.toString()}`);
  };

  const currentFilterValue = searchParams.get("stars") || "all";

  return (
    <div className="pt-8">
      {isLoading ? (
        <div className="flex h-screen">
          <div className="m-auto">
            <Spinner className="text-sky-800" size="large" />
          </div>
        </div>
      ) : (
        <>
          <div className="flex justify-end pr-16 pb-10">
            <Select onValueChange={(v) => handleFiltering(v)} value={currentFilterValue}>
              <SelectTrigger className="w-[240px]">
                <SelectValue placeholder="Sort By" />
              </SelectTrigger>
              <SelectContent>
                {filterOptions.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="flex px-4 mx-4 pb-8">
            <div className="flex w-3xl m-1 rounded-xl">
              <div className="hotel-name font-medium text-5xl [font-variant:small-caps]">
                Hotels
              </div>
            </div>
          </div>
          <div className="grid grid-cols-3 p-4">
            {
              hotels.map((hotel: Hotel) => (
                <div className="flex p-2 m-4 rounded-xl border border-gray-300 shadow-md overflow-hidden" key={hotel.hotel_id}>
                  <div className="flex flex-col">
                    <div className="flex gap-6 p-4 px-6">
                      <div className="hotel-name font-medium text-2xl [font-variant:small-caps]">
                        {hotel.hotel_name}
                      </div>
                    </div>
                    <div className="hotel-stars flex px-6 pb-4">
                      {
                        [...Array(hotel.hotel_stars)].map((e, i) => <Icon key={i} description={`${hotel.hotel_stars} stars`} filepath={"/icons/star.svg"} />)
                      }
                    </div>
                  </div>
                </div>
              ))}
          </div>
          <OffsetPagination onChange={handleChange} />
        </>
      )}
    </div>
  )
}