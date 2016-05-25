#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__title__ = 'pycloudflare-v4'
__version__ = '0.1'
__author__ = 'Michael Zaglada'
__email__ = "zmpbox@gmail.com"
__license__ = 'MIT'


import requests
import json

cf_api_url = "https://api.cloudflare.com/client/v4/"

class CloudFlare(object):
    def __init__(self, email, token):
        self.EMAIL = email
        self.TOKEN = token

    class CONNError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.value

    class APIError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.value

    def api_call_get(self, url, data=None):
        headers = {'X-Auth-Email': self.EMAIL, 'X-Auth-Key': self.TOKEN, 'Content-Type': 'application/json'}
        try:
            r = requests.get(cf_api_url + url, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
            raise self.CONNError(str(e))
        try:
            data = json.loads(r.text)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data['result'] == 'error':
            raise self.APIError(data['msg'])
        return data

    def api_call_post(self, url, data=None):
        headers = {'X-Auth-Email': self.EMAIL, 'X-Auth-Key': self.TOKEN, 'Content-Type': 'application/json'}
        try:
            r = requests.post(cf_api_url + url, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
            raise self.CONNError(str(e))
        try:
            data = json.loads(r.text)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data['result'] == 'error':
            raise self.APIError(data['msg'])
        return data

    def api_call_delete(self, uri, data='{}'):
        headers = {'X-Auth-Email': self.EMAIL, 'X-Auth-Key': self.TOKEN, 'Content-Type': 'application/json'}
        try:
            r = requests.delete(cf_api_url + uri, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
                raise self.CONNError(str(e))
        try:
            data = json.loads(r.text)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data['result'] == 'error':
            raise self.APIError(data['msg'])
        return data

    def api_call_patch(self, uri, data='{}'):
        headers = {'X-Auth-Email': self.EMAIL, 'X-Auth-Key': self.TOKEN, 'Content-Type': 'application/json'}
        try:
            r = requests.patch(cf_api_url + uri, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError,
                requests.RequestException,
                requests.HTTPError,
                requests.Timeout,
                requests.TooManyRedirects) as e:
                raise self.CONNError(str(e))
        try:
            data = json.loads(r.text)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data['result'] == 'error':
            raise self.APIError(data['msg'])
        return data

    ################################################################
    #  Zone (https://api.cloudflare.com/#zone)                     #
    ################################################################
    #  Get all zones
    def get_zones(self):
        """
        Returns an dictionary, where key is domain name and value is dict with everything CF could return,
        including zone ID which is used for any other operations.
        :return: dict
        """
        all_zones = {}
        for p in xrange(self.api_call_get("zones")['result_info']['total_pages']):
            page = p + 1
            zones = self.api_call_get("zones&per_page=50", page)
            if zones['success']:
                for i in zones['result']:
                    all_zones[i['name']] = i
        return all_zones

    # Purge all cache for the zone
    def purge_everything(self, zone_id):
        """
        Deletes all cache in zone.
        :param zone_id:
        :return:
        """
        uri = "zones/" + str(zone_id) + "/purge_cache"
        data = {"purge_everything": True}
        return self.api_call_delete(uri, data)

    ################################################################
    #  Zone Settings (https://api.cloudflare.com/#zone-settings)   #
    ################################################################
    #  Get all zone settings info
    def get_all_zone_settings(self, zone_id):
        """
        This method returns human readable/scripting easy dictionary with all settings of a zone.
        :param zone_id:
        :return:
        """
        result = {}
        response = self.api_call_get("zones/" + str(zone_id) + "/settings")
        if response['success']:
            for i in response['result']:
                result[i['id']] = i
        return result

    #  Edit zone settings info
    def set_zone_settings(self, zone_id, email_obfuscation="on", hotlink_protection="on"):
        uri = "/zones/{0}/settings/".format(zone_id)
        data = {"items":
                    [
                        {"id": "email_obfuscation", "value": "{0}".format(email_obfuscation)},
                        {"id": "hotlink_protection", "value": "{0}".format(hotlink_protection)},
                    ]
                }
        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return set_settings['errors']

    ################################################################
    #  DNS (https://api.cloudflare.com/#dns-records-for-a-zone)    #
    ################################################################
    def dns_records(self, zone_id):
        """
        Returns an dictionary, where key is record type and value is dict with everything CF could return.
        :param zone_id:
        :return: dict
        """
        record_types = ["A", "AAAA", "CNAME", "TXT", "SRV", "LOC", "MX", "NS", "SPF"]  # all available record types
        page = 1  # initial page to start with
        records = {}
        for rt in record_types:
            uri = "zones/" + str(zone_id) + "/dns_records?type={type}&page={page}&per_page=100".format(type=rt,
                                                                                                       page=page)
            for p in xrange(self.api_call_get(uri)['result_info']['total_pages']):
                page = p + 1
                dns_records = self.api_call_get(uri, page)
                if dns_records['success']:
                    for i in dns_records['result']:
                        records[rt] = i
        return records

    #  IPs (https://api.cloudflare.com/#cloudflare-ips-properties)
    def cf_ips(self):
        uri = "ips"
        response = self.api_call_get(uri)
        if response['success']:
            ips = response['result']
        return ips
