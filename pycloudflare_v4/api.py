#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__title__ = 'pycloudflare-v4'
__version__ = '0.6.1'
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

    #  Edit zone settings info
    def set_zone_settings(self, zone_id,
                          challenge_ttl=False,
                          email_obfuscation=False,
                          true_client_ip_header=False,
                          pseudo_ipv4=False,
                          prefetch_preload=False,
                          mirage=False,
                          polish=False,
                          mobile_redirect=False,
                          websockets=False,
                          response_buffering=False,
                          cname_flattening=False,
                          max_upload=False,
                          waf=False,
                          hotlink_protection=False,
                          server_side_exclude=False,
                          advanced_ddos=False,
                          ipv6=False,
                          tls_1_2_only=False,
                          always_online=False,
                          sha1_support=False,
                          minify=False,
                          security_level=False,
                          origin_error_page_pass_thru=False,
                          edge_cache_ttl=False,
                          tls_client_auth=False,
                          ssl=False,
                          browser_cache_ttl=False,
                          ip_geolocation=False,
                          browser_check=False,
                          security_header=False,
                          rocket_loader=False,
                          sort_query_string_for_cache=False,
                          cache_level=False,
                          http2=False,
                          development_mode=False):
        """
        This method edits zone settings. You can edit one setting or all at ones.
        Some settings are editable only in paid plans.
        :param zone_id:
        :param challenge_ttl:
        :param email_obfuscation: on/off
        :param true_client_ip_header:
        :param pseudo_ipv4:
        :param prefetch_preload:
        :param mirage:
        :param polish:
        :param mobile_redirect:
        :param websockets:
        :param response_buffering:
        :param cname_flattening:
        :param max_upload:
        :param waf:
        :param hotlink_protection: on/off
        :param server_side_exclude: on/off
        :param advanced_ddos:
        :param ipv6:
        :param tls_1_2_only:
        :param always_online:
        :param sha1_support:
        :param minify:
        :param security_level:
        :param origin_error_page_pass_thru:
        :param edge_cache_ttl:
        :param tls_client_auth:
        :param ssl:
        :param browser_cache_ttl:
        :param ip_geolocation:
        :param browser_check:
        :param security_header:
        :param rocket_loader:
        :param sort_query_string_for_cache:
        :param cache_level: aggressive/basic/simplified
        :param http2:
        :param development_mode: on/off
        :return:
        """

        uri = "zones/{0}/settings/".format(zone_id)

        change_list = dict()
        change_list['challenge_ttl'] = challenge_ttl if challenge_ttl in (False, 300, 900, 1800, 2700, 3600, 7200, 10800, 14400, 28800, 57600, 86400, 604800, 2592000, 31536000) else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (300, 900, 1800, 2700, 3600, 7200, 10800, 14400, 28800, 57600, 86400, 604800, 2592000, 31536000)')
        change_list['email_obfuscation'] = email_obfuscation if email_obfuscation in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        change_list['true_client_ip_header'] = true_client_ip_header if true_client_ip_header in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(N), ENTERPRISE(Y); valid values: (on, off)')
        change_list['pseudo_ipv4'] = pseudo_ipv4 if pseudo_ipv4 in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        change_list['prefetch_preload'] = prefetch_preload if prefetch_preload in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(N), ENTERPRISE(Y); valid values: (on, off)')
        change_list['mirage'] = mirage if mirage in (False, "on", "off") else self.halt('FREE(N), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        change_list['polish'] = polish if polish in (False, "off", "lossless", "lossy") else self.halt('FREE(N), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (off, lossless, lossy)')
        # change_list['mobile_redirect'] = mobile_redirect if mobile_redirect in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['websockets'] = websockets
        change_list['response_buffering'] = response_buffering if response_buffering in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(N), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['cname_flattening'] = cname_flattening
        # change_list['max_upload'] = max_upload
        # change_list['waf'] = waf
        change_list['hotlink_protection'] = hotlink_protection if hotlink_protection in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        change_list['server_side_exclude'] = server_side_exclude if server_side_exclude in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['advanced_ddos'] = advanced_ddos
        change_list['ipv6'] = ipv6 if ipv6 in (False, "on", "off", "safe") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off, safe)')
        change_list['tls_1_2_only'] = tls_1_2_only if tls_1_2_only in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['always_online'] = always_online
        # change_list['sha1_support'] = sha1_support
        # change_list['minify'] = minify
        change_list['security_level'] = security_level if security_level in (False, "essentially_off", "low", "medium", "high", "under_attack") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (essentially_off, low, medium, high, under_attack)')
        change_list['origin_error_page_pass_thru'] = origin_error_page_pass_thru if origin_error_page_pass_thru in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(N), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['edge_cache_ttl'] = edge_cache_ttl
        # change_list['tls_client_auth'] = tls_client_auth
        change_list['ssl'] = ssl if ssl in (False, "off", "flexible", "full", "full_strict") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (off, flexible, full, full_strict)')
        change_list['browser_cache_ttl'] = browser_cache_ttl if browser_cache_ttl in (False, 30, 60, 300, 1200, 1800, 3600, 7200, 10800, 14400, 18000, 28800, 43200, 57600, 72000, 86400, 172800, 259200, 345600, 432000, 691200, 1382400, 2073600, 2678400, 5356800, 16070400, 31536000) else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (30, 60, 300, 1200, 1800, 3600, 7200, 10800, 14400, 18000, 28800, 43200, 57600, 72000, 86400, 172800, 259200, 345600, 432000, 691200, 1382400, 2073600, 2678400, 5356800, 16070400, 31536000)')
        change_list['ip_geolocation'] = ip_geolocation if ip_geolocation in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        change_list['browser_check'] = browser_check if browser_check in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')
        # change_list['security_header'] = security_header
        change_list['rocket_loader'] = rocket_loader if rocket_loader in (False, "on", "off", "manual") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off, manual)')
        change_list['sort_query_string_for_cache'] = sort_query_string_for_cache if sort_query_string_for_cache in (False, "on", "off") else self.halt('FREE(N), PRO(N), BUSINESS(N), ENTERPRISE(Y); valid values: (on, off)')
        change_list['cache_level'] = cache_level if cache_level in (False, "aggressive", "basic", "simplified") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (aggressive, basic, simplified)')
        # change_list['http2'] = http2
        change_list['development_mode'] = development_mode if development_mode in (False, "on", "off") else self.halt('FREE(Y), PRO(Y), BUSINESS(Y), ENTERPRISE(Y); valid values: (on, off)')

        data = {"items": []}

        for k, v in change_list.iteritems():
            if v:
                data["items"].append({"id": "{settings}".format(settings=k), "value": "{value}".format(value=v)})

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
