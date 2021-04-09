#!/usr/bin/env python
import argparse

import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "saterraform.json"
from google.oauth2 import service_account
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery


def list_projects():
	credentials = GoogleCredentials.get_application_default()

	service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

	request = service.projects().list()
	while request:
		response = request.execute()

		for project in response.get('projects', []):
			# TODO: Change code below to process each `project` resource:
			print(project)

		request = service.projects().list_next(previous_request=request, previous_response=response)



def list_service_accounts(project_id):
	"""Lists all service accounts for the current project."""
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('iam', 'v1', credentials=credentials)
	service_accounts = service.projects().serviceAccounts().list(
		name='projects/' + project_id).execute()

	for account in service_accounts['accounts']:
		try:
			print("SA=" + account['displayName'], end=' ')
			print(account['email'], end=' ')
			print(account['description'], end='')
			secret_keys = service.projects().serviceAccounts().keys().list(
				name=account["name"]).execute()

			for key_item in secret_keys['keys']:
				# print(key_item)
				longKeyName = key_item["name"]
				keyname = longKeyName[longKeyName.rfind("/") + 1:]

				print("Key=" + keyname + " keyType=" + key_item["keyType"] + " validBeforeTime=" + key_item[
					"validBeforeTime"])

			print(' ')
		except KeyError as ke:
			print("")
	return service_accounts


# [START iam_list_roles]
def list_roles(project_id):
	"""Lists roles."""

	# pylint: disable=no-member
	credentials = GoogleCredentials.get_application_default()
	service = discovery.build('iam', 'v1', credentials=credentials)
	roles = service.roles().list(
		parent='projects/' + project_id).execute()['roles']
	for role in roles:
		print(role['name'])

def list_iam(project_id):
	"""Lists roles."""

	# pylint: disable=no-member
	credentials = GoogleCredentials.get_application_default()
	service = googleapiclient.discovery.build(
		'cloudresourcemanager', 'v1', credentials=credentials)
	policy_response = service.projects().getIamPolicy(resource=project_id, body={}).execute()
	members = set()
	for binding in policy_response['bindings']:
		members |= set(binding['members'])

	print('\n'.join(sorted(members)))

# [END iam_list_roles]
def main():
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawDescriptionHelpFormatter)

	subparsers = parser.add_subparsers(dest='command')

	# List
	list_parser = subparsers.add_parser(
		'salist', help=list_service_accounts.__doc__)
	list_parser.add_argument('project_id')
	list_parser = subparsers.add_parser(
		'roles', help=list_service_accounts.__doc__)
	list_parser.add_argument('project_id')
	list_parser = subparsers.add_parser(
		'projects', help=list_service_accounts.__doc__)
	list_parser = subparsers.add_parser(
		'list_iam', help=list_service_accounts.__doc__)
	list_parser.add_argument('project_id')
	args = parser.parse_args()

	if args.command == 'salist':
		list_service_accounts(args.project_id)
	if args.command == 'roles':
		list_roles(args.project_id)
	if args.command == 'projects':
		list_projects()
	if args.command == 'list_iam':
		list_iam(args.project_id)

if __name__ == '__main__':
	main()
