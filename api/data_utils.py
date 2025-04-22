import os
import pandas as pd
import networkx as nx
from temporal_graph import EdgeEvent
from tqdm import tqdm

class Data_Utils:
    class Data_Load:
        file_path=os.path.join(os.getcwd(),"data")
        @staticmethod
        def get_dataset_df(dataset_name="CollegeMsg"):
            file_name=dataset_name+".txt"
            file_path=os.path.join(Data_Utils.Data_Load.file_path,file_name)
            df=pd.read_csv(file_path,sep=" ",header=None,names=["src","tar","time"],dtype={"src":str,"tar":str,"time":int})
            return df
        
        @staticmethod
        def save_dataset_from_df(df:pd.DataFrame,dataset_name="new_dataset"):
            file_name=dataset_name+".txt"
            file_path=os.path.join(Data_Utils.Data_Load.file_path,file_name)
            df.to_csv(file_path,sep=" ",index=False,header=False)
            print(f"save dataset {dataset_name} to txt file")
    
    class Data_Analysis:
        @staticmethod
        def check_ascending_node_id_gap(df:pd.DataFrame):
            unique_nodes=pd.unique(df[["src","tar"]].values.ravel())
            sorted_nodes=sorted(unique_nodes)
            diffs=[next_node-node for node,next_node in zip(sorted_nodes[:-1],sorted_nodes[1:])]
            is_sequential=all(d==1 for d in diffs)
            print("정확히 1씩 증가?: ",is_sequential)
        
        @staticmethod
        def get_min_max_time_of_df(df:pd.DataFrame):
            return df["time"].min(),df["time"].max()

    class Data_Process:
        @staticmethod
        def encode_node_id_of_df(df:pd.DataFrame):
            unique_nodes=pd.unique(df[["src","tar"]].values.ravel())
            sorted_nodes=sorted(unique_nodes)
            mapping={node:idx for idx,node in enumerate(sorted_nodes)}
            df["src"]=df["src"].map(mapping)
            df["tar"]=df["tar"].map(mapping)
            return df
    
        @staticmethod
        def get_edge_event_list_from_df(start_time:int,end_time:int,df:pd.DataFrame):
            df=df[(df['time']>start_time)&(df['time']<=end_time)]
            edge_event_list=[]
            for row in df.itertuples():
                edge_event_list.append(EdgeEvent(src=row.src,tar=row.tar,time=int(row.time)))
            edge_event_list.sort(key=lambda edge_event:edge_event.time)
            return edge_event_list

        @staticmethod
        def get_networkx_graph_from_df(start_time:int,end_time:int,df:pd.DataFrame):
            df=df[(df['time']>start_time)&(df['time']<=end_time)]
            graph=nx.DiGraph()
            for row in df.itertuples():
                graph.add_node(row.src)
                graph.add_node(row.tar)
                graph.add_edge(row.src,row.tar,time=[])
            for row in df.itertuples():
                graph[row.src][row.tar]['time'].append(int(row.time))
            return graph

        @staticmethod
        def compute_single_source_FP(source_id:str,start_time:int,end_time:int,df:pd.DataFrame):
            """
            get graph, edge_event_list
            """
            graph=Data_Utils.Data_Process.get_networkx_graph_from_df(start_time=start_time,end_time=end_time,df=df)
            edge_event_list=Data_Utils.Data_Process.get_edge_event_list_from_df(start_time=start_time,end_time=end_time,df=df)

            """
            initialize gamma table, FP_edge_event_list
            """
            gamma_dict={}
            for node in graph.nodes:
                gamma_dict[node]=([],-1) # (edge_event_list,visited_time) tuple
            
            FP_edge_event_list=[]

            """
            compute foremost path using extended time-centric algorithm
            """
            gamma_dict[source_id]=([],0)
            for edge_event in tqdm(edge_event_list,desc=f"compute FP..."):
                if gamma_dict[edge_event.src][1]!=-1 and gamma_dict[edge_event.tar][1]==-1:
                    if gamma_dict[edge_event.src][1]<edge_event.time:
                        FP=gamma_dict[edge_event.src][0]+[edge_event]
                        gamma_dict[edge_event.tar]=(FP,edge_event.time)
                        FP_edge_event_list.append(edge_event)
            return gamma_dict,FP_edge_event_list
        
        @staticmethod
        def convert_gamma_to_static_graph_and_time_list(gamma_dict):
            graph=nx.DiGraph()
            time_set=set()
            for key,value in gamma_dict.items():
                for edge_event in value[0]:
                    graph.add_node(edge_event.src)
                    graph.add_node(edge_event.tar)
                    graph.add_edge(edge_event.src,edge_event.tar)
                    time_set.add(edge_event.time)
            time_list=sorted(time_set)
            return graph,time_list

        @staticmethod
        def compute_time_axis_list(start_time:int,end_time:int,time_interval:int):
            if (end_time-start_time)%time_interval==0:
                time_axis_list=list(range(start_time,end_time+1,time_interval))
            else:
                time_axis_list=list(range(start_time,end_time+1,time_interval))
                time_axis_list.append(end_time)
            return time_axis_list 