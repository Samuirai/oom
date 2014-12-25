from storage import StorageInterface
import json
import base64
import os
# -*- coding: utf-8 -*-

class FileStorage(StorageInterface):
    def __init__(self):
        self.folder = "/Users/samuirai/coding/oom/file_storage"

    def read_dump(self, dump_name):
        file_content = ""
        try:
            with open('%s/%s.oom' % (self.folder, dump_name), 'r') as fp:
                file_content = fp.read()
                json_dump = json.loads(file_content)
                json_dump['dump_name'] = dump_name
                return json_dump
        except IOError as ex:
            return {
                "dump_name": dump_name,
                "cache": "",
                "entries": [], }
        except ValueError as ex:
            print ex
            return {
                "dump_name": dump_name,
                "cache": "",
                "entries": [], }

    def edit_entry(self, dump_name, entry_id, content=None, title=None, mime=None):
        try:
            dump = self.read_dump(dump_name)
            for entry in dump['entries']:
                if entry['entry_id'] == entry_id:
                    if content:
                        entry['content'] = content
                    if title:
                        entry['title'] = title
                    if mime:
                        entry['mime'] = mime
            self.store_dump(dump_name, dump)
        except IOError as ex:
            raise ex

    def add_entry(self, dump_name, content, title="", mime="text/plain", pos=-1):
        try:
            dump = self.read_dump(dump_name)
            generated_id = self.generate_id()
            if mime.split("/")[0]=="text":
                content = content.decode('utf-8')
            else:
                content = base64.b64encode(content)
            entry = {
                "title": title,
                "mime": mime,
                "content": content,
                "entry_id": generated_id,
            }
            
            dump['dump_name'] = dump_name
            if pos==-1:
                dump['entries'].append(entry)
            else:
                dump['entries'].insert(pos, entry)
            self.store_dump(dump_name, dump)

            return generated_id
        except IOError as ex:
            raise ex

    def store_dump(self, dump_name, dump):
        file_content = json.dumps(dump)
        with open('%s/%s.oom' % (self.folder, dump_name), 'w') as fp:
            fp.write(file_content)

    def remove_dump(self, dump_name):
        os.remove('%s/%s.oom' % (self.folder, dump_name))
        return True


    def remove_entry(self, dump_name, entry_id):
        '''TODO: better iter object'''
        try:
            dump = self.read_dump(dump_name)
            found = None
            i = 0
            for entry in dump['entries']:
                if entry['entry_id'] == entry_id:
                    found=i
                    break
                i+=1
            if found!=None:
                del dump['entries'][found]
                self.store_dump(dump_name, dump)
            else:
                print "Entry not found"
            return dump

        except IOError as ex:
            raise ex

    def get_all_dump_names(self):
        dumps = []
        for f in os.listdir(self.folder):
            if f[-4:]=='.oom':
                dump = self.read_dump(f[:-4])
                dumps.append({
                    "filename": f, 
                    "dump_name": f[:-4], 
                    "entry_count": len(dump["entries"])})
        return dumps