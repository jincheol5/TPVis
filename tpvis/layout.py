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
    @staticmethod
    def compute_time_axis_list_and_pos(config:dict):
        """
        start, end axis 없엘지 말지 고민
        """
        start_time=config['start_time']
        end_time=config['end_time']
        time_interval=config['time_interval']
        layout_width=config['layout_width']

        time_axis_list=[]
        t=start_time
        while t<end_time:
            time_axis_list.append(t)
            t+=time_interval
        time_axis_list.append(end_time)

        time_axis_pos={
            'start_axis':0.0,
            'end_axis':float(layout_width)
        }

        step=layout_width/(len(time_axis_list)+1)
        for i,time_axis in enumerate(time_axis_list,start=1):
            time_axis_pos[time_axis]=i*step
        time_axis_list.insert(0,'start_axis')
        time_axis_list.append('end_axis')
        return time_axis_list,time_axis_pos

    @staticmethod
    def compute_linearized_bipartite_layout(path_tree:nx.DiGraph,config:dict):
        """
        << paper >> 
        Parallel Edge Splatting for Scalable Dynamic Graph Visualization (2011)
        """

    @staticmethod
    def compute_tpvis_layout(path_tree:nx.DiGraph,config:dict):
        """
        << paper >>
        TPVis: A Temporal Path Visualization System for Intuitive Understanding of Information Diffusion Inside Temporal Networks (2025)
        
        Input:
            path_tree
            config
        Output:
            updated path_tree
        """
        ### compute Reingold-Tilford layout using igraph
        path_tree_ig=ig.Graph.from_networkx(g=path_tree)
        nx_nodes=list(path_tree.nodes())
        layout=path_tree_ig.layout_reingold_tilford(root=[config['source_id']])
        pos={nx_nodes[i]:(layout[i][1],-layout[i][0]) for i in range(len(nx_nodes))}

        ### scaling x, y position and update node attr 
        xs=[p[0] for p in pos.values()]
        ys=[p[1] for p in pos.values()]
        min_x,max_x=min(xs),max(xs)
        min_y,max_y=min(ys),max(ys)
        x_range=max_x-min_x if max_x>min_x else 1.0
        y_range=max_y-min_y if max_y>min_y else 1.0
        
        for node,(x,y) in pos.items():
            x_scaled=(x-min_x)/x_range*config["layout_width"]
            y_scaled=(y-min_y)/y_range*config["layout_height"]
            path_tree.nodes[node]["x"]=float(x_scaled)
            path_tree.nodes[node]["y"]=float(y_scaled)

        ### mapping x position to correct time_axis pos
        # 구현 필요
        return path_tree