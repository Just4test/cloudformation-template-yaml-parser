from .funcs import *
#from .funcbase import CfnYamlDumper, CfnYamlLoader
from .funcbase import yaml
from io import StringIO
#from .funcsold import *
#import yaml
#from yaml import load, dump



def dump(data, stream=None, Dumper=None, **kwds):
    if stream is not None:
        return yaml.dump(data, stream, **kwds)
    else:
        stream = StringIO()
        yaml.dump(data, stream, **kwds)
        return stream.getvalue()
    
def load(stream):
    return yaml.load(stream)
#  return yaml.load(stream, CfnYamlLoader)