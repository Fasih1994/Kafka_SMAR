import requests
from retrying import retry
import json


@retry(stop_max_attempt_number=3, wait_fixed=3000)
def get_data(url:str = None, page:str = None, *args, **kwargs):

    try:

        if page:
            url += f'&cursor={page}'

        r = requests.get(url=url, *args, **kwargs)

        if r.status_code==200:
            data = r.json()['data']
            if len(data['items'])>0:
                return data
            return None
        elif str(r.status_code).startswith('5'):
            print(f'Received 524 status code. Retrying...')
            raise Exception('Retry due to 5xx status code')

        else:
            print(f'error occured for {r.url}')
            print(r.status_code, r.json()['error']['message'], sep='\n')
            raise Exception
    except Exception as e:
        print(r.status_code)
        print(str(e))

def join_list(array:list = None)-> str:
    array = [item for item in array if isinstance(item, str)]
    if len(array)>0:
        joined = "--|--".join(array)
        return joined
    return ""

def transform_data(items:list=None, keyword: str=None, task_data: dict=None)->list:
    result = []

    for item in items:
        data = {}
        for k, v in item.items():
            if k == 'attached_videos' and v != None:
                data[k] = v[0]['url']

            if isinstance(v, list):
                data[k] = join_list(v)
            elif isinstance(v, dict):
                data[k] = json.dumps(v)
            else:
                data[k] = v
        data['user_id'] = task_data['user_id']
        data['organization_id'] = task_data['organization_id']
        data['project_id'] = task_data['project_id']
        data['sentiment'] = 'unknown'
        data['tone'] = 'unknown'
        if keyword:
            data['term'] = keyword
        result.append(data)

    return result