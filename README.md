# pycloudflare-v4
Python wrapper for CloudFlare API v4

## Installation

```bash
	$ git clone https://github.com/zmgit/pycloudflare-v4
	$ cd pycloudflare-v4
	$ sudo ./setup.py install
```

## Getting Started

A very simple listing of zones within your account; including the IPv6 status of the zone.

```python
from pycloudflare_v4 import api

def main():

    cfapi = api.CloudFlare("email", "api_token")

    #  Get all zones
    zones = cfapi.get_zones()
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_id, zone_name, zone_status

    #  Purge cache for all zones
    for k, v in zones.iteritems():
        try:
            purged = cfapi.purge_everything(v['id'])
        except BaseException as e:
            print str(e)
        finally:
            if purged['success']:
                print k, "[ SUCCESS ]"
            else:
                print purged['errors'][0]['message']

    #  Get all DNS records
    for k, v in zones.iteritems():
        records = cfapi.dns_records(v['id'])
        print k
        for i, j in records.iteritems():
            print i, j['content']

    #  Get zone settings
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_name, ": ", zone_status
        print cfapi.get_all_zone_settings(zone_id)

    #  Set zone settings
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_name, ": ", zone_status, zone_id
        print cfapi.set_zone_settings(zone_id, email_obfuscation="off", hotlink_protection="off")

if __name__ == '__main__':
    main()
```