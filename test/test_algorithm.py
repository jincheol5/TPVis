import argparse
from modules import GraphUtils,GraphAlgorithm

def main(test_config:dict):
    match test_config['test_num']:
        case 1:
            """
            Test. compute_TP_parallel
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
            path_dict=GraphAlgorithm.compute_TP_parallel(graph=graph,source_id=0)
            for dst,path in path_dict.items():
                print(f"source_id to {dst}:")
                print(path,end="\n\n")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test_num",type=int,default=1)
    args=parser.parse_args()
    test_config={
        "test_num":args.test_num
    }
    main(test_config=test_config)