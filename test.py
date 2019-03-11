import unittest
from cfnyaml import load, dump, Base64


#print(dump(load(open('template.yaml')), open('out.yaml', 'w')))
#exit()

class TestCase(unittest.TestCase):
  
  def test_Base64(self):
    a= "- !Base64 YWJjMTIzIS49JeeugOS9k+e5gemrlOOBq+OBu+OCk+OBk+OCmQ==\n"
    b = [Base64('abc123!.=%简体繁體にほんご', True)]
    
    assert(dump(load(a)) == a)
    assert(dump(b) == a)

  def test_Ref(self):
    a = "!Ref 'aaa'\n"
    b = dump(load(a))
    
  def test_Select(self):
    a = "!Select\n- '1'\n- [apples, grapes, oranges, mangoes]\n"
    b = dump(load(a))
    
    print('====================')
    print(a, b)
    assert(a==b)
    
    a = "!Select\n- 0\n- {'Fn::GetAZs': ''}\n"
    b = dump(load(a))
    print('====================')
    print(a, b)
    assert(a==b)
    
  def test_Sub(self):
    a = '!Sub\n- www.${Domain}\n- {Domain: github.com}\n'
    b = dump(load(a))
    assert(a==b)
    
    a = "- !Sub arn:aws:ssm:${AWS::Region}:${AWS::AccountId}:parameter/sfjs/packagelambda/*\n"
    print(a)
    print(dump(load(a)))
    assert(dump(load(a)) == a)
    
  def test_Equals(self):
    a = '''!Equals ["sg-mysggroup", !Ref "ASecurityGroup"]'''
    print(load(a))
    
  def test_And(self):
    a = '''
    !And
      - !Not [!Equals [!Ref EnvironmentType, prod]]
      - !Equals ["sg-mysggroup", !Ref "ASecurityGroup"]
    '''
    print(load(a))
    print(dump(load(a)))

  def test_Cidr(self):
    a = '!Select [ 0, !Cidr [ !Select [ 0, !Ref VpcCidrBlock], 1, 8 ]]'
    print(load(a))
    print(dump(load(a)))


if __name__ == '__main__':
  unittest.main()