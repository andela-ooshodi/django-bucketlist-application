"""End-to-End testing"""

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BucketAppFunctionalityTestCase(StaticLiveServerTestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1400, 1000)
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def test_bucketlistapp(self):
        self.browser.get(self.live_server_url)

        # asserting index page was successfully reached
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Welcome to myBucketlist', body.text)

        # asserting a successful login
        self.browser.find_element_by_xpath(
            "//button[contains(text(),'Get Started')]").click()
        self.browser.find_element_by_name('username').send_keys('laddeos')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('laddeos')
        password_field.send_keys(Keys.RETURN)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('My bucketlist', body.text)

        # add a new bucketlist
        self.browser.find_element_by_id('add-list-icon').click()
        self.browser.find_element_by_name(
            'name').send_keys('A new bucketlist')
        self.browser.find_element_by_xpath(
            "//button[contains(text(),'Add')]").click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Items', body.text)

        # add a new bucketitem
        self.browser.find_element_by_id('add-item-icon').click()
        self.browser.find_element_by_name(
            'name').send_keys('A new bucketitem')
        self.browser.find_element_by_xpath(
            "//button[contains(text(),'Add')]").click()
        self.browser.refresh()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('A new bucketitem', body.text)

        # delete bucketitem
        self.browser.find_element_by_class_name('delete-item').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('A new bucketitem', body.text)

        # delete bucketlist
        self.browser.find_element_by_id('back').click()
        self.browser.find_element_by_class_name('delete-list').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('A new bucketlist', body.text)

        # assert successful logout
        self.browser.find_element_by_id('logout').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Welcome to myBucketlist', body.text)
