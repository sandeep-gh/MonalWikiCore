DATAID = "dataid"
NAMESPACE = "namespace"
NAME = "name"  # a list of strings, not useful for searching nor sorting, see #364
NAMES = "names"  # fullnames of item separated by |, useful for indexing/searching/display
NAME_SORT = "name_sort"  # useful for sorting, slashes removed because of whoosh, see #209
NAME_OLD = "name_old"

# the name of the backend in which revision is stored
BACKENDNAME = "backendname"
MTIME = "mtime"
PTIME = "ptime"

ITEMID = "itemid"
NAME_EXACT = "name_exact"

LATEST_REVS = 'latest_revs'


# Fields
WIKINAME = "wikiname"
REVID = "revid"
REV_NUMBER = "rev_number"
# in which backend is some revision stored?
BACKENDNAME = "backendname"
MTIME = "mtime"
ITEMTYPE = "itemtype"
CONTENTTYPE = "contenttype"
TAGS = "tags"
HAS_TAG = "has_tag"
LANGUAGE = "language"
USERID = "userid"
ADDRESS = "address"
HOSTNAME = "hostname"
SIZE = "size"
ACTION = "action"
COMMENT = "comment"
DATAID = "dataid"
TRASH = "trash"


#latest rev field
ITEMLINKS = "itemlinks"
ITEMTRANSCLUSIONS = "itemtransclusions"
ACL = "acl"
CONTENTNGRAM = "contentngram"
SUMMARYNGRAM = "summaryngram"
NAMENGRAM = "namengram"

#userprofile fields
EMAIL = "email"
MAILTO_AUTHOR = "mailto_author"
SUBSCRIPTION_IDS = "subscription_ids"
SUBSCRIPTION_PATTERNS = "subscription_patterns"
LOCALE = "locale"
DISABLED = "disabled"
PTIME = "ptime"
