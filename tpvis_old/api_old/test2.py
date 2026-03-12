from data_utils import Data_Utils

df=Data_Utils.Data_Load.get_dataset_df(dataset_name="bitcoin")
min_time,max_time=Data_Utils.Data_Analysis.get_min_max_time_of_df(df=df)
print(f"min: {min_time} max: {max_time}")