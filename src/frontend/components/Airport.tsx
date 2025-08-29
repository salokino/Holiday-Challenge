import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"


export default function Airport(
  {
    iata_code,
    name
  }: {
    iata_code: string
    name: string
  }) {

  return (
    <div>
      <Tooltip>
        <TooltipTrigger>
          <p className="font-bold text-sm text-sky-800">
            {iata_code}
          </p>
        </TooltipTrigger>
        <TooltipContent>
          {name}
        </TooltipContent>
      </Tooltip>
    </div>
  )
}