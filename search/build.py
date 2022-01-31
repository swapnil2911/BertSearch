# define settings

settings = {
        "analysis": {
            "filter": {
            "autocomplete_filter": {
            "type": "edge_ngram",
            "min_gram": 1,
            "max_gram": 5
            }
        },
            "analyzer": {
                "autocomplete_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": [ "lowercase", "autocomplete_filter"]
            }
        }
    }
}

def build_mapping(html_fields,analyzed_fields,keyword_fields,dense_vector):
    mapping = {}

    mapping[dense_vector] = {
        "type": "dense_vector",
        "dims": 768
    }

    for field in html_fields:
        mapping[field] = {
            "type": "text"
        }

    for field in analyzed_fields:
        mapping[field] = {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            },
            "analyzer": "autocomplete_analyzer"
        }

    for field in keyword_fields:
        mapping[field] = {
            "type": "text",
            "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
            }
        }

    return mapping

def build_document(html_fields,analyzed_fields,keyword_fields,dense_vector):
    document = {}

    document['settings'] = settings
    document['mappings'] = {}
    document['mappings']['properties'] = build_mapping(html_fields,analyzed_fields,keyword_fields,dense_vector)

    return document