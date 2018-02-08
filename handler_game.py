import tornado.web
import pyrestful.rest
import json
import jieba
import sys
import datetime
from database import dbHelper
import logging
from pyrestful.rest import get, post, put, delete
from pyrestful import mediatypes
import traceback
import ip2region.ip2Region
import gl
from tornado import gen
class PuzzleHandler(pyrestful.rest.RestHandler):
    @get(_path="/game")
    def index(self):
        self.render("game/puzzle.html")

    @get(_path="/game/puzzle")
    def puzzle(self):
        self.render("game/puzzle.html")

