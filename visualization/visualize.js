export function visualize_layout(response_json){
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
        
        display.append("text")
            .attr("id","axis_label_"+time.toString())
            .attr("x",x_point+count*axis_x_pos_gap)
            .attr("y",y_point-50)
            .style("font-size","15px")
            .style("fill","green")
            .style("text-anchor","middle")
            .text(time.toString())
            .attr("transform","rotate(-45,"+String(x_point+count*axis_x_pos_gap)+","+String(y_point-50)+")");

        count+=1;
    }

    // visualize vertex event
    const vertex_event_list=response_json["vertex_event_list"];
    for (const event of vertex_event_list){
        let color=null;
        let size=null;
        if (event.backward==true){
            color="red";
            size=5;
        }
        else if (event.forward==true){
            color="blue";
            size=5;
        }
        else{
            color="#5b5b5b";
            size=3;
        }

        display.append("circle")
            .attr("id","vertex_event_"+event.id)
            .attr("vertex_id","vertex_"+event.vertex_id)
            .attr("time",event.time)
            .attr("r",size)
            .attr("cx",x_point+event.x_pos)
            .attr("cy",y_point+event.y_pos)
            .attr("fill",color)
            .raise()
            .on("click",function(){
                const vertex=d3.select(this)
                    .attr("r",5)
                    .attr("fill","red");
                display.append("text")
                    .attr("x",x_point+event.x_pos-50)
                    .attr("y",y_point+event.y_pos)
                    .style("font-size","20px")
                    .style("fill","red")
                    .text(event.vertex_id);
                vertex.raise();
            });
        
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    for (const event of edge_event_list){
        let color=null;
        if (event.backward==true){
            color="red";
        }
        else if (event.forward==true){
            color="blue";
        }
        else{
            color="#5b5b5b";
        }
        display.append("line")
            .attr("id","edge_event_"+event.id)
            .attr("source_vertex_event_id",event.source_vertex_event_id)
            .attr("target_vertex_event_id",event.target_vertex_event_id)
            .attr("time",event.time)
            .attr("x1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cx")))
            .attr("y1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cy")))
            .attr("x2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cx")))
            .attr("y2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cy")))
            .attr("stroke",color)
            .style("opacity",1.0);
        
    }

}

export function visualize_TPVis_layout(response_json){
    //get display svg and set point
    const display=d3.select("#display");
    const x_point=100.0
    const y_point=150.0

    // visualize vertex event
    const vertex_event_list=response_json["vertex_event_list"];
    for (const event of vertex_event_list){
        let color=null;
        let size=null;
        if (event.backward==true){
            color="red";
            size=5;
        }
        else if (event.forward==true){
            color="blue";
            size=5;
        }
        else{
            color="#5b5b5b";
            size=3;
        }
        display.append("circle")
            .attr("id","vertex_event_"+event.id)
            .attr("vertex_id","vertex_"+event.vertex_id)
            .attr("time",event.time)
            .attr("r",size)
            .attr("cx",x_point+event.x_pos)
            .attr("cy",y_point+event.y_pos)
            .attr("fill",color)
            .raise()
            .on("click",function(){
                const vertex=d3.select(this)
                    .attr("r",5)
                    .attr("fill","red");

                display.append("text")
                    .attr("x",x_point+event.x_pos-50)
                    .attr("y",y_point+event.y_pos)
                    .style("font-size","20px")
                    .style("fill","red")
                    .text(event.vertex_id);
                
                // time_axis
                display.append("line")
                    .attr("id","axis_"+event.time.toString())
                    .attr("time",event.time)
                    .attr("x1",x_point+event.x_pos)
                    .attr("y1",y_point)
                    .attr("x2",x_point+event.x_pos)
                    .attr("y2",y_point+1100.0)
                    .attr("stroke","green")
                    .attr("stroke-width",1);
                
                // time_axis_label
                display.append("text")
                    .attr("id","axis_label_"+event.time.toString())
                    .attr("time",event.time)
                    .attr("x",x_point+event.x_pos)
                    .attr("y",y_point-50)
                    .style("font-size","15px")
                    .style("fill","green")
                    .style("text-anchor","middle")
                    .text(event.time.toString())
                    .attr("transform","rotate(-45,"+String(x_point+event.x_pos)+","+String(y_point-50)+")");
                
                vertex.raise();
            });
            
            if (event.backward===true||event.forward===true){
                display.append("text")
                    .attr("x",x_point+event.x_pos-50)
                    .attr("y",y_point+event.y_pos)
                    .style("font-size","20px")
                    .style("fill",color)
                    .text(event.vertex_id);
                
                // time_axis
                display.append("line")
                    .attr("id","axis_"+event.time.toString())
                    .attr("time",event.time)
                    .attr("x1",x_point+event.x_pos)
                    .attr("y1",y_point)
                    .attr("x2",x_point+event.x_pos)
                    .attr("y2",y_point+1100.0)
                    .attr("stroke","green")
                    .attr("stroke-width",1);
                
                // time_axis_label
                display.append("text")
                    .attr("id","axis_label_"+event.time.toString())
                    .attr("time",event.time)
                    .attr("x",x_point+event.x_pos)
                    .attr("y",y_point-50)
                    .style("font-size","15px")
                    .style("fill","green")
                    .style("text-anchor","middle")
                    .text(event.time.toString())
                    .attr("transform","rotate(-45,"+String(x_point+event.x_pos)+","+String(y_point-50)+")");
            }
    }

    // visualize edge event
    const edge_event_list=response_json["edge_event_list"];
    for (const event of edge_event_list){
        let color=null;
        if (event.backward==true){
            color="red";
        }
        else if (event.forward==true){
            color="blue";
        }
        else{
            color="#5b5b5b";
        }
        display.append("line")
            .attr("id","edge_event_"+event.id)
            .attr("source_vertex_event_id",event.source_vertex_event_id)
            .attr("target_vertex_event_id",event.target_vertex_event_id)
            .attr("time",event.time)
            .attr("x1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cx")))
            .attr("y1",parseFloat(document.getElementById("vertex_event_"+event.source_vertex_event_id).getAttribute("cy")))
            .attr("x2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cx")))
            .attr("y2",parseFloat(document.getElementById("vertex_event_"+event.target_vertex_event_id).getAttribute("cy")))
            .attr("stroke",color)
            .style("opacity",1.0);
}
}