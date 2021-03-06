"""End-to-End testing"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BucketAppFunctionalityTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1400, 1000)
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_bucketlistapp(self):
        self.browser.get(self.live_server_url)

        # asserting index page was successfully reached
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('myBucketlist', body.text)

        # asserting a successful registration
        self.browser.find_element_by_name('username').send_keys('laddeos')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('laddeos')
        v_password_field = self.browser.find_element_by_name('verify_password')
        v_password_field.send_keys('laddeos')
        v_password_field.send_keys(Keys.RETURN)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('My Bucket Lists', body.text)

        # add a new bucketlist
        self.browser.find_element_by_id('add-list-icon').click()
        block = WebDriverWait(self.browser, 60)
        block.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, 'modal')
            )
        )
        self.browser.find_element_by_name(
            'name').send_keys('A new bucketlist')
        self.browser.find_element_by_xpath(
            "//button[contains(text(),'Add')]").click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('A new bucketlist', body.text)

        # add a new bucketitem
        self.browser.find_element_by_id(
            'bucketitem-input').send_keys('A new bucketitem')
        self.browser.find_element_by_class_name(
            'add-item-btn').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('A new bucketitem', body.text)

        # assert successful logout
        self.browser.find_element_by_id('logout').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('myBucketlist', body.text)
