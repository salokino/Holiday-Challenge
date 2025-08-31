"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react";
import { Spinner } from '@/components/ui/spinner';
import HotelOffer from "@/components/Offer";

import { useParams } from "next/navigation";
import OffsetPagination from "@/components/OffsetPagination";
import Icon from "@/components/Icon";

import { useRouter } from "next/navigation";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

type Offer = {
  count_adults: number
  count_children: number
  duration: number
  hotel_name: string
  hotel_stars: number
  inbound_departure_datetime: string
  mealtype: string
  oceanview: boolean
  offer_id: number
  outbound_departure_datetime: string
  price: number
  roomtype: string
}

const sortOptions = [
  { value: "departure_date_asc", label: "Departure: Date Ascending" },
  { value: "departure_date_desc", label: "Departure: Date Descending" },
  { value: "price_asc", label: "Price: Low to High" },
  { value: "price_desc", label: "Price: High to Low" },
];

export default function Hotels() {
  const params = useParams();
  const hotel_id = params.hotel_id as string;
  const router = useRouter();
  const isBrowser = () => typeof window !== 'undefined';
  const searchParams = useSearchParams();
  const [isLoading, setIsLoading] = useState(false);
  const [hotelOffers, setHotelOffers] = useState<Offer[]>([]);
  const [offset, setOffset] = useState(0);
  const [limit, setLimit] = useState(20);

  useEffect(() => {
    const fetchResults = async () => {
      setIsLoading(true);
      const results = await fetch(`http://127.0.0.1:8000/offers/${hotel_id}?${searchParams.toString()}&offset=${offset}&limit=${limit}`)
      const data = await results.json();
      setHotelOffers(data);
      setIsLoading(false);
    }

    if (!isLoading) {
      fetchResults();
    }

  }, [searchParams, offset])

  const handleSorting = (type: string) => {
    if (type === "departure_date_asc") {
      const params = new URLSearchParams(window.location.search);
      params.set('order_by', 'departure_date_asc');
      router.push(`${window.location.pathname}?${params.toString()}`);
    } else if (type === "departure_date_desc") {
      const params = new URLSearchParams(window.location.search);
      params.set('order_by', 'departure_date_desc');
      router.push(`${window.location.pathname}?${params.toString()}`);
    } else if (type === "price_asc") {
      const sorted = [...hotelOffers].sort((a, b) => a.price - b.price);
      setHotelOffers(sorted);
    } else if (type === "price_desc") {
      const sorted = [...hotelOffers].sort((a, b) => b.price - a.price);
      setHotelOffers(sorted);
    }
  }


  function scrollToTop() {
    if (!isBrowser()) return;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const handleChange = (direction: string) => {
    if (direction === "plus" && hotelOffers.length === limit) {
      setOffset(offset + limit)
    }

    if (direction === "minus" && offset >= limit) {
      setOffset(offset - limit)
    }

    scrollToTop()
  }

  return (
    <div>
      <h1>{offset}</h1>
      {isLoading ? (
        <div className="flex h-screen">
          <div className="m-auto">
            <Spinner className="text-sky-800" size="large" />
          </div>
        </div>
      ) : (
        <>
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
          <div className="flex justify-center pb-8">
            <div className="flex w-3xl m-1 rounded-xl">
              <div className="hotel-name font-medium text-5xl [font-variant:small-caps]">
                {hotelOffers[0]?.hotel_name}
              </div>
              <div className="hotel-stars flex text-2xl px-4 content-center">
                {
                  [...Array(hotelOffers[0]?.hotel_stars)].map((e, i) => <Icon key={i} description={`${hotelOffers[0]?.hotel_stars} stars`} filepath={"/icons/star.svg"} />)
                }
              </div>
            </div>
          </div>
          {hotelOffers.map((offer: Offer) => (
            <div className="flex justify-center" key={offer.offer_id}>
              <HotelOffer hotel_id={hotel_id} key={offer.offer_id} offer={offer} />
            </div>
          ))}
        </>
      )}
      <OffsetPagination onChange={handleChange} />
    </div>
  )
}

export type { Offer }