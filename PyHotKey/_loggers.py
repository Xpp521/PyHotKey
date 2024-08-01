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
from ._info import NAME
from logging import DEBUG, getLogger, StreamHandler, Formatter


class DummyLogger:
    def trace(self, *args, **kwargs):
        pass

    def debug(self, *args, **kwargs):
        pass

    def info(self, *args, **kwargs):
        pass

    def success(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

    def critical(self, *args, **kwargs):
        pass

    def exception(self, *args, **kwargs):
        pass

    def log(self, *args, **kwargs):
        pass


def get_classic_logger(name):
    logger = getLogger(name)
    formatter = Formatter('[%(asctime)s]%(message)s')
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(DEBUG)
    return logger


dummy_logger = DummyLogger()
default_logger = get_classic_logger(NAME)
