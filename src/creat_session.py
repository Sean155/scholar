from .utils import config, client, RequestError, HTTPStatusError
from typing import Union
def creat_session() -> Union[str, None]:
    
    try:
        res_list = client.post(config.over_five_wall_url, 
                        json={
                            'cmd': 'sessions.list',
                            #'session': config.session
                })
    except RequestError as e:
        return f'Failed to  creat a FlareSolverr session. \nPlease check the url: "{e.request.url}" and make sure that you have deployed FlareSolverr.'
    except HTTPStatusError as e:
        return f'Failed to  creat a FlareSolverr session: {e.response.status_code}. \nPlease check the url: "{e.request.url}" and make sure that you have deployed FlareSolverr.'
    if res_list.is_error:
        return f'Failed to  creat a FlareSolverr session: {res_list.status_code} {res_list.reason_phrase}. \nPlease check the url: "{res_list.request.url}" and make sure that you have deployed FlareSolverr.'
    
    if not res_list.json()['status'] == 'ok':
        return f"Failed to  creat a FlareSolverr session. \n '{res_list.json()['message']}'"

    if not res_list.json()['sessions']:
        res_create = client.post(config.over_five_wall_url, 
                                json={
                                    'cmd': 'sessions.create',
                                    'session': config.session
                            })
    else:
        return 
    if not res_create.json()['status'] == 'ok':
        return f"Failed to  creat a FlareSolverr session. \n '{res_create.json()['message']}'"
