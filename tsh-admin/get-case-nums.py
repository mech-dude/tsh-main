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

while not all_conversations:
    # Prepare conversations endpoint with status of conversations we want and the mailbox.
    conversations_endpoint = 'https://api.helpscout.net/v2/conversations?status=active&mailbox=258043&folder=5650311&page={}'.format(
        page
    )
    r = requests.get(conversations_endpoint, headers=endpoint_headers)
    conversations = r.json()

    # Cycle over conversations in response.
    for conversation in conversations['_embedded']['conversations']:
        if page == conversations['page']['totalPages']:
            all_conversations = True
            continue
        else:
            page += 1

print('T2 Escalated Cases:', len(conversations['_embedded']['conversations']))