from .funcs import *
#from .funcbase import CfnYamlDumper, CfnYamlLoader
from .funcbase import yaml
from io import StringIO
from re import sub
#from .funcsold import *
#import yaml
#from yaml import load, dump



def dump(data, stream=None, Dumper=None, **kwds):
    temp = StringIO()
    yaml.dump(data, temp, **kwds)
    
    temp = sub('(?<=\{)Fn::\w*(?=:\ )', 
        lambda matched: "'{}'".format(matched.group()), 
        temp.getvalue(), count=0, flags=0)
    
    if stream is not None:
        stream.write(temp)
    
    return temp
    
def load(stream):
    return yaml.load(stream)
#  return yaml.load(stream, CfnYamlLoader)