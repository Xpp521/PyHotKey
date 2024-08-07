# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2024 Xpp521
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
Platform stuff.
"""
from sys import platform

if 'win32' == platform:
    from .win32 import Key, KeyCode, Controller, Listener, pre_process_key, filter_name, event_filter
elif 'darwin' == platform:
    from .darwin import Key, KeyCode, Controller, Listener, pre_process_key, filter_name, event_filter
else:
    try:
        from .xorg import Key, KeyCode, Controller, Listener, pre_process_key, filter_name, event_filter
    except ImportError:
        raise
if not all([Key, KeyCode, Controller, Listener, pre_process_key, event_filter]):
    raise ImportError('Unsupported platform')
