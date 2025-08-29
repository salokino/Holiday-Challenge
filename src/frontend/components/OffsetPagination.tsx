import { Button } from "@/components/ui/button"
import Image from "next/image"

export default function OffsetPagination(
  {
    onChange
  }: {
    onChange: (direction: "plus" | "minus") => void
  }
) {
  const buttonStyle = "w-3xs bg-sky-800 hover:bg-sky-900 text-white hover:text-white"

  return (

    <div className="flex py-8 justify-center">
      <div className="flex px-2">
        <Button className={buttonStyle} onClick={() => onChange("minus")} variant="outline">
          <Image src="/icons/undo.svg" alt="icon" width={24} height={24} /> Previous
        </Button>
      </div>
      <div>
        <Button className={buttonStyle} onClick={() => onChange("plus")}>
          Next <Image src="/icons/redo.svg" alt="icon" width={24} height={24} />
        </Button>
      </div>
    </div>
  )
}