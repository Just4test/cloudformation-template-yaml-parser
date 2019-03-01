import yaml
import base64

class CfnFunc(yaml.YAMLObject):
  pass
  
class Base64(CfnFunc):
  yaml_tag = '!Base64'
  
  @property
  def originalstr(self):
    return self._originalstr
    
  @originalstr.setter
  def originalstr(self, value):
    self._originalstr = value
    self._base64str = base64.b64encode(value.encode('utf8')).decode()
    
  @property
  def base64str(self):
    return self._base64str
    
  @base64str.setter
  def base64str(self, value):
    self._base64str = value
    self._originalstr = base64.b64decode(value).decode('utf8')
    
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(node.value)

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_scalar('!Base64', data.base64str)
    
  def __init__(self, value, isoriginal=False):
    if isoriginal:
      self.originalstr = value
    else:
      self.base64str = value
      
  def __repr__(self):
    tmp = self.originalstr if len(self.originalstr) <= 13 else self.originalstr[0:10] + '...'
    return '<Base64 "{}">'.format(tmp)
  
  
  
class Ref(CfnFunc):
  yaml_tag = '!Ref'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(node.value)

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_scalar('!Ref', data.logicalName)
  
  def __init__(self, logicalName):
    self.logicalName = logicalName
  def __repr__(self):
    return '<Ref "{}">'.format(self.logicalName)

class GetAtt(CfnFunc):
  yaml_tag = '!GetAtt'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(*[loader.construct_object(v) for v in node.value])

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence('!GetAtt', data.names)
  
  def __init__(self, *names):
    self.names = names
    
  def __repr__(self):
    return '<GetAtt {}>'.format('.'.join(self.names))



class Equals(CfnFunc):
  yaml_tag = '!Equals'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(loader.construct_object(node.value[0]), loader.construct_object(node.value[1]))

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence('!Equals', [data.value1, data.value2])
  
  def __init__(self, value1, value2):
    self.value1 = value1
    self.value2 = value2
    
  def __repr__(self):
    return '<Equals {} == {}>'.format(self.value1, self.value2)
    
class Join(CfnFunc):
  yaml_tag = '!Join'
  
  @classmethod
  def from_yaml(cls, loader, node):
    # 默认情况下，loader会延迟解析复杂对象。如果不指定deep_construct，values的值会是一个空数组，并稍后填充。
    loader.deep_construct = True 
  
    delimiter = loader.construct_object(node.value[0])
    values = loader.construct_object(node.value[1])
    ret = cls(delimiter, *values)
    return ret

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence('!Join', [data.delimiter, data.values])
  
  def __init__(self, delimiter, *values):
    self.delimiter = delimiter
    self.values = list(values)
    
  def __repr__(self):
    return '<Join "{}".join({})>'.format(self.delimiter, self.values)



class Select(CfnFunc):
  yaml_tag = '!Select'
  
  @classmethod
  def from_yaml(cls, loader, node):
    # 默认情况下，loader会延迟解析复杂对象。如果不指定deep_construct，values的值会是一个空数组，并稍后填充。
    loader.deep_construct = True 
  
    index = loader.construct_object(node.value[0])
    values = loader.construct_object(node.value[1])
    ret = cls(index, *values)
    return ret

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence('!Select', [data.index, data.values])
  
  def __init__(self, index, *values):
    self.index = index
    self.values = list(values)
    
  def __repr__(self):
    return '<Select {1}[{0}]>'.format(self.index, self.values)