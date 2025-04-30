import argparse
from data_utils import Data_Utils

def app_data(args):
    match args.case:
        case 1:
            """
            find_highest_total_degree_vertex()
            """
            df=Data_Utils.Data_Load.get_dataset_df(dataset_name=args.dataset_name)
            gamma_dict,_=Data_Utils.Data_Process.compute_single_source_FP(source_id=args.source_id,start_time=args.start_time,end_time=args.end_time,df=df)
            static_graph,_=Data_Utils.Data_Process.convert_gamma_to_static_graph_and_time_list(gamma_dict=gamma_dict,start_time=args.start_time)
            highest_total_degree_vertex=Data_Utils.Data_Analysis.find_highest_total_degree_vertex(graph=static_graph)
            print(f"highest total degree vertex: {highest_total_degree_vertex}")

        case 2:
            """
            find_last_visited_vertex()
            """
            df=Data_Utils.Data_Load.get_dataset_df(dataset_name=args.dataset_name)
            gamma_dict,_=Data_Utils.Data_Process.compute_single_source_FP(source_id=args.source_id,start_time=args.start_time,end_time=args.end_time,df=df)
            last_visited_vertex=Data_Utils.Data_Analysis.find_last_visited_vertex(gamma_dict=gamma_dict)
            print(f"last visited vertex: {last_visited_vertex}")


"""
Execute app_data
"""
parser=argparse.ArgumentParser()
parser.add_argument("--case",type=int,default=1)
parser.add_argument("--dataset_name",type=str,default="simple")
parser.add_argument("--source_id",type=str,default="a")
parser.add_argument("--start_time",type=int,default=0)
parser.add_argument("--end_time",type=int,default=9)
args=parser.parse_args()
app_data(args=args)