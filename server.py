# -*- coding: utf-8 -*-
from mongodb_storage import MongoDBStorage as Storage
from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import Response
from flaskext.markdown import Markdown
from whoosh.fields import Schema, TEXT, KEYWORD, ID
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
import json
import jinja2_highlight


class MyFlask(Flask):
    jinja_options = dict(Flask.jinja_options)
    jinja_options.setdefault('extensions',
        []).append('jinja2_highlight.HighlightExtension')

schema = Schema(dump_name=TEXT(stored=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True),
    mime=KEYWORD(lowercase=True),
    id=ID(stored=True))

search_index = open_dir("indexdir")

app = MyFlask(__name__)
Markdown(app)

@app.context_processor
def global_variables():
    storage = Storage()
    dumps = storage.get_all_dump_names()
    return dict(dumps=dumps)

@app.route('/')
def index():
    return render_template('dump_list.html')

@app.route('/get_dump/<dump_name>')
def get_dump(dump_name):
    storage = Storage()
    dump = storage.read_dump(dump_name)
    return render_template('dump.html', dump=dump, dump_name=dump_name)

@app.route('/search')
def search():
    querystring = request.args.get('q', 'import')
    
    #dump = storage.read_dump(dump_name)
    searcher = search_index.searcher()
    myquery = QueryParser("content", search_index.schema).parse(querystring)
    results = searcher.search(myquery)

    storage = Storage()
    dump = []
    for result in results:
        entry = storage.get_entry(result['dump_name'], result['id'])
        entry['dump_name'] = result['dump_name']
        dump.append(entry)
    return render_template('dump.html', dump=dump)

@app.route('/api.json', methods=['POST','GET'])
def api_json():
    content = request.get_json(force=True)
    if 'action' in content:
        # remove an entry
        if content['action'] == "remove_entry":
            if 'dump_name' in content:
                if '_id' in content:
                    try:
                        storage = Storage()
                        status = storage.remove_entry(content['dump_name'], content['_id'])
                        if status==1:
                            return Response(json.dumps({'status': 'Ok'}), 
                                status=200, mimetype='application/json')
                        else:
                            return Response(json.dumps({'status': 'Error', 'reason': dump}), 
                                status=400, mimetype='application/json')
                    except Exception as err:
                        return Response(json.dumps({'status': 'Error', 'reason': str(err)}), 
                            status=400, mimetype='application/json')
                else:
                    return Response(json.dumps({'status': 'Error', 'reason': '_id of entry not specified'}), 
                        status=400, mimetype='application/json')
            else:
                return Response(json.dumps({'status': 'Error', 'reason': 'dump_name not specified'}), 
                    status=400, mimetype='application/json')
        # get an entry
        elif content['action'] == "get_entry":
            if 'dump_name' in content:
                if '_id' in content:
                    try:
                        storage = Storage()
                        status = storage.get_entry(content['dump_name'], content['_id'])
                        if status:
                            return Response(json.dumps({
                                    'status': 'Ok', 
                                    'content': status.get('content',''), 
                                    'mime': status.get('mime',''),
                                    'title': status.get('title','')    }), 
                                status=200, mimetype='application/json')
                        else:
                            return Response(json.dumps({'status': 'Error', 'reason': status}), 
                                status=400, mimetype='application/json')
                    except Exception as err:
                        return Response(json.dumps({'status': 'Error', 'reason': str(err)}), 
                            status=400, mimetype='application/json')
                else:
                    return Response(json.dumps({'status': 'Error', 'reason': '_id of entry not specified'}), 
                        status=400, mimetype='application/json')
        # edit an entry
        elif content['action'] == "edit_entry":
            if 'dump_name' in content:
                if '_id' in content:
                    try:
                        storage = Storage()
                        status = storage.edit_entry(content['dump_name'], content['_id'], 
                                    content=content.get("content", None), 
                                    mime=content.get("mime", None), 
                                    title=content.get("title", None))
                        return Response(json.dumps({
                                'status': 'Ok'}), 
                            status=200, mimetype='application/json')
                    except Exception as err:
                        raise
                        return Response(json.dumps({'status': 'Error', 'reason': str(err)}), 
                            status=400, mimetype='application/json')
                else:
                    return Response(json.dumps({'status': 'Error', 'reason': '_id of entry not specified'}), 
                        status=400, mimetype='application/json')
        # add an entry
        elif content['action'] == "add_entry":
            if 'dump_name' in content:
                try:
                    storage = Storage()
                    status = storage.add_entry(content['dump_name'],
                                content=content.get("content", None), 
                                mime=content.get("mime", None), 
                                title=content.get("title", None))
                    return Response(json.dumps({
                            'status': 'Ok', '_id': str(status)}), 
                        status=200, mimetype='application/json')
                except Exception as err:
                    raise
                    return Response(json.dumps({'status': 'Error', 'reason': str(err)}), 
                        status=400, mimetype='application/json')
        else:
            return Response(json.dumps({'status': 'Error', 'reason': '%s not implemented' % content['action']}), 
                status=400, mimetype='application/json')
    else:
        return Response(json.dumps({'status': 'Error', 'reason': 'no action specified'}), 
            status=400, mimetype='application/json')

@app.route('/remove_entry/<dump_name>/<entry_id>')
def remove_entry(dump_name, entry_id):
    storage = Storage()
    dump = storage.remove_entry(dump_name, entry_id)
    return "remove_entry"

@app.route('/remove_dump/<dump_name>')
def remove_dump(dump_name):
    storage = Storage()
    dump = storage.remove_dump(dump_name)
    print dump
    return "remove dump"

@app.route('/test_dump/<dump_name>')
def test_dump(dump_name):
    storage = Storage()
    return storage.add_entry(dump_name, "<b>fett</b>", "test titel", ["html", "test"], "html")
if __name__ == '__main__':
    app.run(debug=True)

"""
storage = Storage()
print storage.get_all_dump_names()
entry = {
    "title": "zwei Eintrag",
    "content": "zweiter test eintrag asd",
    "type": "raw",
    "tags": [],
    }
print " ------ add entry -------"
storage.store('test', entry)

print " ------ read dump -------"
print storage.read('test')
"""