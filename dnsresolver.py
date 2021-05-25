#!/bin/python3

from dns import resolver
import argparse
import os

parser = argparse.ArgumentParser(description='To parse an url and a wordlist')
parser.add_argument('--url', type=str, nargs='+', help='parse an url as: http://example.com')
parser.add_argument('--wordlist', type=str, nargs='+', help='parse an wordlist as: /usr/share/wordlist/somewords.txt')
args = parser.parse_args()

def verify_path(path):
	if path is None or path == '':
		return False
	else:
		if os.path.isfile(str(path)):
			return True
		else:
			return False


wordlist = args.wordlist[0] if args.wordlist is not None else ''
url = args.url[0] if args.url is not None else ''


class Main():

	def __init__(self, url, wordlist):
		self.wordlist = str(wordlist).strip()
		self.url = str(url).strip()

	def verify(self):
		if self.url == '':
			print(f'[!!!] You need pass a url with falg "--url"')
			exit()
		if not verify_path(self.wordlist):
			print(f'[!] The path [{self.wordlist}] is not valid!')
			exit()

		return True

	def test(self, domain):
		url = self.url.replace('https://', '').replace('http://','')
		url = f'{domain}.{url}'

		try:
			tst = resolver.resolve(url)
			return [True, tst.nameserver]
		except Exception as e:
			return [False]

	def start(self):
		if self.verify():
			self.run()
	
	def run(self):
		try:
			print(f'[***] Reading wordlist: "{self.wordlist}"')
			with open(self.wordlist, 'rb') as f:
				subdomains = [i.decode('utf-8').replace('\n','') for i in f.readlines()]
				print(f'[+] Testing domains... \n')
				for sdm in subdomains:
					test = self.test(sdm)
					if test[0]:
						print(f'Possible valid subdomain: [{sdm}] -> [{test[1]}]')
				f.close()
		except Exception as e:
			print(f'[!] Error when open file [{self.wordlist}].')
			print(e)
			exit()


if __name__ == '__main__':
	app = Main(url, wordlist)
	app.start()
