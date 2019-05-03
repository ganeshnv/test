Deprecated Job Template Search
get_deprecated.py is a script used to generate a report on jobs that are being run using a deprecated version of an Ansible playbook.

At this version, deprecated job template versions are hard coded into the script until it can be determined how to tag Ansible projects as deprecated. This can be modified at the head of the script under the variable DEPRECATED_RELEASES.

Arguments
Arguments	Flag	Description	Required?	Default
environment	-e	Ansible Tower environment	no	dev
file	-f	File to store the generated report	no	./deprecation_report.csv
days	-d	Age of jobs to filter against	no	30
Notes
In order to view all jobs being run with the CSWTDEVOPS projects, you must be an organization admin of those projects.

This script is currently limited to pulling a maxmimum of 200 jobs. Reduce the number of days to filter against to get all jobs running deprecated versions of job templates in a more recent time period.

Linux
Usage
Clone the repository and change into the scripts directory

git clone ssh://git@github.com/devops/ansible.git
cd ansible/scripts
Run the script. Arguments are optional, but they will generate the report from the development Ansible Tower on any jobs run in the past 30 days into deprecation_report.csv

./get_deprecated.py -e dev -f /tmp/deprecation_report.csv -d 30
This will generate a report of jobs that were run using deprecated versions of playbooks in the past 30 days and in the development Ansible Tower environment to /tmp/deprecation_report.csv.

Windows
Requirements
The following tools are required to run this script from your Windows desktop. These can be requested as https://mytechnology.bankofamerica.com

Python
Git Bash
Usage
After these two have been installed, clone the git repository into a local directory using Git Bash:

cd ~
git clone https://github.com/scm/scm/devops/ansible.git
From the command prompt, run the script using python:

"C:\Program Files\Python27\python.exe" "C:\Users\nbkid\ansible\scripts\get_deprecated.py -e dev -f C:\Users\nbkid\deprecation_report.csv -d 30"
This will generate a report of jobs that were run using deprecated versions of playbooks in the past 30 days and in the development Ansible Tower environment to C\Users\nbkid\deprecation_report.csv.
