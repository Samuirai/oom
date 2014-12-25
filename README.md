oom
===

**O**ut **O**f **M**ind is a personal knowledge base system where you can just dump all your
stuff and hopefully find it again when needed.

Background
----------

I found myself solving problems again that I have solved in the past. 
The problem is, I lost scripts, PoCs, articels, links and other resources.
So I wanted a knowledge base system where I can just dump all my stuff into it and find it again.


Screenshots
-----------

This is the web interface for oom. Here you can see an example entry rendered as markdown.
Each entry can have a `title`, `content` and `mimetype`.
The `mimetype` decides how the entry will be displayed. And this entry has `text/x-markdown` as mimetype:

![entry view](https://raw.githubusercontent.com/Samuirai/oom/master/screenshots/view_entry.png)

Here you can see the raw source of the entry where you could change the `title`, `content` and `mimetype`.

![entry edit](https://raw.githubusercontent.com/Samuirai/oom/master/screenshots/edit_entry.png)

To not rely solely on the webapp there is also a CLI. It uses `libmagic` to guess the `mimetype` of the input
to minimize the work you have do to the knowledge base.

![entry edit](https://raw.githubusercontent.com/Samuirai/oom/master/screenshots/cli.png)

Technical Stuff
---------------
You can have several `dumps`, which is basically the overall category.
Each `entry` is part of a `dump`.
Each entry has `_id`, `title`, `content` and `mimetype`.

* The entries are stored in a MongoDB with `pymongo`.
* Webapp is written with Flask
* `whoosh` is used as simple search engine for your dumps.
* `python-magic` is used to guess mimetypes.


Vision
------
* Browser plugin to quickly add interesting articles and tutorials to a dump.
* More powerful search engine to guess words and autocorrect inputs. Like google.
* Easy backup dump. Maybe something git based.
