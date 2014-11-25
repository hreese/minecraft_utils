import types
from uuid import uuid4
import jinja2

class MinecraftCommand:
	"""Base Class for Commands"""
	def __init__(self, command = "", name = ""):
		self.cmd = command
		self.template = jinja2.Template(command)
		if not isinstance(name, str) or len(name) < 1:
			self.name = str(uuid4())
		else:
			self.name = name
	
	def render(self):
		return str(self)
	
	def __str__(self):
		return self.command

class MinecraftContext:
	"""Base Class for all context classes"""
	def __init__(self):
		self.v = {}
		self.c = []
	
	def addVars(self, name="anon", vars={}):
		self.v.update( {name: vars} )
	
	def addCommand(self, command="", name=""):
		self.c.append( MinecraftCommand() )
	
def setblock(self, x=0, y=0, z=0, tileName='minecraft:air', dataValue=0, oldBlockHandling='replace', dataTag=''):
	return " ".join(("/setblock", str(x),str(y),str(z),tileName,str(dataValue),oldBlockHandling,dataTag))
