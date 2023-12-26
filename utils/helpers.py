import requests

def get_data(url:str = None, page:str = None ):

    try:

        if page:
            url += f'&cursor={page}'

        r = requests.get(url=url)

        if r.status_code==200:
            data = r.json()['data']
            if len(data['items'])>0:
                return data
            print(r.json())
            return None
        else:
            print(f'error occured for {url}')
            print(r.status_code, r.json()['error']['message'], sep='\n')
            raise Exception
    except Exception as e:
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
            else:
                data[k] = v
        data['user_id'] = task_data['user_id']
        data['organization_id'] = task_data['organization_id']
        data['project_id'] = task_data['project_id']
        data['term'] = keyword
        data['sentiment'] = 'unknown'
        data['tone'] = 'unknown'
        result.append(data)

    return result