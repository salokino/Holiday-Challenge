"use client"

import * as React from "react"
import Link from "next/link"
import Image from "next/image"
import { Separator } from "@/components/ui/separator"


const menuLinkStyle = "text-lg text-white font-bold"
const menuLinkHoverStyle = "hover:scale-[1.07]"

export function Navbar() {
  return (
    <div className="flex items-center gap-8 bg-sky-900 px-6 py-2 h-15">
      <Link href="/">
        <Image alt="check24-logo" src="/logo.svg" width={100} height={50} />
      </Link>
      <div className="flex flex-1 justify-center bg-sky-900 [font-variant:small-caps]">
        <div className={menuLinkHoverStyle}>
          <Link className={menuLinkStyle} href="/">Home</Link>
        </div>
        <div className="px-4">
          <Separator orientation="vertical" className="text-white" />
        </div>
        <div className={menuLinkHoverStyle}>
          <Link className={menuLinkStyle} href="/vacation-finder">Vacation Finder</Link>
        </div>
        <div className="px-4">
          <Separator orientation="vertical" className="text-white" />
        </div>
        <div className={menuLinkHoverStyle}>
          <Link className={menuLinkStyle} href="/available-hotels">Hotels</Link>
        </div>
        <div className="px-4">
          <Separator orientation="vertical" className="text-white" />
        </div>
        <div className={menuLinkHoverStyle}>
          <Link className={menuLinkStyle} href="/about">About</Link>
        </div>
      </div>
    </div>
  )
}
