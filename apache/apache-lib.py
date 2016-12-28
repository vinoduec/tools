import urllib
import urllib2
import json
from subprocess import Popen, PIPE
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
PageSize = 100

projects = ["HADOOP", "YARN", "MAPREDUCE", "HDFS"]

def get_git_log(branch):
    git_command = ["git", "log", "--oneline", branch]
    process = Popen(git_command, stdout=PIPE)
    (output, err) = process.communicate()
    return output


def get_tickets(fixVersion):
    return_value = []
    for p in projects:
        jql = "project in (%s) and fixVersion = %s " % (p, fixVersion)
        start = 0;
        while True:
            parameters = urllib.urlencode({'jql': jql, 'startAt': start, 'maxResults': PageSize})
            final_url ="https://issues.apache.org/jira/rest/api/2/search?%s" % parameters
            response = urllib2.urlopen(final_url)
            result = json.loads(response.read())
            for issue in result["issues"]:
                key = issue["key"]
                summary = issue["fields"]["summary"]
                fixVersion0 = "None"
                if len(issue["fields"]["fixVersions"]) >=1:
                    fixVersion0 = issue["fields"]["fixVersions"][0]["name"]
                return_value.append({"key" : key, "summary": summary, "fix-version": fixVersion0})
            response.close()
            start += PageSize
            if (len(result["issues"]) < PageSize) :
                break;
    print "Total number of tickets in : ", fixVersion, len(return_value)
    return return_value

def diff_version_to_branch(args):
  fixVersion = "2.7.2"
  branch = "branch-2.7.2"
  fixVersion = args.fix_version
  branch = args.branch
  print "===== Looking at release: " + fixVersion + ", branch: " + branch + " ====="
  tickets_on_jira = get_tickets(fixVersion)
  git_log = get_git_log(branch)
  for ticket in tickets_on_jira:
      if git_log.find(ticket["key"]) == -1:
          print ticket["key"], ticket["summary"]

project_dirs = [    "hadoop-common-project/hadoop-common",
                    "hadoop-hdfs-project/hadoop-hdfs",
                    "hadoop-mapreduce-project",
                    "hadoop-yarn-project"
               ]

def get_changes_txt(branch):
    output = ""
    for p in project_dirs:
        with open( p + '/CHANGES.txt', 'r') as myfile:
            output = output + "\n" + myfile.read()
    return output

def diff_version_to_changes(args):
  fixVersion = args.fix_version
  branch = args.branch
  print "===== Looking at release: " + fixVersion + ", branch: " + branch + " ====="
  tickets_on_jira = get_tickets(fixVersion)
  changes = get_changes_txt(branch)
  for ticket in tickets_on_jira:
      if changes.find(ticket["key"]) == -1:
          print ticket["key"]

def diff_version_to_version(args):
    versionA = args.fix_version_a
    versionB = args.fix_version_b
    tickets_on_jira_for_A = get_tickets(versionA)
    tickets_on_jira_for_B = get_tickets(versionB)
    # print "a: "
    # print tickets_on_jira_for_A
    # print "b: "
    #print tickets_on_jira_for_B
    ticketsA = []
    ticketsB = {}
    for ticket in tickets_on_jira_for_A:
        ticketsA.append(ticket["key"])
    for ticket in tickets_on_jira_for_B:
        ticketsB[ticket["key"]] = True
    for ticket in ticketsA:
        if not ticket in ticketsB:
            print ticket
    return

def get_tickets_in_version(args):
    tickets_on_jira = get_tickets(args.fix_version)
    for ticket in tickets_on_jira:
        print ticket

import argparse

class ApacheLib(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Apache Release Management utility.')
        subparsers = parser.add_subparsers(dest="subparser_name", help='sub-command help')
        
        parser_diff_version_to_branch = subparsers.add_parser('diff-version-to-branch', help='Show tickets marked against version but not in branch')
        parser_diff_version_to_branch.add_argument('fix_version', help='fix_version help')
        parser_diff_version_to_branch.add_argument('branch', help='branch help')

        parser_diff_version_to_changes = subparsers.add_parser('diff-version-to-changes', help='Show tickets marked against version A but not in CHANGES.txt files')
        parser_diff_version_to_changes.add_argument('fix_version', help='fix_version help')
        parser_diff_version_to_changes.add_argument('branch', help='fix_version help')
        
        parser_diff_version_to_version = subparsers.add_parser('diff-version-to-version', help='Show tickets marked against version A but not in version B')
        parser_diff_version_to_version.add_argument('fix_version_a', help='fix_version help')
        parser_diff_version_to_version.add_argument('fix_version_b', help='fix_version help')
        
        parser_get_tickets_in_version = subparsers.add_parser('get-tickets-in-version', help='Show tickets marked against version')
        parser_get_tickets_in_version.add_argument('fix_version', help='fix_version help')
        
        args = parser.parse_args()

        if args.subparser_name == 'diff-version-to-branch':
            diff_version_to_branch(args)
        elif args.subparser_name == 'diff-version-to-version':
            diff_version_to_version(args)
        elif args.subparser_name == 'diff-version-to-changes':
            diff_version_to_changes(args)
        elif args.subparser_name == 'get-tickets-in-version':
            get_tickets_in_version(args)

if __name__ == '__main__':
  ApacheLib()
