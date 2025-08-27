import Link from "next/link"
import Icon from "./Icon"
import { getMealtypeIconFilename, getRoomtypeIconFilename } from "./functions"
import { Separator } from "@/components/ui/separator"


type CheapestOffer = {
  count_adults: number
  count_children: number
  count_offers: number
  duration: number
  hotel_name: string
  hotel_stars: number
  mealtype: string
  offer_id: number
  price: number
  roomtype: string
}

export default function CheapestHotelOffer(
  {
    offer
  }: {
    offer: CheapestOffer
  }) {

  const mealtypeIconPath = getMealtypeIconFilename(offer.mealtype);
  const roomtypeIconPath = getRoomtypeIconFilename(offer.roomtype);

  return (
    <div className="grid grid-cols-[1fr_auto] w-3xl m-1 rounded-xl border border-gray-300 shadow-md overflow-hidden">
      <div className="flex flex-col justify-between">
        <div className="flex gap-6 p-4 px-6">
          <div className="hotel-name font-medium text-2xl [font-variant:small-caps]">
            {offer.hotel_name}
          </div>
          <div className="hotel-stars flex text-2xl">
            {
              [...Array(offer.hotel_stars)].map((e, i) => <Icon key={i} description={`${offer.hotel_stars} stars`} filepath={"./icons/star.svg"} />)
            }
          </div>
        </div>
        <div className="flex gap-6 px-6 justify-between">
          <div className="flex">
            <Icon description={offer.mealtype} filepath={`./icons/${mealtypeIconPath}`} />
            <div className="flex px-2">
              <Separator orientation="vertical" />
            </div>
            <Icon description={offer.roomtype} filepath={`./icons/${roomtypeIconPath}`} />
          </div>
          <div>
            <div className="text-gray-600">{offer.duration} days · {offer.count_children + offer.count_adults} Pers.</div>
          </div>
        </div>
        <div className="flex gap-6 pb-4 px-6 justify-end">
          <div className="text-lg font-bold text-gray-800">from {offer.price} €</div>
        </div>
      </div>

      <Link
        href="/hotel-details"
        className="flex items-center justify-center bg-sky-800 text-white text-2xl px-6 hover:bg-sky-900 transition-colors h-full"
      >
        <Icon description="go to offers" filepath="./icons/arrow.svg" />
      </Link>
    </div>

  )
}

export type { CheapestOffer }
