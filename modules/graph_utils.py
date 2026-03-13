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

