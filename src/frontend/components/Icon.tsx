import Image from "next/image";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip"

export default function Icon({
  description,
  filepath
}: {
  description: string,
  filepath: string
}) {
  return (
    <div>
      <Tooltip>
        <TooltipTrigger>
          <Image src={filepath} alt="icon" width={24} height={24} />
        </TooltipTrigger>
        <TooltipContent>
          <p>{description}</p>
        </TooltipContent>
      </Tooltip>
    </div>


  )
}