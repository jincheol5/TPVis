from pymongo import MongoClient
from pymongo.errors import PyMongoError

class DBInterface:
    def __init__(self):
        try:
            self.client=MongoClient("mongodb://127.0.0.1:27017/")
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
    
    def connect_db(self):
        try:
            self.client=MongoClient("mongodb://127.0.0.1:27017/")
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def disconnect_db(self):
        self.client.close()

    def upload_dataset(self,dataset_name:str,event_stream:list):
        """
        event_stream: list of tuple (src,tar,time)
        """
        if self.client is None:
            self.connect_db()

        db=self.client["TPVis"]
        db.drop_collection(dataset_name) # 기존 edge_event 컬렉션 삭제
        dataset_collection=db[dataset_name]

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
        dataset_collection.insert_many(edge_docs,ordered=False) # ordered=False: 중복 _id 있으면 skip
    
    def get_dataset_list(self):
        if self.client is None:
            self.connect_db()

        db=self.client["TPVis"]
        dataset_list=db.list_collection_names()
        return dataset_list

    def get_event_stream(self,dataset_name:str):
        """
        """
        if self.client is None:
            self.connect_db()

        db=self.client["TPVis"]
        dataset_collection=db[dataset_name]

        event_stream=[]
        cursor=dataset_collection.find({},{"_id": 0, "src_id":1, "tar_id":1, "time":1})

        for doc in cursor:
            event_stream.append(
                (doc["src_id"],doc["tar_id"],doc["time"])
            )
        return event_stream