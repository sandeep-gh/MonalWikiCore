from typing import Any, NamedTuple
from Registry import RegistryBase
from mime import Type
from operator import attrgetter
from dataclasses import dataclass
#from flask import request, url_for, Response, abort, escape
from contenttypes import (
    GROUP_MARKUP_TEXT, GROUP_OTHER_TEXT, GROUP_IMAGE, GROUP_AUDIO, GROUP_VIDEO,
    GROUP_DRAWING, GROUP_OTHER, CONTENTTYPE_NONEXISTENT, CHARSET
)




class RegistryContent(RegistryBase):
    class Entry(NamedTuple):
        factory:Any
        content_type:Any
        default_contenttype_params: Any
        display_name: Any
        ingroup_order: Any
        priority: Any 
        def __call__(self, content_type, *args, **kw):
            if self.content_type.issupertype(Type(content_type)):
                return self.factory(content_type, *args, **kw)

        def __lt__(self, other):
            if isinstance(other, self.__class__):
                # Within the registry, content_type is sorted in descending
                # order (more specific first) while priority is in ascending
                # order (smaller first).
                return (other.content_type, self.priority) < (self.content_type, other.priority)
            return NotImplemented

    def __init__(self, group_names):
        super(RegistryContent, self).__init__()
        self.group_names = group_names
        self.groups = dict([(g, []) for g in group_names])

    def register(self, e, group):
        """
        Register a contenttype entry and optionally add it to a specific group.
        """
        # If group is specified and contenttype is not a wildcard one
        if group and e.content_type.type and e.content_type.subtype:
            if group not in self.groups:
                raise ValueError('Unknown group name: {0}'.format(group))
            self.groups[group].append(e)
            self.groups[group].sort(key=attrgetter('ingroup_order'))
        return self._register(e)

    
content_registry = RegistryContent([
    GROUP_MARKUP_TEXT,
    GROUP_OTHER_TEXT,
    GROUP_IMAGE,
    GROUP_AUDIO,
    GROUP_VIDEO,
    GROUP_DRAWING,
    GROUP_OTHER
])


class Content:
    """
    Base for content classes defining some helpers, agnostic about content
    data.
    """
    # placeholder values for registry entry properties
    contenttype = None
    default_contenttype_params = {}
    display_name = None
    group = GROUP_OTHER
    ingroup_order = 0

    @classmethod
    def _factory(cls, *args, **kw):
        return cls(*args, **kw)

    @classmethod
    def create(cls, contenttype, item=None):
        content = content_registry.get(contenttype, item)
        #logging.debug("Content class {0!r} handles {1!r}".format(content.__class__, contenttype))
        return content

    def __init__(self, contenttype, item=None):
        # We need to keep the exact contenttype since contents may be handled
        # by a Content subclass with wildcard contenttype (eg. an unknown
        # contenttype some/type gets handled by Binary)
        # TODO use Type instead of strings?
        self.contenttype = contenttype
        self.item = item

    # XXX For backward-compatibility (so code can be moved from Item
    # untouched), remove soon
    @property
    def rev(self):
        return self.item.rev

    @property
    def name(self):
        return self.item.name

    def get_data(self):
        return ''  # TODO create a better method for binary stuff
    data = property(fget=get_data)

    # @timed('conv_in_dom')
    # def internal_representation(self, attributes=None, preview=None):
    #     """
    #     Return the internal representation of a document using a DOM Tree
    #     """
    #     doc = cid = None
    #     if preview is None:
    #         hash_name = HASH_ALGORITHM
    #         hash_hexdigest = self.rev.meta.get(hash_name)
    #         if hash_hexdigest:
    #             cid = cache_key(usage="internal_representation",
    #                             hash_name=hash_name,
    #                             hash_hexdigest=hash_hexdigest,
    #                             attrs=repr(attributes))
    #             doc = app.cache.get(cid)
    #     if doc is None:
    #         # We will see if we can perform the conversion:
    #         # FROM_mimetype --> DOM
    #         # if so we perform the transformation, otherwise we don't
    #         from moin.converters import default_registry as reg
    #         input_conv = reg.get(Type(self.contenttype), type_moin_document)
    #         if not input_conv:
    #             raise TypeError("We cannot handle the conversion from {0} to the DOM tree".format(self.contenttype))
    #         smiley_conv = reg.get(type_moin_document, type_moin_document, icon='smiley')

    #         # We can process the conversion
    #         name = self.rev.fqname.fullname if self.rev else self.name
    #         links = Iri(scheme='wiki', authority='', path='/' + name)
    #         doc = input_conv(preview or self.rev, self.contenttype, arguments=attributes)
    #         # XXX is the following assuming that the top element of the doc tree
    #         # is a moin_page.page element? if yes, this is the wrong place to do that
    #         # as not every doc will have that element (e.g. for images, we just get
    #         # moin_page.object, for a tar item, we get a moin_page.table):
    #         doc.set(moin_page.page_href, str(links))
    #         if self.contenttype.startswith(('text/x.moin.wiki', 'text/x-mediawiki', 'text/x.moin.creole', )):
    #             doc = smiley_conv(doc)
    #         if cid:
    #             app.cache.set(cid, doc)
    #     return doc

    # def _expand_document(self, doc):
    #     from moin.converters import default_registry as reg
    #     flaskg.add_lineno_attr = False  # do not add data-lineno attr for transclusions, footnotes, etc.
    #     include_conv = reg.get(type_moin_document, type_moin_document, includes='expandall')
    #     macro_conv = reg.get(type_moin_document, type_moin_document, macros='expandall')
    #     nowiki_conv = reg.get(type_moin_document, type_moin_document, nowiki='expandall')
    #     link_conv = reg.get(type_moin_document, type_moin_document, links='extern')
    #     flaskg.clock.start('nowiki')
    #     doc = nowiki_conv(doc)
    #     flaskg.clock.stop('nowiki')
    #     flaskg.clock.start('conv_include')
    #     doc = include_conv(doc)
    #     flaskg.clock.stop('conv_include')
    #     flaskg.clock.start('conv_macro')
    #     doc = macro_conv(doc)
    #     flaskg.clock.stop('conv_macro')
    #     flaskg.clock.start('conv_link')
    #     doc = link_conv(doc)
    #     flaskg.clock.stop('conv_link')
    #     if 'regex' in request.args:
    #         highlight_conv = reg.get(type_moin_document, type_moin_document, highlight='highlight')
    #         flaskg.clock.start('highlight')
    #         doc = highlight_conv(doc)
    #         flaskg.clock.stop('highlight')
    #     return doc

    # def _render_data(self, preview=None):
    #     try:
    #         from moin.converters import default_registry as reg
    #         # TODO: Real output format
    #         doc = self.internal_representation(preview=preview)
    #         doc = self._expand_document(doc)
    #         flaskg.clock.start('conv_dom_html')
    #         html_conv = reg.get(type_moin_document, Type('application/x-xhtml-moin-page'))
    #         doc = html_conv(doc)
    #         flaskg.clock.stop('conv_dom_html')
    #         rendered_data = conv_serialize(doc, {html.namespace: ''})
    #     except Exception:
    #         # we really want to make sure that invalid data or a malfunctioning
    #         # converter does not crash the item view (otherwise a user might
    #         # not be able to fix it from the UI).
    #         error_id = uuid.uuid4()
    #         logging.exception("An exception happened in _render_data (error_id = %s ):" % error_id)
    #         rendered_data = render_template('crash.html',
    #                                         server_time=time.strftime("%Y-%m-%d %H:%M:%S %Z"),
    #                                         url=request.url,
    #                                         error_id=error_id)
    #     return rendered_data

    # def _render_data_xml(self):
    #     doc = self.internal_representation()
    #     return conv_serialize(doc,
    #                           {moin_page.namespace: '',
    #                            xlink.namespace: 'xlink',
    #                            html.namespace: 'html',
    #                            }, 'xml')

    def _render_data_highlight(self):
        # override this in child classes
        return ''

    def _get_data_diff_text(self, oldfile, newfile):
        """ Get the text diff of 2 versions of file contents

        :param oldfile: file that contains old content data (bytes)
        :param newfile: file that contains new content data (bytes)
        :return: list of diff lines in a unified format without trailing linefeeds
        """
        return []

    # def get_templates(self, contenttype=None):
    #     """ create a list of templates (for some specific contenttype) """
    #     terms = [Term(WIKINAME, app.cfg.interwikiname), Term(TAGS, TEMPLATE), Term(NAMESPACE, self.item.fqname.namespace)]
    #     if contenttype is not None:
    #         terms.append(Term(CONTENTTYPE, contenttype))
    #     query = And(terms)
    #     revs = flaskg.storage.search(query, sortedby=NAME_EXACT, limit=None)
    #     return [rev.fqname.fullname for rev in revs]


    
# class Content:
#     contenttype = None
#     default_contenttype_params = {}
#     display_name = None
#     group =  GROUP_OTHER
#     ingroup_order = 0
#     @classmethod
#     def _factory(cls, *args, **kw):
#         return cls(*args,
#                    **kw)
#     def __init__(self, contenttype, item=None):
#         # We need to keep the exact contenttype since contents may be handled
#         # by a Content subclass with wildcard contenttype (eg. an unknown
#         # contenttype some/type gets handled by Binary)
#         # TODO use Type instead of strings?
#         self.contenttype = contenttype
#         self.item = item

#     @classmethod
#     def create(cls, contenttype, item=None):
#         content = content_registry.get(contenttype, item)
#         return content


def register(cls):
    content_registry.register(RegistryContent.Entry(cls._factory, Type(cls.contenttype),
                                                    cls.default_contenttype_params, cls.display_name,
                                                    cls.ingroup_order, RegistryContent.PRIORITY_MIDDLE), cls.group)
    return cls


@register
class NonExistentContent(Content):
    """Dummy Content to use with NonExistent."""
    contenttype = CONTENTTYPE_NONEXISTENT
    group = None
    def do_get(self, force_attachment=False, mimetype=None):
        #abort(404)
        raise ValueError("implement starlette abort")
        pass

    def _convert(self, doc):
        #abort(404)
        raise ValueError("not yet implemented")
        pass
        

# @register
# class NonExistentContent(Content):
#     """Dummy Content to use with NonExistent."""
#     contenttype = CONTENTTYPE_NONEXISTENT
#     group = None
#     def do_get(self, force_attachment=False, mimetype=None):
#         #abort(404)
#         raise ValueError("implement starlette abort")
#         pass

#     def _convert(self, doc):
#         raise ValueError("implement starlette abort")
#         #abort(404)
#         pass
