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
            -source_id: str
            -start_time: int
            -end_time: int
            -time_interval: int
        """
        self.config=config
        self.df=Data_Utils.Data_Load.get_dataset_df(dataset_name=self.config["dataset_name"])
        self.gamma_dict,self.FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=self.config["source_id"],start_time=self.config["start_time"],end_time=self.config["end_time"],df=self.df)
        self.static_graph,self.time_list=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=self.gamma_dict)

    def compute_base_layout(self):
        """
        initialize base layout graph
        """
        base_layout_graph=nx.DiGraph()

        """
        compute y position dict
        """
        node_dfs_preorder=list(nx.dfs_preorder_nodes(self.static_graph,source=self.config["source_id"]))
        axis_y_pos_gap=self.config["display_height"]/(len(node_dfs_preorder)-1)
        vertical_y_pos_dic={}
        for idx,node in enumerate(node_dfs_preorder):
            vertical_y_pos_dic[node]=idx*axis_y_pos_gap

        """
        compute x position dict
        """
        time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=self.config["start_time"],end_time=self.config["end_time"],time_interval=self.config["time_interval"])
        axis_x_pos_gap=self.config["display_width"]/(len(time_axis_list)-1)
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
            base_layout_graph.add_node(edge_event.src+"_"+str(time_axis_list[key]),x_pos=axis_x_pos_dict[time_axis_list[key]],y_pos=vertical_y_pos_dic[edge_event.src],vertex_id=edge_event.src,time=time_axis_list[key])
            base_layout_graph.add_node(edge_event.tar+"_"+str(time_axis_list[key+1]),x_pos=axis_x_pos_dict[time_axis_list[key+1]],y_pos=vertical_y_pos_dic[edge_event.tar],vertex_id=edge_event.tar,time=time_axis_list[key+1])
            base_layout_graph.add_edge(edge_event.src+"_"+str(time_axis_list[key]),edge_event.tar+"_"+str(time_axis_list[key+1]),time=edge_event.time)
        
        return base_layout_graph,time_axis_list

    def convert_vertex_event_json(self,vertex_id:str,time:int,x_pos:float,y_pos:float):
        event_dic={}
        event_dic['vertex_id']=vertex_id
        event_dic['time']=time
        event_dic['x_pos']=x_pos
        event_dic['y_pos']=y_pos
        event_dic['highlight']=False

        return event_dic
    
    def convert_edge_event_json(self,source_id:str,target_id:str,time:int):
        event_dic={}
        event_dic['source_id']=source_id
        event_dic['target_id']=target_id
        event_dic['time']=time
        event_dic['highlight']=False

        return event_dic

    def compute_layout_json_string(self,layout_type="base"):
        match layout_type:
            case "base":
                layout_graph,time_axis_list=self.compute_base_layout()
        
        vertex_event_list=[]
        edge_event_list=[]

        for node,attr in layout_graph.nodes(data=True):
            vertex_event_list.append(self.convert_vertex_event_json(vertex_id=node,time=attr.get("time"),x_pos=attr.get("x_pos"),y_pos=attr.get("y_pos")))
        
        for u,v,attr in layout_graph.edges(data=True):
            edge_event_list.append(self.convert_edge_event_json(source_id=u,target_id=v,time=attr.get("time")))

        response_dict={}
        response_dict["time_axis_list"]=time_axis_list
        response_dict["vertex_event_list"]=vertex_event_list
        response_dict["edge_event_list"]=edge_event_list

        return response_dict
        