#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__title__ = 'pycloudflare-v4'
__version__ = '0.6.1'
__author__ = 'Michael Zaglada'
__email__ = "zmpbox@gmail.com"
__license__ = 'MIT'

import json
import requests


import logging
logging.basicConfig(level=logging.DEBUG)


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

    class WRAPPERError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return self.value

    def halt(self, error_message):
        """
        Short method to raise error in one liner 'if else'
        :param error_message:
        :return:
        """
        raise self.WRAPPERError(error_message)

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
            logging.debug(r)
            logging.debug(json.dumps(data))
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

    def api_call_put(self, uri, data='{}'):
        headers = {'X-Auth-Email': self.EMAIL, 'X-Auth-Key': self.TOKEN, 'Content-Type': 'application/json'}
        try:
            r = requests.put(cf_api_url + uri, data=json.dumps(data), headers=headers)
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
        elif data['errors']:
            raise self.APIError(str(data['errors']))
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
        pages = self.api_call_get("zones")['result_info']['total_pages']
        for p in xrange(pages):
            zones = self.api_call_get("zones&page={0}&per_page=50".format(p))
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


    # CHANGE
    def change_always_online_setting(self, zone_id, always_online):
        """

        :param zone_id:
        :param always_online:
        :return:
        """

        uri = "zones/{0}/settings/always_online".format(zone_id)

        set_always_online = always_online if always_online in ("on", "off") else self.halt('FREE(Y),'
                                                                                           ' PRO(Y),'
                                                                                           ' BUSINESS(Y),'
                                                                                           ' ENTERPRISE(Y);'
                                                                                           ' valid values: (on, off)')

        data = {"value": "{0}".format(set_always_online)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_automatic_https_rewrites_setting(self, zone_id, automatic_https_rewrites):
        """
        https://api.cloudflare.com/#zone-settings-change-automatic-https-rewrites-setting
        :param zone_id:
        :param automatic_https_rewrites:
        :return:
        """

        uri = "zones/{0}/settings/automatic_https_rewrites".format(zone_id)


        set_automatic_https_rewrites = automatic_https_rewrites if automatic_https_rewrites in ("on", "off") else self.halt('FREE(Y),'
                                                                                           ' PRO(Y),'
                                                                                           ' BUSINESS(Y),'
                                                                                           ' ENTERPRISE(Y);'
                                                                                           ' valid values: (on, off)')

        data = {"value": "{0}".format(set_automatic_https_rewrites)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_browser_cache_ttl_setting(self, zone_id, browser_cache_ttl):

        uri = "zones/{0}/settings/browser_cache_ttl".format(zone_id)

        set_browser_cache_ttl = browser_cache_ttl if browser_cache_ttl in (30, 60, 300, 1200, 1800, 3600, 7200, 10800,
                                                                           14400, 18000, 28800, 43200, 57600, 72000,
                                                                           86400, 172800, 259200, 345600, 432000,
                                                                           691200, 1382400, 2073600, 2678400, 5356800,
                                                                           16070400, 31536000) else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (30, 60, 300, 1200, 1800, 3600, 7200, 10800, 14400, 18000, 28800, 43200, 57600, 72000, 86400, 172800, 259200, 345600, 432000, 691200, 1382400, 2073600, 2678400, 5356800, 16070400, 31536000)')

        data = {"value": set_browser_cache_ttl}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    ################################################################
    #  DNS (https://api.cloudflare.com/#dns-records-for-a-zone)    #
    ################################################################

    # List DNS records (https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records)
    def dns_records(self, zone_id):
        """
        Returns list of records. Each record is the dict with everything CF could return.
        :param zone_id:
        :return: list
        """
        record_types = ["A", "AAAA", "CNAME", "TXT", "SRV", "LOC", "MX", "NS", "SPF"]  # all available record types
        page = 1  # initial page to start with
        records = []
        for rt in record_types:
            uri = "zones/" + str(zone_id) + "/dns_records?type={type}&page={page}&per_page=100".format(type=rt,
                                                                                                       page=page)
            for p in xrange(self.api_call_get(uri)['result_info']['total_pages']):
                page = p + 1
                dns_records = self.api_call_get(uri, page)
                if dns_records['success']:
                    for i in dns_records['result']:
                        records.append(i)
        return records

    # Create record (https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record)
    def dns_records_create(self, zone_id, record_type, record_name, record_content, record_ttl=1):
        uri = "zones/" + str(zone_id) + "/dns_records/"
        data = {"type": record_type, "name": record_name, "content": record_content, "ttl": record_ttl}
        create_record = self.api_call_post(uri, data)

        if create_record['success']:
            return create_record['result']
        else:
            return "Error", create_record['errors']

    # Update record (https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record)
    def dns_records_update(self, zone_id, record_id,
                           proxied=False,
                           content=False,
                           name=False,
                           ttl=False):
        uri = "zones/" + str(zone_id) + "/dns_records/" + str(record_id)
        change_list = dict()
        change_list['proxied'] = proxied if proxied in (False, 'false', 'true') else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: ("false", "true" in quotes!)')
        change_list['content'] = content
        change_list['name'] = name
        change_list['ttl'] = ttl if ttl in (False, 1, 120, 300, 600, 900, 1800, 2700, 3600, 7200, 18000, 43200) else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (1 - Automatic, 120, 300, 600, 900, 1800, 2700, 3600, 7200, 18000, 43200)')

        #  First, fetch data for the record
        for i in self.dns_records(zone_id):
            if i['id'] == record_id:
                original_data = i

        data = original_data

        for k, v in change_list.iteritems():
            if k == 'proxied' and v:
                data[k] = json.loads(v)  # escape for true/false in proxied settings
            elif v:
                data[k] = v

        return self.api_call_put(uri, data)

    # Delete record ()
    def dns_records_delete(self, zone_id, record_id):
        url = ""
        pass

    ##########################################################################
    # CloudFlare IPs (https://api.cloudflare.com/#cloudflare-ips-properties) #
    ##########################################################################
    def cf_ips(self):
        uri = "ips"
        response = self.api_call_get(uri)
        if response['success']:
            ips = response['result']
        return ips
