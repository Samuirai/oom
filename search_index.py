# -*- coding: utf-8 -*-
from mongodb_storage import MongoDBStorage as Storage
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.index import create_in
from whoosh.query import Term
from whoosh.query import *
from whoosh.qparser import QueryParser
import progressbar
import os

schema = Schema(dump_name=TEXT(stored=True),
	title=TEXT(stored=True),
    content=TEXT(stored=True),
    mime=KEYWORD(lowercase=True),
    id=ID(stored=True))

index = None
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
index = create_in("indexdir", schema)

storage = Storage()
db = storage.db

writer = index.writer()


for dump_name in db.collection_names():
	if dump_name != "system.indexes":
		i=0
		print "indexing:", dump_name
		bar = progressbar.ProgressBar(maxval=db[dump_name].count(), 
   				widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
		for entry in db[dump_name].find():
			bar.update(i+1)
			i+=1
			mime = entry.get('mime',u'')
			content = u''
			if mime==u'' or mime.split("/")[0]=='text':
				content = entry.get('content',u'')
			#print entry.get('title',''), content, dump_name, mime
			writer.update_document(title=entry.get('title',''),
				content=content,
				dump_name=dump_name,
				mime=mime,
				id=unicode(entry.get('_id','')))
print "commiting..."
writer.commit()
print "done."
