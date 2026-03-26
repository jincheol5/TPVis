import {visualize_timeline} from "./modules.js"
import {visualize_display} from "./modules.js"
import {update_dataset_dropdown} from "./modules.js"

const visualize_btn=document.getElementById("visualize");
visualize_btn.onclick=async function(){
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

const file_input_btn=document.getElementById("file_input");
file_input_btn.addEventListener("change", async (e)=>{
    try {
        const file=e.target.files[0];
        if (!file) return;

        const formData=new FormData();
        formData.append("file",file);

        const res=await fetch("http://127.0.0.1:8000/upload_dataset", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            throw new Error("데이터셋 업로드 실패");
        }

        const result=await res.json();
        update_dataset_dropdown(result.datasets, result.saved_dataset);

    } catch (err) {
        console.error(err);
        alert("데이터셋 업로드 중 오류가 발생했습니다.");
    } finally {
        file_input_btn.value="";
    }
});