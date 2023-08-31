""" Notion API
    For Notion API to work follow these steps:
    1. Create a new integration at https://www.notion.com/my-integrations or use an existing one
    2. Link the integration to the workspace
    3. Copy the integration's API token
    4. Copy the database ID from the database's URL
"""

import requests, json, os


def read_database(database_id: str, headers: dict):
    """
    Reads a Notion database and returns a JSON file.
    """

    read_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    res = requests.request("POST", read_url, headers=headers)

    data = res.json()

    return data


def read_page(page_id, headers):
    """
    Reads a Notion page and returns a JSON file.
    """

    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    res = requests.request("GET", url, headers=headers)
    print("read_page: ", res.status_code)

    data = res.json()

    return data


def read_table(table_id, page_num, headers, save=False):
    if not os.path.isfile(f"./data/pages/page_{page_num}_table.json"):
        url = f"https://api.notion.com/v1/blocks/{table_id}/children?page_size=100"
        res = requests.request("GET", url, headers=headers)
        print(res.status_code)

    if save:
        data = res.json()
        with open(f"./data/pages/page_{page_num}_table.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)