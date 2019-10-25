import requests
from bs4 import BeautifulSoup
import time
import csv
import random
import re
import pandas as pd
import numpy as np

with open('coaches.csv', 'r') as f:
	urls = pd.read_csv(f, dtype = {'year':str})
	
urls['team'] = ['St. Louis Cardinals (NFL)' if i == 'St. Louis Cardinals' else i for i in urls['team']]
urls['as'] = 'https://en.wikipedia.org/wiki/' + urls['year'] + ' ' + urls['team'] + ' season'
url_list = sorted([re.sub(' ','_',x) for x in urls['as'].unique()])

bad_urls = ['https://en.wikipedia.org/wiki/1968_Oakland_Raiders_season', \
			'https://en.wikipedia.org/wiki/1987_Washington_Redskins_season',\
		   'https://en.wikipedia.org/wiki/1998_San_Francisco_49ers_season',\
		   'https://en.wikipedia.org/wiki/1999_San_Francisco_49ers_season']

headers = {'User-Agent': \
		   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) \
		   Chrome/58.0.3029.110 Safari/537.36'}

def assign_staff(list_of_folks, name_of_csv, team, year, indx):
	for idx in list_of_folks:
#         print(idx)
		staff = {'name':'','position':'','team': team,'year':year,'wikilink':''}
		name = ''
		position = ''
		wikilink = ''
		try:
			if re.search('—', idx):
				if (idx.find('—')>idx.find(' href') and re.search(' href',idx)):
					position = re.findall('<i>(.*)</i>', idx)[0]
					wikilink = re.findall(' href="(.*)" title="', idx)[0]
					staff['wikilink'] = 'https://en.wikipedia.com' + wikilink
					name = re.findall('">(.*)</a>', idx)[0]
					
				else:
					position = re.findall('(.*)—', idx)[0]

					if re.search(' href',idx):
						name = re.findall('">(.*)</a>', idx)[0]
						wikilink = re.findall(' href="(.*)" title="', idx)[0]
						staff['wikilink'] = 'https://en.wikipedia.com' + wikilink
					else:
						name = re.findall('—(.*)', idx)[0]
					
			elif re.search('–', idx):
				if (idx.find('–')>idx.find(' href') and re.search(' href',idx)):
					position = re.findall('<i>(.*)</i>', idx)[0]
					wikilink = re.findall(' href="(.*)" title="', idx)[0]
					staff['wikilink'] = 'https://en.wikipedia.com' + wikilink
					name = re.findall('">(.*)</a>', idx)[0]
					
				else:
					position = re.findall('(.*)–', idx)[0]

					if re.search(' href',idx):
						name = re.findall('">(.*)</a>', idx)[0]
						wikilink = re.findall(' href="(.*)" title="', idx)[0]
						staff['wikilink'] = 'https://en.wikipedia.com' + wikilink
					else:
						name = re.findall('–(.*)', idx)[0]

			elif re.search('-', idx):
				position = re.findall('(.*)-', idx)[0]
				
				if re.search(' href',idx):
					name = re.findall('">(.*)</a>', idx)[0]
					wikilink = re.findall(' href="(.*)" title="', idx)[0]
					staff['wikilink'] = 'https://en.wikipedia.com' + wikilink
				else:
					name = re.findall('-(.*)', idx)[0]


			staff['name'] = name.strip()
			staff['position'] = position.strip()
			
		except Exception as e:
			print('Error inside', e, team, year, idx)
			
		if staff['name'] != '':
			name_of_csv.writerow(staff.values())
		else:
			continue
		

with open('nfl.csv', 'w', encoding='utf-8') as csvfile:
	nfl = csv.writer(csvfile)

	for indx, url in enumerate(url_list):
		block_of_text = ''
		if any([url == i for i in bad_urls]):
			continue
		try:
#             print(url)
			year = re.findall('https://en.wikipedia.org/wiki/(\d*)_',url)[0]
			team = re.sub('_',' ',re.findall('\d+_(.*)_season',url)[0])
			response = requests.get(url, headers = headers)
			text = BeautifulSoup(response.text, 'html.parser')
			
			if url == 'https://en.wikipedia.org/wiki/1976_Tampa_Bay_Buccaneers_season':
				block_of_text = re.findall('id="Coaching_staff_2"(.*)</tbody>', str(text), flags = re.DOTALL)
			
			elif re.search('id="Coaching_Staff"',str(text)):
				block_of_text = re.findall('id="Coaching_Staff"(.*)</tbody>', str(text), flags = re.DOTALL)

			elif re.search('id="Staff"',str(text)):
				block_of_text = re.findall('id="Staff"(.*)</tbody>', str(text), flags = re.DOTALL)

			elif re.search('id="Staff/Coaches"',str(text)):    
				block_of_text = re.findall('id="Staff/Coaches"(.*)</tbody>', str(text), flags = re.DOTALL)
				
			block_of_staff = re.split('</tbody>',block_of_text[0])[0]
			list_of_staff = re.findall('<li>(.*)</li>',block_of_staff)
			assign_staff(list_of_staff, nfl, team, year, indx)

			time.sleep(random.randint(1,3))
			
		except Exception as e:
			print(e, str(url))

