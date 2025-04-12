import os
import pandas as pd
import networkx as nx

class Data_Utils:
    class Data_Analysis:
        file_path=os.path.join(os.getcwd(),"data")
        @staticmethod
        def check_ascending_node_id_gap(dataset_name="CollegeMsg"):
            file_name=dataset_name+".txt"
            file_path=os.path.join(Data_Utils.Data_Analysis.file_path,file_name)
            df=pd.read_csv(file_path,sep=" ",header=None,names=["source","target","time"])
            unique_nodes=pd.unique(df[["source","target"]].values.ravel())
            sorted_nodes=sorted(unique_nodes)
            diffs=[next_node-node for node,next_node in zip(sorted_nodes[:-1],sorted_nodes[1:])]
            is_sequential=all(d==1 for d in diffs)
            print("정확히 1씩 증가?: ",is_sequential)