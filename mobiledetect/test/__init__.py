
import unittest

from mobiledetect import MobileDetect

from .mobile_useragents import mobile_useragents
from .nonmobile_useragents import nonmobile_useragents
from .pervendor_useragents import pervendor_useragents


class BaseUserAgentsTest(unittest.TestCase):
    def assert_is_mobile(self, useragent):
        mb = MobileDetect(useragent=useragent)
        self.assertTrue(mb.is_mobile(), msg="Failed mobile useragent string: '%s'" % useragent)

    def assert_is_not_mobile(self, useragent):
        mb = MobileDetect(useragent=useragent)
        self.assertFalse(mb.is_mobile(), msg="Failed non mobile useragent string: '%s'" % useragent)

    def assert_mobile_vendor(self, vendor, useragent):
        mb = MobileDetect(useragent=useragent)
        self.assertTrue(mb.is_mobile(), msg="Failed vendor '%s' mobile useragent string: '%s'" % (vendor, useragent))


class MobileUserAgentsTest(BaseUserAgentsTest):
    def test_mobile_useragents(self):
        for ua in mobile_useragents:
            self.assert_is_mobile(ua)


class NonMobileUserAgentsTest(BaseUserAgentsTest):
    def test_nonmobile_useragents(self):
        for ua in nonmobile_useragents:
            self.assert_is_not_mobile(ua)


class PerVendorUserAgentsTest(BaseUserAgentsTest):
    def test_pervendor_useragents(self):
        for vendor, uas in pervendor_useragents.iteritems():
            for ua in uas:
                self.assert_mobile_vendor(vendor, ua)

