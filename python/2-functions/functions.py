import requests, json

requests.packages.urllib3.disable_warnings()
base_url = 'https://198.19.36.167/api'
session = requests.Session()
session.verify = False

# Handle POSTs to the switch
def post(path, data):
  url = f'{base_url}/{path}'
  if url[-5:] != '.json': url+= '.json'
  response = session.post(url, json.dumps(data))
  if not response.ok:
    raise Exception(response.text)

# Manage Authentication
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

# Configure the hostname
def hostname(name):
  payload = {
    'topSystem': {
      'attributes': {
        'name': name
      }
    }
  }
  post('mo', payload)

# Manage switch features
def feature(name, state=True):
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

# Create a VRF
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

# Create a network: VLAN and SVI
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

# Configure HSRP for an SVI
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

# Configure and Access interface
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

# Disconnect
def disconnect():
  session.close()