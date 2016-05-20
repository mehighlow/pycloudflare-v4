# pycloudflare-v4
Python wrapper for CloudFlare API v4

## Installation

```bash
	$ git clone https://github.com/zmgit/pycloudflare-v4
	$ cd pycloudflare-v4
	$ sudo ./setup.py install
	$
```

## Getting Started

A very simple listing of zones within your account; including the IPv6 status of the zone.

```python
from pycloudflare_v4 import api

def main():
	cfapi = api.CloudFlare("email","api_token")
    zones = cfapi.get_zones()
    for z_name, z_details in zones.iteritems():
        zone_name = z_details['name']
        zone_id = z_details['id']
        zone_status = z_details['status']
        print zone_id, zone_name, zone_status

if __name__ == '__main__':
	main()
```