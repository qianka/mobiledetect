#!/usr/bin/env python
"""
Mobile Detect - Python detection mobile phone and tablet devices

Thanks to:
    https://github.com/serbanghita/Mobile-Detect/blob/master/Mobile_Detect.php
"""

import os
import re
import json
from hashlib import sha1

OPERATINGSYSTEMS = {}
DEVICE_PHONES = {}
DEVICE_TABLETS = {}
DEVICE_BROWSERS = {}
ALL_RULES = {}
MOBILE_HTTP_HEADERS = {}
UA_HTTP_HEADERS = {}

class MobileDetectRuleFileError(Exception):
    pass

class MobileDetectError(Exception):
    pass


def load_rules(filename=None):
    global OPERATINGSYSTEMS
    global DEVICE_PHONES
    global DEVICE_TABLETS
    global DEVICE_BROWSERS
    global ALL_RULES
    global MOBILE_HTTP_HEADERS
    global UA_HTTP_HEADERS

    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Mobile_Detect.json")
    rules = json.load(open(filename))
    if not "version" in rules:
        raise MobileDetectRuleFileError("version not found in rule file: %s" % filename)
    if not "headerMatch" in rules:
        raise MobileDetectRuleFileError("section 'headerMatch' not found in rule file: %s" % filename)
    if not "uaHttpHeaders" in rules:
        raise MobileDetectRuleFileError("section 'uaHttpHeaders' not found in rule file: %s" % filename)
    if not "uaMatch" in rules:
        raise MobileDetectRuleFileError("section 'uaMatch' not found in rule file: %s" % filename)

    MOBILE_HTTP_HEADERS = dict((http_header, matches) for http_header, matches in rules["headerMatch"].iteritems())
    UA_HTTP_HEADERS = rules['uaHttpHeaders']
    OPERATINGSYSTEMS = dict((name, re.compile(match, re.IGNORECASE|re.DOTALL)) for name, match in rules['uaMatch']['os'].iteritems())
    DEVICE_PHONES = dict((name, re.compile(match, re.IGNORECASE|re.DOTALL)) for name, match in rules['uaMatch']['phones'].iteritems())
    DEVICE_TABLETS = dict((name, re.compile(match, re.IGNORECASE|re.DOTALL)) for name, match in rules['uaMatch']['tablets'].iteritems())
    DEVICE_BROWSERS = dict((name, re.compile(match, re.IGNORECASE|re.DOTALL)) for name, match in rules['uaMatch']['browsers'].iteritems())
    ALL_RULES = {}
    ALL_RULES.update(OPERATINGSYSTEMS)
    ALL_RULES.update(DEVICE_PHONES)
    ALL_RULES.update(DEVICE_TABLETS)
    ALL_RULES.update(DEVICE_BROWSERS)

load_rules()


class MobileDetect(object):
    def __init__(self, request=None, useragent=None, headers=None):
        self.request = request
        self.useragent = useragent
        self.headers = {}

        if self.request is not None:
            if self.useragent is None:
                for http_header in UA_HTTP_HEADERS:
                    if http_header in request.META:
                        self.useragent = request.META[http_header]
                        break

            for http_header, matches in MOBILE_HTTP_HEADERS.iteritems():
                if not http_header in request.META:
                    continue

                header_value = request.META[http_header]
                if matches and isinstance(matches, dict) and 'matches' in matches:
                    if not header_value in matches['matches']:
                        continue

                self.headers[http_header] = header_value

            if 'HTTP_X_OPERAMINI_PHONE_UA' in request.META:
                self.useragent = "%s %s" % (self.useragent, request.META['HTTP_X_OPERAMINI_PHONE_UA'])

        if headers is not None:
            self.headers.update(headers)

        if self.useragent is None:
            self.useragent = ""

    def __getitem__(self, key):
        try:
            if ALL_RULES[key].search(self.useragent):
                return True
        except KeyError:
            pass
        return False

    def __contains__(self, key):
        try:
            if ALL_RULES[key].search(self.useragent):
                return True
        except KeyError:
            pass
        return False

    @property
    def device_hash(self):
        if not hasattr(self, '_device_hash'):
            hsh = sha1(self.useragent)
            for k, v in self.headers.iteritems():
                hsh.update("%s:%s" % (k, v))
            self._device_hash = hsh.hexdigest()
        return self._device_hash

    def mobile_by_headers(self):
        """
        Check the HTTP Headers for signs of mobile devices.

        This is the fastest mobile check but probably also the most unreliable.
        """

        if self.headers:
            return True

        return False

    def mobile_by_useragent(self):
        return self.is_phone() or self.is_tablet() or self.is_mobile_os() or self.is_mobile_ua()

    def is_phone(self):
        if self.detect_phone():
            return True
        return False

    def is_tablet(self):
        if self.detect_tablet():
            return True
        return False

    def is_mobile_os(self):
        if self.detect_mobile_os():
            return True
        return False

    def is_mobile_ua(self):
        if self.detect_mobile_ua():
            return True
        return False

    def detect_phone(self):
        """ Is Phone Device """
        for name, rule in DEVICE_PHONES.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def detect_tablet(self):
        """ Is Tabled Device """
        for name, rule in DEVICE_TABLETS.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def detect_mobile_os(self):
        """ Is Mobile OperatingSystem """
        for name, rule in OPERATINGSYSTEMS.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def detect_mobile_ua(self):
        """ Is Mobile User-Agent """
        for name, rule in DEVICE_BROWSERS.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def is_mobile(self):
        if self.mobile_by_headers():
            return True

        if self.mobile_by_useragent():
            return True

        return False

    def match(self, item):
        return item in self

    def grade(self):
        """
        Return the browser 'grade'
        """
        raise NotImplementedError()

