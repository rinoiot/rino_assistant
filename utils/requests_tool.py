import requests


def requests_get(api_url, api_key, params):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url=api_url, headers=headers, params=params, timeout=5)
    response.raise_for_status()
    return response.json()


def requests_post(api_url, api_key, data):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url=api_url, headers=headers, data=data,
                             timeout=5)
    response.raise_for_status()
    return response.json()
