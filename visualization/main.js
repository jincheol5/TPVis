import {request_simple_test,request_layout} from './api.js';
import {visualize_simple_test,visualize_base_layout} from './visualize.js';

document.addEventListener("DOMContentLoaded",function(){
    // 페이지가 완전히 로드된 후 실행되는 함수

    // 1. Visualize 버튼 클릭 시
    const visualize_button=document.getElementById("visualize");
    visualize_button.addEventListener("click",function(){
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
            layout_height: 1100.0
        };

        // request_simple_test(request_json)
        // .then(response_json=>{
        //     visualize_simple_test(response_json);
        // })
        // .catch(error => {
        //     console.error("API 요청 또는 시각화 실패:", error);
        // });

        request_layout(request_json)
        .then(response_json=>{
            visualize_base_layout(response_json);
        })
        .catch(error => {
            console.error("API 요청 또는 시각화 실패:", error);
        });

    });
});
