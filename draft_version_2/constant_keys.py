
NAMESPACE_DEFAULT = ''
NAMESPACE_USERPROFILES = 'userprofiles'
NAMESPACE_USERS = 'users'
NAMESPACE_HELP_COMMON = 'help-common'
NAMESPACE_HELP_EN = 'help-en'
NAMESPACE_ALL = 'all'  # An identifier namespace which acts like a union of all the namespaces.
NAMESPACES_IDENTIFIER = [NAMESPACE_ALL, ]  # List containing all the identifier namespaces.


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
ALL_REVS = 'all_revs'


# Fields
WIKINAME = "wikiname"
REVID = "revid"
REV_NUMBER = "rev_number"
PARENTID = "parentid"
PARENTNAMES = "parentnames"
WIKINAME = "wikiname"
CONTENT = "content"
REFERS_TO = "refers_to"

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

SUMMARY = "summary"
TRASH = "trash"


ITEMTYPE_NONEXISTENT = 'nonexistent'
ITEMTYPE_USERPROFILE = 'userprofile'
ITEMTYPE_DEFAULT = 'default'  # == wiki-like
ITEMTYPE_TICKET = 'ticket'
ITEMTYPE_BLOG = 'blog'
ITEMTYPE_BLOGENTRY = 'blogentry'



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

# keys for tickets
EFFORT = "effort"
DIFFICULTY = "difficulty"
SEVERITY = "severity"
PRIORITY = "priority"
ASSIGNED_TO = "assigned_to"
SUPERSEDED_BY = "superseded_by"
DEPENDS_ON = "depends_on"
CLOSED = "closed"
ELEMENT = "element"
REPLY_TO = "reply_to"



# we need a specific hash algorithm to store hashes of revision data into meta
# data. meta[HASH_ALGORITHM] = hash(rev_data, HASH_ALGORITHM)
# some backends may use this also for other purposes.
HASH_ALGORITHM = "sha1"
HASH_LEN = 40  # length of hex str representation of hash value


# magic REVID for current revision:
CURRENT = "current"

# Values that FIELD can take in the composite name: [NAMESPACE/][@FIELD/]NAME
FIELDS = [
    NAME_EXACT, ITEMID, REVID, TAGS, USERID, ITEMLINKS, ITEMTRANSCLUSIONS,
]

# Fields that can be used as a unique identifier.
UFIELDS = [
    NAME_EXACT, ITEMID, REVID,
]

UFIELDS_TYPELIST = [NAME_EXACT, ]
