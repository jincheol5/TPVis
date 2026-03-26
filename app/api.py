import os
import uvicorn
from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from modules import DataUtils,LayoutConfig,Layout,GraphUtils,GraphTransformEngine,DBInterface

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_dataset")
def upload_dataset(file:UploadFile=File(...)):
    """
    """
    # get dataset_name
    dataset_name=os.path.splitext(file.filename)[0] # 확장자 제거

    # convert file to eventstream
    eventstream=[]
    for line in file.file: 
        line=line.decode("utf-8").strip()
        src,tar,t=line.split()
        eventstream.append((int(src),int(tar),int(t)))

    db_IF=DBInterface()
    db_IF.upload_dataset(dataset_name=dataset_name,event_stream=eventstream)
    dataset_list=db_IF.get_dataset_list()
    db_IF.disconnect_db()

    response_dict={}
    response_dict["dataset_list"]=dataset_list
    return response_dict

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
    dataset_name=layout_config.dataset_name
    db_IF=DBInterface()
    eventstream=db_IF.get_event_stream(dataset_name=dataset_name)
    db_IF.disconnect_db()

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
    return response_dict

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)