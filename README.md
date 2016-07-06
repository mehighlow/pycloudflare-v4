# *pycloudflare-v4*
A ***HUMAN READABLE*** and ***SCRIPTING EASY*** Python wrapper for CloudFlare API v4

## *Current Version:*
-  0.6

## *Covered Methods:*

- Zone:
    - List zones (https://api.cloudflare.com/#zone-list-zones)
    - Purge all files (https://api.cloudflare.com/#zone-purge-all-files)
- Zone Settings:
    - Get all Zone Settings (https://api.cloudflare.com/#zone-settings-properties)
    - Set(Edit) any/all Zone Settings(https://api.cloudflare.com/#zone-settings-edit-zone-settings-info)
- DNS Records for a Zone:
    - List DNS records(https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records)
    - Create DNS record(https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record)
    - Update DNS record(https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record)

## *Installation*

```bash
$ git clone https://github.com/zmgit/pycloudflare-v4
$ cd pycloudflare-v4
$ pip install -r requirements.txt
$ sudo ./setup.py install
```

## *Getting Started*

A very simple listing of zones within your account; including the IPv6 status of the zone.

```python
from pycloudflare_v4 import api

def main():

    cfapi = api.CloudFlare("email", "api_token")

    # Get all zones
    zones = cfapi.get_zones()
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_id, zone_name, zone_status

    # Purge cache for all zones
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

    # Get all DNS records
    for k, v in zones.iteritems():
        records = cfapi.dns_records(v['id'])
        print k
        for i in records:
            print i['name'], i['type'], i['id']

    # Create DNS record
    print cfapi.dns_records_create(zone_id=zone_id, record_type="A", record_name="test",
                                   record_content="1.1.1.1")

    # Update DNS record
    for k, v in zones.iteritems():
        records = cfapi.dns_records(v['id'])
        print k
        for i in records:
            print cfapi.dns_records_update(zone_id=zone_id, record_id=i['id'],
                                           proxied='true', ttl=1)

    # Get zone settings
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_name, ": ", zone_status
        print cfapi.get_all_zone_settings(zone_id)

    # Set zone settings
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_name, ": ", zone_status, zone_id
        print cfapi.set_zone_settings(zone_id,
                                      email_obfuscation="off",
                                      hotlink_protection="on")

if __name__ == '__main__':
    main()
```