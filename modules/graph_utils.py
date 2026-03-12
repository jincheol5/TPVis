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
                graph[src][tar]['valid_times'].append(t)
            else:
                graph.add_edge(src,tar,time_list=[t])
        return graph

    @staticmethod
    def get_filtered_event_stream(eventstream:list,start_time:int,end_time:int):
        return [event for event in eventstream if start_time<=event[2]<=end_time]

class GraphAlgorithm:
    @staticmethod
    def initialize_node_attr(graph:nx.DiGraph,source_id:int=0):
        for node in graph.nodes():
            if node==source_id:
                graph.nodes[node]['r']=1
                graph.nodes[node]['visited_t']=0
                graph.nodes[node]['p_visited_t']=0 # predecessor visited time
            else:
                graph.nodes[node]['r']=0
                graph.nodes[node]['visited_t']=float('inf')
                graph.nodes[node]['p_visited_t']=float('inf')
            graph.nodes[node]['p']=node

    @staticmethod
    def compute_TP_parallel_step(graph:nx.DiGraph,source_id:int=0,init:bool=False,Q:set=None):
            Q_next=set()
            if init:
                GraphAlgorithm.initialize_node_attr(graph=graph,source_id=source_id)
                Q_next.add(source_id)
            else:
                for node in Q:
                    # get sorted edge_events
                    edge_events=[]
                    for _,v,data in graph.out_edges(node,data=True):
                        for t in data['valid_times']:
                            if graph.nodes[node]['visited_t']<t:
                                edge_events.append((node,v,t))
                    edge_events.sort(key=lambda x:x[2]) # 시간 순 정렬

                    # compute TR
                    for src,tar,t in edge_events:
                        if t<graph.nodes[tar]['visited_t']:
                            graph.nodes[tar]['r']=1
                            graph.nodes[tar]['visited_t']=t
                            graph.nodes[tar]['p']=src
                            graph.nodes[tar]['p_visited_t']=graph.nodes[src]['visited_t']
                            Q_next.add(tar)
            return Q_next

    @staticmethod
    def compute_TP_parallel(graph:nx.DiGraph,source_id:int=0):
        """
        Input:
            graph
            source_id
        Output:
            gamma_dict
                key=node_id
                value=(reachability,visited_time,predecessor_id,predecessor_visited_time)
        """
        Q=GraphAlgorithm.compute_TP_parallel_step(graph=graph,source_id=source_id,init=True)
        while True:
            if not Q:
                break
            Q=GraphAlgorithm.compute_TP_parallel_step(graph=graph,source_id=source_id,Q=Q)
        gamma_dict={}
        for node in graph.nodes():
            gamma_dict[node]=(graph.nodes[node]['r'],graph.nodes[node]['visited_t'],graph.nodes[node]['p'],graph.nodes[node]['p_visited_t'])
        return gamma_dict

    @staticmethod
    def reconstruct_TP(gamma_dict:dict,source_id:int=0):
        """
        reconstruct temporal paths from gamma_dict
        Input:
            gamma_dict
            source_id
        Output:
            TP_dict

            target node별 temporal path를 재구성해서 transform 해야하는 이유: a->b->c 의 경우, a->b에 대한 변환과 a->b->c에 대한 변환 모두 수행해야 하기 때문. 
            b에 10, c에 20에 도달 하였는데 interval이 20인 경우, b에도 도달 가능하다는 정보를 잃지 않기 위해서 a->b_20과 a->c_20 모두 생성해야 한다.
        """
