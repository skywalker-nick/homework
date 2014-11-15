from novaclient.v1_1.client import Client

context = {
    'user': 'admin',
    'auth_token': '22b07d939fa544769bf625753ecaec18',
    'tenant': '7dfd3b6a98664f7cb78808f57b7984da',
}

# nova_compute_url
url = 'http://192.168.242.10:8774/v2/7dfd3b6a98664f7cb78808f57b7984da'
PROXY_AUTH_URL = 'http://192.168.242.10:5000/v2.0'

client = Client(username=context['user'],
                api_key=context['auth_token'],
                project_id=context['tenant'],
                bypass_url=url,
                auth_url=PROXY_AUTH_URL)
client.client.auth_token = context['auth_token']
client.client.management_url = url

print dir(client)
print client.flavors.list()
