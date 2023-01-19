import json
def serialize(meta):
    text = json.dumps(meta, ensure_ascii=False)
    meta_str = text.encode('utf-8')
    return meta_str



