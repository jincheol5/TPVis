import networkx as nx
from data_utils import Data_Utils

def compute_aggregated_TPVis_layout(gamma_dict,source_id,start_time,time_interval):
    """
    initialize aggregated graph
    """
    aggregated_graph=nx.DiGraph()

    """
    aggregate algorithm
    """
    for value in gamma_dict.values():
        FP_edge_event_list=value[0]
        tau=start_time
        pre_id=source_id
        delta=time_interval
        aggregated_graph.add_node(pre_id+"_"+str(tau),vertex_id=pre_id,time=tau)
        for idx in range(len(FP_edge_event_list)):
            edge_event=FP_edge_event_list[idx]
            while edge_event.time-tau>delta:
                aggregated_graph.add_node(edge_event.src+"_"+str(tau+delta),vertex_id=edge_event.src,time=tau+delta)
                aggregated_graph.add_edge(edge_event.src+"_"+str(tau),edge_event.src+"_"+str(tau+delta),time=tau+delta,pre_time=tau)
                tau=tau+delta
            if idx!=len(FP_edge_event_list)-1 and edge_event.time<tau+delta and FP_edge_event_list[idx+1].time<=tau+delta:
                continue
            aggregated_graph.add_node(edge_event.tar+"_"+str(tau+delta),vertex_id=edge_event.tar,time=tau+delta)
            aggregated_graph.add_edge(pre_id+"_"+str(tau),edge_event.tar+"_"+str(tau+delta),time=tau+delta,pre_time=tau)
            pre_id=edge_event.tar
            tau=tau+delta
    return aggregated_graph

# df=Data_Utils.Data_Load.get_dataset_df(dataset_name="simple")
# gamma_dict,time_list=Data_Utils.Data_Process.compute_single_source_FP(source_id='a',start_time=0,end_time=9,df=df)
# aggregated_graph=compute_aggregated_TPVis_layout(gamma_dict=gamma_dict,source_id="a",start_time=0,time_interval=3)

# for node,data in aggregated_graph.nodes(data=True):
#     print(f"node_id: {node} vertex_id: {data.get("vertex_id")} time: {data.get("time")}")

# for u,v,data in aggregated_graph.edges(data=True):
#     print(f"src: {u} tar: {v} pre time: {data.get("pre_time")} time: {data.get("time")}")

# df=Data_Utils.Data_Load.get_dataset_df(dataset_name="CollegeMsg")
# print(df.dtypes)

# min_time,max_time=Data_Utils.Data_Analysis.get_min_max_time_of_df(df=df)
# print(f"min: {min_time} max: {max_time}")


time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=1082040961,end_time=1098777142,time_interval=1394681)
print(len(time_axis_list))
print(time_axis_list)