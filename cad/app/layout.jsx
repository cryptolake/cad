import React from 'react'
import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Automated Ad generator',
  description: 'An ad generator powered by GPT',
}

export default function RootLayout({children}) {
  return (
    <html lang="en">
	<body className={""+inter.className}>
	    {children}
	</body>
    </html>
  )
}
