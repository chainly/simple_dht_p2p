#!/usr/bin/env python
#coding: utf-8
"""
@Author: COOl (1258626769@qq.com)
@Ctime: 2017年04月28日 11时29分03秒
@Latest: 2017年04月28日 11时29分03秒
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

from .hashring import HashRing


class HashTable(dict):
    """
    @func: cache of node_id: host,port,replicas,time in khashmir.ktable
    @simple: n = len(hash)
             -16**(n-1): {id:[host,port,replicas]}
             .
             .
             -16: {id:{host,port,replicas,time}}
             -1: {id:{host,port,replicas,time}} #pre
             1: {id:{host,port,replicas,time}} #next
             16: {id:{host,port,replicas,time}}
             .
             .
             .
             16**(n-1): ...
    """
    hash_length = HashRing.hash_length
    def __init__(self, *args, **kwargs):
        super(HashTable, self).__init__(*args, **kwargs)
        for i in range(HashTable.hash_length):
            self.setdefault(16**i, None)
            self.setdefault(-16**i, None)

def main():
    import random
    ht = HashTable()
    print(16**(HashRing.hash_length -1))
    assert ht[1] == None
    assert ht[16**(HashRing.hash_length -1)] == None
    assert ht[-16**random.randint(0, HashRing.hash_length -1)] == None
    return ht[16**random.randint(0, HashRing.hash_length -1)] == None

class TestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(),True)
    
if __name__ == '__main__':
    #python -m xx.xx
    unittest.main()