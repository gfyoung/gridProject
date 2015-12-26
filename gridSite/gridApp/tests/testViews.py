from django.test import TestCase

import unittest


class BasicUrlAccessTestCase(TestCase):
    def testGetBackSlash(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashGridApp(self):
        response = self.client.get("/gridApp/")
        self.assertEqual(response.status_code, 302)

    def testGetBackSlashGridAppHome(self):
        response = self.client.get("/gridApp/home")
        self.assertEqual(response.status_code, 200)

    def testGetBackSlashGridAppAbout(self):
        response = self.client.get("/gridApp/about")
        self.assertEqual(response.status_code, 200)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashEventId(self):
        response = self.client.get("/gridApp/event/1")
        self.assertEqual(response.status_code, 200)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashEventAll(self):
        response = self.client.get("/gridApp/event/all")
        self.assertEqual(response.status_code, 200)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashVendorId(self):
        response = self.client.get("/gridApp/vendor/1")
        self.assertEqual(response.status_code, 200)

    @unittest.skip("need Facebook auth")
    def testGetBackSlashVendorAll(self):
        response = self.client.get("/gridApp/vendor/all")
        self.assertEqual(response.status_code, 200)
