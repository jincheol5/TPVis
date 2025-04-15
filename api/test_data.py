from data_utils import Data_Utils


"""
Test. compute_single_source_FP
"""
df=Data_Utils.Data_Load.get_dataset_df(dataset_name="simple")
gamma_dict=Data_Utils.Data_Process.compute_single_source_FP(source_id="a",start_time=0,end_time=10,df=df)

for key,value in gamma_dict.items():
    if isinstance(value,tuple):
        print(f"{key} FP: ")
        for edge_event in value[0]:
            print(f"\t{edge_event.src} -> {edge_event.tar} at {edge_event.time}")