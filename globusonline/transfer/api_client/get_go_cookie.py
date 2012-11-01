#!/usr/bin/env python

# Copyright 2010 University of Chicago
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Login to www.globusonline.org and extract the saml cookie.

When run as a script, takes username as first and only argument, and prompts
for password. The cookie is printed to stdout.
"""

import sys
import urlparse
import getpass
from Cookie import BaseCookie
from collections import namedtuple
import json

from globusonline.transfer.api_client.verified_https \
    import VerifiedHTTPSConnection

HOST = "nexus.api.globusonline.org"
PATH = "/authenticate"
PORT = 443

GOCookieResult = namedtuple("GOCookieResult", "username password cookie")


def get_go_cookie(ca_certs, username=None, password=None):
    """
    POST the login form to www.globusonline.org to get the cookie,
    prompting for username and password on stdin if they were not
    passed as parameters.

    @return: a GOCookieResult instance. The cookie is what most clients will
             be interested in, but if the username is not passed as a
             parameter the caller may need that as well, and may want
             to cache the password.
    """
    if ca_certs is None:
        from globusonline.transfer.api_client import get_ca
        ca_certs = get_ca(HOST)
    if username is None:
        print "GO Username: ",
        sys.stdout.flush()
        username = sys.stdin.readline().strip()
    if password is None:
        password = getpass.getpass("GO Password: ")

    headers = { "Content-type": "application/json; charset=UTF-8",
                "Hostname": HOST,
                "Accept": "application/json; charset=UTF-8" }
    c = VerifiedHTTPSConnection(HOST, PORT, ca_certs=ca_certs)
    body = json.dumps(dict(username=username,
                           password=password))
    c.request("POST", PATH, body=body, headers=headers)
    response = c.getresponse()
    set_cookie_header = response.getheader("set-cookie")
    if not set_cookie_header:
        # TODO: more appropriate exc type
        raise ValueError("No cookies received")

    cookies = BaseCookie(set_cookie_header)
    morsel = cookies.get("saml")
    if not morsel:
        raise ValueError("No saml cookie received")

    return GOCookieResult(username, password, morsel.coded_value)


def _get_host_port(url):
    o = urlparse(url)
    netloc_parts = o.netloc.split(":")
    if len(netloc_parts) == 2:
        host = netloc_parts[0]
        port = int(netloc_parts[1])
    else:
        host = o.netloc
        if o.scheme == "https":
            port = 443
        else:
            port = 80
    return (host, port)


def process_args(args=None, parser=None):
    from optparse import OptionParser

    if not parser:
        usage = "usage: %prog [username]"
        parser = OptionParser(usage=usage)

    parser.add_option("-C", "--server-ca-file", dest="server_ca_file",
                      help="ca file for validating server",
                      metavar="SERVER_CA_FILE")

    options, args = parser.parse_args(args)

    return options, args


if __name__ == '__main__':
    options, args = process_args()

    if len(args):
        username = args[0]
    else:
        username = None

    try:
        result = get_go_cookie(ca_certs=options.server_ca_file,
                               username=username)
        print result.cookie
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(2)
