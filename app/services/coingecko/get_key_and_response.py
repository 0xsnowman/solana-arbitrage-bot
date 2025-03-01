def get_demo_key():
    f = open("/home/vikas/Documents/CG_demo_key.json")
    key_dict = json.load(f)
    return key_dict["key"]

use_demo = {
           "accept": "application/json",
           "x-cg-demo-api-key" : get_demo_key() 
}

def get_response(endpoint, headers, params, URL):
    url = "".join((URL, endpoint))
    response = rq.get(url, headers = headers, params = params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to fetch data, check status code {response.status_code}")