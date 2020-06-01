import mapadroid.utils.pluginBase
from flask import render_template, Blueprint
from mapadroid.madmin.functions import auth_required
from mapadroid.mitm_receiver.MITMReceiver import MITMReceiver
import os


class MadPluginExample(mapadroid.utils.pluginBase.Plugin):
    """This plugin is just the identity function: it returns the argument
    """
    def __init__(self, mad):
        super().__init__(mad)

        self._rootdir = os.path.dirname(os.path.abspath(__file__))

        self._mad = mad

        self._pluginconfig.read(self._rootdir + "/plugin.ini")
        self.author = self._pluginconfig.get("plugin", "author", fallback="unknown")
        self.url = self._pluginconfig.get("plugin", "url", fallback="https://www.maddev.eu")
        self.description = self._pluginconfig.get("plugin", "description", fallback="unknown")
        self.version = self._pluginconfig.get("plugin", "version", fallback="unknown")
        self.pluginname = self._pluginconfig.get("plugin", "pluginname", fallback="https://www.maddev.eu")
        self.staticpath = self._rootdir + "/static/"
        self.templatepath = self._rootdir + "/template/"

        self._routes = [
            ("/example", self.example_route),
            ("/pluginfaq", self.pluginfaq),
        ]

        self._hotlink = [
            ("Plugin faq", "/pluginfaq", "Create own plugin - faq"),
            ("Plugin Example", "/example", "Testpage"),
        ]

        if self._pluginconfig.getboolean("plugin", "active", fallback=False):
            self._plugin = Blueprint(str(self.pluginname), __name__, static_folder=self.staticpath,
                                     template_folder=self.templatepath)

            for route, view_func in self._routes:
                self._plugin.route(route, methods=['GET', 'POST'])(view_func)

            for name, link, description in self._hotlink:
                self._mad['madmin'].add_plugin_hotlink(name, link, self.pluginname, self.description, self.author,
                                                       self.url, description, self.version)

    def perform_operation(self):
        """The actual implementation of the identity plugin is to just return the
        argument
        """

        # do not change this part ▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽
        if not self._pluginconfig.getboolean("plugin", "active", fallback=False):
            return False
        self._mad['madmin'].register_plugin(self._plugin)
        # do not change this part △△△△△△△△△△△△△△△

        # load your stuff now

        return True

    @auth_required
    def example_route(self):
        return render_template("testfile.html",
                               header="Test Plugin", title="Test Plugin"
                               )

    @auth_required
    def pluginfaq(self):
        return render_template("pluginfaq.html",
                               header="Test Plugin", title="Test Plugin"
                               )
