#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__title__ = 'pycloudflare-v4'
__version__ = '0.7.0'
__author__ = 'Michael Zaglada'
__email__ = "zmpbox@gmail.com"
__license__ = 'MIT'

import json
import requests


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

    def change_always_online_setting(self, zone_id, always_online):
        """
        https://api.cloudflare.com/#zone-settings-change-always-online-setting
        :param zone_id:
        :param always_online:
        :return:
        """

        uri = "zones/{0}/settings/always_online".format(zone_id)
        valid_values = ["default", "on", "off"]

        if always_online not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if always_online == "default":
            set_always_online = "on"
        else:
            set_always_online = always_online

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

        if automatic_https_rewrites == "default":
            set_automatic_https_rewrites = "off"
        else:
            set_automatic_https_rewrites = automatic_https_rewrites

        data = {"value": "{0}".format(set_automatic_https_rewrites)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_browser_cache_ttl_setting(self, zone_id, browser_cache_ttl):
        """
        https://api.cloudflare.com/#zone-settings-change-browser-cache-ttl-setting
        :param zone_id:
        :param browser_cache_ttl:
        :return:
        """

        uri = "zones/{0}/settings/browser_cache_ttl".format(zone_id)
        valid_values = ["default", 30, 60, 300, 1200, 1800, 3600, 7200, 10800, 14400, 18000,
                        28800, 43200, 57600, 72000, 86400, 172800, 259200, 345600, 432000,
                        691200, 1382400, 2073600, 2678400, 5356800, 16070400, 31536000]

        if browser_cache_ttl not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if browser_cache_ttl == "default":
            set_browser_cache_ttl = 14400
        else:
            set_browser_cache_ttl = browser_cache_ttl

        data = {"value": set_browser_cache_ttl}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_browser_check_setting(self, zone_id, browser_check):
        """
        https://api.cloudflare.com/#zone-settings-change-browser-check-setting
        :param zone_id:
        :param browser_check:
        :return:
        """
        uri = "zones/{0}/settings/browser_check".format(zone_id)
        valid_values = ["default", "on", "off"]

        if browser_check not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if browser_check == "default":
            set_browser_check = "on"
        else:
            set_browser_check = browser_check

        data = {"value": "{0}".format(set_browser_check)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_cache_level_setting(self, zone_id, cache_level):
        """
        https://api.cloudflare.com/#zone-settings-change-cache-level-setting
        :param zone_id:
        :param cache_level:
        :return:
        """
        uri = "zones/{0}/settings/cache_level".format(zone_id)
        valid_values = ["default", "aggressive", "basic", "simplified"]

        if cache_level not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if cache_level == "default":
            set_cache_level = "aggressive"
        else:
            set_cache_level = cache_level

        data = {"value": "{0}".format(set_cache_level)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_challenge_ttl_setting(self, zone_id, challenge_ttl):
        """
        https://api.cloudflare.com/#zone-settings-change-challenge-ttl-setting
        :param zone_id:
        :param challenge_ttl:
        :return:
        """

        uri = "zones/{0}/settings/challenge_ttl".format(zone_id)
        valid_values = ["default", 300, 900, 1800, 2700, 3600, 7200, 10800, 14400,
                        28800, 57600, 86400, 604800, 2592000, 31536000]

        if challenge_ttl not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if challenge_ttl == "default":
            set_challenge_ttl = 1800
        else:
            set_challenge_ttl = challenge_ttl

        data = {"value": set_challenge_ttl}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_development_mode_setting(self, zone_id, development_mode):
        """
        https://api.cloudflare.com/#zone-settings-change-development-mode-setting
        :param zone_id:
        :param development_mode:
        :return:
        """
        uri = "zones/{0}/settings/development_mode".format(zone_id)
        valid_values = ["default", "on", "off"]

        if development_mode not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if development_mode == "default":
            set_development_mode = "off"
        else:
            set_development_mode = development_mode

        data = {"value": "{0}".format(set_development_mode)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_email_obfuscation_setting(self, zone_id, email_obfuscation):
        """
        https://api.cloudflare.com/#zone-settings-change-email-obfuscation-setting
        :param zone_id:
        :param email_obfuscation:
        :return:
        """
        uri = "zones/{0}/settings/email_obfuscation".format(zone_id)
        valid_values = ["default", "on", "off"]

        if email_obfuscation not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if email_obfuscation == "default":
            set_email_obfuscation = "on"
        else:
            set_email_obfuscation = email_obfuscation

        data = {"value": "{0}".format(set_email_obfuscation)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']

    def change_origin_error_page_pass_thru_setting(self, zone_id, origin_error_page_pass_thru):
        """
        https://api.cloudflare.com/#zone-settings-change-enable-error-pages-on-setting
        :param zone_id:
        :param origin_error_page_pass_thru:
        :return:
        """
        uri = "zones/{0}/settings/origin_error_page_pass_thru".format(zone_id)
        valid_values = ["default", "on", "off"]

        if origin_error_page_pass_thru not in valid_values:
            self.halt('valid values: ("{0}".format(valid_values))')

        if origin_error_page_pass_thru == "default":
            set_origin_error_page_pass_thru = "off"
        else:
            set_origin_error_page_pass_thru = origin_error_page_pass_thru

        data = {"value": "{0}".format(set_origin_error_page_pass_thru)}

        set_settings = self.api_call_patch(uri, data)
        if set_settings['success']:
            return set_settings['result']
        else:
            return "Error", set_settings['errors']



#TODO
# sort_query_string_for_cache
# hotlink_protection
# ip_geolocation
# ipv6
# minify
# mobile_redirect
# mirage
# opportunistic_encryption
# polish
# prefetch_preload
# response_buffering
# rocket_loader
# security_header
# security_level
# server_side_exclude
# ssl
# tls_client_auth
# true_client_ip_header
# tls_1_2_only
# tls_1_3
# waf
# websockets




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
        change_list['proxied'] = proxied if proxied in (False, 'false', 'true') else self.halt(
            'FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: ("false", "true" in quotes!)')
        change_list['content'] = content
        change_list['name'] = name
        change_list['ttl'] = ttl if ttl in (
        False, 1, 120, 300, 600, 900, 1800, 2700, 3600, 7200, 18000, 43200) else self.halt(
            'FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (1 - Automatic, 120, 300, 600, 900, 1800, 2700, 3600, 7200, 18000, 43200)')

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
