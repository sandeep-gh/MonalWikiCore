
from typing import Any, NamedTuple
#from constant_keys import NAME_EXACT
from .constant_keys import CURRENT, FIELDS, NAME_EXACT, NAMESPACE, NAME
from .needs_home import namespaces

def get_fqname(item_name, field, namespace):
    """
    Compute composite name from item_name, field, namespace
    composite name == [NAMESPACE/][@FIELD/]NAME
    """
    print ("in get_fqname = ", item_name, field, namespace)
    if field and field != NAME_EXACT:
        item_name = '@{0}/{1}'.format(field, item_name)
    if namespace:
        item_name = '{0}/{1}'.format(namespace, item_name)
    return item_name

class CompositeName(NamedTuple):
    namespace: Any
    field: Any
    value: Any
    def query(self):
        """
            returns a dict that can be used as a whoosh query
            to lookup index documents matching this CompositeName
            """
        field = NAME_EXACT if not self.field else self.field
        return {NAMESPACE: self.namespace, field: self.value}
    def fullname(self):
        return get_fqname(self.value, self.field, self.namespace)

    @property
    def query_terms(self):
        """
        returns a dict that can be used as a whoosh query
        to lookup index documents matching this CompositeName
        """
        field = NAME_EXACT if not self.field else self.field
        return {NAMESPACE: self.namespace, field: self.value}
    
def split_namespace(url):
    """
    Find the longest namespace in the set.
    the namespaces are separated by  slashes (/).
    Example:
        namespaces_set(['ns1', 'ns1/ns2'])
        url: ns1/urlalasd return: ns1, urlalasd
        url: ns3/urlalasd return: '', ns3/urlalasd
        url: ns2/urlalasd return: '', ns2/urlalasd
        url: ns1/ns2/urlalasd return: ns1/ns2, urlalasd
    param namespaces_set: set of namespaces (strings) to search
    param url: string
    returns: (namespace, url)
    """
    namespace = ''
    tokens_list = url.split('/')
    for token in tokens_list:
        if namespace:
            token = '{0}/{1}'.format(namespace, token)
        if token in namespaces:
            namespace = token
        else:
            break
    if namespace:
        length = len(namespace) + 1
        url = url[length:]
    return namespace, url



def url_to_compositeName(url):
    """
    Split a fully qualified url into namespace, field and pagename
    url -> [NAMESPACE/][@FIELD/]NAME

    :param url: the url to split
    :returns: a namedtuple CompositeName(namespace, field, itemname)
    Examples::

        url: 'ns1/ns2/@itemid/Page' return 'ns1/ns2', 'itemid', 'Page'
        url: '@revid/OtherPage' return '', 'revid', 'OtherPage'
        url: 'ns1/Page' return 'ns1', '', 'Page'
        url: 'ns1/ns2/@notfield' return 'ns1/ns2', '', '@notfield'
    """
    print ("----------")
    print ("in compositeName = ", url)
    if not url:
        return CompositeName('', NAME_EXACT, '')
    # SystemDesign: We currently are not implementing this whole trailing / loging 
    #namespaces = namespaces.keys() # {namespace.rstrip('/') for namespace, _ in namespace_mapping}
    namespace, url = split_namespace(url)
    field = NAME_EXACT
    if url.startswith('@'):
        tokens = url[1:].split('/', 1)
        if tokens[0] in FIELDS:
            field = tokens[0]
            url = tokens[1] if len(tokens) > 1 else ''
    return CompositeName(namespace, field, url)


def get_names(meta):
    """
    Get the (list of) names from meta data and deal with misc. bad things that
    can happen then (while not all code is fixed to do it correctly).

    TODO make sure meta[NAME] is always a list of str

    :param meta: a metadata dictionary that might have a NAME key
    :return: list of names
    """
    #This is called too many times 
    #print ("==>get_names called with meta = ", meta)
    msg = "NAME is not a list but %r - fix this! Workaround enabled."
    names = meta.get(NAME)
    if names is None:
        #logging.warning(msg % names)
        names = []
    elif isinstance(names, bytes):
        #logging.warning(msg % names)
        names = [names.decode('utf-8'), ]
    elif isinstance(names, str):
        #logging.warning(msg % names)
        names = [names, ]
    elif isinstance(names, tuple):
        #logging.warning(msg % names)
        names = list(names)
    elif not isinstance(names, list):
        raise TypeError("NAME is not a list but %r - fix this!" % names)
    if not names:
        names = []
    return names
