"use client"

import * as React from "react"
import { ChevronDownIcon } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { transformDate } from "../functions"

export default function DateFilter(
  {
    classname,
    filtersKey,
    filtername,
    onChange
  }: {
    classname: string,
    filtersKey: string,
    filtername: string,
    onChange: (filterName: string, value: string | undefined) => void

  }
) {
  const [open, setOpen] = React.useState(false)
  const [date, setDate] = React.useState<Date | undefined>(undefined)

  return (
    <div>
      <div className="flex justify-center">
        <strong>{filtername}</strong>
      </div>
      <div className="flex justify-center p-2">
        <Popover open={open} onOpenChange={setOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              id="date"
              className="w-fit justify-between font-normal cursor-pointer"
            >
              {
                date ?
                  <Label className="px-1 cursor-pointer">{date.toLocaleDateString()}</Label> :
                  <Label className="px-1 cursor-pointer">Select Date</Label>
              }
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto overflow-hidden p-0" align="start">
            <Calendar
              mode="single"
              selected={date}
              captionLayout="dropdown"
              onSelect={(date) => {
                setDate(date)
                setOpen(false)
                onChange(filtersKey, date ? transformDate(date) : undefined)
              }}
            />
          </PopoverContent>
        </Popover>
      </div>
    </div>
  )
}
