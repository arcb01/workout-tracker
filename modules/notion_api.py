import requests, json, os


def read_database(database_name, database_id, headers):
    #if not os.path.isfile(f'./data/{database_name}.json'):
    read_url = f'https://api.notion.com/v1/databases/{database_id}/query'
    res = requests.request("POST", read_url, headers=headers)
    #print("read_db: ", res.status_code)

    data = res.json()
    with open(f"./data/{database_name}.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


def read_page(page_id, page_num, headers):
    if not os.path.isfile(f"./data/pages/page_{page_num}.json"):
        url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        res = requests.request("GET", url, headers=headers)
        print("read_page: ", res.status_code)

        data = res.json()
        with open(f"./data/pages/page_{page_num}.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)


def read_table(table_id, page_num, headers, save=False):
    if not os.path.isfile(f"./data/pages/page_{page_num}_table.json"):
        url = f"https://api.notion.com/v1/blocks/{table_id}/children?page_size=100"
        res = requests.request("GET", url, headers=headers)
        print(res.status_code)

    if save:
        data = res.json()
        with open(f"./data/pages/page_{page_num}_table.json", "w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)