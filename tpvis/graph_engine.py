import networkx as nx
from .graph_utils import GraphUtils,GraphAlgorithm

class GraphTransformEngine:
    """
    """
    def __init__(self,eventstream,config:dict):
        self.eventstream=eventstream
        self.config=config
        self.source_id=self.config['source_id']

    def set_event_stream(self,event_stream):
        self.event_steam=event_stream

    def transform_to_path_tree(self):
        graph=GraphUtils.convert_eventstream_to_graph(event_stream=self.eventstream)
        gamma_dict=GraphAlgorithm.compute_TR_parallel(graph=graph,source_id=self.source_id)

        path_tree=nx.DiGraph()
        for target_node,(r,visited_t,p,p_visited_t) in gamma_dict.items():
            if r==1:
                src_id=f"{p}_{p_visited_t}"
                tar_id=f"{target_node}_{visited_t}"
                path_tree.add_node(src_id,time=visited_t)
                path_tree.add_node(tar_id,time=p_visited_t)
                path_tree.add_edge(src_id,tar_id)
        return path_tree