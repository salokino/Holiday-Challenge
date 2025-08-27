import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Slider } from "@/components/ui/slider"



export default function PersonFilter(
  {
    adults,
    childs,
    classname,
    onChange
  }: {
    adults: number,
    childs: number,
    classname: string,
    onChange: (filterName: "adults" | "children", value: number) => void
  }) {
  return (
    <div>
      <div className="flex justify-center">
        <strong>Travelers</strong>
      </div>
      <div className="grid grid-cols-4 p-2">
        <p className="grid pr-2">Adults:</p>
        <Slider className="grid col-span-2" defaultValue={[adults]} max={10} min={0} step={1} onValueChange={(v) => onChange("adults", v[0])} />
        <span className="grid pl-2 w-4 text-right font-medium">{adults}</span>

      </div>
      <div className="grid grid-cols-4 p-2">
        <p className="grid pr-2">Children:</p>
        <Slider className="grid col-span-2" defaultValue={[childs]} max={10} min={0} step={1} onValueChange={(v) => onChange("children", v[0])} />
        <span className="grid pl-2 w-4 text-right font-medium">{childs}</span>

      </div>
    </div>
  )
}