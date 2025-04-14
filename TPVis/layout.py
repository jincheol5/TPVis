import json
import networkx as nx
from data_utils import Data_Utils

class Layout:
    def __init__(self,config):
        """
        config:
            -display_width: float
            -display_height: float
            -dataset_name: str
            -source_id: int
            -start_time: int
            -end_time: int
            -time_interval: int
        """
        self.config=config
        self.df=Data_Utils.Data_Load.get_dataset_df(dataset_name=self.config["dataset_name"])
        self.gamma_dict,self.FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=self.config["source_id"],start_time=self.config["start_time"],end_time=self.config["end_time"],df=self.df)
        self.tree=Data_Utils.Data_Process.convert_gamma_to_tree(gamma_dict=self.gamma_dict)
        self.static_graph,self.time_list=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=self.gamma_dict)

    def compute_base_layout(self):
        """
        initialize base layout graph
        """
        base_layout_graph=nx.DiGraph()

        """
        compute y position dict
        """
        node_dfs_preorder=list(nx.dfs_preorder_nodes(self.static_graph,source=self.source_id))
        axis_y_pos_gap=self.display_height/(len(node_dfs_preorder)-1)
        vertical_y_pos_dic={}
        for idx,node in enumerate(node_dfs_preorder):
            vertical_y_pos_dic[node]=idx*axis_y_pos_gap

        """
        compute x position dict
        """
        time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=self.config["start_time"],end_time=self.config["end_time"],time_interval=self.config["time_interval"])
        axis_x_pos_gap=self.display_width/(len(time_axis_list)-1)
        axis_x_pos_dict={}
        for idx,time_axis in enumerate(time_axis_list):
            axis_x_pos_dict[time_axis]=idx*axis_x_pos_gap

        """
        save base layout to networkx graph
        """
        for edge_event in self.FP_edge_event_list:
            key=edge_event.time//self.config["time_interval"]
            if edge_event.time%self.config["time_interval"]==0 and edge_event.time!=0:
                key-=1
            base_layout_graph.add_node(edge_event.src+"_"+str(time_axis_list[key]),x_pos=axis_x_pos_dict[time_axis_list[key]],y_pos=vertical_y_pos_dic[edge_event.src],node_id=edge_event.src,time=time_axis_list[key])
            base_layout_graph.add_node(edge_event.tar+"_"+str(time_axis_list[key+1]),x_pos=axis_x_pos_dict[time_axis_list[key+1]],y_pos=vertical_y_pos_dic[edge_event.tar],node_id=edge_event.tar,time=time_axis_list[key+1])
            base_layout_graph.add_edge(edge_event.src+"_"+str(time_axis_list[key]),edge_event.tar+"_"+str(time_axis_list[key+1]),time=edge_event.time)

