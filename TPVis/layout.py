import json
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

    def compute_base_layout(self):
        """
        compute x position
        """
        time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=self.config["start_time"],end_time=self.config["end_time"],time_interval=self.config["time_interval"])
        axis_x_pos_gap=self.display_width/(len(time_axis_list)-1)
        axis_x_pos_dict={}
        for idx,time_axis in enumerate(time_axis_list):
            axis_x_pos_dict[time_axis]=idx*axis_x_pos_gap
        
        for edge_event in self.FP_edge_event_list:
            key=edge_event.time//self.config["time_interval"]
            if edge_event.time%self.config["time_interval"]==0 and edge_event.time!=0:
                key-=1
            self.tree.nodes[edge_event.src]["x_pos"]=axis_x_pos_dict[time_axis_list[key]]
            self.tree.nodes[edge_event.tar]["x_pos"]=axis_x_pos_dict[time_axis_list[key+1]]


    def return_vertex_event_json(self,vertex_id,time,x_pos,y_pos):
        event_dic={}
        event_dic['vertex_id']=vertex_id
        event_dic['time']=time
        event_dic['x_pos']=x_pos
        event_dic['y_pos']=y_pos
        event_dic['highlight']=False

        return event_dic
    
    def return_edge_event_json(self,source_id,target_id,time):
        event_dic={}
        event_dic['source_id']=source_id
        event_dic['target_id']=target_id
        event_dic['time']=time
        event_dic['highlight']=False

        return event_dic

    def get_tree_json(self):
        static_graph,time_list=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=self.gamma_dict)
