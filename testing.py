import unittest
import starter
import json
from datetime import datetime

class TestGitLabCounter(unittest.TestCase):

    def test_getClosedIssues(self):
        jsonTest = starter.getClosedIssues()
        self.assertGreater(len(jsonTest), 1)

    def test_countPoints(self):
        dictTest1 = {"estimated" : 3, "done" : 4}
        jsonString = '{"labels": ["4pts", "Est. 3pts", "Servidor"]}'
        jsonTest = json.loads(jsonString)

        test1 = starter.countPoints(jsonTest)

        self.assertEqual(test1["estimated"], dictTest1["estimated"])
        self.assertEqual(test1["done"], dictTest1["done"])

        dictTest2 = {"estimated" : 4, "done" : 4}
        jsonString = '{"labels": ["4pts", "Servidor"]}'
        jsonTest = json.loads(jsonString)
        
        test2 = starter.countPoints(jsonTest)
        self.assertEqual(test2["estimated"], dictTest2["estimated"])
        self.assertEqual(test2["done"], dictTest2["done"])

    def test_stringToDate(self):
        dateObject = datetime.strptime("2017-04-04T07:44:06.327Z", "%Y-%m-%dT%H:%M:%S.%fZ")
        self.assertEqual(dateObject.year, int(2017))       
        self.assertEqual(dateObject.month, int(4))
        self.assertEqual(dateObject.day, int(4))

if __name__ == '__main__':
    unittest.main()
