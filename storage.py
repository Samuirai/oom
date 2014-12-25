import random
# -*- coding: utf-8 -*-


class StorageInterface():
    '''
    Storage Interface
    '''
    def generate_id(self):
        '''
        generate a random id for entries
        '''
        return "".join([random.choice("abcdef0123456789") for _ in range(0,32)])
        

    def read_dump(self, dump_name):
        '''
        Opens a dump and returns the json document.
        '''
        raise NotImplementedError

    def remove_dump(self, dump_name):
        '''
        delete a dump.
        '''
        raise NotImplementedError

    def get_entry(self, dump_name, entry_id):
        '''
        get an entry from a dump
        '''
        raise NotImplementedError

    def edit_entry(self, dump_name, entry_id, content=None, title=None, mime=None):
        '''
        edit an entry
        '''
        raise NotImplementedError

    def add_entry(self, dump_name, content, title="", mime="text/plain", pos=-1):
        '''
        Stores an entry.
        If dump with this dump_name doesn't exist, create it with this single entry.
        If dump exists, then append the entry, or put at position `pos`.
        '''
        raise NotImplementedError

    def remove_entry(self, dump_name, entry_id):
        '''
        removes the entry with the idea `entry_id` from the dump `dump_name` and returns thew
        new dump.
        '''
        raise NotImplementedError

    def get_all_dump_names(self):
        '''
        get all available dump names
        '''
        raise NotImplementedError
