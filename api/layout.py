import json
import networkx as nx
import igraph as ig
from data_utils import Data_Utils

class Layout:
    def __init__(self,config):
        """
        config:
            -dataset_name: str
            -source_id: str
            -start_time: int
            -end_time: int
            -time_interval: int
            -layout_width: float
            -layout_height: float
        """
        self.config=config
        self.df=Data_Utils.Data_Load.get_dataset_df(dataset_name=self.config["dataset_name"])
        self.gamma_dict,self.FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=self.config["source_id"],start_time=self.config["start_time"],end_time=self.config["end_time"],df=self.df)
        self.static_graph,self.time_list=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=self.gamma_dict)
        self.min_time,self.max_time=Data_Utils.Data_Analysis.get_min_max_time_of_df(df=self.df)

    def compute_base_layout(self):
        """
        initialize base layout graph
        """
        graph=nx.DiGraph()

        """
        compute y position dict
        """
        node_dfs_preorder=list(nx.dfs_preorder_nodes(self.static_graph,source=self.config["source_id"]))
        axis_y_pos_gap=self.config["layout_height"]/(len(node_dfs_preorder)-1)
        vertical_y_pos_dic={}
        for idx,node in enumerate(node_dfs_preorder):
            vertical_y_pos_dic[node]=idx*axis_y_pos_gap

        """
        compute x position dict
        """
        time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=self.config["start_time"],end_time=self.config["end_time"],time_interval=self.config["time_interval"])
        axis_x_pos_gap=self.config["layout_width"]/(len(time_axis_list)-1)
        axis_x_pos_dict={}
        for idx,time_axis in enumerate(time_axis_list):
            axis_x_pos_dict[time_axis]=idx*axis_x_pos_gap

        """
        load to graph
        """
        delta=self.config["time_interval"]
        for value in self.gamma_dict.values():
            FP_edge_event_list=value[0]
            tau=self.config["start_time"]
            for idx in range(len(FP_edge_event_list)):
                edge_event=FP_edge_event_list[idx]

                while edge_event.time-tau>delta:
                    tau=tau+delta
                
                if self.max_time<(tau+delta):
                    graph.add_node(edge_event.src+"_"+str(tau),vertex_id=edge_event.src,time=tau)
                    graph.add_node(edge_event.tar+"_"+str(self.max_time),vertex_id=edge_event.tar,time=self.max_time)
                    graph.add_edge(edge_event.src+"_"+str(tau),edge_event.tar+"_"+str(self.max_time),pre_time=tau,time=self.max_time)
                else:
                    graph.add_node(edge_event.src+"_"+str(tau),vertex_id=edge_event.src,time=tau)
                    graph.add_node(edge_event.tar+"_"+str(tau+delta),vertex_id=edge_event.tar,time=tau+delta)
                    graph.add_edge(edge_event.src+"_"+str(tau),edge_event.tar+"_"+str(tau+delta),pre_time=tau,time=tau+delta)

        """
        set node position
        """
        for node in graph.nodes():
            time=graph.nodes[node]["time"]
            vertex_id=graph.nodes[node]["vertex_id"]
            graph.nodes[node]["x_pos"]=axis_x_pos_dict[time]
            graph.nodes[node]["y_pos"]=vertical_y_pos_dic[vertex_id]

        return graph,time_axis_list 

    def compute_aggregated_TPVis_layout(self):
        """
        initialize tree
        """
        tree=nx.DiGraph()

        """
        aggregate algorithm
        """
        for value in self.gamma_dict.values():
            FP_edge_event_list=value[0]
            tau=self.config["start_time"]
            pre_id=self.config["source_id"]
            delta=self.config["time_interval"]
            tree.add_node(pre_id+"_"+str(tau),vertex_id=pre_id,time=tau)
            for idx in range(len(FP_edge_event_list)):
                edge_event=FP_edge_event_list[idx]
                while edge_event.time-tau>delta:
                    tree.add_node(edge_event.src+"_"+str(tau+delta),vertex_id=edge_event.src,time=tau+delta)
                    tree.add_edge(edge_event.src+"_"+str(tau),edge_event.src+"_"+str(tau+delta),time=tau+delta,pre_time=tau)
                    tau=tau+delta
                if idx!=len(FP_edge_event_list)-1 and edge_event.time<tau+delta and FP_edge_event_list[idx+1].time<=tau+delta:
                    continue

                if self.max_time<(tau+delta):
                    tree.add_node(edge_event.tar+"_"+str(self.max_time),vertex_id=edge_event.tar,time=self.max_time)
                    tree.add_edge(pre_id+"_"+str(tau),edge_event.tar+"_"+str(self.max_time),time=self.max_time,pre_time=tau)
                else:
                    tree.add_node(edge_event.tar+"_"+str(tau+delta),vertex_id=edge_event.tar,time=tau+delta)
                    tree.add_edge(pre_id+"_"+str(tau),edge_event.tar+"_"+str(tau+delta),time=tau+delta,pre_time=tau)
                    pre_id=edge_event.tar
                    tau=tau+delta

        """
        compute Reingold-Tilford layout using igraph
        1. convert networkx graph to igraph graph
        2. compute layout_reingold_tilford()
        3. adjust graph node position
        """
        ig_graph=ig.Graph.from_networkx(tree,vertex_attr_hashable="name")
        root_label=self.config["source_id"]+"_"+str(self.config["start_time"])
        root_idx=ig_graph.vs.find(name=root_label).index
        ig_layout=ig_graph.layout_reingold_tilford(root=[root_idx])
        tree_pos={vertex["name"]: ig_layout.coords[vertex.index] for vertex in ig_graph.vs} # (x,y)
        tree_pos={vertex: (y,x) for vertex,(x,y) in tree_pos.items()} # 트리 방향 회전
        # scaling y-coordinate to [0,layout_height]
        ys=[coord[1] for coord in tree_pos.values()]
        min_y,max_y=min(ys),max(ys)
        if max_y-min_y!=0:
            tree_pos={node: (coord[0],(coord[1]-min_y)/(max_y-min_y)*self.config["layout_height"]) for node,coord in tree_pos.items()}
        else:
            tree_pos={node: (coord[0],self.config["layout_height"]/2) for node,coord in tree_pos.items()} # 모든 y 값이 동일한 경우 중간값으로 설정
        
        """
        compute x position dict
        """
        time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=self.config["start_time"],end_time=self.config["end_time"],time_interval=self.config["time_interval"])
        axis_x_pos_gap=self.config["layout_width"]/(len(time_axis_list)-1)
        axis_x_pos_dict={}
        for idx,time_axis in enumerate(time_axis_list):
            axis_x_pos_dict[time_axis]=idx*axis_x_pos_gap

        """
        set node position
        """
        for node in tree.nodes():
            time=tree.nodes[node]["time"]
            tree.nodes[node]["x_pos"]=axis_x_pos_dict[time]
            tree.nodes[node]["y_pos"]=tree_pos[node][1]
        
        return tree,time_axis_list

    def compute_TPVis_layout(self):

        # for key,value in self.gamma_dict.items():
        #     print(f"last time: {value[1]} to {key}: ",end="")
        #     for edge_event in value[0]:
        #         print(f"{edge_event.tar}|{edge_event.time} ",end="")
        #     print()

        # for edge_event in self.FP_edge_event_list:
        #     print(f"{edge_event.src} {edge_event.tar} {edge_event.time}")
        """
        initialize tree
        """
        tree=nx.DiGraph()

        """
        convert to tree
        """
        tree.add_node(self.config["source_id"]+"_"+str(self.config["start_time"]),vertex_id=self.config["source_id"],time=self.config["start_time"])
        for value in self.gamma_dict.values():
            FP_edge_event_list=value[0]
            pre_time=self.config["start_time"]
            for edge_event in FP_edge_event_list:
                tree.add_node(edge_event.tar+"_"+str(edge_event.time),vertex_id=edge_event.tar,time=edge_event.time)
                tree.add_edge(edge_event.src+"_"+str(pre_time),edge_event.tar+"_"+str(edge_event.time),pre_time=pre_time,time=edge_event.time)
                pre_time=edge_event.time
        
        """
        compute Reingold-Tilford layout using igraph
        1. convert networkx graph to igraph graph
        2. compute layout_reingold_tilford()
        3. adjust graph node position
        """
        ig_graph=ig.Graph.from_networkx(tree,vertex_attr_hashable="name")
        root_label=self.config["source_id"]+"_"+str(self.config["start_time"])
        root_idx=ig_graph.vs.find(name=root_label).index
        ig_layout=ig_graph.layout_reingold_tilford(root=[root_idx])
        tree_pos={vertex["name"]: ig_layout.coords[vertex.index] for vertex in ig_graph.vs} # (x,y)
        tree_pos={vertex: (y,x) for vertex,(x,y) in tree_pos.items()} # 트리 방향 회전
        # scaling y-coordinate to [0,layout_height]
        ys=[coord[1] for coord in tree_pos.values()]
        min_y,max_y=min(ys),max(ys)
        if max_y-min_y!=0:
            tree_pos={node: (coord[0],(coord[1]-min_y)/(max_y-min_y)*self.config["layout_height"]) for node,coord in tree_pos.items()}
        else:
            tree_pos={node: (coord[0],self.config["layout_height"]/2) for node,coord in tree_pos.items()} # 모든 y 값이 동일한 경우 중간값으로 설정

        """
        compute x position dict
        """
        axis_x_pos_gap=self.config["layout_width"]/(len(self.time_list)-1)
        axis_x_pos_dict={}
        for idx,time_axis in enumerate(self.time_list):
            axis_x_pos_dict[time_axis]=idx*axis_x_pos_gap

        """
        set node position
        """
        for node in tree.nodes():
            time=tree.nodes[node]["time"]
            tree.nodes[node]["x_pos"]=axis_x_pos_dict[time]
            tree.nodes[node]["y_pos"]=tree_pos[node][1]

        return tree,self.time_list

    def convert_vertex_event_to_json(self,vertex_id:str,time:int,x_pos:float,y_pos:float):
        event_dic={}
        event_dic["id"]=vertex_id+"_"+str(time)
        event_dic["vertex_id"]=vertex_id
        event_dic["time"]=time
        event_dic["x_pos"]=x_pos
        event_dic["y_pos"]=y_pos
        event_dic["highlight"]=False

        return event_dic
    
    def convert_edge_event_to_json(self,source_id:str,target_id:str,time:int,pre_time:int):
        event_dic={}
        event_dic["id"]=source_id+"_"+target_id+"_"+str(time)
        event_dic["source_vertex_event_id"]=source_id+"_"+str(pre_time)
        event_dic["target_vertex_event_id"]=target_id+"_"+str(time)
        event_dic["time"]=time
        event_dic["highlight"]=False

        return event_dic

    def compute_layout_to_response_dict(self,layout_type="base"):
        match layout_type:
            case "base":
                layout_graph,time_axis_list=self.compute_base_layout()
            case "aggregated":
                layout_graph,time_axis_list=self.compute_aggregated_TPVis_layout()
            case "tpvis":
                layout_graph,time_axis_list=self.compute_TPVis_layout()
        
        vertex_event_list=[]
        edge_event_list=[]

        for node,attr in layout_graph.nodes(data=True):
            vertex_event_list.append(self.convert_vertex_event_to_json(vertex_id=node,time=attr.get("time"),x_pos=attr.get("x_pos"),y_pos=attr.get("y_pos")))
        
        for u,v,attr in layout_graph.edges(data=True):
            edge_event_list.append(self.convert_edge_event_to_json(source_id=u,target_id=v,time=attr.get("time"),pre_time=attr.get("pre_time")))

        response_dict={}
        response_dict["time_axis_list"]=time_axis_list
        response_dict["vertex_event_list"]=vertex_event_list
        response_dict["edge_event_list"]=edge_event_list

        return response_dict
        