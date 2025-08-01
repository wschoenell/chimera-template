# This is an example of an simple instrument.

from chimera.core.chimeraobject import ChimeraObject


class ControllerExample(ChimeraObject):
    __config__ = {"param1": "a string parameter"}

    def __init__(self):
        ChimeraObject.__init__(self)

    def __start__(self):
        self.do_something("test argument")

    def do_something(self, arg):
        self.log.warning("Hi, I'm doing something.")
        self.log.warning("My arg=%s" % arg)
        self.log.warning("My param1=%s" % self["param1"])
