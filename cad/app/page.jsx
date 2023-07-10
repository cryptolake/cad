'use client'

import React from 'react';
import './globals.css'
import { AdList, PromptList, Form } from './components/ad.jsx'
import { useState, Suspense } from 'react';

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

async function getPrompts() {
    const res = await fetch("/api/prompts", {
	method: "GET",
    });

    if (!res.ok) {
	throw new Error('Failed to fetch prompts');

    }

    return res.json();
} 

export default async function Page() {
    const promptsData = await getPrompts()

    return (
	<div className="flex flex-row">
	    <div className="basis-1/6">
		<Suspense fallback={<div>Loading...</div>}>
		    <PromptList promptList={promptsData} />
		</Suspense>
	    </div>
	    <div className="basis-4/5 p-1 flex flex-col items-center">
		<Suspense fallback={<div>Loading...</div>}>
		    <AdGenerator />
		</Suspense>
	    </div>
	</div>
    );
}
