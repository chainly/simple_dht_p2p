#!/usr/bin/env python
#coding: utf-8
"""
@Author: COOl (1258626769@qq.com)
@Ctime: 2017年04月14日 10时54分06秒
@Latest: 2017-04-26 18:06:30
@Purpose: Hash_Ring


"""
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys, re, time, datetime, traceback, logging, json

from hashlib import sha1
def get_id(*args):
    h = sha1()
    h.update( ''.join([ str(i) for i in args]) )
    return h.hexdigest() 

from functools import wraps
"""
@w =  w(func) ==> inner
@w(xx) = w(xx)(func) ==> inner
"""
def update_ring(func):
    @wraps(func)
    def inner(*args, **kwargs):
        #assert hasattr(args[0], 'ring')
        #assert hasattr(args[0], 'nodes')  
        #assert hasattr(args[0].nodes, 'keys') 
        try:
            ret = func(*args, **kwargs)
        finally:
            try:
                args[0].ring = sorted(args[0].hnode.keys())
            except AttributeError:
                pass
        return ret
    return inner

#from khashmir.khash import intify, stringify, distance
def hextoint(hstring ):
    """
    'f' ==> 16
    """
    return int(hstring,16)
def inttohex(num):
    """
    16 ==> 'f'
    """
    ret = hex(num)
    return ret.endswith('L') and ret[2:-1] or ret[2:]
def dist(x, y):
    return abs(hextoint(x)-hextoint(y))

class HashRing(object):
    """
    @ref: django_redis.HashRing
    @q: pos ?
    @future: (***X: NOT_BEST_ENOUGH: use raid/or more HashRing***) backup rule:  nodes = = => [ (uuid(path), uuid(path)),... ] ==> ["node1", "node2"  ]
             add (del/add_gnode( maybe_not_allowed ); 
                  del/add_node( replace(_with)_redundancy(清空redundancy并同步?));
                  status(redundancy?);
                  __init__,首先检查ping?(path): use redundancy to replace the invalid()
                  )
    """
    hash_length = 20
    def __init__(self, nodes=None, replicas=128):
        """
        @func: consistent hashing 
        @parm: nodes real nodes; vnode for vir_node, key for hash
        @key: gnode  { hash: 'node|replicas' }#use dict for simple
        """
        self.hnode = {}
        self.ring = []
        self.replicas = replicas
        self.hash_length = HashRing.hash_length
        if not nodes:
            nodes = []
        
        for node in nodes:
            self.add_node(node)

    def gen_vnode(self, node):
        """
        @ret node|replicas
        """
        return ( '%s|%s'% (node, i) for i in xrange(self.replicas) )
    def retrieve_vnode(self, vnode):
        return vnode.rsplit('|',1)[0]
    @update_ring
    def add_node(self, node):
        for vnode in self.gen_vnode(node):
            # exists ignore, unless same hash for diff node
            self.hnode.setdefault(get_id(vnode), vnode)
    @update_ring   
    def remove_node(self, node):
        for vnode in self.gen_vnode(node):
            try:
                self.hnode.pop(get_id(vnode))        
            except KeyError:
                pass
    def get_vnode_name(self, key):
        return self.hnode[key]
    def get_node(self, key):
        return self.retrieve_vnode(self.hnode[key])
    def get_pos(self, node):
        return ( self.ring.index(get_id(i)) for i in self.gen_vnode(node) )
    def find_range(self, node):
        """
        @func: 按顺时针归属上个,查找[me, next)"""
        return ( [ self.ring[i],
                   hex(int( self.ring[ i-len(self.ring)+1 ],
                           16) -1)[2:-1] 
                ] for i in self.get_pos(node) )
    def find_node(self, vkey):
        """
        @func: ref: khashmir(折半查找,网络消耗>>>CPU消耗)
               ring = [1,2,.......n] #max f*20 
               avg = hextoint('f'*20)//length
               1: dis = dist(ring[0], vkey)
                  n= dis/avg
                  n旁边最可能
               2: khashmir(ring, n, vkey)
         """
        if not self.ring: return -1
        length = len(self.ring)
        if length == 1: return self.ring[0]
        avg = hextoint('f'*self.hash_length)//length
        dis = dist(vkey, self.ring[0])
        n = dis//avg
        if n >= length:
            if self.ring[-1] <= vkey:
                return self.get_vnode_name(self.ring[-1])
            else:
                return self.get_vnode_name(self._khashmir(self.ring, length-1, vkey))
        else:
            return self.get_vnode_name(self._khashmir(self.ring, n, vkey))
     
    def _khashmir(self, ring, n, vkey):
        len_max = len(ring) - 1
        for i in range(self.hash_length):
            # ring[n] =< vkey, 递加
            if vkey == ring[n]:
                return ring[n]
            if vkey > ring[n]:
                m = n + 16**i
                # ring[n] < vkey ? ring[n + 1]
                if i == 0:
                    if vkey < ring[m]:
                        return ring[n]
                    elif vkey == ring[m]:
                        return ring[m]
                    else:
                        continue
                # ring[ n+2**(i-1) ] < vkey ? ring[m]
                if m <= len_max:
                    if vkey < ring[m]:
                        return self._khashmir(ring[:], n+2**(i-1), vkey)
                    elif vkey == ring[m]:
                        return ring[m]
                    else:
                        continue
                # ring[n] < vkey ?  ring[len_max] 
                else:                    
                    if vkey < ring[len_max]:
                        return self._khashmir(ring[:], n+2**(i-1), vkey)
                    elif  ring[len_max] <= vkey <= 'f'*self.hash_length:
                        return ring[len_max]
                    else:
                        raise ValueError('overflow %s'%vkey)
                    
            # ring[n] > vkey, 递减                
            else:
                m = n - 2**i
                # ring[n] > vkey ? ring[n - 1]
                if i == 0:
                    if vkey >= ring[m]:
                        return ring[m]
                    else:
                        continue
                # ring[ n+2**(i-1) ] > vkey ? ring[m]
                if m >= 0:
                    if vkey < ring[m]:
                        return self._khashmir(ring[:], n-2**(i-1), vkey)
                    elif vkey == ring[m]:
                        return ring[m]
                    else:
                        continue
                # ring[n] > vkey ?  ring[0] 
                else:                    
                    if vkey > ring[0]:
                        return self._khashmir(ring[:], n-2**(i-1), vkey)
                    elif ring[0] == vkey:
                        return ring[0]
                    elif '0'*self.hash_length <= vkey < ring[0]:
                        return ring[-1]
                    else:
                        raise ValueError('bad value %s'%vkey)
                
import unittest
def test():
    nodes = ["/data1",
             "/data2",
             "/data3"]
    hr = HashRing(nodes,10)
    hr.add_node("/data3")
    assert len(hr.hnode) == 3*hr.replicas, '%r,%r'%(len(hr.hnode),len(hr.ring))
    hr.add_node("/data4")
    assert len(hr.hnode) == len(hr.ring), '%r,%r'%(len(hr.hnode),len(hr.ring))
    hr.remove_node("/data5")
    assert len(hr.hnode) == 4*hr.replicas, '%r,%r'%(len(hr.hnode),len(hr.ring))
    hr.remove_node("/data4")
    assert len(hr.hnode) == len(hr.ring), '%r,%r'%(len(hr.hnode),len(hr.ring))  
    print( '%r\n%r'%(hr.hnode, hr.ring) )
    #assert list(hr.find_range("/data2")) == [['8e591c5cf23529b4a2d78d96a47d93bb79ba488d', '9dd00df202ab2e79019a15b82af4f9fa385a746e']]
    print(hr.find_node('9dd00df202ab2e79019a15b82af4f9fa385a746e'))
    print(hr.find_node('0'*20))
    print(hr.find_node('88ae636fc74c5648ca138aa15961beffd85dc6ee'))
    return True

class TestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(test(),True)
    
if __name__ == '__main__':
    #python -m xx.xx
    unittest.main()            
        