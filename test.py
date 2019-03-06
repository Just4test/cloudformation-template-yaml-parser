import unittest
from cfnyaml import yaml, Base64

class TestCase(unittest.TestCase):
  
  def test_base64(self):
    a= "!Base64 'YWJjMTIzIS49JeeugOS9k+e5gemrlOOBq+OBu+OCk+OBk+OCmQ=='\n"
    b = Base64('abc123!.=%简体繁體にほんご', True)
    
    assert(yaml.dump(yaml.load(a)) == a)
    assert(yaml.dump(b) == a)

  def test_Ref(self):
    a = "!Ref 'aaa'\n"
    b = yaml.dump(yaml.load(a))
    
    assert(yaml.load(a))
    assert(a == b)
    
  def test_Select(self):
    a = "!Select\n- '1'\n- [apples, grapes, oranges, mangoes]\n"
    b = yaml.dump(yaml.load(a))
    assert(a==b)
    
    
    a = "!Select\n- 0\n- {'Fn::GetAZs': ''}\n"
    b = yaml.dump(yaml.load(a))
    assert(a==b)
    
  def test_Sub(self):
    a = '!Sub\n- www.${Domain}\n- {Domain: github.com}\n'
    b = yaml.dump(yaml.load(a))
    
    assert(a==b)

  def test_Cidr(self):
    a = '!Select [ 0, !Cidr [ !Select [ 0, !Ref VpcCidrBlock], 1, 8 ]]'
    print(yaml.load(a))
    print(yaml.dump(yaml.load(a)))


if __name__ == '__main__':
  unittest.main()