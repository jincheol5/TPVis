import {visualize_timeline} from "./modules.js"
import {visualize_display} from "./modules.js"

const btn=document.getElementById("visualize");

btn.onclick=async function(){
    
    const background=d3.select("#background")
    const width=background.node().getBoundingClientRect().width
    const height=background.node().getBoundingClientRect().height
    const margin_x=width*0.05
    const margin_y=height*0.05
    const timeline_height=height*0.15

    const timeline=d3.select("#timeline")
    timeline.attr("transform",`translate(${margin_x},${margin_y})`)

    const display=d3.select("#display")
    display.attr("transform",`translate(${margin_x},${margin_y+timeline_height})`)

    const request_json={
        dataset_name: document.getElementById("dataset_name").value,
        path_type: document.getElementById("path_type").value,
        start_time: Number(document.getElementById("start_time").value),
        end_time: Number(document.getElementById("end_time").value),
        time_interval: Number(document.getElementById("time_interval").value),
        source_id: Number(document.getElementById("source_id").value),
        layout_width: width-margin_x*2,
        layout_height: height-margin_y*2-timeline_height
    }

    const res=await fetch("http://127.0.0.1:8000/compute_layout",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(request_json)
    })

    const response_json=await res.json()
    visualize_timeline(response_json,width-margin_x*2,timeline_height)
    visualize_display(response_json,height-margin_y*2-timeline_height)
}
