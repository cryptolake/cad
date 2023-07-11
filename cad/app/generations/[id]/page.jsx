'use client'

import React, { Suspense } from 'react';
import { AdList, Prompt } from '../../components/ad.jsx';
import { Title } from '../../components/title.jsx'

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
	<>
	    <Title className="mb-10" title='Ad Generator' />
	    <Suspense fallback={<div>Loading...</div>}>
		<div>
		    <Prompt prompt={await prompt} />
		    <AdList  adList={await prompt.ads} />
		</div>
	    </Suspense>
	</>

    );
}
