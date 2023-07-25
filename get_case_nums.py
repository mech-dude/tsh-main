import csv
import datetime
import requests

# The token endpoint.
auth_endpoint = 'https://api.helpscout.net/v2/oauth2/token'

# Preparing our POST data.
post_data = ({
    'grant_type': 'client_credentials',
    'client_id': 'cnWB3FZahRsE6TsYhm1srOflEAlX1N5B',
    'client_secret': 'NdRn1g5jimsUfgF62KzlYUaV5BgvIlbz'
})

# Send the data.
r = requests.post(auth_endpoint, data=post_data)

# Save our token.
token = r.json()['access_token']

all_conversations = False
page = 1

# Prepare our headers for all endpoints using token.
endpoint_headers = {
    'Authorization': 'Bearer {}'.format(token)
}

# Creates our file, or rewrites it if one is present.
with open('cases.csv', mode="w", newline='', encoding='utf-8') as fh:
    # Define our columns.
    columns = ['ID', 'Number', 'Customer Name', 'Customer email addresses', 'Assignee', 'Status', 'Subject', 'Created At',
               'Closed At', 'Closed By', 'Resolution Time (seconds)']  
    csv_writer = csv.DictWriter(fh, fieldnames=columns) # Create our writer object.
    csv_writer.writeheader() # Write our header row.
    
    while not all_conversations:
        # Prepare conversations endpoint with status of conversations we want and the mailbox.
        conversations_endpoint = 'https://api.helpscout.net/v2/conversations?status=all&mailbox=258043&folder=5650311&page={}'.format(
            page
        )
        r = requests.get(conversations_endpoint, headers=endpoint_headers)
        conversations = r.json()

        # Cycle over conversations in response.
        for conversation in conversations['_embedded']['conversations']:

            # If the email is missing, we won't keep this conversation.
            # Depending on what you will be using this data for,
            # You might omit this.
            if 'email' not in conversation['primaryCustomer']:
                print('Missing email for {}'.format(customer_name))
                continue

            # Prepare customer name.
            customer_name = '{} {}'.format(
                conversation['primaryCustomer']['first'],
                conversation['primaryCustomer']['last']
            )

            # Prepare assignee, subject, and closed date if they exist.
            assignee = '{} {}'.format(conversation['assignee']['first'], conversation['assignee']['last']) \
                if 'assignee' in conversation else ''
            subject = conversation['subject'] if 'subject' in conversation else 'No subject'
            closed_at = conversation['closedAt'] if 'closedAt' in conversation else ''

            # If the conversation has been closed, let's get the resolution time and who closed it.
            closed_by = ''
            resolution_time = 0
            if 'closedByUser' in conversation and conversation['closedByUser']['id'] != 0:
                closed_by = '{} {}'.format(
                    conversation['closedByUser']['first'], conversation['closedByUser']['last']
                )
                createdDateTime = datetime.datetime.strptime(conversation['createdAt'], "%Y-%m-%dT%H:%M:%S%z")
                closedDateTime = datetime.datetime.strptime(conversation['closedAt'], "%Y-%m-%dT%H:%M:%S%z")
                resolution_time = (closedDateTime - createdDateTime).total_seconds()

            csv_writer.writerow({
                'ID': conversation['id'],
                'Number': conversation['number'],
                'Customer Name': customer_name,
                'Customer email addresses': conversation['primaryCustomer']['email'],
                'Assignee': assignee,
                'Status': conversation['status'],
                'Subject': subject,
                'Created At': conversation['createdAt'],
                'Closed At': closed_at,
                'Closed By': closed_by,
                'Resolution Time (seconds)': resolution_time
            })

        if page == conversations['page']['totalPages']:
            all_conversations = True
            continue
        else:
            page += 1

print('T2 Escalated Cases:', len(conversations['_embedded']['conversations']))