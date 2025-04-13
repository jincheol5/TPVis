import argparse
from data_utils import Data_Utils

def app_data(app_number=1):
    match app_number:
        case 1:
            """
            encoding datasets and save to txt file
            """
            CollegeMsg_df=Data_Utils.Data_Load.get_dataset_df(dataset_name="CollegeMsg")
            Data_Utils.Data_Load.save_dataset_from_df(df=Data_Utils.Data_Process.encoding_node_id_in_df(df=CollegeMsg_df),dataset_name="encoded_CollegeMsg")
            bitcoin_df=Data_Utils.Data_Load.get_dataset_df(dataset_name="bitcoin")
            Data_Utils.Data_Load.save_dataset_from_df(df=Data_Utils.Data_Process.encoding_node_id_in_df(df=bitcoin_df),dataset_name="encoded_bitcoin")

"""
Execute app_data
"""
parser=argparse.ArgumentParser()
parser.add_argument("--app",type=int,default=1)
args=parser.parse_args()
app_data(app_number=args.app)