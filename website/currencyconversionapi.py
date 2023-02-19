import requests
import json

def exchange_rates(AMOUNT,FROMcurrency,TOcurrency):
  #opening the token file to get the API key
  with open('./website/TOKEN.txt') as file_in:
      token = file_in.readline()

  #parameters for the API request
  parameters = {
    'access_key': token
  }

  #API request
  response = requests.get(f"https://v6.exchangerate-api.com/v6/{token}/pair/{FROMcurrency}/{TOcurrency}/{AMOUNT}", parameters)

  #cloning the created json file from the API
  with open('conversions.json', 'w') as file_out:
      json.dump(response.json(), file_out, indent=2)