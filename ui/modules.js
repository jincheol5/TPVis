export function visualize_display(response_json){
    // get display svg
    const display=d3.select("#display");

    // 기존 시각화 삭제
    display.selectAll("*").remove();

    // visualize time_axis
    const layout_height=display.node().getBoundingClientRect().height;
    const time_axis_list=response_json["time_axis_list"];
    const time_axis_pos=response_json["time_axis_pos"];

    for (const time of time_axis_list){
        display.append("line")
            .attr("id","axis_"+time.toString())
            .attr("time",time)
            .attr("x1",time_axis_pos[time])
            .attr("y1",0)
            .attr("x2",time_axis_pos[time])
            .attr("y2",layout_height)
            .attr("stroke","gray")
            .attr("stroke-dasharray","5,5")
            .attr("stroke-width",1);
    }

    // visualize node event
    const node_event_list=response_json["node_event_list"];
    const node_pos_map={};
    for (const event of node_event_list){
        node_pos_map[event.id]={
            x: event.x_pos,
            y: event.y_pos
        }

        display.append("circle")
            .attr("id","node_event_"+event.id)
            .attr("cx",event.x_pos)
            .attr("cy",event.y_pos)
            .attr("r",3)
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    const color="black";
    const stroke_width=1;
    const opacity=0.5;
    for (const event of edge_event_list){
        const source=node_pos_map[event.source_id]
        const target=node_pos_map[event.target_id]
        display.append("line")
            .attr("x1",source.x)
            .attr("y1",source.y)
            .attr("x2",target.x)
            .attr("y2",target.y)
            .attr("stroke","black")
            .attr("stroke-width",stroke_width)
            .style("opacity",opacity);
            
    }

}