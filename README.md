# CloudFormation Yaml

Let you load cloudformation template.yaml

This package only run in python 3.

# Install

pip3 install -U cfn-yaml

# How to use
(In Python 3)
```
> import cfnyaml
> template = cfnyaml.load(open('template.yaml'))
> cfnyaml.dump(template)
> template['Resources']['lambdaFunc1']['Layers'].append(cfnyaml.Ref('lambdaLayer1'))
```


