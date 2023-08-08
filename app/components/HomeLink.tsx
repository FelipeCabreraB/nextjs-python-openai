'use client'

import Link from 'next/link'
import React from 'react'
import { usePathname } from 'next/navigation'

const HomeLink = () => {
  const pathname = usePathname()
  if (pathname === '/') return null;

  return (
    <nav className='p-5 flex justify-center'>
        <Link href='/' className='text-green text-xl'>Back to Home</Link>
    </nav>
  )
}

export default HomeLink;
