#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import re
import sys
import urllib
import urlparse
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")

## External Libraries
import mechanize
from bs4 import BeautifulSoup

class WeChall:
	def __init__(self, cookie  =None):
		self.browser  =mechanize.Browser()

		## Set attributes
		self.browser.set_handle_equiv(False)
		self.browser.set_handle_gzip(False)
		self.browser.set_handle_robots(False)
		self.browser.set_debug_redirects(True)
		self.browser.set_debug_http(True)

		if cookie is None:
			self.browser.addheaders  =[("User-Agent", "")]
		else:
			self.browser.addheaders  =[("User-Agent", ""), ("Cookie", "WC=%s" % cookie)]

		## Once visit the top page
		self.browser.open("http://www.wechall.net/")


	def show_wc_message(self, html):
		soup  =BeautifulSoup(html, "html.parser")
		text  =soup.get_text()

		gwf_messages  =soup.find_all(class_="gwf_messages")
		gwf_errors    =soup.find_all(class_="gwf_errors")

		if len(gwf_errors) != 0:
			print "-" * 40
			for h2 in soup.find_all("h2"): print h2.text
			print "-" * 40
			for error in gwf_errors: print error.text
		if len(gwf_messages) != 0:
			print "-" * 40
			for h2 in soup.find_all("h2"): print h2.text
			print "-" * 40
			for message in gwf_messages: print message.text


	def open(self, problem_url):
		## Parse URL into objects
		self.url_obj  =urlparse.urlparse(problem_url)

		## Visit the problem page
		response   =self.browser.open(self.url_obj.geturl())
		self.html  =response.read()
		self.soup  =BeautifulSoup(self.html, "html.parser")
		self.text  =self.soup.get_text()

		## Detect and select the submssion form
		for form in self.browser.forms():
			if form.action == self.browser.geturl():
				self.browser.form  =form

		self.show_wc_message( self.html )
		"""
		self.html  =response.read()
		self.soup  =BeautifulSoup(self.html, "html.parser")
		self.text  =self.soup.get_text()

		## Detect and select the submssion form
		for form in self.browser.forms():
			if form.action == self.browser.geturl():
				self.browser.form  =form

		gwf_messages  =self.soup.find_all(class_="gwf_messages")
		gwf_errors    =self.soup.find_all(class_="gwf_errors")

		if len(gwf_errors) != 0:
			print "-" * 40
			for h2 in self.soup.find_all("h2"): print h2.text
			print "-" * 40
			for error in gwf_errors: print error.text
		if len(gwf_messages) != 0:
			print "-" * 40
			for h2 in self.soup.find_all("h2"): print h2.text
			print "-" * 40
			for message in gwf_messages: print message.text
		"""


	def submit(self, solution):
		self.browser["answer"]  =solution
		response   =self.browser.submit()
		self.show_wc_message( response.read() )

# [EOF]
