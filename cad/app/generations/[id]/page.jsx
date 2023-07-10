'use client'

import React, { Suspense } from 'react';
import { AdList, Prompt } from '../../components/ad.jsx';

async function fetchPrompt(id) {
    const res = await fetch(`/api/prompts/${id}`, {
	method: "GET",
    });

    if (!res.ok) {
	throw new Error('Failed to fetch prompt');
    }

    return res.json();
}

export default async function Page({ params }) {
    const prompt = await fetchPrompt(params.id);

    console.log(await prompt.ads)

    return (
	<Suspense>
	    <div>
		<Prompt prompt={await prompt} />
		<AdList className="overflow-y-scroll" adList={await prompt.ads} />
	    </div>
	</Suspense>

    );
}
