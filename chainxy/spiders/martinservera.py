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


class Martinservera(scrapy.Spider):

	name = 'martinservera'

	domain = 'https://www.martinservera.se'

	history = []

	output = []

	def __init__(self):

		pass
	
	def start_requests(self):

		url = 'https://www.martinservera.se/Produktkatalog/09'
		
		yield scrapy.Request(url, callback=self.parse)

	def parse(self, response):

		product_list = response.xpath('//div[@class="name-remark-wrap"]//a[@class="product-name pdp-modal-link"]/@href').extract()

		for product in product_list:

			try:

				if product not in self.history:

					yield scrapy.Request(product, callback=self.parse_detail)

					self.history.append(product)

			except Exception as e:

				print('~~~~~~', e)

				pass

		try:
		
			next_page = self.validate(response.xpath('//div[@class="pagination-list-item next"]//a[@class="await-body-loaded pagination-list-link"]//@data-href').extract_first())

			if next_page:

				yield scrapy.Request(next_page, callback=self.parse)

		except Exception as e:

			print('~~~~~~~~', e)

			pass

	def parse_detail(self, response):

		item = ChainItem()

		item['Product_Name'] = ''.join(self.eliminate_space(response.xpath('//div[contains(@class, "content-top")]//h1[contains(@class, "product-title")]//text()').extract()))
		
		data = response.xpath('//*[contains(@class, "data-pair-item")]')

		for pro in data:

			try:

				prop = self.eliminate_space(pro.xpath('.//text()').extract())

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
			except:

				pass

		yield item

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
