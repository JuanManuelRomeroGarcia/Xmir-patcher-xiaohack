
import json

version_json = '''
{"date": "2025-01-23T03:07:35.098902", "dirty": false, "error": null, "full-revisionid": "221e2fd425c80041b57b09a7e0af0d33d548fb87", "version": "1.1.2.post1"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

