import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules import LayoutConfig,Layout,GraphUtils,GraphTransformEngine


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compute_layout")
def compute_layout(layout_config:LayoutConfig):
    """
    layout_config
        dataset_name
        path_type
        source_id
        start_time
        end_time
        time_interval
        layout_width
        layout_height
    """
    eventstream=[
                (0,2,1),
                (0,2,2),
                (0,3,3),
                (1,7,4),
                (0,1,5),
                (1,6,6),
                (0,3,7),
                (3,6,7),
                (3,4,8),
                (2,5,9)
            ]
    layout_config=GraphUtils.check_layout_config_time_range(eventstream=eventstream,layout_config=layout_config)

    graph_engine=GraphTransformEngine(eventstream=eventstream)
    path_tree=graph_engine.transform_to_aggregated_path_tree(
        source_id=layout_config.source_id,
        start_time=layout_config.start_time,
        end_time=layout_config.end_time,
        time_interval=layout_config.time_interval
    )

    layout=Layout(path_tree=path_tree)
    time_axis_list,time_axis_pos=layout.compute_time_axis_list_and_pos(layout_config=layout_config.model_dump())

    updated_path_tree=layout.compute_tpvis_layout(
        time_axis_pos=time_axis_pos,
        layout_config=layout_config.model_dump()
    )
    response_dict=GraphUtils.convert_to_response_dict(
        path_tree=updated_path_tree,
        time_axis_list=time_axis_list,
        time_axis_pos=time_axis_pos
    )

    print(response_dict["node_event_list"])
    print(response_dict["edge_event_list"])


    return response_dict

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)