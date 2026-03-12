import networkx as nx
import igraph as ig

class Layout:
    """
    config
        source_id
        start_time
        end_time
        time_interval
        layout_width
        layout_height
    """
    def __init__(self,path_tree:nx.DiGraph):
        self.path_tree=path_tree

    def set_path_tree(self,path_tree:nx.DiGraph):
        self.path_tree=path_tree

    def initialize_node_pos(self):
        for node in self.path_tree.nodes():
            self.path_tree.nodes[node]['x']=0.0
            self.path_tree.nodes[node]['y']=0.0

    def compute_time_axis_list_and_pos(self,config:dict):
        """
        len(time_axis_list)==1 인 경우 오류 
        """
        start_time=config['start_time']
        end_time=config['end_time']
        layout_width=config['layout_width']

        time_axis_list=[]
        time_axis_pos={}

        time_interval=config['time_interval']
        if time_interval==0.0:
            time_axis_list=[self.path_tree.nodes[node]['time'] for node in self.path_tree.nodes()]
            time_axis_list=sorted(set(time_axis_list)) # 중복 제거
            x_pos_gap=float(layout_width/(len(time_axis_list)-1))
            for i,time_axis in enumerate(time_axis_list):
                time_axis_pos[time_axis]=i*x_pos_gap
        else:
            t=start_time
            while t<end_time:
                time_axis_list.append(t)
                t+=time_interval
            time_axis_list.append(end_time)

            x_pos_gap=float(layout_width/(len(time_axis_list)-1))
            for i,time_axis in enumerate(time_axis_list):
                time_axis_pos[time_axis]=i*x_pos_gap
        return time_axis_list,time_axis_pos

    def compute_linearized_bipartite_layout(self,config:dict):
        """
        << paper >> 
        Parallel Edge Splatting for Scalable Dynamic Graph Visualization (2011)
        """

    def compute_tpvis_layout(self,time_axis_pos:dict,config:dict):
        """
        << paper >>
        TPVis: A Temporal Path Visualization System for Intuitive Understanding of Information Diffusion Inside Temporal Networks (2025)
        
        Input:
            path_tree
            config
        Output:
            updated path_tree
        """
        ### initialize node position
        self.initialize_node_pos()

        ### compute Reingold-Tilford layout using igraph
        path_tree_ig=ig.Graph.from_networkx(g=self.path_tree)
        nx_nodes=list(self.path_tree.nodes())
        layout=path_tree_ig.layout_reingold_tilford(root=[config['source_id']])
        pos={nx_nodes[i]:(layout[i][1],-layout[i][0]) for i in range(len(nx_nodes))}

        ### scaling y position and update node attr 
        ys=[p[1] for p in pos.values()]
        min_y,max_y=min(ys),max(ys)
        y_range=max_y-min_y if max_y>min_y else 1.0
        
        ### set updated x, y position
        for node,(x,y) in pos.items():
            # set y position
            y_scaled=(y-min_y)/y_range*config["layout_height"]
            self.path_tree.nodes[node]['y']=float(y_scaled)
            # set x position (mapping x position to correct time_axis pos)
            valid_time=self.path_tree.nodes[node]['time']
            self.path_tree.nodes[node]['x']=time_axis_pos[valid_time]
        return self.path_tree