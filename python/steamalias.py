# creates a unique vanity url by searching the steam web api
# useful for bot creation

from random import choice, randrange
from sys import exit
import requests

strings = [
  'cypher', 'persephone', 'seraph', 'switch', 'smith',
  'tank', 'mifune', 'keymaker', 'oracle', 'apoc',
  'merovingian', 'lock', 'niobe', 'link', 'neo',
  'ghost', 'ajax', 'morpheus', 'malachi', 'trinity',
  'architect', 'mouse', 'dozer'
]

api_key = ''

while True:

  name = choice(strings) + str(randrange(123, 789))

  params = {
    'key': api_key,
    'vanityurl': name,
    'format': 'json',
    'url_type': 1
  }

  resp = requests.get('https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/', params, timeout=8)

  if resp.status_code != 200:
    exit('Steam web API returned non 200 code.')

  if resp.json()['response']['success'] == 1:
    continue

  print(name)
  print('http://steamcommunity.com/id/' + name)

  input('\n')
