#!/usr/bin/env python
#coding: utf-8
"""
@Author: COOl (1258626769@qq.com)
@Ctime: 2017年04月13日 14时13分39秒
@Latest: 2017年04月13日 14时13分39秒
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

"""
@ref: http://seanjoflynn.com/research/bittorrent.html

sudo pip install bencode.py
import bencode
bencode.bdecode(open('The Unforseeable Fate Of Mr. Jones.torrent','rb').read())
# torrent文件
{'announce': 'http://tracker.bundles.bittorrent.com/announce',
 'announce-list': [['http://tracker.bundles.bittorrent.com/announce'],
  ['udp://tracker.publicbt.com:80/announce',
   'udp://tracker.openbittorrent.com:80/announce']],
 'creation date': 1449085733,
 'info': {'collections': ['com.bittorrent.bundles.5654f27000d41d03001b6fab'],
# length或files的关键字，这两个关键字只能出现一个。如果是length，那么表示要下载的仅仅是单个文件，如果是files那么要下载的是一个目录中的多个文件。 如果是单个文件，那么length是该文件的长度。
  'files': [{'length': 1860, 'path': ["00_What's-Inside.html"]},
   {'length': 92700, 'path': ['background.jpg']},
   {'length': 28627, 'path': ['cover.jpg']},
   {'length': 12606611, 'path': ['The Unforeseeable Fate Of Mr. Jones.mp3']},
   {'length': 767452, 'path': ['FTP-MADLIB-edit.pdf']}],
  'name': 'The Unforseeable Fate Of Mr. Jones',
  'originator': '0\x82\x03:0\x82\x02"\x02\x01\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000L1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x0b0\t\x06\x03U\x04\x08\x13\x02CA1\x170\x15\x06\x03U\x04\n\x13\x0eBitTorrent Inc1\x170\x15\x06\x03U\x04\x03\x13\x0ecom.bittorrent0\x1e\x17\r140520235304Z\x17\r160509235304Z0z1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x0b0\t\x06\x03U\x04\x08\x0c\x02CA1\x170\x15\x06\x03U\x04\n\x0c\x0eBitTorrent Inc1\x1f0\x1d\x06\x03U\x04\x03\x0c\x16com.bittorrent.bundles1$0"\x06\t*\x86H\x86\xf7\r\x01\t\x01\x16\x15neteng@bittorrent.com0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xdc\x88\x0ePoR--\xadlr\xdf\xdb*\xf7u\xb2\xac\xe2-m\xb0y\xc5K\x0f\x84\xaf\xedj\xe9\xad\x88:\x00\xe8VK\xef\xce\xf1\r\x83\xb6\x0c\xb9n\xdf\xc2X\xae,\xbdOf\xb2j*l~\xaeO\xc6V\x81\x04\x03\x11R\x12\x03t\x02\xda\xc7\x1d\xb1\x1b\xe8\xed\x88Z\xcc|\xb5\xc0IZuY\x1b\x9c\x93\xde\xa1\xe1\xadFR\xc6\x1d\xbd\x80\xf6\xc1zV\xa2\x8c\xa2\xd90\x06\xe1.\xc2\xc3e\x15\xfc,5ki\xa8\x87i\xbe[\xb4`\xc9-\x81\x81w\x1d\x811\xb4y\x97\xda\x81L\xe6\xces\x9b\xd0\x7f\x9e\x93\xffZ/\xe2R\x8fIP4&=ia^\xe9\x9c\xbf{\xc3\xce\xf3\x9a\x06\x04\xf0I\x11\xfb\xc1\xb9U8v:\xad87\x9a\xeb\xad\x1d\x90\xa7\xeb#\xce\x81PPXct\x80\'\x8dv,Y}|\x1b\xb3F\xe1\xeb\x85\xd2Y\xe7\x9f\x8c\xb1y\xa2\xeb\xd2\x9aU\x8b\xc2\x05\xf3zpQ\xf4\xd4\x18$\xc1\xc2\xfc{1J\x1f\x8c\xa7\x0efM,\'\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00\x1e}\xb1\x9f\x8e\x07L\xaa\xd2\xb5\xe0eR\xe9\xfb\x18t\xf7rJn~\xe5%\xc1\x8d\xa1\xa5>\xbe#Q\xed\x17x\xa4B\x83M\x1eg\xef\x1dbt\t\xcc\xd7\xca\x10\xb2\xad_\x02\x07#\x08g7\xae\xf3"\xc9\xd5v:#)?e\x98\xd4\xe6\xd2@u\x7f\xbac\xf7"\xa4]\x81k\xca-\xe3\x08\x18\x8e$\xf3c\xa0\xd4\xd3\xf6**\xf4\xe2\xe1W|f\xea\xfd\xb7\x12E\xa3D\xa2+.`\xb3V\x04.!H\xeb\xcet\x84\x08\xfc\xde\x1c\x85\x1e\xdf\x04n2?\x03\xdc\xd35\x10S9\xd1\x8d\x92\x9c)#\xfd8\x97\xe5\x87\x0c\xe7\xc7\xcf\x8a\x91\xef9H\x83\xecaK_e9_\xf9\xef\xd3q\x03\x05\x13\xb6\'\x8f\xb3\x1c\x03[\x99\xa5T\x84I\xcc\xdb\xdc^\x05S%\x85\x17!\xc6\xaa\xa6\xc0\x0f\xff%\xcf\xf3\x10]\xc0Q\x94]\xbfD\xc3\xf9\xb5s\xe6\x99\xa2\xa3\xf0\xb0#\xa9_\xbbze\xe1\xc9\xc9\xe8I\xdb\xd8\xbe\tB\xa6\xecQ\x87\xca\x0c\xe2\x8e%\xd8\xcc',
# 片断的大小
  'piece length': 262144,
# 一个长度为20的整数倍的字符串。它将再被分隔为20字节长的字符串，每个子串都是相应片断的hash值
  'pieces': '\x16\xcbed+\xe8\xe1\t\x83#`4g\xc4Y\xa1\x87Rwg\xe1\x07s\xa1{\xf3\xc4\x91\x03\x0c\xeb\xa6\xbehe\xd5\xa7\xa8\x0f\xef\x16\xb4\x17K\xd8\x95\x8cdNI\x06\xdf\xdc1*\xe2\x19\xec>\x14\xfc\x0f\xa73\x1f\xc96L\xe4\xa3|W2T\xd5\x1a\xba\xda\xc6\xf1O\x80M\x94\x90}\xa4\xc8\xe92\xf5\xa3=\x0c\x95U\xf4\xc9@6\x00\x9c\x8e\t\xc5\x1d\x0ct\x95\xd8\xe6\x95\x9b\x16\x12,\x82:\x16\xb5\xa2\x1d\xf1\x935e\xb1\x93$(\xc0\x11\xfd\xd4G\xc8b\x94o.\xc5J?D\t\xee\x88\xa8\x0e\xfa.q,`\xb1\xe1\xe1j\xd7\x92\xa9\x06\x17D\x8b\xfa\xf6\xa8El\n\x05\xeb\xdf&.m9Vq\xednI\x0c\xaa\xfc\x11a{\xd9\x8be\xdc\xd9\x046\xe5\xdb\xfc\x80\n\xe6\x89\x1d\x98U\x07s\xa2\xbe;e\xb8\n\x08#\xf7*\xa4\xca\xa3\xcf[\xb2iE\xd9\xd1Y)\xf2\xc9\xa0\xd1\x97g\xdbsT\x14\xe6\xbcT\xc02\x12\xce%\xed\xb9\xadD\xfa\xa3\xc5\xb0\x10\x0f\x85rz6\xc9z\xbezI8^3="\xfa\xedq\x08B\x82\x94\x8f\xb0f*\xa6@\x99Bf\xfc\x14V\xb7y+\xf4\xbd\x9c\xef\x03\xdc\xab\xab\xd2\xb0\x85%\xc0M\x88\x8c\x1c\xfa\r\xdaL\xf2\xc0b\r\xc7@\xb7I\xb5i\xf1U\xfbc\x99\xcb\xdc\xa5\x82\x98e\xfag\xd4\x91\xa0s\xd9\x93\xf1\x7f,3n\xb8\x91\xf7\xd2\'\x94\xa7\x8dM\x162\xc6_\xe6\xf7!\xabE\x10\x9d\xbcHb\x87\x13T\x14\xc4\xe5\x14\tc@\xb6\x16\x1f]\xd6\x98\xb7+\xb6\xef\xff\xe3T%\xdf\xce\xbd_y\xa6>\xa2\xb4\x1dSP\x89\xc8\xe2\xea\x98\xd0\x15\x96^\xfd\r\xd3\xc5\r\xb5*\x8dE\x8b\xae\x0f\xc5\xd5\tl\x8f#`\xf5\xe16\xcf\xb8\n\x0c\xa3\r\xae4\xb6Y\x7f\x81n\x0b\x00$\x06&\x9e.m{1(\x07\xd2\xde\x89\xa9\xe00\x03\xf9\xce\x06\xe0\xeb\xbd\x9e^\x01\xb4\xe2\x94j\x84\xdc\x1e\xa9*}\x84^\x81V\x17\x08\x08\rbYP\xf2\xb9w\x1el\x82\rF\x088\xc5\xd5|p\x91\xd1\xf6\x0e\x89\xe0\xf2ac\xf2\xee\xab&\'Olu\xf3\xdf\xc5\x12\xfb\x00\xb0) \x115G\xf8\x0c\\A;\xd3(c\x96Q\x1bK&\x0e\xa0Sh\xe9B\xab\xc3\xc5\xde\xc4\xa6A\x81\x9e\xb3\x1b\x0c\xbc\x80\xe8\x10\xa8\x11\xd2 \x8e\xb0v\xd3\xa6\xefE\x99\xe5\xf7tI\x94`T\xb1\xfe,6~\xbcM;5M\xf7\xe4*\\.bv\xf6\x18[\x92\xa3\xe4\x9d\xbeQ\xd0OM\\!\x84\xc7\xf9j\xb9\x1d\x90\xc8\x0c\xceE\xaa\x17\xe21\xb1IqnIV\x8f@]\x1c\xa7\n\xc8\x9c\xfb\x0e\x16\xebZM\xe4z\x9aJe\x9f,\nO\x1b\xfd\xd4\xf4V\xe35\xe3\xfb\xb8\x15\x15S\xb0\xb8\x15k\x7f<\xcb\xc0\x93\xe3\xf06\xef\x1cqf\x1c\x1e\xf0\x13\x11O6\xef\xb7\xddKI\x9d\xbe\xa1\x12\x106\x1a0\x8d\xea7\xdb\x9c\x1c\xfd\xb6\xe2+3\x9c1;I\x95\xbeW\x8b\xe9\xf0\\\xf6r_\'\x97\xf6\x7f\x1c\xc0\xe15\x8e\x975<\xdb\x89=\xa5\xb55i\xc2\x9chR\xee\x82\x1a\x02%_rv\xbe\xf7k\xf3z>q\x9d\xe1}\xdd\x05R\xd6U\x19\xed\xa0\xa1\xf82\xef\xff\x81\x10#\x90`4\xe0\x88w&*\xcf\xbc\xe0\xab\xc1\xe5,\xb1\xa7\xee\xe6"\x9f\x91\xce#\xebZ\xd3{\x1afwk\xb25\xf4\x88e\xe1\x17\xe9\xef\x8e\x96\xa5\xa8\x8eY\x8bP\xc8C\x93\xa2\x0cU\x9d;\x9fq\xb4\xb3\xc3\xa4Y\x8bp\x02\x91\xfc\x96\xaeM\x9at\x01kb\xd8\xd6py\x1bO<KI\x81YZ)\x0e6\x10do\x0e\xb2bo\xdc>*}\xeeBwP\x84\xf3\'j\xd7\xe1)\xe9\x11\xbc\x00Q\xa8e\xec\x1cC\x00G/E\xa2\x04}\x0c\x1c\x045:\xbcq\n\xc1L\xc3\xd2*\xf7\nK\xd3\xce\xd7*5\xafYS\xcc-\xd1`\xf3\xb4\xfe\xadSd\xbc\xc31\xc2iz\xda2.\xb5\xb2~\xc7y\xf2\xbd\xb6\x9f\n\xc3\xd2y\x90\xbb\xcc\x16KN#\xd7\xb51\xbd\x14\x98\xf4\xc9\x15\xe6U\x0fk\x95\x8et\xf0\x07eAh\x9d\xb1q\x9c\x9fy\xca=\xe7\x9cv\x1e&\xa6\x91\x14\x87\x9fu\xfd\x06'},
 'signatures': {'com.bittorrent.bundles': {'certificate': '0\x82\x03:0\x82\x02"\x02\x01\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x000L1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x0b0\t\x06\x03U\x04\x08\x13\x02CA1\x170\x15\x06\x03U\x04\n\x13\x0eBitTorrent Inc1\x170\x15\x06\x03U\x04\x03\x13\x0ecom.bittorrent0\x1e\x17\r140520235304Z\x17\r160509235304Z0z1\x0b0\t\x06\x03U\x04\x06\x13\x02US1\x0b0\t\x06\x03U\x04\x08\x0c\x02CA1\x170\x15\x06\x03U\x04\n\x0c\x0eBitTorrent Inc1\x1f0\x1d\x06\x03U\x04\x03\x0c\x16com.bittorrent.bundles1$0"\x06\t*\x86H\x86\xf7\r\x01\t\x01\x16\x15neteng@bittorrent.com0\x82\x01"0\r\x06\t*\x86H\x86\xf7\r\x01\x01\x01\x05\x00\x03\x82\x01\x0f\x000\x82\x01\n\x02\x82\x01\x01\x00\xdc\x88\x0ePoR--\xadlr\xdf\xdb*\xf7u\xb2\xac\xe2-m\xb0y\xc5K\x0f\x84\xaf\xedj\xe9\xad\x88:\x00\xe8VK\xef\xce\xf1\r\x83\xb6\x0c\xb9n\xdf\xc2X\xae,\xbdOf\xb2j*l~\xaeO\xc6V\x81\x04\x03\x11R\x12\x03t\x02\xda\xc7\x1d\xb1\x1b\xe8\xed\x88Z\xcc|\xb5\xc0IZuY\x1b\x9c\x93\xde\xa1\xe1\xadFR\xc6\x1d\xbd\x80\xf6\xc1zV\xa2\x8c\xa2\xd90\x06\xe1.\xc2\xc3e\x15\xfc,5ki\xa8\x87i\xbe[\xb4`\xc9-\x81\x81w\x1d\x811\xb4y\x97\xda\x81L\xe6\xces\x9b\xd0\x7f\x9e\x93\xffZ/\xe2R\x8fIP4&=ia^\xe9\x9c\xbf{\xc3\xce\xf3\x9a\x06\x04\xf0I\x11\xfb\xc1\xb9U8v:\xad87\x9a\xeb\xad\x1d\x90\xa7\xeb#\xce\x81PPXct\x80\'\x8dv,Y}|\x1b\xb3F\xe1\xeb\x85\xd2Y\xe7\x9f\x8c\xb1y\xa2\xeb\xd2\x9aU\x8b\xc2\x05\xf3zpQ\xf4\xd4\x18$\xc1\xc2\xfc{1J\x1f\x8c\xa7\x0efM,\'\x02\x03\x01\x00\x010\r\x06\t*\x86H\x86\xf7\r\x01\x01\x05\x05\x00\x03\x82\x01\x01\x00\x1e}\xb1\x9f\x8e\x07L\xaa\xd2\xb5\xe0eR\xe9\xfb\x18t\xf7rJn~\xe5%\xc1\x8d\xa1\xa5>\xbe#Q\xed\x17x\xa4B\x83M\x1eg\xef\x1dbt\t\xcc\xd7\xca\x10\xb2\xad_\x02\x07#\x08g7\xae\xf3"\xc9\xd5v:#)?e\x98\xd4\xe6\xd2@u\x7f\xbac\xf7"\xa4]\x81k\xca-\xe3\x08\x18\x8e$\xf3c\xa0\xd4\xd3\xf6**\xf4\xe2\xe1W|f\xea\xfd\xb7\x12E\xa3D\xa2+.`\xb3V\x04.!H\xeb\xcet\x84\x08\xfc\xde\x1c\x85\x1e\xdf\x04n2?\x03\xdc\xd35\x10S9\xd1\x8d\x92\x9c)#\xfd8\x97\xe5\x87\x0c\xe7\xc7\xcf\x8a\x91\xef9H\x83\xecaK_e9_\xf9\xef\xd3q\x03\x05\x13\xb6\'\x8f\xb3\x1c\x03[\x99\xa5T\x84I\xcc\xdb\xdc^\x05S%\x85\x17!\xc6\xaa\xa6\xc0\x0f\xff%\xcf\xf3\x10]\xc0Q\x94]\xbfD\xc3\xf9\xb5s\xe6\x99\xa2\xa3\xf0\xb0#\xa9_\xbbze\xe1\xc9\xc9\xe8I\xdb\xd8\xbe\tB\xa6\xecQ\x87\xca\x0c\xe2\x8e%\xd8\xcc',
   'signature': '\x9e\x81\xed\x88\xed\x1d<\x93wG\xc3;\xd0\xd8\x7fX\xb4\x8c7`\x86\xe4\xc0\x91VG\xee\xedANG&\xea\xb58G\xb8,~S\xff\x84sK\xad\xebPy\xd9\x1b$Kj\xc8\xf6=\x10\xd2c\xa7\xab%\x91\xa8,)\xc6o\x97\xc6Q8\x81\xb9\xe0\xde\xf5A\xfbF\x82&Qb\xcb\x93\'3\x8d\x9f\x1b\x0c\tC\xda\r\xc0:M\xa2(\xe48j\xfe\xb4\x8d\xdd\x01G\x19\xc9\xb3]\xfd\xef\xf6\x9cB\x94\'\xe8\x8a\x8f\x18p\xbfV\xa2[>\xf9\t)`\xc6\xdb\x06\x1eV9\xed\xbc\xb7\xacW:E\xf6\xd1\xa8Ra\x1f\xe3T\xce\xfaD\xed\x95\xbf\xdfvxw\xdaW\xc1\xb7h\xb9G\x85\x131\xad\x8b]2t\x19$I\x14\xcd1\xd4\xdcTc\x0fN+\xb4\x87"JF\x81,\xf4\xbe?,\xe6t\x19\xf9\xe3\xd7\x9e\xcf\xf4\x94\xdf\xf7\x01\xea3\xd41\'\xc9\x89\x02\xff\x0b\xe1\xbe\xe9eq\xbe \xb9y?\x89\xcd\x8a&\x18X\xeaz\xe8\xe9\xc8\x07Q\xb7m\xb2\x82V'}},
 'url-list': ['http://s3.amazonaws.com/content-bundles/production-df0ec56d-0fbb-bc2c-11e7-354ff3af9c4e/0aed07388ff765f43c4c173bc44ce40b7385f138c3bf8a452f38d844f5f29b1f/originals/']}


# 请求tracker
In [33]: urllib.urlencode({"a": c["info"]["pieces"][:20]})
Out[33]: 'a=%16%CBed%2B%E8%E1%09%83%23%604g%C4Y%A1%87Rwg'

curl -v "http://tracker.bundles.bittorrent.com/announce?info_hash=%16%CBed%2B%E8%E1%09%83%23%604g%C4Y%A1%87Rwg&
peer_id=76433642664923430920&
port=56723&
uploaded=0&
downloaded=0&
left=0&
# the current state of the client. Either started, paused or stopped
# These let the tracker know whether to add or remove us from its list of peers.
event=started&
# either 0 or 1 indicating whether or not to return a compact peer list.
compact=1"


curl -v "http://tracker.bundles.bittorrent.com/announce?info_hash=%16%CBed%2B%E8%E1%09%83%23%604g%C4Y%A1%87Rwg&peer_id=YT%A7%28c%DD%3F%D1%96Z%07%8E%00z%3F5%5C%2Fu%89&port=56723&uploaded=0&downloaded=0&left=0&event=started&compact=1"
*   Trying 23.23.109.78...
* TCP_NODELAY set
* Connected to tracker.bundles.bittorrent.com (23.23.109.78) port 80 (#0)
> GET /announce?info_hash=%16%CBed%2B%E8%E1%09%83%23%604g%C4Y%A1%87Rwg&peer_id=76433642664923430920&port=56723&uploaded=0&downloaded=0&left=0&event=started&compact=1 HTTP/1.1
> Host: tracker.bundles.bittorrent.com
> User-Agent: curl/7.52.1
> Accept: */*
> 
< HTTP/1.1 302 Moved Temporarily
< Server: Cowboy
< Connection: keep-alive
< Location: http://54.173.144.112/announce?info_hash=%16%CBed%2B%E8%E1%09%83%23%604g%C4Y%A1%87Rwg&peer_id=76433642664923430920&port=56723&uploaded=0&downloaded=0&left=0&event=started&compact=1
< Vary: Accept
< Content-Type: text/plain; charset=utf-8
< Content-Length: 238
< Date: Thu, 13 Apr 2017 10:15:56 GMT
< Via: 1.1 vegur
< 
* Curl_http_done: called premature == 0
* Connection #0 to host tracker.bundles.bittorrent.com left intact
Moved Temporarily. Redirecting to http://54.173.144.112/announce?info_hash=%2516%25CBed%252B%25E8%25E1%2509%2583%2523%25604g%25C4Y%25A1%2587Rwg&peer_id=S58B-----664923430920&port=56723&uploaded=0&downloaded=0&left=0&event=started&compact=1

d14:failure reason63:Requested download is not authorized for use with this tracker.e
# http://www.bittorrent.org/beps/bep_0020.html
peer_id
http://54.173.144.112/announce?info_hash=%2516%25CBed%252B%25E8%25E1%2509%2583%2523%25604g%25C4Y%25A1%2587Rwg&peer_id=-AZ2200-6wfG2wk6wWLc&port=56723&uploaded=0&downloaded=0&left=0&event=started&compact=1

# d8:completei2e10:downloadedi0e10:incompletei1e8:intervali1769e12:min intervali884e5:peers18:??J??Jݓ??J??e
complete: the number of peers with the complete file
downloaded: I couldn't find any documentation for this
incomplete: the number of peers without the complete file (leechers)
interval: frequency the client should request an updated peer list from the tracker
min interval: (optional) minimum frequency the client should request an updated peer list
peers: with the compact option specified, this is a byte[]. Every 6 bytes is a peer – the first four are the four numbers in an IPv4 address and the last two are a big endian char representing the port number.
"""



"""
已完成: task分发
待完成: # task分层发送(routing), #可先指定源为DHT tracker 
       #
待定:  # 回源逻辑(socket代理?直接); ==> 1. http # do like aliyun(callback/for)  2. p2p # 分片下载
      # 请求介质所需信息(sha1?path?) ==> DHT tracker and store in redis
      # 
      
      
P2P-DHT: http://www.bittorrent.org/beps/bep_0005.html
第一步 DHT, khashmir
第二步 p2p
"""
from hashlib import sha1
def get_id(*args):
    h = sha1()
    h.update( ''.join([ str(i) for i in args]) )
    return h.hexdigest()    


class Node(object):
    def __init__():
        self.host = ''
        self.port = ''
        self.id = get_hash_id(self.host,self.port)
        self.nodes = {}
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
    def ping():
        """
        ping Query = {"t":"aa", "y":"q", "q":"ping", "a":{"id":"abcdefghij0123456789"}}
        bencoded = d1:ad2:id20:abcdefghij0123456789e1:q4:ping1:t2:aa1:y1:qe
        Response = {"t":"aa", "y":"r", "r": {"id":"mnopqrstuvwxyz123456"}}
        bencoded = d1:rd2:id20:mnopqrstuvwxyz123456e1:t2:aa1:y1:re
        """
        pass
    def find_node(self, server, nid):
        """
        find_node Query = {"t":"aa", "y":"q", "q":"find_node", "a": {"id":"abcdefghij0123456789", "target":"mnopqrstuvwxyz123456"}}
        bencoded = d1:ad2:id20:abcdefghij01234567896:target20:mnopqrstuvwxyz123456e1:q9:find_node1:t2:aa1:y1:qe
        Response = {"t":"aa", "y":"r", "r": {"id":"0123456789abcdefghij", "nodes": "def456..."}}
        bencoded = d1:rd2:id20:0123456789abcdefghij5:nodes9:def456...e1:t2:aa1:y1:re
        """
        """
        @func: ref: khashmir(折半查找,网络消耗>>>CPU消耗)
               ring = [1,2,.......n] #max f*20 
               avg = hextoint('f'*20)//length
               1: dis(ring[0], vkey) ? avg
                   >) : avg = avg                && n= dis(ring[0], vkey)/ 
                   <=): avg = dis(ring[0], vkey) &&
               2: n ? len(ring)
         """
        if not self.ring: return -1
        length = len(self.ring)
        if length == 1: return self.ring[0]
        avg = hextoint('f'*20)//length
        dis = dist(vkey, self.ring[0])
        if not dis:
            return self.get_node(self.ring[0])
        else:
            i = dis // avg + 1
            ckey = self.ring[i]
            dis = dist(vkey,)
            if not dis:
                return self.get_node(ckey)
            elif vkey > ckey:
                ranges = range(i+1, length)
            else:
                ranges = range(i).reverse()
    
            for i in ranges:
                pass

    
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
    
    # we use http(json) to get/post data
    def _request(self, ip, port, data):
        try:
            url = 'http://%s:%s/%s' % (ip, port, 'announce')
            data = json.dumps(data)
            ret = urllib2.urlopen(url, data)
            return json.load(ret)
        except:
            return False













def main():

    return True

class TestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(),True)

if __name__ == '__main__':
    #python -m xx.xx
    import six
    six.str
    a='中'
    print(type(a))
    print(type(a.encode('utf-8')))    
    unittest.main()
