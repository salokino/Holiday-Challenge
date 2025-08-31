import { Navbar } from "@/components/navbar"

export default function AvailableHotelsLayout({
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
        <div className="grow ">
          <main>{children}</main>
        </div>
      </div>
    </>
  )
}