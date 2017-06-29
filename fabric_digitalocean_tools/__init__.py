# The MIT License (MIT)
#
# Copyright (c) 2017 Eran Sandler
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import
import os
from fabric.api import env

import requests

BASE_URL = "https://api.digitalocean.com/v2"

def _get_headers(token):
    return {
        "Authorization" : "Bearer {0}".format(token)
    }

def _get_token():
    token = os.environ["TOKEN"]
    if not token:
        token = os.environ["DO_TOKEN"]

    return token

def update_roles_digitalocean():
    token = _get_token()
    if not token:
        raise Exception("Can't find TOKEN or DO_TOKEN environment variable")

    url = BASE_URL + "/droplets"
    r = requests.get(url, headers=_get_headers(token))
    if r.status_code != 200:
        raise Exception("Request failed with status {0}. Reason: {1}".format(r.status_code, r.text))

    roles = {}

    data = r.json()

    for droplet in data.get("droplets", {}):
        droplet_tags = droplet.get("tags", [])
        if droplet_tags and len(droplet_tags) > 0:
            for t in droplet_tags:
                if t not in roles:
                    roles[t] = []

                roles[t].append(droplet.get("networks",{}).get("v4", [{}])[0].get("ip_address"))

    env.roledefs.update(roles)

__all__ = [
    "update_roles_digitalocean"
]
