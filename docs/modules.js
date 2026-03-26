export function visualize_timeline(response_json,layout_width,timeline_height){
    const timeline=d3.select("#timeline");
    timeline.selectAll("*").remove();

    const time_axis_list=response_json["time_axis_list"];
    const time_axis_pos=response_json["time_axis_pos"];

    const axis_y=timeline_height*0.7;   // timeline 내부에서 y 위치

    // 가로 axis
    timeline.append("line")
        .attr("x1",0)
        .attr("y1",axis_y)
        .attr("x2",layout_width)
        .attr("y2",axis_y)
        .attr("stroke","black")
        .attr("stroke-width",2);

    // tick + label
    const formatYear=d3.timeFormat("%Y");
    const formatDate=d3.timeFormat("%m-%d");
    const formatTime=d3.timeFormat("%H:%M");
    for(const time of time_axis_list){
        const x=time_axis_pos[time];
        const date=new Date(time*1000);
        
        // year
        timeline.append("text")
            .attr("x",x)
            .attr("y",axis_y-50)
            .attr("text-anchor","middle")
            .attr("font-size",10)
            .attr("fill","#555")
            .text(formatYear(date));

        // date
        timeline.append("text")
            .attr("x",x)
            .attr("y",axis_y-36)
            .attr("text-anchor","middle")
            .attr("font-size",10)
            .attr("fill","#555")
            .text(formatDate(date));

        // time
        timeline.append("text")
            .attr("x",x)
            .attr("y",axis_y-22)
            .attr("text-anchor","middle")
            .attr("font-size",10)
            .attr("fill","#555")
            .text(formatTime(date));

        // tick
        timeline.append("line")
            .attr("x1",x)
            .attr("y1",axis_y)
            .attr("x2",x)
            .attr("y2",axis_y-8)
            .attr("stroke","black")
            .attr("stroke-width",2);
    }
}


export function visualize_display(response_json,layout_height){
    // get display svg
    const display=d3.select("#display");
    display.selectAll("*").remove();
    d3.selectAll(".node-tooltip").remove();

    // tooltip (메시지 박스)
    let tooltip=d3.select("body").select("#node-tooltip");
    if (tooltip.empty()){
        tooltip = d3.select("body")
            .append("div")
            .attr("id","node-tooltip")
            .attr("class","node-tooltip")
            .style("position","absolute")
            .style("background","white")
            .style("border","1px solid gray")
            .style("padding","4px 8px")
            .style("font-size","12px")
            .style("pointer-events","none")
            .style("display","none");
    }

    // visualize time_axis
    const time_axis_list=response_json["time_axis_list"];
    const time_axis_pos=response_json["time_axis_pos"];

    for (const time of time_axis_list){
        const x=time_axis_pos[time];

        display.append("line")
            .attr("id","axis_"+time)
            .attr("time",time)
            .attr("x1",x)
            .attr("y1",0)
            .attr("x2",x)
            .attr("y2",layout_height)
            .attr("stroke","gray")
            .attr("stroke-dasharray","5,5")
            .attr("stroke-width",1);
    }

    // visualize node event
    const node_event_list=response_json["node_event_list"];
    const node_pos_map={};
    for (const event of node_event_list){
        const x=event.x_pos;
        const y=event.y_pos;

        node_pos_map[event.id]={x,y};

        display.append("circle")
            .attr("id","node_event_"+event.id)
            .attr("cx",x)
            .attr("cy",y)
            .attr("r",3)
            .attr("fill","black")
            .on("click",function(){
                const node=d3.select(this);
                const node_id=event.node_id;
                const tooltip_id="tooltip_"+node_id;
                const existing_tooltip=d3.select("#"+tooltip_id);

                // 이미 선택된 상태 → 원상복구
                if(node.classed("selected")){
                    node
                        .classed("selected",false)
                        .attr("r",3)
                        .attr("fill","black");
                    existing_tooltip.remove();
                    return;
                }
                // 선택 상태
                node
                    .classed("selected",true)
                    .attr("r",5)
                    .attr("fill","red")
                    .raise();

                // node 위치
                const cx=+node.attr("cx");
                const cy=+node.attr("cy");

                // svg 위치
                const svgRect=display.node().getBoundingClientRect();

                // tooltip 생성
                d3.select("body")
                    .append("div")
                    .attr("id",tooltip_id)
                    .style("position","absolute")
                    .style("background","white")
                    .style("border","1px solid gray")
                    .style("padding","3px 6px")
                    .style("font-size","12px")
                    .style("pointer-events","none")
                    .style("left",(svgRect.left+cx-30)+"px")
                    .style("top",(svgRect.top+cy-50)+"px")
                    .text("node_id: "+node_id);
            });
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    for (const event of edge_event_list){
        const source=node_pos_map[event.source_id];
        const target=node_pos_map[event.target_id];
        display.append("line")
            .attr("x1",source.x)
            .attr("y1",source.y)
            .attr("x2",target.x)
            .attr("y2",target.y)
            .attr("stroke","black")
            .attr("stroke-width",1)
            .style("opacity",0.5);
    }
}

export function update_dataset_dropdown(dataset_list){
    const dataset_select=document.getElementById("dataset_select");

    // 1. 기존 옵션 초기화
    dataset_select.innerHTML="";

    // 2. 기본 옵션 추가
    const default_option=document.createElement("option");
    default_option.value="";
    default_option.disabled=true;
    default_option.textContent="Select Dataset";
    dataset_select.appendChild(default_option);

    // 3. datasets로 옵션 생성
    dataset_list.forEach((name)=>{
        const option=document.createElement("option");
        option.value=name;
        option.textContent=name;
        dataset_select.appendChild(option);
    });

    // 4. Semantic UI dropdown 갱신
    $("#dataset_select").dropdown("clear");
    $("#dataset_select").dropdown("refresh");
}
