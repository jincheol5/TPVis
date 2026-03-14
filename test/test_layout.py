import argparse
from modules import GraphUtils,GraphTransformEngine,Layout

def main(test_config:dict):
    match test_config['test_num']:
        case 1:
            """
            Test. transform_to_aggregated_path_tree
            """
            eventstream=[
                (0,2,1),
                (0,2,2),
                (0,3,3),
                (1,7,4),
                (0,1,5),
                (1,6,6),
                (0,3,7),
                (3,6,7),
                (3,4,8),
                (2,5,9)
            ]
            graph=GraphUtils.convert_eventstream_to_graph(eventstream=eventstream)
            graph_engine=GraphTransformEngine(eventstream=eventstream)
            path_tree=graph_engine.transform_to_aggregated_path_tree(source_id=0,start_time=0,end_time=10,time_interval=2)
            layout=Layout(path_tree=path_tree)
            layout_config={
                "start_time":0,
                "end_time":10,
                "time_interval":3,
                "layout_width":10
            }
            time_axis_list,time_axis_pos=layout.compute_time_axis_list_and_pos(layout_config=layout_config)
            print(f"time_axis_list:")
            print(time_axis_list,end="\n\n")
            print(f"time_axis_pos:")
            print(time_axis_pos)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test_num",type=int,default=1)
    args=parser.parse_args()
    test_config={
        "test_num":args.test_num
    }
    main(test_config=test_config)