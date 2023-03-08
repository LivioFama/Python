import requests.api
import re
import yaml

url = 'https://api.domainsdb.info/v1/domains/search?domain=syntra.be'
response = requests.get(url)
data = response.text
output=[]


#Regex van de datum (jaar - maand - dag)

create_regex = r'\d{4}'
create_year = re.search(create_regex, response.text).group(0)

create_regex = r'[-.\/](0[1-9]|1[012])'
create_month = re.search(create_regex, response.text).group(1)

create_regex = r'-(\d{2})+T'
create_day = re.search(create_regex, response.text).group(1)

#Regex van het ip adres

ip_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
ip_adres = re.search(ip_regex, response.text).group(0)

#Regex van het Land

land = re.search(r'"country":\s*"(.*?)"', data).group(1)

#Regex van de provider

provider_regex = r'(?<=\.)belnet(?=\.)'                     
provider = re.search(provider_regex, response.text).group(0)



output.append({'ip': ip_adres, 'land': land, 'Dag': create_day, 'Maand': create_month, 'Jaar': create_year, 'Provider': provider})

#conversie naar een YAML file
if response.status_code == 200:
    data = response.json()
    yaml_data = yaml.dump({"Examen opdracht": output})

    with open('output.yaml', 'w') as file:
        file.write(yaml_data)

    print("YAML output written to output.yaml")
else:
    print(f"Error fetching data: {response.status_code} - {response.text}")
