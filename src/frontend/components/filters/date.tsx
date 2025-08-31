"use client"

import * as React from "react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { transformDate } from "../functions"
import { useState } from "react"

export default function DateFilter(
  {
    classname,
    date,
    filtersKey,
    filtername,
    onChange,
    startDate
  }: {
    classname: string,
    date: string | null,
    filtersKey: string,
    filtername: string,
    onChange: (filterName: string, value: string | undefined) => void,
    startDate?: Date | undefined
  }
) {
  const [open, setOpen] = useState(false)
  const currentDate = date ? new Date(date) : undefined

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
                currentDate ?
                  <Label className="px-1 cursor-pointer">{currentDate.toLocaleDateString()}</Label> :
                  <Label className="px-1 cursor-pointer">Select Date</Label>
              }
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto overflow-hidden p-0" align="start">
            <Calendar
              mode="single"
              selected={currentDate}
              captionLayout="dropdown"
              disabled={startDate ? { before: startDate } : undefined}
              onSelect={(date) => {
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
