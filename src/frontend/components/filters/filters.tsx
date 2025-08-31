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

const defaultFilters: FiltersType = {
  adults: 2,
  airport: [],
  children: 0,
  duration: 7,
  earliestDeparture: null,
  latestReturn: null
}


export default function Filters(
  {
    airportOptions
  }: {
    airportOptions: { iata_code: string, name: string }[]
  }) {
  const router = useRouter()
  const [filters, setFilters] = useState<FiltersType>(defaultFilters)


  const handleFilterChange = (filterName: string, value: string | number | string[] | undefined) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value
    }))
  }

  const resetFilters = () => {
    setFilters(defaultFilters)
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

  const getStartDate = () => {
    if (filters.earliestDeparture) {
      const earliestDepartureDate = new Date(filters.earliestDeparture);
      const latestReturnStartDate = earliestDepartureDate.setDate(earliestDepartureDate.getDate() + filters.duration)

      return latestReturnStartDate
    }

    return undefined
  }


  return (
    <div>
      <div className="grid pt-6 px-6">
        <PersonFilter adults={filters.adults} childs={filters.children} classname="pl-1" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DurationFilter classname="pl-1 w-full" duration={filters.duration} onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DateFilter classname="pl-1" date={filters.earliestDeparture} filtername="Earliest Departure" filtersKey="earliestDeparture" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <DateFilter classname="pl-1" date={filters.latestReturn} filtername="Latest Return" filtersKey="latestReturn" onChange={handleFilterChange} startDate={getStartDate()} />
        <Separator className="my-2" />
        <AirportFilter airport={filters.airport} airportOptions={airportOptions} classname="pl-1" onChange={handleFilterChange} />
        <Separator className="my-2" />
        <Button className="bg-gray-200 cursor-pointer hover:bg-gray-300 text-gray-800 hover:text-gray-900 mb-2" variant="outline" onClick={resetFilters}>Reset</Button>
        <Button className="bg-sky-800 cursor-pointer hover:bg-sky-900 text-white hover:text-white" type="submit" variant="outline" onClick={handleSearch}>Search</Button>
      </div>
    </div>
  )
}