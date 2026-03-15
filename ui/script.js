import {visualize_display} from './modules.js'

const btn=document.getElementById("visualize");

btn.onclick=async function(){

    const display=d3.select("#display");

    const request_json={
        dataset_name: document.getElementById("dataset_name").value,
        path_type: document.getElementById("path_type").value,
        start_time: Number(document.getElementById("start_time").value),
        end_time: Number(document.getElementById("end_time").value),
        time_interval: Number(document.getElementById("time_interval").value),
        source_id: Number(document.getElementById("source_id").value),
        layout_width: display.node().getBoundingClientRect().width,
        layout_height: display.node().getBoundingClientRect().height
    }

    const res=await fetch("http://127.0.0.1:8000/compute_layout",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify(request_json)
    })

    const response_json=await res.json()
    visualize_display(response_json)
}