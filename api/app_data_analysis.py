import argparse
from data_utils import Data_Utils

def app_data(args):
    match args.case:
        case 1:
            """
            find_highest_total_degree_vertex()
            """
            df=Data_Utils.Data_Load.get_dataset_df(dataset_name=args.dataset_name)
            static_graph=Data_Utils.Data_Process.get_networkx_graph_from_df(start_time=args.start_time,end_time=args.end_time,df=df)
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

        case 3:
            """
            count_visual_misalignment()
            """
            df=Data_Utils.Data_Load.get_dataset_df(dataset_name=args.dataset_name)
            gamma_dict,FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=args.source_id,start_time=args.start_time,end_time=args.end_time,df=df)
            _,max_time=Data_Utils.Data_Analysis.get_min_max_time_of_FP_tree(FP_edge_event_list=FP_edge_event_list)
            if max_time<args.end_time:
                time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=args.start_time,end_time=max_time,time_interval=args.time_interval)
            else:
                time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=args.start_time,end_time=args.end_time,time_interval=args.time_interval)
            visual_misalignment=Data_Utils.Data_Analysis.count_visual_misalignment(gamma_dict=gamma_dict,time_axis_list=time_axis_list)
            print(f"visual misalignment: {visual_misalignment}")

        case 4:
            """
            count_visual_disconnection()
            """
            df=Data_Utils.Data_Load.get_dataset_df(dataset_name=args.dataset_name)
            gamma_dict,FP_edge_event_list=Data_Utils.Data_Process.compute_single_source_FP(source_id=args.source_id,start_time=args.start_time,end_time=args.end_time,df=df)
            _,max_time=Data_Utils.Data_Analysis.get_min_max_time_of_FP_tree(FP_edge_event_list=FP_edge_event_list)
            if max_time<args.end_time:
                time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=args.start_time,end_time=max_time,time_interval=args.time_interval)
            else:
                time_axis_list=Data_Utils.Data_Process.compute_time_axis_list(start_time=args.start_time,end_time=args.end_time,time_interval=args.time_interval)
            visual_disconnection=Data_Utils.Data_Analysis.count_visual_disconnection(gamma_dict=gamma_dict,time_axis_list=time_axis_list,source_id=args.source_id)
            print(f"visual disconnection: {visual_disconnection}")

"""
Execute app_data
"""
parser=argparse.ArgumentParser()
parser.add_argument("--case",type=int,default=1)
parser.add_argument("--dataset_name",type=str,default="simple")
parser.add_argument("--source_id",type=str,default="a")
parser.add_argument("--start_time",type=int,default=0)
parser.add_argument("--end_time",type=int,default=9)
parser.add_argument("--time_interval",type=int,default=0)
args=parser.parse_args()
app_data(args=args)