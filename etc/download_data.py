from mikatools import *
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

url = "http://publications.europa.eu/code/fi/fi-5000500.htm"

def get_langs():
	
	html = requests.get(url).text

	soup = BeautifulSoup(html, 'html.parser')
	#open_write("html.html").write(html)
	langselect = soup.find_all("div", {"class": "langselnoscript"})[0]
	langs = [x.text.strip() for x in langselect.find_all("a")]
	return langs

def clean_name(name):
	ranska_panska = ["(l’)", "(le)", "(les)", "(la)"]
	for r in ranska_panska:
		name = name.replace(r, "")
	name = name.replace("/",",").replace(";",",").replace(" "," ").replace("­","").replace("\r\n"," ").split(",")
	res = [x.split("(")[0].strip() for x in name]
	if len(res) == 1:
		return res
	return [x for x in res if len(x) > 1]

def get_tables():
	langs = get_langs()
	res = {}
	for lang in tqdm(langs):
		lang_res = {}
		urli = url.replace("fi", lang)
		html = requests.get(urli).text
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find("table", {"id":"listOfCountriesTable"})
		for row in table.find_all("tr"):
			tds = [x.text for x in row.find_all("td")]
			if len(tds) < 9:
				continue
			if lang in ["et","hu"]:
				tds = tds[0:6] + [tds[5]] + tds[6:]
			if len(tds) < 10:
				continue
			if lang == "mt":
				tds = tds[1:]
			if len(tds) == 11:
				tds = tds[0:2] + tds[3:]
			country_name = clean_name(tds[1])
			long_name = clean_name(tds[2])
			iso_code = clean_name(tds[3])[0]
			capital = clean_name(tds[4])
			demonym = clean_name(tds[5])
			adjective = clean_name(tds[6])
			currency_name = clean_name(tds[7])[0]
			currency_code = clean_name(tds[8])[0]
			lang_res[iso_code.lower()] = {"country_name":country_name, "long_name": long_name, "capital":capital,"demonym":demonym,"adjective":adjective,"currency_name":currency_name,"currency_code":currency_code}
		res[lang.lower()] = lang_res
	json_dump(res, "countries.json")

def check_data():
	cs = json_load("countries.json")
	for c in cs:
		print(c)
		print(cs[c]["fi"])


#get_tables()
check_data()