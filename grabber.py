#!/usr/local/bin/python3
# coding: utf-8 

# Settings
threads_count = 10
user_agents   = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'}
proxies       = {
 #"http" : '149.56.106.104:3128',
 #"https": '149.56.106.104:3128',
}

# Import modules
import os
from requests import get
from random import choice
from threading import Thread
from bs4 import BeautifulSoup
from strgen import StringGenerator

# Print logo
print('''
 █░░ ░▀░ █▀▀▀ █░░█ ▀▀█▀▀   █▀▀ █░░█ █▀▀█ █▀▀█ ▀▀█▀▀ █▀▀ █▀▀█
 █░░ ▀█▀ █░▀█ █▀▀█ ░░█░░   ▀▀█ █▀▀█ █░░█ █░░█ ░░█░░ █▀▀ █▄▄▀
 ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░░▀ ░░▀░░   ▀▀▀ ▀░░▀ ▀▀▀▀ ▀▀▀▀ ░░▀░░ ▀▀▀ ▀░▀▀
                                          Created by LimerBoy
''')

# Create images directory
if not os.path.exists('images'):
	os.mkdir('images')

# Save image to file
def save(url):
	file = url.split('/')[-1]
	try:
		data = get(url, allow_redirects = True, headers = user_agents, proxies = proxies)
	except:
		pass
	else:
		path = 'images/' + file
		open(path, 'wb').write(data.content)
		if os.path.exists(path):
			print('[+] File ' + file + ' saved. Size: ' + str(os.path.getsize(path)) + ' bytes')

# Scan function
def scan():
	while True:
		# Random url
		random = StringGenerator('[\h]{6}').render().lower()
		url    = 'https://prnt.sc/' + random
		# Make a GET request to get HTML
		content = get(url, timeout = 3, headers = user_agents, proxies = proxies).text
		# Parse HTML to get page title
		soup  = BeautifulSoup(content, 'html.parser')
		# Check if Cloudflare block request
		if 'Cloudflare' in soup.title.get_text().split():
			print('[-] Cloudflare blocked request!')
			break
		# Try to download image
		else:
			try:
				image = soup.img['src']
			except TypeError:
				continue
			else:
				if image.startswith('http'):
					save(image)

# Start threads
for i in range(1, threads_count):
	thread = Thread(target = scan)
	thread.start()
	print('[*] Starting thread: ' + '[' + str(i) + '/' + str(threads_count) + ']')