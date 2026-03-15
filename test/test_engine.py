import argparse
from modules import GraphUtils,GraphAlgorithm,GraphTransformEngine

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
            graph_engine=GraphTransformEngine(eventstream=eventstream)
            path_tree=graph_engine.transform_to_aggregated_path_tree(source_id=0,start_time=1,end_time=9,time_interval=2)
            print(path_tree.nodes())


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test_num",type=int,default=1)
    args=parser.parse_args()
    test_config={
        "test_num":args.test_num
    }
    main(test_config=test_config)