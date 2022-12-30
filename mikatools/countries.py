import json, codecs, os

_country_data =  {}
with codecs.open(os.path.join(os.path.dirname(__file__), 'countries.json'), 'r', encoding="utf-8") as jfile:
	_country_data = json.load(jfile)

def supported_languages():
	ls= list(_country_data.keys())
	ls.sort()
	return ls

def supported_countries():
	ls = list(_country_data["fi"])
	ls.sort()
	return ls

def iso_to_country(iso, language):
	return _country_data[language][iso]
