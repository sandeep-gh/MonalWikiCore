# we need
# - index_storage
# have

# lets create a index_storage and in it build a bunch of indexes in the 

# unprotected_storage = IndexingMiddleware(,
#                                                   None
#                                                   wiki_name="dummy_wiki",
#                                                   acl_rights_contents=None                                                  )

from .IndexingMiddleware import setup_index_storage


