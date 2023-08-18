import React from 'react';
import '../globals.css';

export function ListEntry({ title, para }) {
    return (
        <div className="flex flex-col">
            <h2 className="font-bold">{title}:</h2>
            <p className="">{para}</p>
        </div>
    );
}

export function ListImage({ title, src }) {
    return (
        <div className="flex flex-col">
            <h2 className="font-bold">{title}:</h2>
            <img src={src} className="overflow-scroll max-w-sm max-h-sm" />
        </div>

    );

}
