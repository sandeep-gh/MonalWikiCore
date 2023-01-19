import pickle
import jsbeautifier
import json
opts = jsbeautifier.default_options()

    
with open("/tmp/moin_context", "rb") as fh:
    context = pickle.load(fh)

res = jsbeautifier.beautify(json.dumps(context), opts)
print(res)
