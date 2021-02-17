import configparser
from imgurpython import ImgurClient

config = configparser.ConfigParser()
config.read('auth.ini')

client_id = config.get('credenials','client_id')
client_secret = config.get('credenials','client_secret')
client = ImgurClient(client_id,client_secret)
items = client.gallery()
print(items)