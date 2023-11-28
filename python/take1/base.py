#!/usr/bin/python3
import requests

requests.packages.urllib3.disable_warnings()
session = requests.Session()
session.verify = False

payload = {
  'aaaUser': {
    'attributes': {
      'name': 'cisco',
      'pwd': 'cisco'
    }
  }
}
response = session.post('https://198.19.36.167/api/aaaLogin.json', json=payload)

payload = {
  'topSystem': {
    'attributes': {
      'name': 'tres-python'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo.json', json=payload)

payload = {
  'fmInterfaceVlan': {
    'attributes': {
      'adminSt': 'enabled'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/fm.json', json=payload)

payload = {
  'fmHsrp': {
    'attributes': {
      'adminSt': 'enabled'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/fm.json', json=payload)

payload = {
  'l3Inst': {
    'attributes': {
      'dn': 'sys/inst-chiefs',
      'name': 'chiefs'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo/sys.json', json=payload)

payload = {
  'l2BD': {
    'attributes': {
      'dn': 'sys/bd/bd-[vlan-15]',
      'name': 'Mahomes'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/bd.json', json=payload)

payload = {
  'sviIf': {
    'attributes': {
      'adminSt': 'up',
      'descr': 'Mahomes',
      'id': 'vlan15'
    },
    'children': [
      {
        'nwRtVrfMbr': {
          'attributes': {
            'tDn': 'sys/inst-chiefs'
          }
        }
      }
    ]
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/intf.json', json=payload)

payload = {
  'ipv4If':{
    'attributes': {
      'id': f'vlan15'
    },
    'children': [
      {
        'ipv4Addr': {
          'attributes': {
            'addr': '192.168.15.2/24'
          }
        }
      }
    ]
  }
} 
response = session.post('https://198.19.36.167/api/mo/sys/ipv4/inst/dom-[chiefs]', json=payload)

payload = {
  'hsrpIf': {
    'attributes': {
      'id': 'vlan15'
    },
    'children': [
      {
        'hsrpGroup': {
          'attributes': {
            'id': 15,
            'af': 'ipv4',
            'ctrl': 'preempt',
            'prio': 110,
            'fwdUprThrld': 110,
            'ip': '192.168.15.1'
          }
        }
      }
    ]
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/hsrp/inst.json', json=payload)

payload = {
  'l1PhysIf': {
    'attributes': {
      'id': 'eth1/5',
      'accessVlan': 'vlan-15',
      'descr': 'Mahomes',
      'adminSt': 'up',
      'layer': 'Layer2'
    }
  }
}
response = session.post('https://198.19.36.167/api/mo/sys/intf.json', json=payload)
session.close()

