
import requests
import json

def get_header(api_key) -> dict[str, str]:
  """
  get_header controi o header padrão para utilização da api, de acordo com o indicado pela documentação.
  :param api_key: chave de acesso da api, como str

  :return: dict a ser utilizado em chamadas para a api
  """ 
  headers = dict()
  headers["X-GitHub-Api-Version"] = "2022-11-28"
  headers["Accept"] = "application/vnd.github+json"
  headers["Authorization"] = "Bearer {}".format(api_key)
  return headers

def get_user_from_api(api_key, user) -> tuple[int,dict]:
  """
  get_user_from_api coleta a informação de um único usuario, e retorna juntamente ao statuscode da requisição.
  :param api_key: chave de acesso da api, como str
  :param user: login do usuário a ser coletado

  :return: tupla com o statuscode, como int e o objeto json do retorno, em caso de status 200
  """ 
  url = "https://api.github.com/users/{}".format(user)
  headers = get_header(api_key)
  resp = requests.get(url, headers=headers)
  if resp.status_code != 200:
    return resp.status_code, None
  return resp.status_code, json.loads(resp.text)

def tail_rec_get_followers_from_api(api_key, user, page=1, acc_load=None) -> list[list[str]]:
  """
  tail_rec_get_followers_from_api coleta a lista de seguidores um único usuario, utilizando recursividade para lidar com a paginação da API.
  Levanta erro em caso de falha.
  O retorno como list[list] foi escolhido para facilitar a transição para um dataframe.

  :param api_key: chave de acesso da api, como str
  :param user: login do usuário
  :param page: indice de paginação
  :acc_load: lista cumulativa para o retorno, a ser passsado para a recursividade.

  :return: lista de 'logins' dos usuários seguidores como list[list[str]]
  """ 
  if acc_load is None:
      acc_load = []
  url = "https://api.github.com/users/{}/followers".format(user)
  headers = get_header(api_key)
  parameters = {
     "per_page": 100,
     "page": page,
  }
  resp = requests.get(url, headers=headers, params=parameters)
  if resp.status_code != 200:
   raise Exception("Failed to get followers, {} was returned from api.".format(resp.text))
  currentFollowers = [[user["login"]] for user in json.loads(resp.text)]
  acc_load = acc_load + currentFollowers
  if("next" not in resp.headers.get("link","")):
    return acc_load
  return tail_rec_get_followers_from_api(api_key, user, page +1, acc_load)