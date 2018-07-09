from tornado.web import UIModule
from tornado import escape
from tornado import template
class import_html(UIModule):
    def render(self, html,**kwargs):
        loader = template.Loader("templates")
        kwargs = {

        }
        return loader.load(html).generate(err='err msg')

class fghj(UIModule):

    def render(self, *args, **kwargs):
        return [1,2,3,4,5]