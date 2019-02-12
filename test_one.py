import pytest
import pyrandomtools as under_test

def test_parse_arn():
    reply = under_test.parse_arn('arn:aws::us-east-1:123456789012:stack/test/1234')
    assert reply['Arn'] == 'arn'
    assert reply['Partition'] == 'aws'
    assert reply['Region'] == 'us-east-1'
    assert reply['Account'] == '123456789012'
    assert reply['ResourceType'] == 'stack'
    assert reply['Resource'] == 'test'
    assert reply['Qualifier'] == '1234'

    reply = under_test.parse_arn('arn:aws::us-east-1:123456789012:stack:test/1234')
    assert reply['ResourceType'] == 'stack'
    assert reply['Resource'] == 'test'
    assert reply['Qualifier'] == '1234'

    reply = under_test.parse_arn('arn:aws::us-east-1:123456789012:stack:test:1234')
    assert reply['ResourceType'] == 'stack'
    assert reply['Resource'] == 'test'
    assert reply['Qualifier'] == '1234'

    reply = under_test.parse_arn('arn:aws::us-east-1:123456789012:stack/test:1234')
    assert reply['ResourceType'] == 'stack'
    assert reply['Resource'] == 'test'
    assert reply['Qualifier'] == '1234'

    reply = under_test.parse_arn('abc:aws::us-east-1:123456789012:stack/test:1234')
    assert reply['Arn'] == None

    reply = under_test.parse_arn('string')
    assert reply['Arn'] == None

    reply = under_test.parse_arn(None)
    assert reply['Arn'] == None
    

def test_firstValid():
    assert under_test.firstValid(None,None,1,None,2) == 1
    assert under_test.firstValid(1,None,2) == 1
    assert under_test.firstValid(None,None,None) == None

def test_rangePick():
    assert under_test.rangePick(5,1,10) == 5

    # MinCheck
    assert under_test.rangePick(1,5,10) == 5
    assert under_test.rangePick(0,1,5) == 1
    assert under_test.rangePick(-20,-10,5) == -10

    # MaxCheck
    assert under_test.rangePick(5,1,4) == 4
    assert under_test.rangePick(11,5,10) == 10
    assert under_test.rangePick(6,1,5) == 5

def test_str2bool():
    assert under_test.str2bool('y') is True
    assert under_test.str2bool('n') is False
    assert under_test.str2bool('Y') is True
    assert under_test.str2bool('N') is False
    assert under_test.str2bool('yes') is True
    assert under_test.str2bool('no') is False
    assert under_test.str2bool('YES') is True
    assert under_test.str2bool('NO') is False
    assert under_test.str2bool('Yes') is True
    assert under_test.str2bool('No') is False
    assert under_test.str2bool('yES') is True
    assert under_test.str2bool('nO') is False

    assert under_test.str2bool('t') is True
    assert under_test.str2bool('f') is False
    assert under_test.str2bool('true') is True
    assert under_test.str2bool('false') is False
    assert under_test.str2bool('True') is True
    assert under_test.str2bool('False') is False

    assert under_test.str2bool(True) is True
    assert under_test.str2bool(False) is False
    assert under_test.str2bool(-1) is True
    assert under_test.str2bool(1) is True
    assert under_test.str2bool(0) is False
    assert under_test.str2bool('1') is True
    assert under_test.str2bool('0') is False
    
    assert under_test.str2bool(None) is False

class Dummy(object):
    def __init__(self):
        return
        
def test_name_of():
    assert under_test.name_of(Dummy()) == '{}.Dummy'.format(__name__)

def test_lcase_keys():
    assert under_test.lcase_keys({'Key':1}) != {'Key':1}
    assert under_test.lcase_keys({'Key':1}) == {'key':1}
    
def test_treeGet():
    myTree = {
        'dict': {
            'one': 1,
            'two': '2',
            'three': False
            },
            'list': [
                'a',
                { 'test': 'answer'},
                3
            ],
            'string': 'test'
    }
    
    myList = [5, 6, 7]

    assert under_test.treeGet(myTree,'dict.one') == 1
    assert under_test.treeGet(myTree,'dict.two') == '2'
    assert under_test.treeGet(myTree,'dict.three') == False
    assert under_test.treeGet(myTree,'dict.three') != True
    assert under_test.treeGet(myTree,'list[2]') == 3
    assert under_test.treeGet(myTree,'list.[2]') == 3
    assert under_test.treeGet(myTree,'list[-1]') == 3
    assert under_test.treeGet(myTree,'list.[-1]') == 3
    assert under_test.treeGet(myTree,'list.[-3]') == 'a'
    assert under_test.treeGet(myTree,'list[0]') == 'a'
    assert under_test.treeGet(myTree,'list[1].test') == 'answer'
    assert under_test.treeGet(myTree,'list[1]') == { 'test': 'answer'}
    assert under_test.treeGet(myList,'[1]') == 6
    assert under_test.treeGet(myList,'[-1]') == 7
    assert under_test.treeGet(myTree,'string') == 'test'

def test_asList():
    assert under_test.asList("string") == ["string"]
    assert under_test.asList(False) == [False]
    assert under_test.asList([1,2,3]) == [1,2,3]
    
def test_listContains():
    with pytest.raises(TypeError) as e:
        under_test.listContains(False, [])
    assert e.type is TypeError
    
    with pytest.raises(TypeError) as e:
        under_test.listContains("string", 1)
    assert e.type is TypeError
    
    under_test.listContains("string", ['string','data'])
    under_test.listContains("string", ['this is a string of data' ,'data'])
    under_test.listContains("string", ['start', 'this is a string of data' ,'data'])
    
    
def test_validators():
    assert under_test.validNumber(42)
    assert under_test.validInt(42)
    assert under_test.validNumber(42.1)
    
    assert not under_test.validInt(42.1)
    
    assert under_test.validNumber('42')
    assert under_test.validNumber('-42')
    assert under_test.validNumber('42.0')
    assert under_test.validInt('42')
    assert under_test.validInt('-42')
    
    assert not under_test.validInt('42.0')

def test_validate_region():
    assert under_test.validate_region('us-east-1')
    assert not under_test.validate_region('su-east-1')
