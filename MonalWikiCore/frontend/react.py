"""
Contains all event handlers 
"""
import ofjustpy as oj
import ofjustpy_react as ojr

@ojr.CfgLoopRunner
def on_modify_hlitem_savebtn_click():
    """
    handle event savebtn click on modify/create item page
    """

    res = {'content': b"lots of stuff in binary",
           'title': "atitle",
           'tags' : []
           'comment': "a comment"
           }
    
           
    return  "/modify_hlitem", ojr.OpaqueDict(res)
