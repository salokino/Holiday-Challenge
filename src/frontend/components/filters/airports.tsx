"use client";

import { MultiSelect } from "@/components/ui/multi-select";


export default function AirportFilter(
  {
    airport,
    airportOptions,
    classname,
    onChange
  }: {
    airport: string[],
    airportOptions: { iata_code: string, name: string }[],
    classname: string,
    onChange: (filterName: "airport", value: string[]) => void
  }) {

  return (
    <div>
      <div className="flex justify-center">
        <strong>Airports</strong>
      </div>
      <div className="p-2 max-w-sm">
        <MultiSelect
          className="max-w-3xs"
          defaultValue={airport}
          maxCount={2}
          onValueChange={(v) => onChange("airport", v)}
          options={airportOptions.map(airport => ({ value: airport.iata_code, label: airport.name }))}
          placeholder="Select Airports"
        />
      </div>
    </div>
  )
}