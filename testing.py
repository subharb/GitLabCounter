import unittest
import starter
import json
from datetime import datetime
from pprint import pprint

class TestGitLabCounter(unittest.TestCase):

    def test_getClosedIssues(self):
        jsonTest = starter.getIssues(True)
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

    def test_getInfoIssue(self):
        issue = starter.getInfoIssue(323)        
        self.assertEqual(issue["project_id"], 17)

    def test_updateIssue(self):
        issueId = 175;
        #starter.getInfoIssue(issueId)
        
        data = "due_date=2017-02-14"
        result = starter.updateIssue(issueId, data)
        self.assertEqual(result["due_date"], "2017-02-14")

        data = "due_date=2017-02-13"
        result = starter.updateIssue(issueId, data)
        self.assertEqual(result["due_date"], "2017-02-13")
    
    def test_postOnSlack(self):
        starter.postOnSlack("Testing")

if __name__ == '__main__':
    unittest.main()
