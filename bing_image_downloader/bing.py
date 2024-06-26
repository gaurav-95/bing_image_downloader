from pathlib import Path
import urllib.request
import urllib
import posixpath
import re

class Bing:
    def __init__(self, query, limit, adult, timeout, filter='', verbose=True):
        self.image_links = []
        self.query = query
        self.adult = adult
        self.filter = filter
        self.verbose = verbose
        self.seen = set()

        assert type(limit) == int, "limit must be an integer"
        self.limit = limit
        assert type(timeout) == int, "timeout must be an integer"
        self.timeout = timeout

        self.page_counter = 0
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}

    def get_filter(self, shorthand):
        if shorthand == "line" or shorthand == "linedrawing":
            return "+filterui:photo-linedrawing"
        elif shorthand == "photo":
            return "+filterui:photo-photo"
        elif shorthand == "clipart":
            return "+filterui:photo-clipart"
        elif shorthand == "gif" or shorthand == "animatedgif":
            return "+filterui:photo-animatedgif"
        elif shorthand == "transparent":
            return "+filterui:photo-transparent"
        else:
            return ""

    def extract_image_links(self, html):
        links = re.findall('murl&quot;:&quot;(.*?)&quot;', html)
        return links

    def fetch_page_html(self, request_url):
        request = urllib.request.Request(request_url, None, headers=self.headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf8')
        return html

    def run(self):
        while len(self.image_links) < self.limit:
            if self.verbose:
                print('\n\n[!!] Indexing page: {}\n'.format(self.page_counter + 1))

            request_url = 'https://www.bing.com/images/async?q=' + urllib.parse.quote_plus(self.query) \
                          + '&first=' + str(self.page_counter) + '&count=' + str(self.limit) \
                          + '&adlt=' + self.adult + '&qft=' + ('' if self.filter is None else self.get_filter(self.filter))
            
            html = self.fetch_page_html(request_url)
            if html == "":
                print("[%] No more images are available")
                break
            
            links = self.extract_image_links(html)
            
            if self.verbose:
                print("[%] Indexed {} Images on Page {}.".format(len(links), self.page_counter + 1))
                print("\n===============================================\n")

            for link in links:
                if len(self.image_links) < self.limit and link not in self.seen:
                    self.seen.add(link)
                    self.image_links.append(link)

            self.page_counter += 1

        print("\n\n[%] Done. Retrieved {} image links.".format(len(self.image_links)))
        return self.image_links
