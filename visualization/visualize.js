export function visualize_base_layout(response_json){
    //get display svg and set point
    const display=d3.select("#display");
    const x_point=100.0
    const y_point=150.0

    // visualize time_axis
    const layout_width=1800.0
    const time_axis_list=response_json["time_axis_list"];
    const axis_x_pos_gap=layout_width/(time_axis_list.length-1);
    let count=0;
    for (const time of time_axis_list){
        display.append("line")
            .attr("id","axis_"+time.toString())
            .attr("time",time)
            .attr("x1",x_point+count*axis_x_pos_gap)
            .attr("y1",y_point)
            .attr("x2",x_point+count*axis_x_pos_gap)
            .attr("y2",y_point+1100.0)
            .attr("stroke","green")
            .attr("stroke-width",1);
        count+=1;
    }

    // visualize vertex event
    const vertex_event_list=response_json["vertex_event_list"];
    for (const event of vertex_event_list){
        display.append("circle")
            .attr("id","vertex_event_"+event.id)
            .attr("vertex_id","vertex_"+event.vertex_id)
            .attr("time",event.time)
            .attr("r",2)
            .attr("cx",x_point+event.x_pos)
            .attr("cy",y_point+event.y_pos)
            .attr("fill","#5b5b5b");
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    for (const event of edge_event_list){
        display.append("line")
            .attr("id","edge_event_"+event.id)
            .attr("source_vertex_event_id",event.source_vertex_event_id)
            .attr("target_vertex_event_id",event.target_vertex_event_id)
            .attr("time",event.time)
            .attr("x1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cx")))
            .attr("y1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cy")))
            .attr("x2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cx")))
            .attr("y2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cy")))
            .attr("stroke","#444444")
            .style("opacity",0.3);
    }

}