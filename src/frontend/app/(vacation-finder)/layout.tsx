import Filters from "@/components/filters/filters"
import { Navbar } from "@/components/navbar"

const airports = await fetch('http://localhost:8000/airports').then(res => res.json());

export default async function VacationFinderLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <div className="sticky top-0 z-50 bg-white shadow">
        <Navbar />
      </div>
      <div className="flex items-start">
        <div className="flex-none max-w-sm w-xs sticky top-15">
          <Filters airportOptions={airports} />
        </div>
        <div className="grow ">
          <main>{children}</main>
        </div>
      </div>
    </>
  )
}