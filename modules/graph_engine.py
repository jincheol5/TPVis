import networkx as nx
from .graph_utils import GraphUtils,GraphAlgorithm

class GraphTransformEngine:
    """
    """
    def __init__(self,eventstream:list=None):
        self.eventstream=eventstream

    def set_event_stream(self,eventstream:list):
        self.eventstream=eventstream
    
    def transform_to_aggregated_path_tree(self,source_id:int,start_time:int,end_time:int,time_interval:int):
        eventstream=GraphUtils.get_filtered_eventstream(
            eventstream=self.eventstream,
            start_time=start_time,
            end_time=end_time
        )
        min_t,max_t=GraphUtils.get_min_max_time_in_eventstream(eventstream=eventstream)
        graph=GraphUtils.convert_eventstream_to_graph(eventstream=eventstream)
        path_dict=GraphAlgorithm.compute_TP_parallel(graph=graph,source_id=source_id)

        path_tree=nx.DiGraph()
        path_tree.add_node(f"{source_id}_{start_time}",node_id=source_id,time=start_time)
        for node,path in path_dict.items():
            """
            """
            tau=start_time
            pre_id=source_id
            for idx,(src,tar,t) in enumerate(path):
                while time_interval<t-tau:
                    path_tree.add_node(f"{src}_{tau+time_interval}",node_id=src,time=tau+time_interval)
                    path_tree.add_edge(f"{src}_{tau}",f"{src}_{tau+time_interval}",time=tau+time_interval)
                    tau=tau+time_interval
                if idx!=len(path)-1 and t<tau+time_interval and path[idx+1][2]<=tau+time_interval:
                    continue

                if max_t<(tau+time_interval):
                    path_tree.add_node(f"{tar}_{max_t}",node_id=tar,time=max_t)
                    path_tree.add_edge(f"{pre_id}_{tau}",f"{tar}_{max_t}",time=max_t)
                else:
                    path_tree.add_node(f"{tar}_{tau+time_interval}",node_id=tar,time=tau+time_interval)
                    path_tree.add_edge(f"{pre_id}_{tau}",f"{tar}_{tau+time_interval}",time=tau+time_interval)
                pre_id=tar
                tau=tau+time_interval
        return path_tree
