#!/usr/bin/env python

###
# Name: get_deprecated.py
# Date: 11-02-18
# Author: Benjamin Leung
# Description: This script generates a report of jobs run recently using deprecated Ansible playbooks (universal templates)
###

import datetime
import urllib2
import base64
import getpass
import pprint
import json
import csv

DEPRECATED_RELEASES=[
    "1.00",
    "2.00",
    "3.00",
    "4.00"
]

class CSWT(object):

    def __init__(self, username, password, env="dev"):
        self.tower_api="https://tower.%s.ansible.apps.baml.com/api/v2/" % (env)
        base64string=base64.encodestring('%s:%s' % (username, password))[:-1]
        self.authheader="Basic %s" % (base64string)

    def request_get(self, url):
        req=urllib2.Request(url)
        req.add_header("Authorization", self.authheader)
        response=urllib2.urlopen(req).read()
        return eval(response.replace('null','None').replace('false','False').replace('true','True'))

    def get_projects(self, project_names):
        '''
        Return a dictionary of project names and project IDs based on a list of project names that are passed in
        '''

        project_lookup=self.tower_api+"projects/?"

        for project in project_names:
            project_lookup+="or__name=CSWTDEVOPS/Release/%s&" % (project)

        project_lookup_response=self.request_get(project_lookup)
        
        projects={}

        for project in project_lookup_response.get('results'):
            projects[project.get('id')]=project.get('name')
  
        return projects

    def job_query(self, projects, age):
        '''
        Return a list containing the details of jobs that have been run recently and that use one of a list of projects. A list of projects are required to be passed in. 
        The default for age of jobs is 30 days.
        '''

        lookup_date=(datetime.date.today() - datetime.timedelta(days=age)).isoformat()

        job_lookup=self.tower_api+"jobs/?page_size=200&created__gt=%s&" % (lookup_date)

        for job_id, name in projects.iteritems():
            job_lookup+="or__project=%s&" % (job_id)

        job_lookup_response=self.request_get(job_lookup)
    
        return job_lookup_response
    
    def parse_jobs(self, jobs, report_file):
        '''
        Parse list of job results for relevant details.
        '''

        parsed_jobs=[]

        for job in jobs.get('results'):
            summary=job.get('summary_fields')

            job_details={
                'created': job.get('created'),
                'release': summary.get('project').get('name'),
                'created_by': summary.get('created_by').get('username'),
                'job_template': summary.get('job_template').get('name') if summary.get('job_template') else job.get('name')
            }

            parsed_jobs.append(job_details)

        job_data=open(report_file, 'w')
        csv_writer=csv.writer(job_data)
        header=parsed_jobs[0].keys()
        csv_writer.writerow(header)
        for job in parsed_jobs:
            csv_writer.writerow(job.values())
        job_data.close()

        return parsed_jobs

def parse_args():
    import argparse

    parser=argparse.ArgumentParser()
    parser.add_argument("-e", "--environment", help="Ansible Tower environment. Options: dev, prod", dest="environment", default="dev")
    parser.add_argument("-f", "--file", help="File or path to write report to", dest="report_file", default="./deprecation_report.csv")
    parser.add_argument("-d", "--days", help="Number of days worth of jobs to run the report again", dest="age", default=30, type=int)

    return parser.parse_args()

if __name__=="__main__":
    # Prompt for Ansible Tower credentials
    username=raw_input("Enter your Ansible Tower log-on username: ")
    password=getpass.getpass("Password: ")

    args=parse_args()

    cswt_lookup=CSWT(username, password, env=args.environment)

    projects=cswt_lookup.get_projects(DEPRECATED_RELEASES)
    jobs=cswt_lookup.job_query(projects, args.age)
    cswt_lookup.parse_jobs(jobs, report_file=args.report_file)
