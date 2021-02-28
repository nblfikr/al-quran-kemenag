import time 
import json
import os.path
import requests 
from os import path
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 


def is_exist(filename):
	return path.exists(filename)



def make_dir(dir_name):
	if os.makedirs('res'):
		return True


def generate_daftar():
	# url = "https://quran.kemenag.go.id/sura/1"
	url = 'https://quran.kemenag.go.id'

	driver = webdriver.Chrome('./driver/chromedriver')
	driver.get(url)

	time.sleep(5)

	html = driver.page_source 

	soup = BeautifulSoup(html, "html.parser")
	section = soup.find('section', {'class': 'g-py-100'})
	li = section.find_all('li')

	daftar = []

	for item in li:
		div = item.find('div')
		a = item.find_all('a')
		span = item.find('span')

		nomor = div.text
		arab = a[1].text
		arti = span.text
		plain = a[0].text

		index = plain.find("(")
		index2 = plain.find(")")
		x = slice(index)	# nama surah
		y = slice(index + 1, index2)	# ayat

		daftar.append({
			"nomor": div.text,
			"ayat": plain[y],
			"surah": plain[x].strip(),
			"surah_arab": a[1].text,
			"terjemah": span.text
		})

		with open('res/daftar.json', 'w') as file:
			json.dump(daftar, file, indent=4)

		# break


def generate_surah():
	for x in range(114):
		filename = str(x + 1)
		if not is_exist('res/surah/' + filename + '.json'):
			url = "https://quran.kemenag.go.id/sura/" + filename
		  
			driver = webdriver.Chrome('./driver/chromedriver')  
			driver.get(url)  

			time.sleep(5)  # time for manual scrolling haha..
			  
			html = driver.page_source 

			soup = BeautifulSoup(html, "html.parser") 
			div = soup.find('div', {'id' : 'list-aya'}) 
			section = div.find_all('section', {'class': 'container'})
			 
			result = []

			for i, item in enumerate(section):
				p = item.find_all('p')
				arab = p[0].text
				
				if filename == 1:
					terjemah = p[2].text
				else:
					terjemah = p[1].text


				index = arab.find("-")
				x = slice(index)

				result.append({
					"ayat": i + 1,
					"lafal": arab[x].strip(),
					"terjemah": terjemah,
				})
				with open('res/surah/' + filename + '.json', 'w') as file:
					json.dump(result, file, indent=4)
				# break

			# driver.close()
			driver.quit()
		# break



def main():
	dir_name = 'res'
	file_name = 'daftar.json'

	if not is_exist(dir_name):
		os.makedirs('res')
		generate_daftar()	# Generating daftar.json

	generate_surah()	# Generating surah to res/surah/



if __name__ == "__main__":
	main()