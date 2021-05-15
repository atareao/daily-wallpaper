import unittest
import os
import sys
sys.path.insert(1, 'src')
from systemdu import SystemdUser
from systemdu import USER_PATH

TEST_TIMER_FILE = 'test.timer'
TEST_SERVICE_FILE = 'test.service'


class TestSystemdUser(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_TIMER_FILE):
            os.remove(TEST_TIMER_FILE)
        if os.path.exists(TEST_SERVICE_FILE):
            os.remove(TEST_SERVICE_FILE)
        with open(TEST_TIMER_FILE, 'w') as fw:
            fw.write('[Unit]\n')
            fw.write('Description=Test Timer every 5 minutes\n')
            fw.write('\n')
            fw.write('[Timer]\n')
            fw.write('OnCalendar=minutely\n')
            fw.write('\n')
            fw.write('[Install]\n')
            fw.write('WantedBy=timers.target\n')

        with open(TEST_SERVICE_FILE, 'w') as fw:
            fw.write('[Unit]\n')
            fw.write('Description=Test Service\n')
            fw.write('\n')
            fw.write('[Service]\n')
            fw.write('Type=oneshot\n')
            fw.write('ExecStart=echo "Test timer"\n')

    def test_install(self):
        systemdu = SystemdUser()
        systemdu.install(TEST_TIMER_FILE)
        self.assertTrue(os.path.exists(os.path.join(USER_PATH, TEST_TIMER_FILE)))
        systemdu.install(TEST_SERVICE_FILE)
        self.assertTrue(os.path.exists(os.path.join(USER_PATH, TEST_SERVICE_FILE)))

    def test_enable(self):
        try:
            systemdu = SystemdUser()
            systemdu.install(TEST_TIMER_FILE)
            self.assertTrue(os.path.exists(os.path.join(USER_PATH, TEST_TIMER_FILE)))
            systemdu.install(TEST_SERVICE_FILE)
            self.assertTrue(os.path.exists(os.path.join(USER_PATH, TEST_SERVICE_FILE)))
            systemdu.enable(TEST_TIMER_FILE)
            self.assertTrue(systemdu.is_enabled(TEST_TIMER_FILE))
        finally:
            systemdu.disable(TEST_TIMER_FILE)

    def test_start(self):
        try:
            systemdu = SystemdUser()
            systemdu.install(TEST_TIMER_FILE)
            systemdu.install(TEST_SERVICE_FILE)
            systemdu.enable(TEST_TIMER_FILE)
            systemdu.start(TEST_TIMER_FILE)
            self.assertTrue(systemdu.is_active(TEST_TIMER_FILE))
        finally:
            systemdu.stop(TEST_TIMER_FILE)
            systemdu.disable(TEST_TIMER_FILE)

    def test_stop(self):
        try:
            systemdu = SystemdUser()
            systemdu.install(TEST_TIMER_FILE)
            systemdu.install(TEST_SERVICE_FILE)
            systemdu.enable(TEST_TIMER_FILE)
            systemdu.start(TEST_TIMER_FILE)
            self.assertTrue(systemdu.is_active(TEST_TIMER_FILE))
            systemdu.stop(TEST_TIMER_FILE)
            self.assertFalse(systemdu.is_active(TEST_TIMER_FILE))
        finally:
            systemdu.stop(TEST_TIMER_FILE)
            systemdu.disable(TEST_TIMER_FILE)

    def test_disable(self):
        try:
            systemdu = SystemdUser()
            systemdu.install(TEST_TIMER_FILE)
            systemdu.install(TEST_SERVICE_FILE)
            systemdu.enable(TEST_TIMER_FILE)
            systemdu.start(TEST_TIMER_FILE)
            self.assertTrue(systemdu.is_active(TEST_TIMER_FILE))
            systemdu.stop(TEST_TIMER_FILE)
            self.assertFalse(systemdu.is_active(TEST_TIMER_FILE))
            systemdu.disable(TEST_TIMER_FILE)
            self.assertFalse(systemdu.is_enabled(TEST_TIMER_FILE))
        finally:
            systemdu.stop(TEST_TIMER_FILE)
            systemdu.disable(TEST_TIMER_FILE)

    def test_uninstall(self):
        try:
            systemdu = SystemdUser()
            systemdu.install(TEST_TIMER_FILE)
            systemdu.install(TEST_SERVICE_FILE)

            systemdu.enable(TEST_TIMER_FILE)
            systemdu.start(TEST_TIMER_FILE)
            self.assertTrue(systemdu.is_active(TEST_TIMER_FILE))
            systemdu.stop(TEST_TIMER_FILE)
            self.assertFalse(systemdu.is_active(TEST_TIMER_FILE))
            systemdu.disable(TEST_TIMER_FILE)
            systemdu.uninstall(TEST_TIMER_FILE)
            self.assertFalse(os.path.exists(os.path.join(USER_PATH, TEST_SERVICE_FILE)))
        finally:
            systemdu.stop(TEST_TIMER_FILE)
            systemdu.disable(TEST_TIMER_FILE)


    def tearDown(self):
        if os.path.exists(os.path.join(USER_PATH, TEST_TIMER_FILE)):
            os.remove(os.path.join(USER_PATH, TEST_TIMER_FILE))
        if os.path.exists(os.path.join(USER_PATH, TEST_SERVICE_FILE)):
            os.remove(os.path.join(USER_PATH, TEST_SERVICE_FILE))
        if os.path.exists(TEST_TIMER_FILE):
            os.remove(TEST_TIMER_FILE)
        if os.path.exists(TEST_SERVICE_FILE):
            os.remove(TEST_SERVICE_FILE)


if __name__ == '__main__':
    unittest.main()
