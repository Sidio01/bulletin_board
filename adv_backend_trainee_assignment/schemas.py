AD_SCHEMA = {
    '$schema': 'http://json-schema.org/schema#',
    'type': 'object',
    'properties': {
        'title': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 200
        },
        'description': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1000
        },
        'urls_list': {
            'type': 'string',
            'minLength': 1,
            'maxLength': 1000
        },
        'price': {
            'anyOf': [
                {
                    'type': 'integer',
                    'minimum': 1
                },
                {
                    'type': 'string',
                    'minLength': 1,
                    'pattern': '^\d+$'
                }
            ]
        },
    },
    'required': ['title', 'description', 'urls_list', 'price'] 
}


# ADD_ITEM_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'title': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 64
#         },
#         'description': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024
#         },
#         'price': {
#             'anyOf': [
#                 {
#                     'type': 'integer',
#                     'minimum': 1,
#                     'maximum': 1000000,
#                 },
#                 {
#                     'type': 'string',
#                     'minLength': 1,
#                     'pattern': '^\d+$'
#                 }
#             ]
#         },
#     },
#     'required': ['title', 'description', 'price']
# }

# POST_REVIEW_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'text': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024
#         },
#         'grade': {
#             'anyOf': [
#                 {
#                     'type': 'integer',
#                     'minimum': 1,
#                     'maximum': 10,
#                 },
#                 {
#                     'type': 'string',
#                     'minLength': 1,
#                     'pattern': '^\d+$'
#                 }
#             ]
#         },
#     },
#     'required': ['text', 'grade']
# }

# GET_ITEM_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'rstName': {
#             'type': 'string'
#         },
#         'lastName': {
#             'type': 'string'
#         },
#         'age': {
#             'description': 'Age in years',
#             'type': 'integer',
#             'minimum': 0
#         }
#     },
#     'required': ['rstName', 'lastName']
# }
