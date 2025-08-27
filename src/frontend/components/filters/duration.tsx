import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"


export default function DurationFilter(
  {
    classname,
    duration,
    onChange
  }: {
    classname: string,
    duration: number,
    onChange: (filterName: "duration", value: number) => void
  }) {
  return (
    <div>
      <div className="flex justify-center">
        <strong>Duration</strong>
      </div>
      <div className="flex justify-center p-2">
        <div className="flex">
          <Input className="w-12 justify-items-center" defaultValue={duration} onChange={(v) => onChange("duration", Number(v.target.value))} />
          <Label className="pl-2">days</Label>
        </div>
      </div>
    </div>
  )
}