#!/usr/bin/env python
#coding: utf-8
"""
@Author: COOl (1258626769@qq.com)
@Ctime: 2017年04月28日 11时29分39秒
@Latest: 2017年04月28日 11时29分39秒
@Purpose: 


"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys, re, time, datetime, traceback, logging, json
# more: http://python-future.org/automatic_conversion.html
# python3 urllib, python2's urllib is deprecated (use urllib_parse).
from six.moves import urllib  
# all in six._moved_attributes
# python2 urllib2
from six.moves import urllib_request as urllib2
# urllib.parse for parse
from six.moves import urllib_parse as urlparse 
# urllib.error for error
from six.moves import urllib_error 
# http.client here only for httplib.HTTPException
from six.moves import http_client as httplib 
import unittest

from .hashring import *
from .hashtable import *

def rept_decorator(num=3):
    """
    @update: 2017-01-17 11:23:35
    @func: repeat n times of func
    @repr: =0 ==> break,else continue.
    """
    def log_func(func):
        @wraps(func)
        def real_func(*args,**kwargs):
            res = False
            for itv in xrange(num):
                res = func(*args,**kwargs)
                if res:
                    break
                else:
                    time.sleep(10)
                    continue
            return res
        return real_func      
    return log_func  

class HashNode(object):
    """
    @func: a node in hashnet, khashmir.node
    @howto: init
            ping_root until succ
            find_node(id+-1) ... find_node(id+-2**4**(n-1)) to general table
            check time up, do ping in table, succ:update, failed:find_node
            do in loop
    @maybe: callback failed and del ,find_node
    @variable: vid: {host,port,replicas}
               vnode|tnode: {id,host,port,replicas}
               key: any hash id
               
    """
    def __init__(self, **kwargs):
        self.host = kwargs.setdefault('host', '')
        self.port = kwargs.setdefault('port', '7777')
        # This can be weight, or one disk for one node...
        self.replicas = kwargs.setdefault('replicas', 1)
        assert bool(self.host) != None, 'host required!'
        assert self.replicas >=1, 'replicas > =1:%s' % self.replicas
        self.vids = self.gen_vids()
        self.hashtables = self.init_htable()
        self.send_data = ["id", "host", "port", "replicas", "time"]
    def __str__(self):
        return '%s:%s_%r'%(self.host,self.port,self.vids)
    def gen_vids(self):
        ret = {}
        for i in range(self.replicas):
            ret.setdefault(
                get_id(
                    '%s:%s_%d'%(self.host,self.port,i)
                    ),
                {'host':self.host,
                 'port':self.port,
                 'replicas':i,
                }
            )
        return ret
    def init_htable(self):
        ret = {}
        for i in self.vids:
            ret.setdefault(i, HashTable())
            

    # we use http(json) to get/post data
    @rept_decorator(3)
    def _request(self, host, port, data):
        try:
            url = 'http://%s:%s/%s' % (host, port, 'announce')
            data = json.dumps(data)
            ret = urllib2.urlopen(url, data)
            return json.load(ret)
        except:
            return False

    def updateLastSeen(self, vid, key, tnode):
        hashtable = self.hashtables[vid] 
        if hashtable[key] and hashtable[key]['id'] == tnode["id"]:
            pass
        else:
            hashtable[key] = tnode
        hashtable[key]['time'] = time.time()
        
    def msgFailed(self):
        self.find_node(server, nid)
    
    def ping(self, vid, key, tnode):
        """
        ping Query = {"t":"aa", "y":"q", "q":"ping", "a":{"id":"abcdefghij0123456789"}}
        bencoded = d1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe
        Response = {"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}
        bencoded = d1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re
        """
        host = tnode["host"]
        port = tnode["port"]
        tid = tnode["id"]
        data = {
            "type": "ping",
            "me": {
                "id": vid,
                "info": self.vids[vid]
                },
            "you": tid
        }
        ret = self._request(host, port, data)
        if ret and ret["code"] == 0:
            self.updateLastSeen(tnode)
        else:
            self.msgFailed(key, tnode)
            
    def find_node(self, vid, key):
        """
        find_node Query = {"t":"aa", "y":"q", "q":"find_node", "a": {"id":"abcdefghij0123456789", "target":"mnopqrstuvwxyz123456"}}
        bencoded = d1:ad2:id20:abcdefghij01234567896:target20:mnopqrstuvwxyz123456e1:q9:find_node1:t2:aa1:y1:qe
        Response = {"t":"aa", "y":"r", "r": {"id":"0123456789abcdefghij", "nodes": "def456..."}}
        bencoded = d1:rd2:id20:0123456789abcdefghij5:nodes9:def456...e1:t2:aa1:y1:re
        """
        
    
    def mark_failed(self, vid, key, tnode):
        """
        @func: callback with mark failed vnode
        """
        hashtable = self.hashtables[vid] 
        
            
    # p2p
    def search_info_hash(self, info_hash):
        """
        查找info_hash,
        get? ==> test_conn()==>inside/httpserver ==> add? ==> update(peers)
             ==> None ==> return 404
        GET /announce?peer_id=aaaaaaaaaaaaaaaaaaaa&info_hash=aaaaaaaaaaaaaaaaaaaa
            &port=6881&left=0&downloaded=100&uploaded=0&compact=1
        """
        pass 
    def gen_info_hash(self, key):
        """
        根据文件生成info_hash: 上述torrent文件
        """
    
    # http://www.bittorrent.org/beps/bep_0005.html
    def get_peers():
        """
        get_peers Query = {"t":"aa", "y":"q", "q":"get_peers", "a": {"id":"abcdefghij0123456789", "info_hash":"mnopqrstuvwxyz123456"}}
bencoded = d1:ad2:id20:abcdefghij01234567899:info_hash20:mnopqrstuvwxyz123456e1:q9:get_peers1:t2:aa1:y1:qe
Response with peers = {"t":"aa", "y":"r", "r": {"id":"abcdefghij0123456789", "token":"aoeusnth", "values": ["axje.u", "idhtnm"]}}
bencoded = d1:rd2:id20:abcdefghij01234567895:token8:aoeusnth6:valuesl6:axje.u6:idhtnmee1:t2:aa1:y1:re
Response with closest nodes = {"t":"aa", "y":"r", "r": {"id":"abcdefghij0123456789", "token":"aoeusnth", "nodes": "def456..."}}
bencoded = d1:rd2:id20:abcdefghij01234567895:nodes9:def456...5:token8:aoeusnthe1:t2:aa1:y1:re
"""
        pass
    def announce_peer():
        """
        announce_peers Query = {"t":"aa", "y":"q", "q":"announce_peer", "a": {"id":"abcdefghij0123456789", "implied_port": 1, "info_hash":"mnopqrstuvwxyz123456", "port": 6881, "token": "aoeusnth"}}
        bencoded = d1:ad2:id20:abcdefghij01234567899:info_hash20:<br />
        mnopqrstuvwxyz1234564:porti6881e5:token8:aoeusnthe1:q13:announce_peer1:t2:aa1:y1:qe
        Response = {"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}
        bencoded = d1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re"""
        pass
    








def main():
    
    return True

class TestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(),True)
    
if __name__ == '__main__':
    #python -m xx.xx
    unittest.main()