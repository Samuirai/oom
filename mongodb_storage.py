# -*- coding: utf-8 -*-
import pymongo
from bson.objectid import ObjectId
import random
import base64
import config
from storage import StorageInterface


class MongoDBStorage(StorageInterface):
    def __init__(self):
        self.client = pymongo.MongoClient()
        self.db = self.client[config.mongodb_client]

    def read_dump(self, dump_name):
        dump = self.db[dump_name].find()
        return dump

    def remove_dump(self, dump_name):
        return self.db.drop_collection(dump_name)

    def get_entry(self, dump_name, entry_id):
        return self.db[dump_name].find_one({"_id": ObjectId(entry_id)})


    def edit_entry(self, dump_name, entry_id, content=None, title=None, mime=None):
        dump = self.db[dump_name]
        if content:
            dump.update({"_id": ObjectId(entry_id)}, {"$set": {'content': content}})
        if title:
            dump.update({"_id": ObjectId(entry_id)}, {"$set": {'title': title}})
        if mime:
            dump.update({"_id": ObjectId(entry_id)}, {"$set": {'mime': mime}})

    def add_entry(self, dump_name, content="", title="", mime="text/plain", pos=-1):
        try:
            dump = self.db[dump_name]

            if mime.split("/")[0]=="text" or mime=="":
                content = content.decode('utf-8')
            else:
                content = base64.b64encode(content)
            entry = {
                "title": title,
                "mime": mime,
                "content": content,
            }

            return dump.insert(entry)
        except IOError as ex:
            raise ex

    def remove_entry(self, dump_name, entry_id):
        dump = self.db[dump_name]
        status = dump.remove({"_id": ObjectId(entry_id)})
        if status['ok'] == 1:
            return True
        else:
            return False

    def get_all_dump_names(self):
        dumps = []
        for dump_name in self.db.collection_names():
            if dump_name != "system.indexes":
                dump = self.db[dump_name]
                dumps.append({
                    "filename": dump_name, 
                    "dump_name": dump_name, 
                    "entry_count": dump.count() })
        return dumps
