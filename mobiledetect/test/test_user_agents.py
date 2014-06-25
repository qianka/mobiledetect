import os
import json
import unittest

from ..detect import MobileDetect

class UserAgentsTest(unittest.TestCase):
    def setUp(self):
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_user_agents.json')
        self.user_agents = json.load(open(filename))

    def test_is_mobile(self):
        for entry in self.user_agents['user_agents']:
            if not 'mobile' in entry:
                continue
            useragent = entry['user_agent']
            is_mobile = MobileDetect(useragent=useragent).is_mobile()
            if entry['mobile']:
                self.assertTrue(is_mobile, msg="Failed mobile useragent string: '%s'" % useragent)
            else:
                self.assertFalse(is_mobile, msg="Failed mobile useragent string: '%s'" % useragent)

    def test_is_tablet(self):
        for entry in self.user_agents['user_agents']:
            if not 'tablet' in entry:
                continue
            useragent = entry['user_agent']
            is_tablet = MobileDetect(useragent=useragent).is_tablet()
            if entry['tablet']:
                self.assertTrue(is_tablet, msg="Failed tablet useragent string: '%s'" % useragent)
            else:
                self.assertFalse(is_tablet, msg="Failed tablet useragent string: '%s'" % useragent)
