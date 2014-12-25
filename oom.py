#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import sys
import magic
#from file_storage import FileStorage as Storage
from mongodb_storage import MongoDBStorage as Storage

parser = argparse.ArgumentParser(description='push something out of your mind')
parser.add_argument('dump_name', metavar='dump_name',
                   help='dump name')
parser.add_argument('--files', '-f', metavar='files', nargs='+',
                   help='file[s] to add to a dump')
parser.add_argument('--content', '-c', metavar='content',
                   help='content of an entry')
parser.add_argument('--title', '-t', metavar='title',
                   help='title of an entry')

args = parser.parse_args()

storage = Storage()
if args.files:
    for f in args.files:
        try:
            with open(f, 'rb') as fp:
                entry_title = f
                if args.title:
                    entry_title = args.title
                content = fp.read()
                mime = typ=magic.from_buffer(content, mime=True)
                entry_id = storage.add_entry(args.dump_name, content, entry_title, mime=mime)
                
                '''
                TODO: use filemagic to determine type
                '''
            print "added %s (%s) to %s with id %s" % (f, mime, args.dump_name, entry_id)
        except IOError, err:
            print "Error with file:", f
            print err
        except UnicodeDecodeError, err:
            print "Error with file:", f
            print err

elif args.content:
    entry_title = ""
    if args.title:
        entry_title = args.title
    entry_id = storage.add_entry(args.dump_name, args.content, entry_title)
    print "added a simple entry with size=%d byte to %s" % (len(args.content), args.dump_name)

else:
    print "CMD+D / CTRL+D to finish input"
    print "------------------------------"
    stdin = ""
    for line in sys.stdin:
        stdin+=line
    print "------------------------------"
    if stdin:
        entry_title = ""
        if args.title:
            entry_title = args.title
        mime = typ=magic.from_buffer(stdin, mime=True)
        entry_id = storage.add_entry(args.dump_name, stdin, entry_title, mime=mime)
        print "added a %s entry with size=%d byte to %s" % (mime, len(stdin), args.dump_name)