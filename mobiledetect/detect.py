#!/usr/bin/env python
"""
Mobile Detect - Python detection mobile phone and tablet devices

Thanks to:
    https://github.com/serbanghita/Mobile-Detect/blob/master/Mobile_Detect.php
"""

from .rules import ALL_RULES, DEVICE_PHONES, DEVICE_TABLETS, OPERATINGSYSTEMS, MOBILE_USER_AGENTS, UTILITIES, PROPERTIES


class MobileDetect(object):
    def __init__(self, request=None, useragent=None, headers=None):
        self.request = request
        self.useragent = useragent
        self.headers = {}

        if self.useragent is None:
            self.useragent = request.META.get('HTTP_USER_AGENT')

        if self.useragent is None:
            self.useragent = request.META.get('HTTP_X_DEVICE_USER_AGENT')

        if self.useragent is None:
            self.useragent = ""

        if self.request is not None:
            self.headers = dict((k, v) for k, v in request.META.iteritems() if k.startswith("HTTP_"))
            if 'HTTP_X_OPERAMINI_PHONE_UA' in request.META:
                self.useragent = "%s %s" % (self.useragent, request.META['HTTP_X_OPERAMINI_PHONE_UA'])

        if headers is not None:
            self.headers.update(headers)

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

    def mobile_by_headers(self):
        """
        Check the HTTP Headers for signs of mobile devices.

        This is the fastest mobile check but probably also the most unreliable.
        """

        try:
            if self.headers['HTTP_ACCEPT'] in ('application/x-obml2d', 'application/vnd.rim.html', 'text/vnd.wap.wml', 'application/vnd.wap.xhtml+xml'):
                return True
        except KeyError:
            pass

        mobile_headers = (
            'HTTP_X_WAP_PROFILE',  # @todo: validate
            'HTTP_X_WAP_CLIENTID',
            'HTTP_WAP_CONNECTION'
            'HTTP_PROFILE',
            'HTTP_X_OPERAMINI_PHONE_UA',  # Reported by Nokia devices (eg. C3)
            'HTTP_X_NOKIA_IPADDRESS',
            'HTTP_X_NOKIA_GATEWAY_ID',
            'HTTP_X_ORANGE_ID',
            'HTTP_X_VODAFONE_3GPDPCONTEXT',
            'HTTP_X_HUAWEI_USERID',
            'HTTP_UA_OS',  # Reported by Windows Smartphones.
            'HTTP_X_MOBILE_GATEWAY',  # Reported by Verizon, Vodafone proxy system.
            'HTTP_X_ATT_DEVICEID',  # Seend this on HTC Sensation. @ref: SensationXE_Beats_Z715e
            # HTTP_X_NETWORK_TYPE = WIFI
        )
        for name in mobile_headers:
            if name in self.headers:
                return True

        try:
            if self.headers['HTTP_UA_CPU'] in ('ARM', ):
                return True
        except KeyError:
            pass

        return False

    def mobile_by_useragent(self):
        return self.is_phone() or self.is_tablet() or self.is_mobile_os() or self.is_mobile_ua()

    def is_phone(self):
        """ Is Phone Device """
        for name, rule in DEVICE_PHONES.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def is_tablet(self):
        """ Is Tabled Device """
        for name, rule in DEVICE_TABLETS.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def is_mobile_os(self):
        """ Is Mobile OperatingSystem """
        for name, rule in OPERATINGSYSTEMS.iteritems():
            if rule.search(self.useragent):
                return name
        return False

    def is_mobile_ua(self):
        """ Is Mobile User-Agent """
        for name, rule in MOBILE_USER_AGENTS.iteritems():
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
        is_mobile = self.is_mobile()

        # TODO

        return 'C'

