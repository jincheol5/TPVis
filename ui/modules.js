export function visualize_display(response_json){
    // get display svg
    const display=d3.select("#display");

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
            .attr("stroke-width",1);
    }

    // visualize node event
    const node_event_list=response_json["node_event_list"];
    for (const event of node_event_list){
        const color="black";
        const size=3;

        display.append("circle")
            .attr("id","node_event_"+event.id)
            .attr("node_id","node_"+event.node_id)
            .attr("time",event.time)
            .attr("r",size)
            .attr("cx",event.x_pos)
            .attr("cy",event.y_pos)
            .attr("fill",color);
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    for (const event of edge_event_list){
        const color="black";
        const stroke_width=1;
        const opacity=0.5;
        
        display.append("line")
            .attr("id","edge_event_"+event.id)
            .attr("source_id",event.source_vertex_event_id)
            .attr("target_id",event.target_vertex_event_id)
            .attr("x1",parseFloat(document.getElementById("node_event_"+event.source_id).getAttribute("cx")))
            .attr("y1",parseFloat(document.getElementById("node_event_"+event.source_id).getAttribute("cy")))
            .attr("x2",parseFloat(document.getElementById("node_event_"+event.target_id).getAttribute("cx")))
            .attr("y2",parseFloat(document.getElementById("node_event_"+event.target_id).getAttribute("cy")))
            .attr("stroke",color)
            .attr("stroke-width",stroke_width)
            .style("opacity",opacity);
    }
}