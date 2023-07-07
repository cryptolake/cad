'use client'

import React from 'react';
import './globals.css'
import { TextInput, TextArea, NumberInput } from './components/input';
import { useState, Suspense } from 'react';

async function AdList({ adList }) {

    return (
    <>
	<ul className="overflow-y-auto h-1/2 p-6 divide-y divide-slate-200">
	    {adList.map(ad => (
	    <li key={ad.id} className="m-6 p-3 rounded shadow-lg ml-3 overflow-hidden">
		<div className="flex flex-col">
		    <h2 className="font-bold">Headline:</h2>
		    <p className="">{ad.headline}</p>
		</div>
		<div className="flex flex-col">
		    <h2 className="font-bold">Short Text:</h2>
		    <p className="">{ad.short_text}</p>
		</div>
		<div className="flex flex-col">
		    <h2 className="font-bold">Text:</h2>
		    <p className="">{ad.text}</p>
		</div>
	    </li>
	    ))}
	</ul>
    </>
    );

}

function Form({submitFun}) {

    return (
	<form className="w-full max-w-lg" onSubmit={submitFun}>
	    <div className="flex flex-row -mx-3 mb-6">
		<TextInput label="Brand Name" name="brand_name" placeholder=""/>
		<TextInput label="Product Name" name="product_name" placeholder=""/>
	    </div>

	    <div className="flex flex-col  mb-6">
		<TextArea label="Product Description" name="product_description" placeholder="" />
		<TextArea label="Parameters" name="parameters" placeholder="" />
	    </div>

	    <div className="flex flex-row -mx-3 mb-6">
		<NumberInput label="Number of Generations" name="n" placeholder="" value='10' step='1' />
		<NumberInput label="Temperature (model randomness)" name="temp" placeholder="" value='1.0' step='0.1'/>
	    </div>
	    <div className="flex items-center m-8">
		<NumberInput label="Max tokens" name="max_words" placeholder="" value='40' step='1'/>
	    </div>

	 <div className="flex flex-col items-center m-8">
	    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit">Generate</button>
	 </div>
	</form>
    );

}

function AdGenerator() {
    const [isDataFetching, setDataFetching] = useState(false);
    const [adList, setAdList] = useState(null);

    async function generateAds(event) {

	event.preventDefault()

	const prompt = {
	    brand_name: event.target.brand_name.value,
	    product_name: event.target.product_name.value,
	    product_description: event.target.product_description.value,
	    parameters: event.target.parameters.value,
	    n: event.target.n.value,
	    temp: event.target.temp.value,
	    max_words: event.target.max_words.value
	};

	const res = await fetch("/api/ads", {
	    method: "POST",
	    body: JSON.stringify(prompt),
	    headers: {
		    "Content-Type": "application/json",
	    },
	})

	if (!res.ok) {
	    throw new Error('Failed to create ad')
	}
	setDataFetching(true);
	setAdList(await res.json());
    }

    if (isDataFetching) {
	return (
	    <Suspense fallback={<div>Loading...</div>}>
		<AdList adList={adList} />
	    </Suspense>
	);
    };

    return (
	<div className="flex flex-col items-center">
	    <Suspense fallback={<div>Loading...</div>}>
		<Form submitFun={generateAds}/>
	    </Suspense>
	</div>
    );

}

export default function Page() {
    return (
	<div className="p-1 flex flex-col items-center">
	    <div className="border-2 rounded-md border-sky-400 p-0 m-20 shadow-xl">
		<a href='/'><h1 className="text-3xl m-3 m-0 font-bold">AD GENERATOR</h1></a>
	    </div>
	    <Suspense fallback={<div>Loading...</div>}>
		<AdGenerator />
	    </Suspense>
	</div>
    );
}
