import os

class DataUtils:
    dir_path=os.path.join('..','data','tpvis')
    """
    DataUtils의 Docstring
    """
    @staticmethod
    def load_dataset_to_eventstream(dataset_name:str):
        file_path=os.path.join(DataUtils.dir_path,f"{dataset_name}.txt")
        eventstream=[]
        with open(file=file_path,mode="r") as f:
            for line in f:
                src,tar,t=line.strip().split()
                eventstream.append((int(src),int(tar),int(t)))
        return eventstream