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

	    <div className="flex flex-col items-center">
		<div className="flex flex-col items-center border-2 rounded-md border-sky-400 p-0 m-5 shadow-xl w-1/6">
		    <a href='/'>
			<h1 className="text-3xl m-3 m-0 font-bold">AD GENERATOR</h1>
		    </a>
		</div>
	    </div>
	    <div className="mt-10">
		{children}
	    </div>
	</body>
    </html>
  )
}
