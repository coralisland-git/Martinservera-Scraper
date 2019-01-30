# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import math

import time

import pdb

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

# from selenium.webdriver.support import expected_conditions as ec

import selenium.webdriver.support.expected_conditions as EC



class Martinservera_sel(scrapy.Spider):

	name = 'martinservera_sel'

	domain = 'https://www.martinservera.se'

	history = []

	output = []

	source_list = []


	def __init__(self):
	
		chrome_options = webdriver.ChromeOptions()

		self.driver = webdriver.Chrome('chromedriver.exe')

		
	def start_requests(self):

		url = 'https://www.martinservera.se'
		
		yield scrapy.Request(url, callback=self.parse)


	def parse(self, response):

		self.driver.get('https://www.martinservera.se/Produktkatalog/09')

		time.sleep(5)

		index = 0

		page_limit = 189

		while True:

			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")

			time.sleep(2)

			self.driver.execute_script("window.scrollTo(0, 2*document.body.scrollHeight/5);")

			time.sleep(2)

			self.driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/5);")

			time.sleep(2)

			self.driver.execute_script("window.scrollTo(0, 4*document.body.scrollHeight/5);")

			time.sleep(2)

			self.driver.execute_script("window.scrollTo(0, 5*document.body.scrollHeight/5);")

			time.sleep(2)

			product_list = self.driver.find_elements_by_xpath('//div[contains(@class, "product-tile product-has-data")]//a[contains(@class, "product-image-wrap pdp-modal-link")]')

			# product_list = self.driver.find_elements_by_xpath('//div[@class="product-list row"]/div')

			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/6);")

			time.sleep(2)

			for idx, product in enumerate(product_list):

				idx = idx + 1

				# try:

				if idx / 4 == 1 :
					self.driver.execute_script("window.scrollTo(0, 2*document.body.scrollHeight/6);")

				if idx / 4 == 2 :
					self.driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/6);")

				if idx / 4 == 3 :
					self.driver.execute_script("window.scrollTo(0, 4*document.body.scrollHeight/6);")

				if idx / 4 == 4 :
					self.driver.execute_script("window.scrollTo(0, 5*document.body.scrollHeight/6);")


				if idx / 4 == 5 :
					self.driver.execute_script("window.scrollTo(0, 6*document.body.scrollHeight/6);")

				time.sleep(4)

				product.click()

				time.sleep(4)

				source = self.driver.page_source.encode("utf8")

				source = etree.HTML(source)
				
				self.source_list.append(source)

				# for source in self.source_list:

				item = ChainItem()

				item['Product_Name'] = ''.join(self.eliminate_space(source.xpath('//div[@class="ms-bootstrap-modal modal fade product-detail-modal show"]//div[contains(@class, "content-top")]//h1[contains(@class, "product-title")]//text()')))
				
				data = source.xpath('//div[@class="ms-bootstrap-modal modal fade product-detail-modal show"]//*[contains(@class, "data-pair-item")]')

				for prop in data:

					try:

						prop = self.eliminate_space(prop.xpath('.//text()'))

						if 'Bruttovikt'.lower() in prop[0].lower():

							item['Weight'] = prop[1]

						if 'Enhet'.lower() in prop[0].lower():

							item['Unit'] = prop[1]

						if 'Antal per enhet'.lower() in prop[0].lower():

							item['Number_Per_Unit'] = prop[1]

						if 'Lagringsform'.lower() in prop[0].lower():

							item['Storage_Form'] = prop[1]

						if 'Antal/hel'.lower() in prop[0].lower():

							item['Number_Whole_Package'] = prop[1]

						if 'Art.nr leveran'.lower() in prop[0].lower():

							item['Art_Nr_Supplier'] = prop[1]

						if 'Artikelnr'.lower() in prop[0].lower():

							item['Article_Number'] = prop[1]

						if 'Land'.lower() in prop[0].lower():

							item['Country'] = prop[1]

						if 'GTIN'.lower() in prop[0].lower():

							item['GTIN'] = prop[1]

						if 'Kategori'.lower() in prop[0].lower():

							item['Category'] = prop[1]

					except Exception as e:

						print('~~~~~~~~~~~~~~~', e)

						pass

				yield item

				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ms-bootstrap-modal modal fade product-detail-modal show"]//span[@class="ms-popup-close"]'))).click()

				# except Exception as e:

				# 	print('~~~~~~~~~~~~~~~', e)

				# 	pdb.set_trace()

				# 	time.sleep(3)

				# 	pass

			self.driver.find_element_by_xpath('//div[@class="pagination-list-item next"]//a[@class="await-body-loaded pagination-list-link"]').click()

			time.sleep(5)

			index += 1

			if index >= page_limit:
				break;




	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '' and self.validate(item) != ':':

	            tmp.append(self.validate(item))

	    return tmp
