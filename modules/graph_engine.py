import networkx as nx
from .graph_utils import GraphUtils,GraphAlgorithm

class GraphTransformEngine:
    """
    """
    def __init__(self,eventstream:list=None):
        self.eventstream=eventstream

    def set_event_stream(self,eventstream:list):
        self.eventstream=eventstream
    
    def transform_to_path_tree(self,source_id:int,start_time:int,end_time:int,time_interval:int):
        eventstream=GraphUtils.get_filtered_event_stream(
            eventstream=self.eventstream,
            start_time=start_time,
            end_time=end_time
        )
        graph=GraphUtils.convert_eventstream_to_graph(eventstream=eventstream)
        gamma_dict=GraphAlgorithm.compute_TP_parallel(graph=graph,source_id=source_id)

        for tar,(r,tar_t,src,src_t) in gamma_dict.items():
            if r==1:
                






    # def transform_to_path_tree_old(self):
    #     graph=GraphUtils.convert_eventstream_to_graph(event_stream=self.eventstream)
    #     gamma_dict=GraphAlgorithm.compute_TR_parallel(graph=graph,source_id=self.source_id)

    #     path_tree=nx.DiGraph()
    #     for target_node,(r,visited_t,p,p_visited_t) in gamma_dict.items():
    #         if r==1:
    #             src_id=f"{p}_{p_visited_t}"
    #             tar_id=f"{target_node}_{visited_t}"
    #             path_tree.add_node(src_id,time=visited_t)
    #             path_tree.add_node(tar_id,time=p_visited_t)
    #             path_tree.add_edge(src_id,tar_id)
    #     return path_tree