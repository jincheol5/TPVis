import networkx as nx

class GraphUtils:
    @staticmethod
    def convert_eventstream_to_graph(eventstream:list):
        """
        Input:
            eventstream: List of (src,tar,t)
        Output:
            graph
        """
        graph=nx.DiGraph()
        for (src,tar,t) in eventstream:
            if graph.has_edge(src,tar):
                graph[src][tar]['times'].append(t)
            else:
                graph.add_edge(src,tar,times=[t])
        return graph

    @staticmethod
    def get_filtered_eventstream(eventstream:list,start_time:int,end_time:int):
        return [event for event in eventstream if start_time<=event[2]<=end_time]
    
    @staticmethod
    def get_min_max_time_in_eventstream(eventstream:list):
        t_min=min(t for _,_,t in eventstream)
        t_max=max(t for _,_,t in eventstream)
        return t_min,t_max

    @staticmethod
    def _convert_node_event_to_dict(node_id:str,time:int,x_pos:float,y_pos:float):
        event_dic={}
        event_dic["id"]=f"{node_id}_{time}"
        event_dic["node_id"]=node_id
        event_dic["time"]=time
        event_dic["x_pos"]=x_pos
        event_dic["y_pos"]=y_pos
        return event_dic
    
    def _convert_edge_event_to_dict(self,source_id:str,target_id:str):
        """
        source_id: source node event id
        target_id: target node event id
        """
        event_dic={}
        event_dic["id"]=f"{source_id}_{target_id}"
        event_dic["source_id"]=source_id
        event_dic["target_id"]=target_id
        return event_dic

    @staticmethod
    def convert_to_response_dict(path_tree:nx.DiGraph,time_axis_list:list,time_axis_pos:dict):
        node_event_list=[]
        edge_event_list=[]

        for _,attr in path_tree.nodes(data=True):
            node_event_list.append(
                GraphUtils._convert_node_event_to_dict(
                    node_id=attr.get("node_id"),
                    time=attr.get("time"),
                    x_pos=attr.get("x_pos"),
                    y_pos=attr.get("y_pos")
                )
            )
        
        for u,v,attr in path_tree.edges(data=True):
            edge_event_list.append(
                GraphUtils._convert_edge_event_to_dict(
                    source_id=u,
                    target_id=v,
                )
            )

        response_dict={}
        response_dict["time_axis_list"]=time_axis_list
        response_dict["time_axis_pos"]=time_axis_pos
        response_dict["node_event_list"]=node_event_list
        response_dict["edge_event_list"]=edge_event_list
        return response_dict

class GraphAlgorithm:
    @staticmethod
    def _initialize_node_attr(graph:nx.DiGraph,source_id:int=0):
        for node in graph.nodes():
            if node==source_id:
                graph.nodes[node]['r']=1
                graph.nodes[node]['t']=0
                graph.nodes[node]['path']=[]
            else:
                graph.nodes[node]['r']=0
                graph.nodes[node]['t']=float('inf')
                graph.nodes[node]['path']=[]

    @staticmethod
    def _compute_TP_parallel_step(graph:nx.DiGraph,source_id:int=0,init:bool=False,Q:set=None,path_dict:dict=None):
            Q_next=set()
            if init:
                GraphAlgorithm._initialize_node_attr(graph=graph,source_id=source_id)
                Q_next.add(source_id)
                path_dict={}
                for node in graph.nodes():
                    path_dict[node]=[]
            else:
                for node in Q:
                    # get sorted edge_events
                    edge_events=[]
                    for _,v,data in graph.out_edges(node,data=True):
                        for t in data['times']:
                            if graph.nodes[node]['t']<t:
                                edge_events.append((node,v,t))
                    edge_events.sort(key=lambda x:x[2]) # 시간 순 정렬

                    # compute TR
                    for src,tar,t in edge_events:
                        if t<graph.nodes[tar]['t'] and graph.nodes[tar]['r']==0:
                            graph.nodes[tar]['r']=1
                            graph.nodes[tar]['t']=t
                            path_dict[tar]=path_dict[src]+[(src,tar,t)]
                            Q_next.add(tar)
            return Q_next,path_dict

    @staticmethod
    def compute_TP_parallel(graph:nx.DiGraph,source_id:int=0):
        """
        Input:
            graph
            source_id
        Output:
            path_dict
                key=destination node id
                value=path, List of (src,tar,t)
        """
        Q,path_dict=GraphAlgorithm._compute_TP_parallel_step(graph=graph,source_id=source_id,init=True)
        while True:
            if not Q:
                break
            Q,path_dict=GraphAlgorithm._compute_TP_parallel_step(graph=graph,source_id=source_id,Q=Q,path_dict=path_dict)
        return path_dict

