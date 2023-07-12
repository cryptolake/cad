'use client'

import React from 'react';
import './globals.css'
import { AdList, PromptList, Form, Prompt } from './components/ad.jsx'
import { Title } from './components/title.jsx'
import { useState, Suspense } from 'react';

function AdGenerator() {
    const [isDataFetched, setDataFetched] = useState(false);
    const [adList, setAdList] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [prompt, setPrompt] = useState(null);

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

	const req = fetch("/api/ads", {
	    method: "POST",
	    body: JSON.stringify(prompt),
	    headers: {
		    "Content-Type": "application/json",
	    },
	})

	setIsLoading(true);
	const res = await req;
	
	if (!res.ok) {
	    setIsLoading(false);
	    throw new Error('Failed to create ad')
	}

	setDataFetched(true);
	setIsLoading(false);
	setPrompt(prompt);
	setAdList(await res.json());
    }

    if (isDataFetched) {
	return (
	    <Suspense fallback={<div>Loading...</div>}>
		<div className='h-screen'>
		    <Prompt prompt={prompt} />
		    <AdList className='h-screen' adList={adList} />
		</div>
	    </Suspense>
	);
    };

    return (
	<div className="flex flex-col items-center">
	    <Suspense fallback={<div>Loading...</div>}>
		<Form submitFun={generateAds} isLoading={isLoading} />
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
	    <div className="basis-1/5">
		<Suspense fallback={<div>Loading...</div>}>
		    <PromptList promptList={promptsData} />
		</Suspense>
	    </div>
	    <div className="basis-4/5 p-1 flex flex-col items-center">
		<Title className="mb-10" title='Ad Generator' />
		<Suspense fallback={<div>Loading...</div>}>
		    <AdGenerator />
		</Suspense>
	    </div>
	</div>
    );
}
