#  -*- coding: utf-8 -*-
# *****************************************************************************
# NICOS, the Networked Instrument Control System of the FRM-II
# Copyright (c) 2009-2012 by the NICOS contributors (see AUTHORS)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#   Georg Brandl <georg.brandl@frm2.tum.de>
#
# *****************************************************************************

"""NICOS cache protocol support."""

import re
import cPickle as pickle
from ast import parse, Str, Num, Tuple, List, Dict, BinOp, UnaryOp, \
     Add, Sub, USub, Name, Call
from base64 import b64encode, b64decode


DEFAULT_CACHE_PORT = 14869

OP_TELL = '='
OP_ASK = '?'
OP_WILDCARD = '*'
OP_SUBSCRIBE = ':'
OP_TELLOLD = '!'
OP_LOCK = '$'
OP_REWRITE = '~'

# put flags between key and op...
FLAG_NO_STORE = '#'

# regular expression matching a cache protocol message
msg_pattern = re.compile(r'''
    ^ (?:
      \s* (?P<time>\d+\.?\d*)?                   # timestamp
      \s* (?P<ttlop>[+-]?)                       # ttl operator
      \s* (?P<ttl>\d+\.?\d*(?:[eE][+-]?\d+)?)?   # ttl
      \s* (?P<tsop>@)                            # timestamp mark
    )?
    \s* (?P<key>[^=!?:*$]*?)                     # key
    \s* (?P<op>[=!?:*$~])                        # operator
    \s* (?P<value>[^\r\n]*?)                     # value
    \s* $
    ''', re.X)

line_pattern = re.compile(r'([^\r\n]*)\r?\n')


# PyON -- "Python object notation"

def cache_dump(obj):
    res = []
    if isinstance(obj, (int, long, bool, float, str, unicode)):
        res.append(repr(obj))
    elif isinstance(obj, list):
        res.append('[')
        for item in obj:
            res.append(cache_dump(item))
            res.append(',')
        res.append(']')
    elif isinstance(obj, tuple):
        res.append('(')
        for item in obj:
            res.append(cache_dump(item))
            res.append(',')
        res.append(')')
    elif isinstance(obj, dict):
        res.append('{')
        for key, value in obj.iteritems():
            res.append(cache_dump(key))
            res.append(':')
            res.append(cache_dump(value))
            res.append(',')
        res.append('}')
    elif obj is None:
        return 'None'
    else:
        try:
            resstr = 'cache_unpickle("' + \
                     b64encode(pickle.dumps(obj, protocol=0)) + '")'
            res.append(resstr)
        except Exception, err:
            raise ValueError('unserializable object: %r (%s)' % (obj, err))
    return ''.join(res)

_safe_names = {'None': None, 'True': True, 'False': False,
               'inf': float('inf'), 'nan': float('nan')}

def ast_eval(node):
    # copied from Python 2.7 ast.py, but added support for float inf/-inf/nan
    def _convert(node):
        if isinstance(node, Str):
            return node.s
        elif isinstance(node, Num):
            return node.n
        elif isinstance(node, Tuple):
            return tuple(map(_convert, node.elts))
        elif isinstance(node, List):
            return list(map(_convert, node.elts))
        elif isinstance(node, Dict):
            return dict((_convert(k), _convert(v)) for k, v
                        in zip(node.keys, node.values))
        elif isinstance(node, Name):
            if node.id in _safe_names:
                return _safe_names[node.id]
        elif isinstance(node, UnaryOp) and \
             isinstance(node.op, USub) and \
             isinstance(node.operand, Name) and \
             node.operand.id in _safe_names:
            return -_safe_names[node.operand.id]
        elif isinstance(node, BinOp) and \
             isinstance(node.op, (Add, Sub)) and \
             isinstance(node.right, Num) and \
             isinstance(node.right.n, complex) and \
             isinstance(node.left, Num) and \
             isinstance(node.left.n, (int, long, float)):
            left = node.left.n
            right = node.right.n
            if isinstance(node.op, Add):
                return left + right
            else:
                return left - right
        raise ValueError('malformed literal string')
    return _convert(node)

def cache_load(entry):
    try:
        # parsing with 'eval' always gives an ast.Expression node
        expr = parse(entry, mode='eval').body
        if isinstance(expr, Call) and expr.func.id == 'cache_unpickle':
            return pickle.loads(b64decode(ast_eval(expr.args[0])))
        else:
            return ast_eval(expr)
    except Exception, err:
        raise ValueError('corrupt cache entry: %r (%s)' % (entry, err))
