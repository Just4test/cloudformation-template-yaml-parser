from .funcs import *
from .funcbase import CfnYamlDumper, CfnYamlLoader
#from .funcsold import *
import yaml
#from yaml import load, dump


def dump(data, stream=None, Dumper=None, **kwds):
  return yaml.dump(data, stream, CfnYamlDumper, **kwds)
  
def load(stream):
  return yaml.load(stream, CfnYamlLoader)