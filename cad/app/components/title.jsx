import React from 'react'

export function Title({ title }) {
    return (
	<div className="flex flex-col items-center">
	    <div className="flex flex-col items-center border-2 rounded-md border-sky-400 p-0 m-5 shadow-xl">
		<a href='/'>
		    <h1 className="text-3xl m-3 m-0 font-bold">{ title }</h1>
		</a>
	    </div>
	</div>
    );
}
