from bs4 import BeautifulSoup 
import urllib2
import requests

def match_class(target):
	def do_match(tag):
		classes = tag.get('class', [])
		return all(c in classes for c in target)
	return do_match

def get_html(url):
	html_content = urllib2.urlopen(url)
	return BeautifulSoup(html_content, "html.parser")


def get_from_web_md(text):
	
	response = ''

	if text[:2] == "hy":
			
		search_url = 'http://www.webmd.com/search/2/results?query='+text


		page_url = ''

		for link in get_html(search_url).find_all(match_class(["search-results-doc-title"])):
				page_url = link.find_all('a')[0]['href']
				break


		response += '{ "overview": "' + get_html(page_url).find_all(match_class(["teaser_fmt"]))[0].find('p').getText() + '" },'


		symptoms_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "3"})[1]['href']
		symptoms_url2 = get_html(symptoms_url).findAll(match_class(["link-title"]))[1]['href']
		symptoms = get_html(symptoms_url2).findAll(match_class(["article-page"]))[0].findAll('ul')[0].getText()
		response += ' { "symptoms": "' + symptoms + '" },'


		measure_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "4"})[1]['href']
		measure_url2 = get_html(measure_url).findAll(match_class(["link-title"]))[1]['href']
		measure = get_html(measure_url2).findAll(match_class(["article-page"]))[0]
		measure1 = measure.findAll('p')[0].getText()
		measure2 = measure.findAll('ul')[0].getText()
		response += ' { "measure": "' + measure1 + measure2 + '" },'


		nextsteps_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "5"})[1]['href']
		nextsteps_url2 = get_html(nextsteps_url).findAll(match_class(["link-title"]))[0]['href']
		nextsteps = get_html(nextsteps_url2).findAll(match_class(["article-page"]))[0].findAll('ul')[0].getText()
		response += ' { "nextsteps": "' + nextsteps + '" },'
		
		response += ' { "organ": "2212" } '


		print response		

		return response

	elif text[:2] == "al":
		search_url = 'http://www.webmd.com/search/2/results?query='+text

		page_url = ''

		for link in get_html(search_url).find_all(match_class(["search-results-doc-title"])):
				page_url = link.find_all('a')[0]['href']
				break

		response += '{ "overview": "' + get_html(page_url).find_all(match_class(["teaser_fmt"]))[0].find('p').getText() + '" },'


		symptoms_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "3"})[1]['href']
		symptoms_url2 = get_html(symptoms_url).findAll(match_class(["link-title"]))[0]['href']
		symptoms = get_html(symptoms_url2).findAll(match_class(["article-page"]))[0]
		symptoms1 = symptoms.findAll('p')[3].getText()
		symptoms2 = symptoms.findAll('p')[5].getText()
		symptoms3 = symptoms.findAll('p')[7].getText()
		symptoms4 = symptoms.findAll('p')[9].getText()
		symptoms5 = symptoms.findAll('p')[11].getText()
		response += ' { "symptoms": "' + symptoms1 + symptoms2 + symptoms3 + symptoms4 + symptoms5 + '" },'


		measure_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "4"})[1]['href']
		measure_url2 = get_html(measure_url).findAll(match_class(["link-title"]))[0]['href']
		measure = get_html(measure_url2).findAll(match_class(["article-page"]))[0].findAll("section")[2]
		measure1 = measure.findAll('p')[0].getText()
		measure2 = measure.findAll('ul')[0].getText()
		response += ' { "measure": "' + measure1 + measure2 + '" },'


		nextsteps_url = get_html(page_url).findAll(attrs = {"data-metrics-link" : "5"})[1]['href']
		nextsteps_url2 = get_html(nextsteps_url).findAll(match_class(["link-title"]))[0]['href']
		nextsteps = get_html(nextsteps_url2).findAll(match_class(["article-page"]))[0].findAll('ul')[0].getText()
		response += ' { "nextsteps": "' + nextsteps + '" },'
		
		response += ' { "organ": "1295" } '
		
		print response

		return response		

	else:
		return ''		


