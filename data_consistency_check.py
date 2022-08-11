import json
from jsonschema import validate as validate



def validate_data(data_directory):
    data_list = []

    # reading data from storage
    with open(data_directory) as f:
        for json_obj in f:
            data_dict = json.loads(json_obj)
            data_list.append(data_dict)

    # schema to check

    schema = {
        "type": "object",

        "properties": {


            "id": {"type": "number"},
            "id_str": {"type": "string"},
            "created_at": {"type": "string"},
            "full_txt": {"type": "string"},
            "lang": {"type": "string"},
            "truncated": {"type": "boolean"},
            "entities": {
                "type": "object",
                "properties": {
                    "hashtags": {
                        "type": "array",
                        "properties": {
                            "text": {"type": "string"}
                        },
                        "required": ["text"],
                        #                     "additionalProperties" : True,
                    }
                }
            },
            "user": {
                "type": "object",
                "properties": {
                    "name": {"type":  "string"},
                    "id": {"type": "number"}
                },
                "required": ["id", "name"],

            }
        },

        "required": ["full_text", "id", "lang", "user"],
        "additionalProperties": True,


    }

    # evaluating each line
    count = 0
    try:
        for x in data_list:
            validate(
                instance=x, schema=schema,
            )
            count += 1
    except:
        return [False, count]
    else:
        return [True, count]
