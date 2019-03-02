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
    return dumper.represent_scalar(cls.yaml_tag, data.base64str)
    
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
    return dumper.represent_scalar(cls.yaml_tag, data.logicalName)
  
  def __init__(self, logicalName):
    self.logicalName = logicalName
  def __repr__(self):
    return '<Ref "{}">'.format(self.logicalName)

class GetAtt(CfnFunc):
  yaml_tag = '!GetAtt'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(node.value)

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_scalar(cls.yaml_tag, data.path)
  
  def __init__(self, path):
    self.path = path
    
  def __repr__(self):
    return '<GetAtt {}>'.format('.'.join(self.path))



class Equals(CfnFunc):
  yaml_tag = '!Equals'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls(loader.construct_object(node.value[0]), loader.construct_object(node.value[1]))

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence(cls.yaml_tag, [data.value1, data.value2])
  
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
    return dumper.represent_sequence(cls.yaml_tag, [data.delimiter, data.values])
  
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
    return dumper.represent_sequence(cls.yaml_tag, [data.index, data.values])
  
  def __init__(self, index, *values):
    self.index = index
    self.values = list(values)
    
  def __repr__(self):
    return '<Select {1}[{0}]>'.format(self.index, self.values)
    
    

class If(CfnFunc):
  yaml_tag = '!If'
  
  @classmethod
  def from_yaml(cls, loader, node):
    return cls( \
      loader.construct_object(node.value[0]), \
      loader.construct_object(node.value[1]), \
      loader.construct_object(node.value[2]))

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence(cls.yaml_tag, [data.condition, data.value_if_true, data.value_if_false])
  
  def __init__(self, condition, value_if_true, value_if_false):
    self.condition = condition
    self.value_if_true = value_if_true
    self.value_if_false = value_if_false
    
  def __repr__(self):
    return '<If {} ? {} : {}>'.format(self.condition, self.value_if_true, self.value_if_false)
    

    
class Sub(CfnFunc):
  yaml_tag = '!Sub'
  
  @classmethod
  def from_yaml(cls, loader, node):
    # 默认情况下，loader会延迟解析复杂对象。如果不指定deep_construct，values的值会是一个空数组，并稍后填充。
    loader.deep_construct = True 
  
    template = loader.construct_object(node.value[0])
    values = loader.construct_object(node.value[1])
    ret = cls(template, **values)
    return ret

  @classmethod
  def to_yaml(cls, dumper, data):
    return dumper.represent_sequence(cls.yaml_tag, [data.template, data.values])
  
  def __init__(self, template, **values):
    self.template = template
    self.values = values
    
  def __repr__(self):
    return '<Sub "{}".format({})>'.format(self.template, self.values)