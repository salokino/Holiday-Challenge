import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { toast } from "sonner"

export default function DurationFilter(
  {
    classname,
    duration,
    onChange
  }: {
    classname: string,
    duration: number,
    onChange: (filterName: "duration", value: number) => void
  }
) {

  const handleDurationChange = (value: string) => {
    if (!isNaN(Number(value))) {
      onChange("duration", Number(value))
    } else {
      return toast.error(
        "You can only enter numbers.",
        {
          duration: 3000,
          position: "top-center"
        }
      )
    }
  }

  return (
    <div>
      <div className="flex justify-center">
        <strong>Duration</strong>
      </div>
      <div className="flex justify-center p-2">
        <div className="flex">
          <Input className="w-12 justify-items-center" type="text" value={duration} onChange={(v) => handleDurationChange(v.target.value)} />
          <Label className="pl-2">days</Label>
        </div>
      </div>
    </div>
  )
}