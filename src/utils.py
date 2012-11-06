#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012 smallevilbeast
#
# Author:     smallevilbeast <houshao55@gmail.com>
# Maintainer: smallevilbeast <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
import string
import urllib
import random
import urllib2
import threading

try:
    import simplejson as json
except ImportError:    
    import json
    
    

from xdg import get_cache_file
from logger import newLogger

logger  = newLogger("utils")

DEFAULT_TIMEOUT = 10

def timestamp():
    return int(time.time() * 1000)

def get_parent_dir(filepath, level=1):
    '''Get parent dir.'''
    parent_dir = os.path.realpath(filepath)
    
    while(level > 0):
        parent_dir = os.path.dirname(parent_dir)
        level -= 1
    
    return parent_dir

def get_random_t():
    return random.random()

def radix(n, base=36):
    digits = string.digits + string.lowercase
    def short_div(n, acc=list()):
        q, r = divmod(n, base)
        return [r] + acc if q == 0 else short_div(q, [r] + acc)
    return ''.join(digits[i] for i in short_div(n))

def timechecksum():
    return radix(timestamp())

def quote(s):
    if isinstance(s, unicode):
        s = s.encode("gbk")
    else:    
        s = unicode(s, "utf-8").encode("gbk")
    return urllib.quote(s)    

def unquote(s):
    return urllib.unquote(s)

def get_cookie_file():
    return get_cache_file("cookie.txt")


def parser_json(raw):
    try:
        data = json.loads(raw)
    except:    
        try:
            data = eval(raw, type("Dummy", (dict,), dict(__getitem__=lambda s,n: n))())
        except:    
            data = {}
    return data    

def download(remote_uri, local_uri, buffer_len=4096, timeout=DEFAULT_TIMEOUT):
    try:
        logger.logdebug("download %s starting...", remote_uri)
        handle_read = urllib2.urlopen(remote_uri, timeout=timeout)
        handle_write = open(local_uri, "w")
        
        data = handle_read.read(buffer_len)
        handle_write.write(data)
        
        while data:
            data = handle_read.read(buffer_len)
            handle_write.write(data)
            
        handle_read.close()    
        handle_write.close()
        logger.logdebug("download %s finish." % remote_uri)
    except Exception, e:
        logger.loginfo("Error while downloading %s, %s", remote_uri, e)
        try:
            os.unlink(local_uri)
        except:    
            pass
        return False
    if not os.path.exists(local_uri):
        return False
    return True
