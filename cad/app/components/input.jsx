import '../globals.css'

export function TextInput({label, name, placeholder, value}) {

    return (
	<div className="w-full px-3 mb-6 md:mb-0">
	    <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor={name}>
		{label}
	    </label>
	    <input className="appearance-none block w-full bg-gray-200 text-gray-700 border border-sky-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id={name} name={name} placeholder={placeholder} type='text' defaultValue={value}></input>
	</div>
    );

}


export function NumberInput({label, name, placeholder, value, step}) {

    return (
	<div className="w-full px-3 mb-6 md:mb-0">
	    <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor={name}>
		{label}
	    </label>
	    <input className="appearance-none block w-full bg-gray-200 text-gray-700 border border-sky-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id={name} name={name} placeholder={placeholder} type='number' defaultValue={value} step={step}></input>
	</div>
    );

}

export function TextArea({label, name, placeholder}) {
    return (
	<div className="w-full px-0 mb-6 md:mb-0">
	    <label className="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" htmlFor={name}>
		{label}
	    </label>
	    <textarea className="appearance-none block w-full bg-gray-200 text-gray-700 border border-sky-500 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white" id={name} name={name} placeholder={placeholder} type="text"></textarea>
	</div>
    );

}
