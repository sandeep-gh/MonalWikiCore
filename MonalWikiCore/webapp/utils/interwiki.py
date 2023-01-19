import sys
import logging
import justpy as jp
from moin.utils.interwiki import  get_fqname,  join_wiki
from moin.constants.keys import CURRENT, FIELDS, NAME_EXACT, NAMESPACE
from moin.constants.contenttypes import CHARSET

def is_local_wiki(wiki_name):
    """
    check if <wiki_name> is THIS wiki
    """
    return wiki_name in ['', 'Self', jp.wikiConfig.interwikiname, ]

def url_for_item(request, item_name, wiki_name='', field='', namespace='', rev=CURRENT, endpoint_name='show_item', _external=False, regex=''):
    """
    Compute URL for some local or remote/interwiki item.

    For local items:
    give <rev> to get the url of some specific revision.
    give the <endpoint> to get the url of some specific view,
    give _external=True to compute fully specified URLs.

    For remote/interwiki items:
    If you just give <item_name> and <wiki_name>, a generic interwiki URL
    will be built.
    If you also give <rev> and/or <endpoint>, it is assumed that remote wiki
    URLs are built in the same way as local URLs.
    Computed URLs are always fully specified.
    """
    # traceback.print_stack(file=sys.stdout)
    if field == NAME_EXACT:
        field = ''

    if _external:
        #TODO: how to handle external 
        raise ValueError("Uncharted terriority")
    if is_local_wiki(wiki_name):
        item_name = get_fqname(item_name, field, namespace)
        if rev is None or rev == CURRENT:
            print (f"get_url for {endpoint_name} {item_name}")
            #url = request.url_for(endpoint_name, item_name=item_name, _external=_external)
            
            url = jp.app.url_path_for(endpoint_name, item_name=item_name)

        else:
            raise ValueError("In uncharted waters")
            url = jp.app.url_path_for(endpoint_name, item_name=item_name, rev=rev, _external=_external)
    else:
        raise ValueError("In uncharted waters")
        try:
            wiki_base_url = jp.wikiConfig.interwiki_map[wiki_name]
        except KeyError as err:
            logging.warning("no interwiki_map entry for {0!r}".format(wiki_name))
            item_name = get_fqname(item_name, field, namespace)
            if wiki_name:
                url = '{0}/{1}'.format(wiki_name, item_name)
            else:
                url = item_name
            url = '/{0}'.format(url)
        else:
            if (rev is None or rev == CURRENT) and endpoint == 'frontend.show_item':
                # we just want to show latest revision (no special revision given) -
                # this is the generic interwiki url support, should work for any remote wiki
                url = join_wiki(wiki_base_url, item_name, field, namespace)
            else:
                # rev and/or endpoint was given, assume same URL building as for local wiki.
                # we need this for moin wiki farms, e.g. to link from search results to
                # some specific item/revision in another farm wiki.
                item_name = get_fqname(item_name, field, namespace)
                local_url = jp.app.url_path_for(request.endpoint, item_name=item_name, rev=rev, _external=False)
                # we know that everything left of the + belongs to script url, but we
                # just want e.g. +show/42/FooBar to append it to the other wiki's
                # base URL.
                i = local_url.index('/+')
                path = local_url[i + 1:]
                url = wiki_base_url + path
    if regex:
        raise ValueError("Uncharted terriroty")
        url += '?regex={0}'.format(request.url_quote(regex, charset=CHARSET))
    return url
