import React, { useState, useRef, useEffect } from 'react';
import ParamSetter from './paramsetter.jsx';
import '../globals.css';

export function ThemeCreator({ setTheme }) {
    const [image, setImage] = useState(null);
    const [isCreated, setIsCreated] = useState(false);
    const [headlineParams, setHeadlineParams] = useState(
        {
            size: 50,
            color: "#000000"
        }
    );

    const [ctcParams, setCtcParams] = useState(
        {
            size: 25,
            color: "#000000"
        }
    );

    const [changing, setChanging] = useState(null);

    const parent = useRef();
    const dragh = useRef();
    const dragc = useRef();

    let selected = null;

    const headLine = {
        x_pos: 0,
        y_pos: 0,
    };

    const callAction = {
        x_pos: 0,
        y_pos: 0,
    };

    const pointer = {
        x: 0,
        y: 0
    }

    function _drag_init(elem, obj) {


        selected = elem;

        const selectedLocX = selected.offsetLeft;
        const selectedLocY = selected.offsetTop;


        obj.x_pos = (pointer.x - selectedLocX)
        obj.y_pos = (pointer.y - selectedLocY)
        return false;

    }

    function _move_elem(e) {

        let obj = callAction;



        if (e.target.id == 'hl')
            obj = headLine;

        pointer.x = e.pageX;
        pointer.y = e.pageY;

        if (selected !== null) {
            selected.style.left = (pointer.x - obj.x_pos) + 'px';
            selected.style.top = (pointer.y - obj.y_pos) + 'px';
        }
        return false;

    }

    function _destroy() {
        selected = null;
        return false;
    }

    async function handleUpload(e) {

        const body = new FormData()
        body.append("image", e.target.files[0]);
        const res = await fetch("/api/upload_image", {

            method: "POST",
            body
        })

        if (!res.ok) {
            setImage(null);
        }

        else {
            const imageRes = await res.json();
            setImage(imageRes.location);
        }

    }

    function handleCancel() {
        setImage(null);
    }

    async function handleThemeUpload() {

        const parentLocX = parent.current.offsetLeft;
        const parentLocY = parent.current.offsetTop;

        const headline = {
            x: dragh.current.offsetLeft,
            y: dragh.current.offsetTop,
            font: "static/Emoji.ttf",
            size: headlineParams.size,
            color: headlineParams.color
        }

        const short = {
            x: dragc.current.offsetLeft,
            y: dragc.current.offsetTop,
            font: "static/Emoji.ttf",
            size: ctcParams.size,
            color: ctcParams.color
        }


        headline.x -= parentLocX;
        headline.y -= parentLocY;

        short.x -= parentLocX;
        short.y -= parentLocY;

        const reqBody = {
            headline: headline,
            short: short,
            image_loc: image
        }

        const req = fetch("/api/themes", {
            method: "POST",
            body: JSON.stringify(reqBody),
            headers: {
                "Content-Type": "application/json",
            },
        })

        const res = await req;
        if (!res.ok) {
            setImage(null);
            throw new Error('Failed to create theme')
        }
        setIsCreated(true);
        setTheme(await res.json());

    }

    useEffect(() => {
        if (image !== null && !isCreated) {
            if (dragc.current) {
                dragc.current.style.fontSize = ctcParams.size + 'px';
                dragc.current.style.color = ctcParams.color;

                dragc.current.onclick = () => {
                    setChanging('ctc');
                    return false;
                }
                dragc.current.onmousedown = () => {
                    _drag_init(dragc.current, callAction);
                    return false;
                }
                dragc.current.onmouseup = _destroy
            }

            if (dragh.current) {
                dragh.current.style.fontSize = headlineParams.size + 'px';
                dragh.current.style.color = headlineParams.color;

                dragh.current.onclick = () => {
                    setChanging('head');
                    return false;
                }
                dragh.current.onmousedown = () => {
                    _drag_init(dragh.current, headLine);
                    return false;
                }
                dragh.current.onmouseup = _destroy
            }

            if (parent.current) {
                parent.current.onmousemove = _move_elem
                parent.current.onmouseup = _destroy
            }
        }

    });


    return (
        <div className="flex flex-col items-center rounded-md p-0 shadow-xl ml-20">
            {image == null &&

                <>
                    <h2 className="mb-5">Upload Ad Image for Theme:</h2>
                    <input type="file" onChange={handleUpload} />
                </>

            }
            {image != null &&
                <div>
                    <div className="absolute cursor-move flex flex-col items-center shadow-xl" ref={dragh}>
                        <p className="m-3">
                            Headline Location
                        </p>
                    </div>
                    <div className="absolute cursor-move flex flex-col items-center shadow-xl" ref={dragc}>
                        <p className="m-3">
                            Call To action Location
                        </p>
                    </div>
                    <img ref={parent} src={image} />
                </div>
            }
            {image != null && !isCreated &&
                <div className="flex">
                    <button className="flex flex-col items-center border-2 rounded-md border-sky-400 p-2 m-2 pl-4 pr-4 shadow-xl" onClick={handleCancel}>
                        <p>Cancel</p>
                    </button>
                    <button className="flex flex-col items-center border-2 rounded-md border-sky-400 p-2 m-2 pl-4 pr-4 shadow-xl" onClick={handleThemeUpload}>
                        <p>Upload Theme</p>
                    </button>
                </div>
            }

            {image != null && !isCreated && changing === "head" &&
             <ParamSetter params={headlineParams} setParams={setHeadlineParams} setChanging={setChanging}/>
            }

            {image != null && !isCreated && changing === "ctc" &&
             <ParamSetter params={ctcParams} setParams={setCtcParams} setChanging={setChanging}/>
            }
            
        </div>
    );

}
