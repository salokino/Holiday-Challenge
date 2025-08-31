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
      <div className="flex justify-center items-center gap-2">
        <p className="w-20 pl-4">Adults:</p>
        <Slider className="flex-1" value={[adults]} max={10} min={0} step={1} onValueChange={(v) => onChange("adults", v[0])} />
        <span className="w-4 pr-6 text-right font-medium">{adults}</span>
      </div>
      <div className="flex justify-center items-center gap-2">
        <p className="w-20 pl-4">Children:</p>
        <Slider className="flex-1" value={[childs]} max={10} min={0} step={1} onValueChange={(v) => onChange("children", v[0])} />
        <span className="w-4 pr-6 text-right font-medium">{childs}</span>
      </div>
    </div>
  )
}