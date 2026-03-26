from pymongo import MongoClient
from pymongo.errors import PyMongoError

class DBInterface:
    def __init__(self):
        try:
            self.client=MongoClient("mongodb://localhost:27017/")
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
    
    def disconnect_db(self):
        self.client.close()

    def upload_dataset(self,dataset_name:str,event_stream:list):
        """
        event_stream: list of tuple (src,tar,time)
        """
        db=self.client[dataset_name]
        db.drop_collection("edge_event") # 기존 edge_event 컬렉션 삭제
        edge_event_collection=db["edge_event"]

        # edge events 저장
        unique_map={
            f"{src}_{tar}_{time}": {
                "_id": f"{src}_{tar}_{time}",
                "src_id": src,
                "tar_id": tar,
                "time": time
            }
            for src,tar,time in event_stream
        } # 중복 edge_event 제거
        edge_docs=list(unique_map.values())
        edge_event_collection.insert_many(edge_docs,ordered=False) # ordered=False: 중복 _id 있으면 skip
    
    def get_dataset_list(self):
        dataset_list=self.client.list_database_names()
        return dataset_list

    def get_event_stream(self,dataset_name:str):
        """
        """