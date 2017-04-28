#!/usr/bin/env python
#coding: utf-8
"""
@Author: COOl (1258626769@qq.com)
@Ctime: 2017年04月28日 15时45分48秒
@Latest: 2017年04月28日 15时45分48秒
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

class HashNet():
    """
    @func: khashmir.knet, do simulate network of nodes
    """
    pass


def main():
    
    return True

class TestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(),True)
    
if __name__ == '__main__':
    #python -m xx.xx
    unittest.main()