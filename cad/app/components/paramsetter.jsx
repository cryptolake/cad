import React, { useState } from 'react';
import '../globals.css';


export default function ParamSetter({ params, setParams, setChanging }) {

    function changeColor(e) {
        setParams({
            color: e.target.value,
            size: params.size
        });
    }

    function changeNumber(e) {
        setParams({
            color: params.color,
            size: e.target.value
        });
    }

    function quit() {
        setChanging(null);
    }


    return (
        <div className="flex flex-col">
            <div className="flex border-2 rounded-md border-sky-400 p-2 m-2">
                <div className="flex">
                    <p className="flex mr-2">Font Color:</p>
                    <input onChange={changeColor} value={params.color} type="color" />
                </div>
                <div className="flex">
                    <p className="flex ml-10 mr-2">Font Size:</p>
                    <input onChange={changeNumber} value={params.size} type="number" />
                </div>
            </div>
            <button className="flex flex-col items-center border-2 rounded-md border-sky-400 p-2 m-2 pl-4 pr-4 shadow-xl" onClick={quit}>
                <p>Close</p>
            </button>
        </div>
    );
}
