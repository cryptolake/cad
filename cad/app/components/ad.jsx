'use client'

import React from 'react';
import { TextInput, TextArea, NumberInput } from './input';

export function ListEntry({ title, para })
{
    return (
	<div className="flex flex-col">
	    <h2 className="font-bold">{title}:</h2>
	    <p className="">{para}</p>
	</div>
    );
}

export async function Prompt({ prompt }) {
    return (
	<div className="m-6 p-3 rounded shadow-lg overflow-hidden">
	    <ListEntry title="Brand Name" para={prompt.brand_name} />
	    <ListEntry title="Product Name" para={prompt.product_name} />
	    <ListEntry title="Product Description" para={prompt.product_description} />
	</div>
    );

}

export async function AdList({ adList }) {

    return (
    <ul className="overflow-y-auto h-1/2 p-6 divide-y divide-slate-200">
	{adList.map(ad => (
	<li key={ad.id} className="m-6 p-3 rounded shadow-lg ml-3 overflow-hidden">
	    <ListEntry title="Headline" para={ad.headline} />
	    <ListEntry title="Short Text" para={ad.short_text} />
	    <ListEntry title="Text" para={ad.text} />
	</li>
	))}
    </ul>
    );

}


export async function PromptList({ promptList }) {
    return (
	<ul className="overflow-y-scroll h-1/6 p-4">
	    {promptList.reverse().map(prompt => (
		<li key={prompt.id} className="h-35 m-5 p-3 rounded shadow-lg overflow-hidden">
		    <a href={`/generations/${prompt.id}`}>
			<ListEntry title="Brand Name" para={prompt.brand_name} />
			<ListEntry title="Product Name" para={prompt.product_name} />
		    </a>
		</li>
	    ))}
    </ul>
 );
}


export function Form({submitFun}) {

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
