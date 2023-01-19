from MonalWikiCore.wiki import WikiItem

from addict import Dict
import justpy as jp
import ofjustpy as oj
import ofjustpy_react as ojr


from MonalWikiCore.constant_keys import CURRENT
from MonalWikiCore.constant_keys import ITEMTYPE_NONEXISTENT, ITEMTYPE_DEFAULT
from MonalWikiCore.Name import url_to_compositeName
from MonalWikiCore.wiki import WikiItem
from MonalWikiCore.wiki.Content import CONTENTTYPE_NONEXISTENT

from MonalWikiCore.wikicfg import NAMESPACES, WIKINAME, BACKEND_DATADIR_BASE
from MonalWikiCore.engine.storage_routing import storage_routing
from MonalWikiCore.constant_keys import NAME, NAMESPACE
from MonalWikiCore.engine import indexes

from MonalWikiCore.frontend.view_function import modify_wikiItem_
from MonalWikiCore.frontend.wp_template_components import page_builder

from addict import Dict
storage_base_dir = f"{BACKEND_DATADIR_BASE}/{WIKINAME}"

# initialize storage 
storage_routing(NAMESPACES, storage_base_dir)

# initialize indexes  
indexes.indexes(storage_base_dir)


rev = CURRENT
itemtype = ITEMTYPE_NONEXISTENT
contenttype = None
item_name = "Home"
fqcn = url_to_compositeName(item_name)
wikiItem = WikiItem.create(fqcn, rev_id=rev, itemtype = itemtype, contenttype=contenttype)

request = Dict()
request.session_id = "abc"

wp = page_builder("wp_show_wikiItem",
                  "Show contents of a wiki item",
                  modify_wikiItem_(wikiItem)
                  )(request)

#wp = renderhtml_wikiItem(request, wikiItem)
#print(wp)
_sm = wp.session_manager
_ss = _sm.stubStore
msg = Dict()
msg.value = "just click it"
_ss.tlctx.body.submit.target.on_click(msg)
