from flask import current_app as app
from flask.ext.plugins import Plugin
#from flask.ext.plugins import PluginManager
__plugin__ = "QuestionEditor"

class QuestionEditor(Plugin):
    def setup(self):
        from .views import blueprint
        app.register_blueprint(blueprint, url_prefix="/project")
