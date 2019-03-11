from setuptools import setup, find_packages

setup(
    name = 'cfn-yaml',
    version = '0.1.3',
    keywords = ('CloudFormation', 'YAML'),
    description = 'Let you load cloudformation template.yaml',
    url = 'https://github.com/Just4test/cfn-yaml',
    license = 'wtfpl',
    install_requires = ['ruamel.yaml'],

    author = 'Just4test',
    author_email = 'myservice@just4test.net',
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3 :: Only'
    ],
    
    packages = find_packages(),
    platforms = 'any'
)