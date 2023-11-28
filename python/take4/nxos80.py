#!/usr/bin/python3
import requests, json, yaml
from getpass import getpass

requests.packages.urllib3.disable_warnings()

class Switch(object):
  def __init__(self, address, username=None, password=None):
    self.address = address
    self.__username = username
    self.__password = password
    self.__session = requests.Session()
    self.__session.verify = False
    self.authenticate()

  def post(self, path, data):
    url = f'http://{self.address}/api/{path}'
    if url[-5:] != '.json': url+= '.json'
    response = self.__session.post(url, json=data)
    if not response.ok:
      raise Exception(response.text)

  def authenticate(self, username=None, password=None):
    if self.__username is None: self.__username = input("User: ")
    if self.__password is None: self.__password = getpass("Password: ")
    auth = {
      'aaaUser': {
        'attributes': {
          'name': self.__username,
          'pwd': self.__password
        }
      }
    }
    self.post('aaaLogin', auth)

  def hostname(self, name):
    payload = {
      'topSystem': {
        'attributes': {
          'name': name
        }
      }
    }
    self.post('mo', payload)

  def feature(self, name, state=True):
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
    self.post('mo/sys/fm.json', payload)

  def vrf(self, name):
    payload = {
      'l3Inst': {
        'attributes': {
          'dn': f'sys/inst-{name}',
          'name': name
        }
      }
    }
    self.post('mo/sys', payload)

  def network(self, name, vlan, ip, vrf='default'):
    payload = {
      'l2BD': {
        'attributes': {
          'dn': f'sys/bd/bd-[vlan-{vlan}]',
          'name': name,
        }
      }
    }
    self.post('mo/sys/bd', payload)
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
    self.post('mo/sys/intf', payload)
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
    self.post(f'mo/sys/ipv4/inst/dom-[{vrf}]', payload)

  def hsrp(self, vlan, ip, priority):
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
    self.post('mo/sys/hsrp/inst', payload)

  def access_interface(self, interface, vlan, description):
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
    self.post('mo/sys/intf', payload)

  def close(self):
    self.__session.close()

def process_file(filename):
  with open(filename) as f: data = f.read()
  config = yaml.safe_load(data)
  username = config['switch']['username'] if 'username' in config['switch'].keys() else None
  password = config['switch']['password'] if 'password' in config['switch'].keys() else None
  switch = Switch(config['switch']['address'], username, password)
  if 'hostname' in config.keys(): switch.hostname(config['hostname'])
  if 'features' in config.keys():
    for feature in config['features']:
      switch.feature(feature)
  if 'vrfs' in config.keys():
    for vrf in config['vrfs']:
      switch.vrf(vrf)
  if 'networks' in config.keys():
    for network in config['networks']:
      switch.network(network['name'], network['id'], network['ip'], network['vrf'])
      if 'hsrp' in network.keys():
        switch.hsrp(network['id'], network['hsrp']['ip'], network['hsrp']['priority'])
  if 'interfaces' in config.keys():
    for interface in config['interfaces']:
      if interface['mode'] == 'access':
        switch.access_interface(interface['interface'], interface['vlan'], interface['description'])

