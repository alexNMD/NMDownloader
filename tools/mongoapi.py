from pymongo import MongoClient


class MongoAPI:
    def __init__(self):
        self.client = MongoClient("mongodb://alexnmd_admin:xxxxxxxxxxx@mongodb-alexnmd.alwaysdata.net:27017/bdd?authSource=alexnmd_db")
        self.db = self.client['alexnmd_db']
    
    def get_collection(self, name: str):
        collection = self.db[name]

        return collection
    
    def insert_data(self, data: dict, collection: str):
        collection = self.get_collection(collection)
        try:
            collection.insert_one(data)
            return True
        except Exception as e:
            print(e)

    def get_data(self, data: str, collection: str):
        collection = self.get_collection(collection)
        
        return collection.find_one(data)
    
    def get_all_data(self, collection: str):
        collection = self.get_collection(collection)
        data = list(collection.find({}))

        return data
    
    def get_all_videos(self, type, skip=0):
        collection = self.get_collection(type)
        skip = skip * 32

        data = list(collection.find({})
            .skip(skip)
            .limit(32)
            .sort('added_at', -1))
        total = collection.find({}).count()

        return data, total

    def get_mailing_list(self):
        collection = self.get_collection("mailing_list")
        data = list(collection.find({}))
        emails = []
        for d in data:
            emails.append(d['email'])

        return emails

    def update_ded_link(self, id, newlink):
        collection = self.get_collection("movies")
        try:
            collection.find_one_and_update({'_id': id}, {'$set': {'link': newlink}})
            return True
        except:
            return False
    
    def search_videos(self, type, search, search_type: str, skip=0):
        collection = self.get_collection(type)
        skip = skip * 32
        if search_type == "by_title":
            # collection.create_index([('Title', 'text')])
            results = list(collection.find({ '$text': { '$search': search } })
                .skip(skip)
                .limit(32)
                .sort('added_at', -1))
            total = collection.find({ '$text': { '$search': search } }).count()
        elif search_type == "by_genre":
            results = list(collection.find({ 'genre': search })
                .skip(skip)
                .limit(32)
                .sort('added_at', -1))
            total = collection.find({ 'genre': search }).count()

        return results, total
    
    def get_active_link(self):
        collection = self.get_collection("movies")
        active_link = collection.find({"status": True}).count()

        return active_link
