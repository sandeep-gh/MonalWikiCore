from whoosh.fields import Schema, TEXT, ID, IDLIST, NUMERIC, DATETIME, KEYWORD, BOOLEAN, NGRAMWORDS
from ..constant_keys import WIKINAME, NAMESPACE, NAME, NAMES, NAME_SORT, NAME_EXACT, NAME_OLD, REVID, REV_NUMBER, PARENTID, BACKENDNAME, MTIME, ITEMTYPE, CONTENTTYPE, TAGS, HAS_TAG, LANGUAGE, USERID, ADDRESS, HOSTNAME, SIZE, ACTION, COMMENT, SUMMARY, DATAID, TRASH, CONTENT, ITEMID, ITEMLINKS, ITEMTRANSCLUSIONS, ACL, CONTENTNGRAM, SUMMARYNGRAM, NAMENGRAM, EMAIL, MAILTO_AUTHOR, DISABLED, LOCALE, SUBSCRIPTION_IDS, SUBSCRIPTION_PATTERNS, EFFORT, DIFFICULTY, SEVERITY, PRIORITY, ASSIGNED_TO, REPLY_TO, REFERS_TO, ELEMENT, SUPERSEDED_BY, DEPENDS_ON, CLOSED, PTIME, ITEMID
from .SearchAnalyzers import item_name_analyzer, MimeTokenizer, AclTokenizer
from .ACL import ACL_RIGHTS_CONTENTS




common_fields = {
            # wikiname so we can have a shared index in a wiki farm, always check this!
            WIKINAME: ID(stored=True),
            # namespace, so we can have different namespaces within a wiki, always check this!
            NAMESPACE: ID(stored=True),
            # since name is a list whoosh will think it is a list of tokens see #364
            # we store list of names, but do not use for searching
            NAME: TEXT(stored=True),
            # string created by joining list of Name strings, we use NAMES for searching
            NAMES: TEXT(stored=True, multitoken_query="or", analyzer=item_name_analyzer(), field_boost=30.0),
            # names without slashes, slashes cause strange sort sequences
            NAME_SORT: TEXT(stored=True),
            # unmodified NAME from metadata - use this for precise lookup by the code.
            # also needed for wildcard search, so the original string as well as the query
            # (with the wildcard) is not cut into pieces.
            NAME_EXACT: ID(field_boost=1.0),
            # history and mychanges views show old name for deleted items
            NAME_OLD: TEXT(stored=True),
            # revision id (aka meta id)
            REVID: ID(unique=True, stored=True),
            # sequential revision number for humans: 1, 2, 3...
            REV_NUMBER: NUMERIC(stored=True),
            # parent revision id
            PARENTID: ID(stored=True),
            # backend name (which backend is this rev stored in?)
            BACKENDNAME: ID(stored=True),
            # MTIME from revision metadata (converted to UTC datetime)
            MTIME: DATETIME(stored=True),
            # ITEMTYPE from metadata, always matched exactly hence ID
            ITEMTYPE: ID(stored=True),
            # tokenized CONTENTTYPE from metadata
            CONTENTTYPE: TEXT(stored=True, multitoken_query="and", analyzer=MimeTokenizer()),
            # unmodified list of TAGS from metadata
            TAGS: KEYWORD(stored=True, commas=True, scorable=True, field_boost=30.0),
            # search on HAS_TAG improves response time of global tags
            # https://whoosh.readthedocs.io/en/latest/api/query.html?highlight=#whoosh.query.Every
            HAS_TAG: BOOLEAN(stored=False),
            LANGUAGE: ID(stored=True),
            # USERID from metadata

            USERID: ID(stored=True),
            # ADDRESS from metadata
            ADDRESS: ID(stored=True),
            # HOSTNAME from metadata
            HOSTNAME: ID(stored=True),
            # SIZE from metadata
            SIZE: NUMERIC(stored=True),
            # ACTION from metadata
            ACTION: ID(stored=True),
            # tokenized COMMENT from metadata
            COMMENT: TEXT(stored=True, field_boost=30.0),
            # SUMMARY from metadata
            SUMMARY: TEXT(stored=True, field_boost=10.0),
            # DATAID from metadata
            DATAID: ID(stored=True),
            # TRASH from metadata
            TRASH: BOOLEAN(stored=True),
            # data (content), converted to text/plain and tokenized
            CONTENT: TEXT(stored=True, spelling=True),
        }

latest_revs_fields = {
    # ITEMID from metadata - as there is only latest rev of same item here, it is unique
    ITEMID: ID(unique=True, stored=True),
    # unmodified list of ITEMLINKS from metadata
    ITEMLINKS: ID(stored=True),
    # unmodified list of ITEMTRANSCLUSIONS from metadata
    ITEMTRANSCLUSIONS: ID(stored=True),
    # tokenized ACL from metadata
    ACL: TEXT(analyzer=AclTokenizer(ACL_RIGHTS_CONTENTS), multitoken_query="and", stored=True),
    # index ngrams of words, field_boosts favor hits on name and summary over content
    CONTENTNGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=0.01),
    SUMMARYNGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=1.0),
    NAMENGRAM: NGRAMWORDS(minsize=3, maxsize=6, queryor=True, field_boost=1.0),
}
latest_revs_fields.update(**common_fields)

userprofile_fields = {
    # Note: email (if given) should be unique, but we might
    # have lots of empty values if it is not given and thus it is NOT
    # unique overall! Wrongly declaring it unique would lead to whoosh
    # killing other users from index when update_document() is called!
    EMAIL: ID(stored=True),
    MAILTO_AUTHOR: BOOLEAN(stored=True),
    DISABLED: BOOLEAN(stored=True),
    LOCALE: ID(stored=True),
    SUBSCRIPTION_IDS: ID(),
    SUBSCRIPTION_PATTERNS: ID(),
}

    

latest_revs_fields.update(**userprofile_fields)

# XXX This is a highly adhoc way to support indexing of ticket items.
ticket_fields = {
    EFFORT: NUMERIC(stored=True),
    DIFFICULTY: NUMERIC(stored=True),
    SEVERITY: NUMERIC(stored=True),
    PRIORITY: NUMERIC(stored=True),
    ASSIGNED_TO: ID(stored=True),
    REPLY_TO: ID(stored=True),
    REFERS_TO: ID(stored=True),
    ELEMENT: ID(stored=True),
    SUPERSEDED_BY: ID(stored=True),
    DEPENDS_ON: ID(stored=True),
    CLOSED: BOOLEAN(stored=True),
}

latest_revs_fields.update(**ticket_fields)

blog_entry_fields = {
    # blog publish time from metadata (converted to UTC datetime)
    PTIME: DATETIME(stored=True),
}
latest_revs_fields.update(**blog_entry_fields)

all_revs_fields = {
    ITEMID: ID(stored=True),
    
}
all_revs_fields.update(**common_fields)

latest_revisions_schema = Schema(**latest_revs_fields)
all_revisions_schema = Schema(**all_revs_fields)
