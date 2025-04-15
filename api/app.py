from data_utils import Data_Utils
from layout import Layout
import json


config={
    "display_width": 100.0,
    "display_height": 100.0,
    "dataset_name": "simple",
    "source_id": "a",
    "start_time": 0,
    "end_time": 9,
    "time_interval": 3
}

layout=Layout(config=config)
response_dict=layout.compute_layout_json_string(layout_type="base")
print(json.dumps(response_dict,indent=2))


# import networkx as nx
# df=Data_Utils.Data_Load.get_dataset_df(dataset_name=config["dataset_name"])
# gamma_dict,FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=config["source_id"],start_time=config["start_time"],end_time=config["end_time"],df=df)
# static_graph,time_list=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=gamma_dict)
# node_dfs_preorder=list(nx.dfs_preorder_nodes(static_graph,source=config["source_id"]))
# print(node_dfs_preorder)