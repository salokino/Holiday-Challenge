"use client"

import AirportFilter from "./airports";
import DateFilter from "./date";
import DurationFilter from "./duration";
import PersonFilter from "./persons";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { useRouter } from 'next/navigation'
import { useState } from "react";

type FiltersType = {
  adults: number,
  airport: string[],
  children: number,
  duration: number,
  earliestDeparture: string | null,
  latestReturn: string | null
};


export default function Filters(
  {
    airportOptions
  }: {
    airportOptions: { iata_code: string, name: string }[]
  }) {
  const router = useRouter()
  const [filters, setFilters] = useState<FiltersType>({
    adults: 2,
    airport: [],
    children: 0,
    duration: 7,
    earliestDeparture: null,
    latestReturn: null
  })


  const handleFilterChange = (filterName: string, value: string | number | string[] | undefined) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value
    }))
  }


  const handleSearch = () => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      const shouldBeIncluded = value !== null && value !== undefined && value !== '';

      // if value is not an array, simply add the value as an query param
      if (shouldBeIncluded && !Array.isArray(value)) {
        params.append(key, value.toString())
      }

      // if value is an array, append each item of it
      if (shouldBeIncluded && Array.isArray(value) && value.length > 0) {
        value.forEach((item: string) => params.append(key, item))
      }
    })
    const queryString = params.toString();

    const path = queryString ? `/hotels?${queryString}` : '/hotels';
    router.push(path);
  }

  return (
    <div>
      <div className="grid pt-4 px-2">
        <PersonFilter adults={filters.adults} childs={filters.children} classname="pl-1" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DurationFilter classname="pl-1 w-full" duration={filters.duration} onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DateFilter classname="pl-1" filtername="Earliest Departure" filtersKey="earliestDeparture" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DateFilter classname="pl-1" filtername="Latest Return" filtersKey="latestReturn" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <AirportFilter airportOptions={airportOptions} classname="pl-1" onChange={handleFilterChange} />
        <Separator className="my-2" />

        <Button className="bg-sky-800 hover:bg-sky-900 text-white hover:text-white" type="submit" variant="outline" onClick={handleSearch}>Search</Button>
      </div>
    </div>
  )


}