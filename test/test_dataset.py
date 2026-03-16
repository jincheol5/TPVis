import argparse
from datetime import datetime
from modules import DataUtils,GraphUtils

def main(test_config:dict):
    match test_config['test_num']:
        case 1:
            """
            Test. check dataset min, max time
            """
            match test_config['dataset_name']:
                case "Simple":
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
                case _:
                    eventstream=DataUtils.load_dataset_to_eventstream(dataset_name=test_config['dataset_name'])
            
            min_time,max_time=GraphUtils.get_min_max_time_in_eventstream(eventstream=eventstream)
            print(f"{test_config['dataset_name']} min time: {min_time} max time: {max_time}")
            print(f"{test_config['dataset_name']} min time: {datetime.fromtimestamp(min_time).strftime("%Y-%m-%d %H:%M")} max time: {datetime.fromtimestamp(max_time).strftime("%Y-%m-%d %H:%M")}")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test_num",type=int,default=1)
    parser.add_argument("--dataset_name",type=str,default=f"Simple")
    args=parser.parse_args()
    test_config={
        "test_num":args.test_num,
        "dataset_name":args.dataset_name
    }
    main(test_config=test_config)