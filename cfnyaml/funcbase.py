from ruamel.yaml import YAML, Node, ScalarNode, SequenceNode

yaml = YAML()



@classmethod
def from_yaml(cls, loader, node):
    def getv(v):
        return v if not isinstance(v, Node) else loader.construct_object(v)
#    if isinstance(cls.argnames, str):
    if isinstance(node, ScalarNode): # Compatible with optional parameters
        return cls(node.value)
#    elif isinstance(cls.argnames, list) or isinstance(cls.argnames, tuple):
    elif isinstance(node, SequenceNode): # Compatible with optional parameters
        return cls(*[getv(v) for v in node.value])
    else:
        raise ValueError('{}.argnames should be a string or an array'.format(cls.__name__))
    
@classmethod
def to_yaml(cls, dumper, data):
    if isinstance(cls.argnames, str):
        return dumper.represent_scalar(cls.yaml_tag, getattr(data, cls.argnames))
    elif isinstance(cls.argnames, list) or isinstance(cls.argnames, tuple):
        return dumper.represent_sequence(cls.yaml_tag, [getattr(data, argname) for argname in cls.argnames])
    else:
        raise ValueError('{}.argnames should be a string or an array'.format(cls.__name__))
    

def __init__(self, *args):
    names = [self.argnames] if isinstance(self.argnames, str) else self.argnames
#    print('INIT', names, args)
    if len(args) is not len(names):
        raise TypeError('__init__(self, {}) takes {} argumenst, but {} were given'.format(
        ', '.join(names), len(names) + 1, len(args) + 1))
    for i in range(len(names)):
        setattr(self, names[i], args[i])
        
def __repr__(self):
    names = [self.argnames] if isinstance(self.argnames, str) else self.argnames
    return self.reprtemplate.format(*[getattr(self, name) for name in names])

class FuncBaseMetaCls(type):

    def __new__(cls, name, bases, kwds):
        if kwds.get('yaml_tag') is None:
            kwds['yaml_tag'] = '!' + name
            
        if kwds.get('from_yaml') is None:
            kwds['from_yaml'] = from_yaml
            
        if kwds.get('to_yaml') is None:
            kwds['to_yaml'] = to_yaml
            
        if kwds.get('__init__') is None:
            kwds['__init__'] = __init__  
            
        if kwds.get('__repr__') is None:
            kwds['__repr__'] = __repr__
            if kwds.get('reprtemplate') is None:
                if isinstance(kwds['argnames'], str):
                    kwds['reprtemplate'] = '<{} {{}}>'.format(name)
                else:
                    temp = ', '.join(['{}={{}}'.format(name) for name in kwds['argnames']])
                    kwds['reprtemplate'] = '<{} {}>'.format(name, temp)
            
#        print('new!!!!!!!!!!', cls, name, bases, kwds)
        return type.__new__(cls, name, bases, kwds)
        
        
    def __init__(cls, name, bases, kwds):
        super(FuncBaseMetaCls, cls).__init__(name, bases, kwds)
#        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
#            CfnYamlLoader.add_constructor(cls.yaml_tag, cls.from_yaml)
#            CfnYamlDumper.add_representer(cls, cls.to_yaml)
        yaml.register_class(cls)

class FuncBase(metaclass=FuncBaseMetaCls):
    argnames = []
    
    
    
def construct_mapping(self, node, deep=False):
    
    mapping = ODict()

    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        value = self.construct_object(value_node, deep=deep)

        mapping[key] = value

    return mapping