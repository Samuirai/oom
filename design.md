A dump is a collection of entries.

JSON like format for a dump

{
	"title": "",
	"entries": [
		{ 
			"title": base64(""),
			"content": base64(""),
			"type": "markdown", ("binary", "html", "raw") 
			"tags": base64(""),
			"id": random(),
		}, { 
			"title": base64(""),
			"content": base64(""),
			"type": "markdown", ("binary", "html", "raw") 
			"tags": base64(""),
			"id": random(),
		},
	],
	"cache": sha1(""),
}

If cache value is set, then there is an already compiled output.
Has to be cleared when new entry is added.
