from __future__ import annotations
from abc import ABC, abstractmethod
import requests
import json


class AbstractServiceRegistryClient(ABC):

    @abstractmethod
    def request_access_token(self):
        pass

    @abstractmethod
    def register_service(self, service_id, redirect_uris):
        pass

    @abstractmethod
    def get_services_implementing_template(self, template_name):
        pass

    @abstractmethod
    def get_service(self, service_id):
        pass

    @abstractmethod
    def get_service_pairing_info(self, service_id):
        pass

    @abstractmethod
    def get_service_api(self, service_id):
        pass

    @abstractmethod
    def get_service_status(self, service_id):
        pass

    @abstractmethod
    def fetch_pairing_info(self, service_pairing_url):
        pass

    @abstractmethod
    def get_service_templates(self):
        pass


class ServiceRegistryClient(AbstractServiceRegistryClient):

    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None
        self.refresh_expires_in = None
        self.pairing_info = None
        self.service_registry_base_url = 'https://sensorsystems.iais.fraunhofer.de/api'
        self.service_registry_service_url = self.service_registry_base_url + '/services'

    def request_access_token(self):
        data = {'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        access_token_response = requests.post(self.token_url, data=data, verify=True, allow_redirects=False)
        resp_json = json.loads(access_token_response.text)
        self.access_token = resp_json['access_token']
        self.expires_in = resp_json['expires_in']
        self.refresh_token = resp_json['refresh_token']
        self.refresh_expires_in = resp_json['refresh_expires_in']

    def register_service(self, service_id, redirect_uris):

        hdr = {'Authorization': 'Bearer ' + self.access_token, 'Content-Type': 'application/json'}
        body = json.dumps({'redirect_uris': redirect_uris})
        registration_url = self.service_registry_service_url + '/' + service_id + '/register'
        print('registration URL', registration_url)
        print('Header', hdr)
        print('Body', body)
        registration_response = requests.post(registration_url, headers=hdr, data=body, verify=True,
                                              allow_redirects=False)
        print('Response', registration_response.text)
        return json.loads(registration_response.text)

    def get_services_implementing_template(self, template_name):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        resp = requests.get(self.service_registry_service_url, params={'template_name': template_name}, headers=hdr,
                            verify=True, allow_redirects=False)
        return json.loads(resp.text)

    def get_service(self, service_id):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        resp = requests.get(self.service_registry_service_url + '/' + service_id, headers=hdr, verify=True,
                            allow_redirects=False)
        return json.loads(resp.text)

    def get_service_pairing_info(self, service_id):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        url = self.service_registry_service_url + '/' + service_id + '/pairing'
        resp = requests.get(url, headers=hdr, verify=True, allow_redirects=False)
        return json.loads(resp.text)

    def get_service_api(self, service_id):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        url = self.service_registry_service_url + '/' + service_id + '/api'
        resp = requests.get(url, headers=hdr, verify=True, allow_redirects=False)
        return json.loads(resp.text)

    def get_service_status(self, service_id):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        url = self.service_registry_service_url + '/' + service_id + '/status'
        resp = requests.get(url, headers=hdr, verify=True, allow_redirects=False)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 410:
            return False

    def fetch_pairing_info(self, service_pairing_url):
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        self.pairing_info = requests.get(service_pairing_url, headers=hdr, verify=True, allow_redirects=False)
        return self.pairing_info

    def get_service_templates(self):
        self.request_access_token()
        hdr = {'Authorization': 'Bearer ' + self.access_token}
        url = 'https://sensorsystems.iais.fraunhofer.de/api/resource/templates'
        resp = requests.get(url, headers=hdr, verify=True, allow_redirects=False)
        return json.loads(resp.text)
