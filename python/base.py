#!/usr/bin/python3
import requests, json

requests.packages.urllib3.disable_warnings()
base_url = 'https://198.19.36.167/api'
session = requests.Session()
session.verify = False

def post(path, data):
  url = f'{base_url}/{path}'
  if url[-5:] != '.json': url+= '.json'
  response = session.post(url, json.dumps(data))
  if not response.ok:
    raise Exception(response.text)

def authenticate(username, password):
  auth = {
    'aaaUser': {
      'attributes': {
        'name': username,
        'pwd': password
      }
    }
  }
  post('aaaLogin', auth)

def hostname(name):
  payload = {
    'topSystem': {
      'attributes': {
        'name': name
      }
    }
  }
  post('mo', payload)

def feature(name, state):
  feature_key = {
    'hsrp': 'fmHsrp',
    'interface-vlan': 'fmInterfaceVlan'
  }
  if name.lower() not in feature_key.keys():
    raise Exception(f'Undefined feature: {name}')
  payload = {
    feature_key[name.lower()]: {
      'attributes': {
        'adminSt': 'enabled' if state else 'disabled'
      }
    }
  }
  post('mo/sys/fm.json', payload)

def vrf(name):
  payload = {
    'l3Inst': {
      'attributes': {
        'dn': f'sys/inst-{name}',
        'name': name
      }
    }
  }
  post('mo/sys', payload)

def network(name, vlan, ip, vrf='default'):
  payload = {
    'l2BD': {
      'attributes': {
        'dn': f'sys/bd/bd-[vlan-{vlan}]',
        'name': name,
      }
    }
  }
  post('mo/sys/bd', payload)
  payload = {
    'sviIf': {
      'attributes': {
        'adminSt': 'up',
        'descr': name,
        'id': f'vlan{vlan}'
      },
      'children': [
        {
          'nwRtVrfMbr': {
            'attributes': {
              'tDn': f'sys/inst-{vrf}'
            }
          } 
        }
      ]
    }
  }
  post('mo/sys/intf', payload)
  payload = {
    'ipv4If':{
      'attributes': {
        'id': f'vlan{vlan}'
      },
      'children': [
        {
          'ipv4Addr': {
            'attributes': {
              'addr': ip
            }
          }
        }
      ]
    }
  } 
  post(f'mo/sys/ipv4/inst/dom-[{vrf}]', payload)

def hsrp(vlan, ip, priority):
  payload = {
    'hsrpIf': {
      'attributes': {
        'id': f'vlan{vlan}'
      },
      'children': [
        {
          'hsrpGroup': {
            'attributes': {
              'id': vlan,
              'af': 'ipv4',
              'ctrl': 'preempt',
              'prio': priority,
              'fwdUprThrld': priority,
              'ip': ip
            }
          }
        }
      ]
    }
  }
  post('mo/sys/hsrp/inst', payload)

def access_interface(interface, vlan, description):
  payload = {
    'l1PhysIf': {
      'attributes': {
        'id': interface,
        'accessVlan': f'vlan-{vlan}',
        'descr': description,
        'adminSt': 'up',
        'layer': 'Layer2'
      }
    }
  }
  post('mo/sys/intf', payload)

authenticate('cisco', 'cisco')
feature('interface-vlan', True)
feature('hsrp', True)
hostname('tres-python')
vrf('chiefs')
network('mahomes', '15', '192.168.15.2/24', 'chiefs')
network('kelce', '87', '192.168.87.2/24', 'chiefs')
network('jones', '95', '192.168.95.2/24', 'chiefs')
hsrp('15', '192.168.15.1', 110)
hsrp('87', '192.168.87.1', 110)
hsrp('95', '192.168.95.1', 110)
access_interface('eth1/5', '15', 'Mahomes')
access_interface('eth1/6', '87', 'Kelce')
access_interface('eth1/7', '95', 'Jones')

session.close()
