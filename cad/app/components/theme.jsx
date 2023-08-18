'use client'

import React, { useState, Suspense } from 'react';
import { ListEntry, ListImage } from './list';
import '../globals.css';

function AdImages({ template, ads }) {
    const [images, setImages] = useState([]);

    async function createImages()
    {
        const images = []

        ads.forEach( async (ad) => {
            const data = {
                "template": template.uid,
                modifications: [
                    {
                        "name": "headline",
                        "text": ad.headline
                    },
                    {
                        "name": "ctc",
                        "text": ad.short
                    },
                ]

            }
            const req = await fetch('https://sync.api.bannerbear.com/v2/images', {
                method: 'POST',
                body: JSON.stringify(data),
                headers: {
                    'Authorization': 'Bearer bb_pr_ef33c6f33918e2d14702e9b1ca77d3'
                }
            });

            if (!req.ok) {

                throw new Error(`Failed to create image: ${req.status} ${req.body}`);
            } else {

                const image = await req.json();

                images.push(image);

                const upAd = await fetch(`/api/images?uid=${image.uid}&ad_id=${ad.id}`, {
                    method: 'POST',
                    body: JSON.stringify({
                        location: image.image_url,
                    }),
                    headers: {
                        "Content-Type": "application/json",
                    }
                });

                if (!upAd.ok) {

                    throw new Error(`Failed to register image: ${upAd.status} ${upAd.body}`);
                }
            }

        })

        setImages(images);
    }

    if (images.length != 0) {
        return (
            <div className="overflow-x-scroll w-100">
                <Suspense fallback={<div>Loading...</div>}>
                    <ul className="flex flex-row flex-wrap">
                        {images.map(image => (
                            <li className="m-6 p-3 rounded shadow-lg ml-3 overflow-hidden">
                                <ListImage title="Ad Image" src={image.image_url} />
                            </li>
                        ))}
                    </ul>
                </Suspense>
            </div>
        );
    } else {
        return (
            <div className="flex flex-col items-center m-5">
                <Suspense fallback={<div>Loading...</div>}>
                    <img src={template.preview_url} className="overflow-scroll max-w-sm max-h-sm" />
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2" onClick={createImages}>
                        Generate Images
                    </button>
                </Suspense>
            </div>

        );

    }
}

export function ThemeSelector({ ads }) {

    const [templates, setTemplates] = useState(null);
    const [template, setTemplate] = useState(null);
    const [clicked, setClicked] = useState(false);

    async function fetchTemplates() {
        const req = await fetch('https://api.bannerbear.com/v2/templates', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer bb_pr_ef33c6f33918e2d14702e9b1ca77d3'
            }
        });

        if (!req.ok) {

            throw new Error(`Failed to fetch themes: ${req.status} ${req.body}`);
        }

        setTemplates(await req.json());
    }

    fetchTemplates();

    if (clicked && template === null) {
        return (
            <div className="flex flex-col items-center rounded-md p-0 shadow-xl ml-20 h-1/2">
                <ul className="flex flex-row p-6 divide-y divide-slate-200">
                    {templates.map(template => (
                        <li key={template.uid} className="m-6 p-3 rounded shadow-lg ml-3 overflow-hidden">
                            <ListEntry title="Theme Name" para={template.name} />
                            <ListImage title="Theme Preview" src={template.preview_url} />
                            <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2" onClick={() => { setTemplate(template); }}>
                                select
                            </button>

                        </li>
                    ))}
                </ul>
                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2" onClick={() => { setClicked(false); }}>
                    Close
                </button>
            </div>
        );

    }

    else if (clicked && template !== null) {
        return (
            <div className="flex flex-col items-center rounded-md p-0 shadow-xl ml-20">
                <Suspense fallback={<div>Loading...</div>}>
                    <AdImages template={template} ads={ads} />
                </Suspense>
                <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2" onClick={() => { setClicked(false); setTemplate(null); }}>
                    Close
                </button>
            </div>

        );
    } else {
        return (
            <>
                <div className="m-5 flex flex-col items-center">
                    <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onClick={() => { setClicked(true); }}>
                        Choose a theme
                    </button>
                </div>
            </>

        );

    }
}
