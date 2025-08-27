"use client";

import { MultiSelect } from "@/components/ui/multi-select";


export default function AirportFilter(
  {
    airportOptions,
    classname,
    onChange
  }: {
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
          options={airportOptions.map(airport => ({ value: airport.iata_code, label: airport.name }))}
          onValueChange={(v) => onChange("airport", v)}
          maxCount={2}
          placeholder="Select Airports"
          className="max-w-3xs"
        />
      </div>
    </div>
  )
}