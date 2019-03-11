from .funcbase import FuncBase
import base64
from ruamel.yaml import Node




class Ref(FuncBase):
  argnames = 'logicalName'

class Base64(FuncBase):
  argnames = 'base64str'
  
  @property
  def originalstr(self):
    return base64.b64decode(self.base64str).decode('utf8')
    
  @originalstr.setter
  def originalstr(self, value):
    self.base64str = base64.b64encode(value.encode('utf8')).decode()
  
  def __init__(self, value, isoriginal=False):
    if isoriginal:
      self.originalstr = value
    else:
      self.base64str = value
      
  def __repr__(self):
    tmp = self.originalstr if len(self.originalstr) <= 13 else self.originalstr[0:10] + '...'
    return '<Base64 "{}">'.format(tmp)


class Cidr(FuncBase):
  argnames = ['ipblock', 'count', 'cidrbits']
  reprtemplate = '<Cidr {} / {} ({})>'
  

class FindInMap(FuncBase):
  argnames = ['mapName', 'topLevelKey', 'secondLevelKey']
  reprtemplate = '<FindInMap {}[{}][{}]>'
  
class GetAtt(FuncBase):
  argnames = 'path'

  
class GetAZs(FuncBase):
  argnames = 'region'

class ImportValue(FuncBase):
  argnames = 'sharedValueToImport'
  
class Equals(FuncBase):
  argnames = ['value1', 'value2']
  reprtemplate = '<Equals {} == {}>'
    
class Join(FuncBase):
  argnames = ['delimiter', 'values']
  reprtemplate = '<Join "{}".join({})>'



class Select(FuncBase):
  argnames = ['index', 'values']
  reprtemplate = '<Select {1}[{0}]>'

class Split(FuncBase):
  argnames = ['delimiter', 'sourcestr']
  reprtemplate = '<Select "{1}".split("{0}")>'
    
class Sub(FuncBase):
  argnames = ['template', 'values']
  reprtemplate = '<Sub "{}".format({})>'
  
  def __init__(self, template, values=None):
    self.template = template
    self.values = values
      
  @classmethod
  def to_yaml(cls, dumper, data):
    if data.values is None:
      return dumper.represent_scalar(cls.yaml_tag, data.template)
    else:
      return dumper.represent_sequence(cls.yaml_tag, [getattr(data, argname) for argname in cls.argnames])

class Transform(FuncBase):
  argnames = ['name', 'params']
  
  
######## Condition Functions ###############
    
class And(FuncBase):
  @classmethod
  def from_yaml(cls, loader, node):
    def getv(v):
      return v if not isinstance(v, Node) else loader.construct_object(v)
    return cls(*[getv(v) for v in node.value])
    
  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence(cls.yaml_tag, [getattr(data, argname) for argname in cls.argnames])
  
  def __init__(self, *values):
    self.values = values
      
  def __repr__(self):
    return '<And {}>'.format(' && '.join([str(v) for v in self.values]))
  

class Equals(FuncBase):
  argnames = ['value1', 'value2']
  reprtemplate = '<Equals {} == {} >'

class If(FuncBase):
  argnames = ['condition', 'value_if_true', 'value_if_false']
  reprtemplate = '<If {} ? {} : {}>'
  
class Not(FuncBase):
  argnames = ['value']
  reprtemplate = '<Not {}>'
  
class Or(FuncBase):
  @classmethod
  def from_yaml(cls, loader, node):
    def getv(v):
      return v if not isinstance(v, Node) else loader.construct_object(v)
    return cls(*[getv(v) for v in node.value])
    
  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence(cls.yaml_tag, [getattr(data, argname) for argname in cls.argnames])

  def __init__(self, *values):
    self.values = values
      
  def __repr__(self):
    return '<Or {}>'.format(' || '.join([str(v) for v in self.values]))
    
    

                  