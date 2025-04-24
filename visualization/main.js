import {request_layout} from './api.js';
import {visualize_layout,visualize_TPVis_layout} from './visualize.js';

document.addEventListener("DOMContentLoaded",function(){
    // 페이지가 완전히 로드된 후 실행되는 함수

    // 1. Visualize 버튼 클릭 시
    const visualize_button=document.getElementById("visualize_button");
    visualize_button.addEventListener("click",function(){

        const svg=d3.select("#display");
        svg.selectAll("*").remove();  // 이전 시각화 지우기

        // 입력값들을 읽어오기
        const dataset_name=document.getElementById("dataset_name").value;
        const source_id=document.getElementById("source_id").value;
        const start_time=parseInt(document.getElementById("start_time").value,10);
        const end_time=parseInt(document.getElementById("end_time").value,10);
        const time_interval=parseInt(document.getElementById("time_interval").value,10);

        // Semantic UI 드롭다운 값 읽기
        const dropdown=document.querySelector(".ui.dropdown");
        const layout_type=dropdown.value||dropdown.querySelector("select").value;

        // JSON 객체 생성
        const request_json={
            dataset_name: dataset_name,
            source_id: source_id,
            start_time: start_time,
            end_time: end_time,
            time_interval:time_interval,
            layout_type: layout_type,
            layout_width: 1800.0,
            layout_height: 1100.0,
            backward_id: null,
            forward_id: null
        };

        request_layout(request_json)
        .then(response_json=>{
            if (response_json["layout_type"]==="base"||response_json["layout_type"]==="tpvis_aggr"){
                visualize_layout(response_json);
            }
            else{
                visualize_TPVis_layout(response_json);
            }
        })
        .catch(error => {
            console.error("API 요청 또는 시각화 실패:", error);
        });

    });

    // 2. backward 버튼 클릭 시
    const backward_button=document.getElementById("backward_button");
    backward_button.addEventListener("click",function(){

        const svg=d3.select("#display");
        svg.selectAll("*").remove();  // 이전 시각화 지우기

        // 입력값들을 읽어오기
        const dataset_name=document.getElementById("dataset_name").value;
        const source_id=document.getElementById("source_id").value;
        const start_time=parseInt(document.getElementById("start_time").value,10);
        const end_time=parseInt(document.getElementById("end_time").value,10);
        const time_interval=parseInt(document.getElementById("time_interval").value,10);
        let backward_id=document.getElementById("backward_id").value;
        if (!backward_id){
            backward_id=null;
        }
        let forward_id=document.getElementById("forward_id").value;
        if (!forward_id){
            forward_id=null;
        }

        // Semantic UI 드롭다운 값 읽기
        const dropdown=document.querySelector(".ui.dropdown");
        const layout_type=dropdown.value||dropdown.querySelector("select").value;

        // JSON 객체 생성
        const request_json={
            dataset_name: dataset_name,
            source_id: source_id,
            start_time: start_time,
            end_time: end_time,
            time_interval:time_interval,
            layout_type: layout_type,
            layout_width: 1800.0,
            layout_height: 1100.0,
            backward_id: backward_id,
            forward_id: forward_id
        };

        request_layout(request_json)
        .then(response_json=>{
            if (response_json["layout_type"]==="base"||response_json["layout_type"]==="tpvis_aggr"){
                visualize_layout(response_json);
            }
            else{
                visualize_TPVis_layout(response_json);
            }
        })
        .catch(error => {
            console.error("API 요청 또는 시각화 실패:", error);
        });

    });

    // 3. forward 버튼 클릭 시
    const forward_button=document.getElementById("forward_button");
    forward_button.addEventListener("click",function(){
        const svg=d3.select("#display");
        svg.selectAll("*").remove();  // 이전 시각화 지우기

        // 입력값들을 읽어오기
        const dataset_name=document.getElementById("dataset_name").value;
        const source_id=document.getElementById("source_id").value;
        const start_time=parseInt(document.getElementById("start_time").value,10);
        const end_time=parseInt(document.getElementById("end_time").value,10);
        const time_interval=parseInt(document.getElementById("time_interval").value,10);
        let backward_id=document.getElementById("backward_id").value;
        if (!backward_id){
            backward_id=null;
        }
        let forward_id=document.getElementById("forward_id").value;
        if (!forward_id){
            forward_id=null;
        }

        // Semantic UI 드롭다운 값 읽기
        const dropdown=document.querySelector(".ui.dropdown");
        const layout_type=dropdown.value||dropdown.querySelector("select").value;

        // JSON 객체 생성
        const request_json={
            dataset_name: dataset_name,
            source_id: source_id,
            start_time: start_time,
            end_time: end_time,
            time_interval:time_interval,
            layout_type: layout_type,
            layout_width: 1800.0,
            layout_height: 1100.0,
            backward_id: backward_id,
            forward_id: forward_id
        };

        request_layout(request_json)
        .then(response_json=>{
            if (response_json["layout_type"]==="base"||response_json["layout_type"]==="tpvis_aggr"){
                visualize_layout(response_json);
            }
            else{
                visualize_TPVis_layout(response_json);
            }
        })
        .catch(error => {
            console.error("API 요청 또는 시각화 실패:", error);
        });
    });
});
