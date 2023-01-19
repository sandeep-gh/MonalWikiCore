
# Table of Contents

1.  [Nuts/Bolts/DataGuide](#orgf364210)
    1.  [webpage rendering logic](#org683602b)
        1.  [A wikiItem with itemtype default and contenttype None](#org2726a7d)
        2.  [A wikiItem with itemtype default and contenttype non-none but revid is None](#org6fe33ab)
        3.  [A wikiItem with itemtype default and contenttype non-none and not none revid](#orga3907f9)
    2.  [The datatypes](#org4c36fba)
        1.  [WikiItem is abstract type/a tag/](#org2f9aaad)
        2.  [Revision](#orgda0adac)
        3.  [IndexItem](#org96e1230)
2.  [tracking Contenttype](#org11ba090)
3.  [Tracking revision and revid](#org1469d39)
4.  [Code Review](#org9ea3675)
    1.  [Data Store](#org3b1ed4f)
        1.  [sqlite storage is very simple](#org9e5f78c)
        2.  [create<sub>storage</sub>](#org97c49bd)
        3.  [storage<sub>routing</sub>](#orga9729ed)
    2.  [indexes](#org256fe8e)
        1.  [IndexItem](#orgc28c376)
        2.  [Revision](#org1a106b2)
        3.  [Meta (a class)](#orgbca1400)
        4.  [indexible<sub>content</sub>](#orge384a16)
        5.  [storageItem<sub>to</sub><sub>whooshDoc</sub>](#org259c8d9)
        6.  [document<sub>search</sub>](#orgd0cb406)
        7.  [index<sub>revision</sub>](#org063c3a4)
        8.  [retry<sub>document</sub><sub>search</sub><sub>until</sub><sub>succeed</sub>](#org78a9b97)
        9.  [store<sub>revision</sub>](#org574abd5)
    3.  [wiki](#org090c10c)
        1.  [WikiItem](#org125f52c)
5.  [Code Layout](#org46f5400)
    1.  [MonalWikiCore](#orgd960d26)
        1.  [MonalWikiCore](#org97cdc5c)
        2.  [tests](#orgfa363f3)
6.  [logic flow](#org4bb2512)
    1.  [starting  from new meta and data for a given item with item<sub>name</sub>](#orgd66bcb6)
        1.  [the backend-storage story](#org0f6af5d)
        2.  [create wikiItem story](#orgfdf0828)
        3.  [the indexes](#org7764429)
7.  [GamePlan](#org8249625)
8.  [](#org7610ad1)


<a id="orgf364210"></a>

# Nuts/Bolts/DataGuide


<a id="org683602b"></a>

## webpage rendering logic


<a id="org2726a7d"></a>

### A wikiItem with itemtype default and contenttype None

outcome: render a page that gives options for contentype : markdown or csv


<a id="org6fe33ab"></a>

### A wikiItem with itemtype default and contenttype non-none but revid is None

offer a webpage to fill out the contents


<a id="orga3907f9"></a>

### A wikiItem with itemtype default and contenttype non-none and not none revid

render the contents


<a id="org4c36fba"></a>

## The datatypes


<a id="org2f9aaad"></a>

### WikiItem is abstract type/a tag/

-   Realized types: [NonExistent| Default]

defined in WikiItem.py/needs<sub>home.py</sub>: is create by show/modify items endpoints

1.  NonExistent

    -   fields
        -   fqcn
        -   shown #unused for now

2.  Default

    -   fields
        -   fqcn : A composite name
        -   rev # A revision (see below)
        -   content # is of type [NonExistent| CSV | Markdown]


<a id="orgda0adac"></a>

### Revision

1.  fields

    -   idxitem
    -   revid
    -   doc
    -   meta
    -   name


<a id="org96e1230"></a>

### IndexItem

1.  fields

    -   name
    -   current # the whoosh search result


<a id="org11ba090"></a>

# tracking Contenttype

from wikiItem:

-   wikiItem.content.contenttype


<a id="org1469d39"></a>

# Tracking revision and revid


<a id="org9ea3675"></a>

# Code Review


<a id="org3b1ed4f"></a>

## Data Store

will store data and meta

-   data is binary blob
-   meta is a json object


<a id="org9e5f78c"></a>

### sqlite storage is very simple

simply call connect(filepath) and it wil build/setup the storage backend
provides set and get item apins 


<a id="org97c49bd"></a>

### create<sub>storage</sub>

create two tables in one db or two databases (with one table)
and provides metatbl<sub>manager</sub> and datatbl<sub>manager</sub>.

-   provides store<sub>manager</sub> funcinst
    -   store<sub>meta</sub>
        create a revid, serialize meta and store in table via metatbl<sub>manager</sub>
    -   store<sub>data</sub>
        create dataid and store dataid, data


<a id="orga9729ed"></a>

### storage<sub>routing</sub>

create storage for each namespace; route meta,data to namespace listed in meta


<a id="org256fe8e"></a>

## indexes


<a id="orgc28c376"></a>

### IndexItem

-   Name
-   current # this is the current doc that is stored-into/returned-from from Whoosh search


<a id="org1a106b2"></a>

### Revision

-   idxItem
-   revid
-   doc # doc keeps old revision of the item
-   meta
-   name #why we need a name


<a id="orgbca1400"></a>

### Meta (a class)

-   revision #revision has meta; meta has revision
-   doc # why meta has doc
-   meta # the meta dict


<a id="orge384a16"></a>

### indexible<sub>content</sub>

from data to content for whoosh-indexing 


<a id="org259c8d9"></a>

### storageItem<sub>to</sub><sub>whooshDoc</sub>

a doc/dict that fed to whoosh index


<a id="orgd0cb406"></a>

### document<sub>search</sub>

search for document with set of key-value pairs 


<a id="org063c3a4"></a>

### index<sub>revision</sub>

do the write to whoosh index


<a id="org78a9b97"></a>

### retry<sub>document</sub><sub>search</sub><sub>until</sub><sub>succeed</sub>

search for document using key-value search; fail in timedout


<a id="org574abd5"></a>

### store<sub>revision</sub>

store a new revision for a wikiItem 


<a id="org090c10c"></a>

## wiki


<a id="org125f52c"></a>

### WikiItem

-   fqname
-   rev
-   content


<a id="org46f5400"></a>

# Code Layout


<a id="orgd960d26"></a>

## MonalWikiCore


<a id="org97cdc5c"></a>

### MonalWikiCore

1.  wikicfg.py

    reads .env and initializes
    
    -   BACKEND<sub>DATADIR</sub><sub>BASE</sub>
    -   WIKINAME
    -   NAMESPACES
    -   STORAGETYPE
    -   STORAGEARGS

2.  constant<sub>keys.py</sub>

    All namespace definition, schema attribute names, and other constants

3.  system<sub>params.py</sub>

    knobs to configure the wiki engine

4.  needs<sub>home.py</sub>

    -   provides
        -   namespaces
        -   namespace<sub>mapping</sub>
        -   fieldnotuniqueerror

5.  utils.py

    -   provides:
        -   TrackingFileWrapper:class
            -   memfuncs:
                -   read
                -   size
                -   hash

6.  app<sub>fornow.py</sub>

    the entry point for uvicorn

7.  actions.py

    all backend actions

8.  Name

    -   provides
        -   split<sub>namespace</sub>:func
            god knows what it does
        -   split<sub>fqname</sub>
            returns CompositeName
        -   CompositeName
            A tuple of namespace, field, value
        -   get<sub>fqname</sub>:
            return namespaces/item<sub>name</sub><sub>name</sub>

9.  engine

    1.  indexes.py
    
        -   provides
            -   indexes: funcinst
                -   open
                -   document<sub>search</sub>
    
    2.  IndexItem
    
        -   provides
            -   create: func 
                -
    
    3.  IndexSchema.py
    
        Whoosh indexes use schema. There are two indexes latest revision and all revision.
        They have different schemas. 
    
    4.  ACL.py
    
        keywords/constants related to ACL 
    
    5.  SearchAnalyzers.py
    
        Not sure what it does
        
        -   provides
            -   MimeTokenizer: Class
            -   AclTokenizer: Class
            -   item<sub>name</sub><sub>analyzer</sub>:func
    
    6.  storage.py
    
        -   provides:
            -   create<sub>storage</sub>:func 
                -   returns:
                    -   store<sub>manager</sub>:funcinst
                        -   memfuncs:
                            -   store(meta, data)
    
    7.  storage<sub>routing.py</sub>
    
        -   provides
            -   storage<sub>routing</sub>: funcinst
                -   on-return-has
                    -   storage<sub>routing.store</sub>(meta, data)
    
    8.  crypto.py
    
        -   provides
            -   make<sub>uuid</sub>:func

10. wiki

    The constructs that make up the wiki:
    schema, Names, functions
    
    1.  Dummy
    
        provide rev and item, also,  explains their structures.
    
    2.  Revision
    
        -   provides
            -   create: function
                queries index to find indexItem that match

11. tests

    1.  storage<sub>routing.py</sub>
    
        tests both storage<sub>routing</sub> and storage.py


<a id="orgfa363f3"></a>

### tests

-   .env


<a id="org4bb2512"></a>

# logic flow


<a id="orgd66bcb6"></a>

## starting  from new meta and data for a given item with item<sub>name</sub>

this will happen when user fills out form for new item .

-   your meta will consists of itemtype, contenttype, namespace, tags, summary and etc.
    -   data is converted to  BytesIO
        -   store the meta and data in backend-storage will return the revid
            -   revid = storage<sub>routing.store</sub>(meta, data)
                -   create a wikiItem
                    -   call indexes.save(wikiItem, meta, data, and storage<sub>revid</sub> = revid)


<a id="org0f6af5d"></a>

### TODO the backend-storage story


<a id="orgfdf0828"></a>

### create wikiItem story

-   retrieve the current revision from index indexes.get<sub>storage</sub><sub>revision</sub>(fqcn, itemtype, contenttype, rev<sub>id</sub>, item)
    -   get contenttype from stored revision or from input one
        -   create \`placeholder content\` object based on contenttype
            -   get itemtype from rev.meta or parameter argument otherwise ITEMTYPE<sub>DEFAULT</sub>
                -   create placeholder item get<sub>item</sub>
                    -   return wikiitem

1.  get<sub>storage</sub><sub>revision</sub> story (fqcn:Name.CompositeName, itemtype=None, contenttype=None, rev<sub>id</sub>=CURRENT, item:IndexItem=None)

    -   if item is none then query the indexes using fqcn to get a wdoc (a whoosh document)
        -   if there is no document/whoosh-index-Entry-item the wdoc.id is None
            -   if wdoc.id is None
                -   create dummy.item(fqcn) and Dummy.rev(item) return rev
                -   else if wdoc exists
                    -   create Revision with item and asked rev<sub>id</sub>
                -   return rev


<a id="org7764429"></a>

### the indexes

1.  document<sub>search</sub>

    -   super simple one shot search in the index: returns None  if no matching document is found

2.  create (an indexitem from query)

    -   get the name from query
        -   perform document<sub>search</sub> using query over whoose index 
            -   if document<sub>search</sub> returns none then create a dict and populate with name
                -   return IndexItem(name, latest<sub>doc</sub>)

3.  save (save a wikiItem with meta and data and other attributes)

    -   create an indexItem from wikiItem.fqcn
        -   set currentrev and contenttype<sub>current</sub> from retrieved indexItem
            -   set COMMENT and REV<sub>NUMBER</sub> field of meta
                -   something about PARENTID : skip for now
                    -   set data from currentrev if data argument is None 
                        -   fix encoding
                            -   fix data format to Bytes io
                                -   create and store a new revision using updated meta, data, storage<sub>revid</sub> : store<sub>revision</sub>
    
    1.  the store<sub>revision</sub> story
    
        -   create indexible content from data
            -   update REVID of meta to storage<sub>revid</sub>
                -   store the meta, content  pair in index using index<sub>revision</sub>
                    -   get the whoosh-query-result-doc (wqrd) using retry<sub>document</sub><sub>search</sub><sub>until</sub><sub>succeed</sub> using revid
                        -   create IndexItem(name, wqrd)
                            -   create revision (idxItem, storage<sub>revid</sub>)
    
    2.  the index<sub>revision</sub> story
    
        -   main point is to use storageItem<sub>to</sub><sub>whooshDoc</sub> to convert the meta and content to doc
            -   store this doc in whoosh index


<a id="org8249625"></a>

# GamePlan

-   An index page that lists all the items. Has a button for new item
-   when clicked redirects to show<sub>item</sub> view function which creates nonexistent item
-   render nonexistent item shows types of item that can be created
-   when selected a url is generated like this: "eknayaitem?itemtype=default&contenttype=text%2Fx-markdown%3Bcharset%3Dutf-8&template="
-   from there its back to show<sub>item</sub>


<a id="org7610ad1"></a>

# 

