import ofjustpy as oj
import justpy as oj

#dervied from moin/templates/{show.html, itemviews.html} 
def header_itemviews_(itemviews = None, cfg= None):

    for endpoint, label, title in filter(lambda x: x[0] not in cfg.endpoints_excluded, cfg.item_views):
        if not check_exits or check_exists and exists:
            if endpoint in ['frontend.show_item',
                            'frontend.show_item_meta',
                            'frontend.history',
                            'frontend.download_item'
                            ]:
                oj.A_(title, rel="nofollow", href=url_for(endpoint, item_name=fqname), text=label)
            
        
    oj.Subsection_("itemviewsPanel", "Item Views", cgens = [])
    pass
