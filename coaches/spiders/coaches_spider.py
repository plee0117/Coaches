from scrapy import Spider, Request
from coaches.items import CoachesItem
import re
import math

coaching_positions = ['Coach:', 'Offensive Coordinator:', 'Defensive Coordinator:', 'General Manager:']

class CoachesSpider(Spider):
	name = 'coaches_spider'
	allowed_domains = ['www.pro-football-reference.com']
	start_urls = ['https://www.pro-football-reference.com/years']

	def parse(self, response):
		result_urls_nfl = ['https://www.pro-football-reference.com/years/' + str(year) + '/' for year in range(1966,2019)]
		result_urls_afl = ['https://www.pro-football-reference.com/years/' + str(year) + '_AFL' + '/' for year in range(1966,1970)]
		result_urls = result_urls_afl + result_urls_nfl
		# print(result_urls)

		for url in result_urls[:]:
			yield Request(url = url, callback = self.parse_season_page, meta= {'url': url})
			# print(url)
			# print('='*40)


	def parse_season_page(self, response):
		url = response.meta['url']
		year = re.findall('\d+', url)[-1]
		if int(year) < 1970:
			if re.findall('AFL/\Z', url):
				div_id = 'AFL'
			else:
				div_id = 'NFL'

			teams = response.xpath('//div[@id="div_'+div_id+'"]//tr//a/text()').extract()
			
			for team in teams:
				team_url = 'https://www.pro-football-reference.com' + \
				response.xpath('//div[@id="div_'+div_id+'"]//a[text()="'+team+'"]/@href').extract()[0]
				
				wins = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="wins"]/text()').extract()[0]
				losses = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="losses"]/text()').extract()[0]
				try: #response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]:
					ties = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]
				except:
					ties = 0

				yield Request(url = team_url, callback = self.parse_team_page, 
					meta = {'year': year, 'team': team, 'wins': wins, 'losses': losses, 'ties': ties})

			# else:
			# 	teams = response.xpath('//div[@id="div_NFL"]//tr//a/text()').extract()
				
			# 	for team in teams:
			# 		team_url = 'https://www.pro-football-reference.com' + \
			# 		response.xpath('//div[@id="div_NFL"]//a[text()="'+team+'"]/@href').extract()[0]
					
			# 		wins = response.xpath('//div[@id="div_NFL"]//tr[th//a/text()="'+team+'"]/td[@data-stat="wins"]/text()').extract()[0]
			# 		losses = response.xpath('//div[@id="div_NFL"]//tr[th//a/text()="'+team+'"]/td[@data-stat="losses"]/text()').extract()[0]
			# 		ties = response.xpath('//div[@id="div_NFL"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]
					
			# 		yield Request(url = team_url, callback = self.parse_team_page, 
			# 			meta = {'year': year, 'team': team, 'wins': wins, 'losses': losses, 'ties': ties})
		else:
			div_id = 'AFC'
			teams = response.xpath('//div[@id="div_'+div_id+'"]//tr//a/text()').extract()
			
			for team in teams:
				team_url = 'https://www.pro-football-reference.com' + \
				response.xpath('//div[@id="div_'+div_id+'"]//a[text()="'+team+'"]/@href').extract()[0]
				
				wins = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="wins"]/text()').extract()[0]
				losses = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="losses"]/text()').extract()[0]
				try: #response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]:
					ties = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]
				except:
					ties = 0

				yield Request(url = team_url, callback = self.parse_team_page, 
					meta = {'year': year, 'team': team, 'wins': wins, 'losses': losses, 'ties': ties})

			div_id = 'NFC'
			teams = response.xpath('//div[@id="div_'+div_id+'"]//tr//a/text()').extract()
			
			for team in teams:
				team_url = 'https://www.pro-football-reference.com' + \
				response.xpath('//div[@id="div_'+div_id+'"]//a[text()="'+team+'"]/@href').extract()[0]
				
				wins = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="wins"]/text()').extract()[0]
				losses = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="losses"]/text()').extract()[0]
				try: #response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]:
					ties = response.xpath('//div[@id="div_'+div_id+'"]//tr[th//a/text()="'+team+'"]/td[@data-stat="ties"]/text()').extract()[0]
				except:
					ties = 0

				yield Request(url = team_url, callback = self.parse_team_page, 
					meta = {'year': year, 'team': team, 'wins': wins, 'losses': losses, 'ties': ties})



	def parse_team_page(self, response):
		items = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p').extract()
		year = response.meta['year']
		team = response.meta['team']
		wins = response.meta['wins']
		losses = response.meta['losses']
		ties = response.meta['ties']

		# print(items)
		for item_no in range(1,len(items)):

			# print(item_no, ' / ', len(items))
			if response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/strong/text()').extract():
				position = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/strong/text()').extract()[0]
				if position == 'Other Notable Asst.:':
					people = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']//@href').extract()
					names = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/a/text()').extract()
					positions = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/text()').extract()[1:]
					positions = list(map(lambda y: str.strip(y), filter(lambda x: re.search('[(]',x),positions)))
					positions = [z.strip('(') for z in (y.strip(')') for y in (x.strip(' and') for x in positions))]
					for idx in range(0,len(names)):
						position = positions[idx]
						link = people[idx]
						name = names[idx]
						# print(name, link, position)
						item = CoachesItem()
						item['name'] = name
						item['link'] = link
						item['position'] = position
						item['team'] = team
						item['year'] = year
						item['win'] = wins
						item['loss'] = losses
						item['tie'] = ties
						yield item


					# write to file should happen here
					
				elif position in coaching_positions:
				#check to see if the item is relavent; need a list of positions to check for

					people = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']//@href').extract()
					#check to see if multiple people are listed
					if len(people) == 1:
						name = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/a/text()').extract()[0]
						link = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/a/@href').extract()[0]
						#saving to file should happen here
						# print(name, link, position)
						item = CoachesItem()
						item['name'] = name
						item['link'] = link
						item['position'] = position
						item['team'] = team
						item['year'] = year
						item['win'] = wins
						item['loss'] = losses
						item['tie'] = ties
						yield item
					else:
						#mid-season change
						names = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/a/text()').extract()
						records = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p['+str(item_no)+']/text()').extract()
						
						#take out the unnecessary items from records list
						records = list(filter(lambda x: re.search('[(]',x),records))

						# print(names)
						# print(records)
						for idx in range(0,len(people)):
							name = names[idx]
							link = people[idx]
							try: #re.findall('\d+',records[idx]):
								record = re.findall('\d+',records[idx])
								# print(record)
								wins = record[0]
								losses = record[1]
								ties = record[2]
								# print(name, link, position)
							except:
								pass
							item = CoachesItem()
							item['name'] = name
							item['link'] = link
							item['position'] = position
							item['team'] = team
							item['year'] = year
							item['win'] = wins
							item['loss'] = losses
							item['tie'] = ties
							yield item
							
				else:
					continue
			else:
				continue


				# for person in people:

	# 	link = response.xpath('//div[@data-template="Partials/Teams/Summary"]/p[strong/text()="Coach:"]/a/@href').extract()

