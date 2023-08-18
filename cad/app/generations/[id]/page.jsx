'use client'

import React, { Suspense } from 'react';
import { AdList, Prompt } from '../../components/ad.jsx';
import { Title } from '../../components/title.jsx';
import { ThemeSelector } from './../../components/theme.jsx'

async function fetchPrompt(id) {
    const res = await fetch(`/api/prompts/${id}`, {
        method: "GET",
    });

    if (!res.ok) {
        throw new Error(`Failed to fetch prompt ${req.status} ${req.body}`);
    }

    return await res.json();
}

export default async function Page({ params }) {
    const prompt = await fetchPrompt(params.id);

    return (
        <>
            <Title className="mb-10" title='Ad Generator' />
            <Suspense fallback={<div>Loading...</div>}>
                <div>
                    <Prompt prompt={prompt} />
                </div>
            </Suspense>
            <Suspense fallback={<div>Loading...</div>}>
                <div className="border-2 border-blue-500 m-5">
                    <AdList adList={prompt.ads} />
                </div>
            </Suspense>
            <Suspense fallback={<div>Loading...</div>}>
                <div className="border-2 border-blue-500 m-5">
                    <ThemeSelector ads={prompt.ads} />
                </div>
            </Suspense>
        </>

    );
}
