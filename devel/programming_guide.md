
# Table of Contents

1.  [Index](#orgacf54d3)
    1.  [Create Index](#org6600a2e)
    2.  [index query](#org3ff2c2a)
    3.  [index save](#orgc52d46a)
2.  [Content and contenttypes](#orgf44b1f4)
    1.  [tests:](#orgb77a280)
        1.  [engine/](#orgbb6ed88)
        2.  [wiki/](#orgcd8cba4)
3.  [GetStorageRevision](#orgde2faa8)
    1.  [when called for item theat doesn't exists](#org034cd70)
    2.  [when called with item in the store](#orga524e81)
4.  [Code structure](#org92eec89)
    1.  [indexes.py](#org67c9c1f)
        1.  [indexes](#orgda6bfc9)
        2.  [get<sub>storage</sub><sub>revision</sub>](#orgf725a6d)
        3.  [storageItem<sub>to</sub><sub>whooshDoc</sub>](#org6442663)
        4.  [indexible<sub>content</sub>](#org746c5a7)
        5.  [class Revision](#org46764d7)
    2.  [./wiki/wikiItemTypes.py](#orgc638422)


<a id="orgacf54d3"></a>

# Index


<a id="org6600a2e"></a>

## Create Index

TBD


<a id="org3ff2c2a"></a>

## index query

indexes.create(\*\*fqcn.query<sub>terms</sub>)
returns IndexQueryAnswer


<a id="orgc52d46a"></a>

## index save

    meta = {...
    	'name': ['Home2'],
    	....
    	}
    data = b"...}
    
    content = indexible_content(meta, data)
    indexes.index_revision(meta, content)
    
    fqcn = CompositeName(NAMESPACE_DEFAULT, NAME_EXACT, 'Home2')
    
    whoosh_doc = indexes.document_search(**fqcn.query_terms)


<a id="orgf44b1f4"></a>

# Content and contenttypes

-   ./contenttypes.py

defines  contenttypes and its classes 
NonExistent, Markdown, 


<a id="orgb77a280"></a>

## tests:


<a id="orgbb6ed88"></a>

### engine/

1.  test<sub>indexible</sub><sub>content</sub>

    gets indexible plain text for data in Contenttype

2.  test<sub>get</sub><sub>storage</sub><sub>revision</sub>

    gets a revision. 


<a id="orgcd8cba4"></a>

### wiki/

1.  createwikiitem.py

    1.  when item is present in index
    
        <class 'MonalWikiCore.wiki.wikiItemTypes.Default'>


<a id="orgde2faa8"></a>

# GetStorageRevision


<a id="org034cd70"></a>

## when called for item theat doesn't exists

<class 'MonalWikiCore.engine.Dummy.Rev'>
revid =  None
meta = {'itemtype': 'nonexistent', 'contenttype': 'application/x-nonexistent'}


<a id="orga524e81"></a>

## when called with item in the store

class 'MonalWikiCore.engine.indexes.Revision'
revid =  117893a77a744d56b81dd283d5e2665
big-thick meta 


<a id="org92eec89"></a>

# Code structure


<a id="org67c9c1f"></a>

## indexes.py


<a id="orgda6bfc9"></a>

### indexes


<a id="orgf725a6d"></a>

### get<sub>storage</sub><sub>revision</sub>


<a id="org6442663"></a>

### storageItem<sub>to</sub><sub>whooshDoc</sub>


<a id="org746c5a7"></a>

### indexible<sub>content</sub>


<a id="org46764d7"></a>

### class Revision


<a id="orgc638422"></a>

## ./wiki/wikiItemTypes.py

-   class Default <==> ITEMTYPE<sub>DEFAULT</sub>
-   class NonExistent <==> ITEMTYPE\_

