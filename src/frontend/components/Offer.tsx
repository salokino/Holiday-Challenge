"use client"

import { Offer } from "@/app/(vacation-finder)/offers/[hotel_id]/page";
import { getMealtypeIconFilename, getRoomtypeIconFilename, getTimeDifference } from "./functions";
import Icon from "./Icon";
import { useEffect, useState } from "react";
import Image from "next/image";
import { Spinner } from "@/components/ui/spinner";
import Airport from "./Airport";
import { getFormattedDate, getFormattedTime } from "./functions"
import { Separator } from "./ui/separator";


type FlightDetails = {
  inbound_arrival_airport: string,
  inbound_arrival_datetime: string,
  inbound_departure_airport: string,
  inbound_departure_datetime: string,
  outbound_arrival_airport: string,
  outbound_arrival_datetime: string,
  outbound_arrival_name: string,
  outbound_departure_airport: string,
  outbound_departure_datetime: string
  outbound_departure_name: string
}

export default function HotelOffer(
  {
    hotel_id,
    offer
  }: {
    hotel_id: string
    offer: Offer
  }) {

  const mealtypeIconPath = getMealtypeIconFilename(offer.mealtype);
  const roomtypeIconPath = getRoomtypeIconFilename(offer.roomtype);
  const oceanview = offer.oceanview ? "oceanview" : "no_oceanview"

  const [isOpen, setIsOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false);
  const [flightDetails, setFlightDetails] = useState<FlightDetails | null>(null);


  const handleDetailToggle = async () => {
    setIsOpen(!isOpen)
    setIsLoading(true);
    const results = await fetch(`http://127.0.0.1:8000/flight-details/${offer.offer_id}`)
    const data = await results.json();
    setFlightDetails(data);
    setIsLoading(false);
  }

  return (
    <div className="grid grid-rows-[1fr_auto] w-3xl m-1 rounded-xl border border-gray-300 shadow-md overflow-hidden">
      <div className="grid grid-cols-5">
        <div className="grid col-span-4 p-4">
          <div className="flex flex-col gap-1">
            <p className="font-bold text-xl">
              {getFormattedDate(offer.outbound_departure_datetime)} – {getFormattedDate(offer.inbound_departure_datetime)}
            </p>
            <p className="text-gray-700">
              {offer.duration} days · {offer.count_adults} adults · {offer.count_children} children
            </p>
          </div>
          <div className="grid col-span-4 pt-4">
            <div className="flex">
              <Icon description={offer.mealtype} filepath={`/icons/${mealtypeIconPath}`} />
              <p className="px-4">
                {offer.mealtype}
              </p>
              <Separator className="mr-4" orientation="vertical" />
              <Icon description={offer.roomtype} filepath={`/icons/${roomtypeIconPath}`} />
              <p className="px-4">
                {offer.roomtype}
              </p>
              <Separator className="mr-4" orientation="vertical" />
              <Icon description={offer.oceanview ? "oceanview" : "no oceanview"} filepath={`/icons/${oceanview}.svg`} />
              <p className="px-4">
                {offer.oceanview ? "oceanview" : "no oceanview"}
              </p>
            </div>
          </div>
        </div>
        <div className="grid text-2xl col-5 font-bold text-sky-800 items-center justify-center">
          {offer.price} €
        </div>
      </div>
      <div>
        {isOpen ? (
          <div className="p-2 bg-gray-50">
            <div className="pb-2 ">
              <div>
                {isLoading ? (
                  <div className="m-auto">
                    <Spinner className="text-sky-800" size="large" />
                  </div>
                ) : (
                  flightDetails ? (
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="font-bold">Outbound</div>
                        <div className="grid pl-2">
                          <div className="flex justify-between">
                            <Airport iata_code={flightDetails.outbound_departure_airport} name={flightDetails.outbound_departure_name} />
                            <p className="flex text-sm text-sky-800 pr-12 items-center">
                              {getFormattedTime(flightDetails.outbound_departure_datetime)}
                            </p>
                          </div>
                          <div className="flex items-center gap-4 py-1 pl-3 h-12">
                            <div className="border-l-2 border-dotted border-gray-300 h-full"></div>
                            <p className="text-xs text-gray-400">{getTimeDifference(flightDetails.outbound_arrival_datetime, flightDetails.outbound_departure_datetime)}</p>
                          </div>
                          <div className="flex justify-between">
                            <Airport iata_code={flightDetails.outbound_arrival_airport} name={flightDetails.outbound_arrival_name} />
                            <p className="flex text-sm text-sky-800 pr-12 items-center">
                              {getFormattedTime(flightDetails.outbound_arrival_datetime)}
                            </p>
                          </div>
                        </div>
                      </div>
                      <div>
                        <div className="font-bold">Inbound</div>
                        <div className="grid pl-2">
                          <div className="flex justify-between">
                            <Airport iata_code={flightDetails.inbound_departure_airport} name={flightDetails.outbound_arrival_name} />
                            <p className="flex text-sm text-sky-800 pr-12 items-center">
                              {getFormattedTime(flightDetails.inbound_departure_datetime)}
                            </p>
                          </div>
                          <div className="flex items-center gap-4 py-1 pl-3 h-12">
                            <div className="border-l-2 border-dotted border-gray-300 h-full"></div>
                            <p className="text-xs text-gray-400">{getTimeDifference(flightDetails.inbound_arrival_datetime, flightDetails.inbound_departure_datetime)}</p>
                          </div>
                          <div className="flex justify-between">
                            <Airport iata_code={flightDetails.inbound_arrival_airport} name={flightDetails.outbound_departure_name} />
                            <p className="flex text-sm text-sky-800 pr-12 items-center">
                              {getFormattedTime(flightDetails.inbound_arrival_datetime)}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div>No flight details available</div>
                  )
                )}
              </div>
            </div>
          </div>) : null}
      </div>
      <div className="flex items-center justify-center bg-sky-800 text-white py-2 hover:bg-sky-900 transition-colors cursor-pointer" onClick={handleDetailToggle}>
        <p className="px-4">{isOpen ? "hide flight details" : "show flight details"}
        </p>
        <Image src={isOpen ? "/icons/collapse.svg" : "/icons/expand.svg"} alt="icon" width={24} height={24} />
      </div>
    </div >
  )
}