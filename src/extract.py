import requests

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
 
def get_package_resources(package_name):
    url = f"{base_url}/api/3/action/package_show"
    params = { "id": package_name }
    package = requests.get(url, params=params)
    package.raise_for_status() # safety net
    return package.json()['result']['resources']
 
# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):
 
       # for datastore_active resources:
       if resource["datastore_active"]:
 
           # To get all records in CSV format:
           url = f"{base_url}/datastore/dump/{resource['id']}"
           resource_dump_data = requests.get(url).text
           print(resource_dump_data)
 
           # To selectively pull records and attribute-level metadata:
           url = f"{base_url}/api/3/action/datastore_search"
           p = { "id": resource["id"] }
           resource_search_data = requests.get(url, params = p).json()["result"]
           print(resource_search_data)
           # This API call has many parameters. They're documented here:
           # https://docs.ckan.org/en/latest/maintaining/datastore.html
 
       # To get metadata for non datastore_active resources:
       if not resource["datastore_active"]:
           url = f"{base_url}/api/3/action/resource_show?id={resource['id']}"           
           resource_metadata = requests.get(url).json()
           print(resource_metadata)