'''
:: Process ::
1. Gets the URL from textPreprocessing.py
2. Fetches the HTML using URL and cleans the HTML page (removes unwanted code blocks)
3. Using html2text it converts the cleaned HTML to text.
4. Returns the text to textPreprocessing.py
'''

import requests 
from bs4 import BeautifulSoup
import html5lib
import html2text
import codecs
import sys


class FetchWikipage:

    def __init__(self):
        self.text_maker = html2text.HTML2Text()
        self.define_html2text_parms()  # init html2text params
        self.headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
                }

    def define_html2text_parms(self) -> None:
        self.text_maker.ignore_links = True
        self.text_maker.ignore_images = True
        self.text_maker.escape_all = True  #Escape all special characters. Output is less readable, but avoids corner case formatting issues.
        self.text_maker.unicode_snob = True  # Use unicode throughout instead of ASCII
        self.text_maker.single_line_break = True
        self.text_maker.google_list_indent = 0
        self.text_maker.body_width = 0  # 0 for no wrap
        # self.text_maker.wrap_list_items = True  # Wrap list items during text wrapping.
        self.text_maker.no_automatic_links = True  #Do not use automatic links like https://www.google.com/
        # risky to remove them ?
        self.text_maker.ignore_emphasis = True

    def generateHTML2text(self, url:str=None) -> str:
        try:
            if(url == None or url == ""):
                raise Exception('\033[91m'+"[URL ERR] URL is Missing !!"+'\033[0m')
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200:
                raise Exception('\033[91m'+"[URL ERR] Status = {} !!".format(res.status_code)+'\033[0m')
        except Exception as e:
            print(e)
            print('\033[91m'+"[ERR] Got some error with the URL '{}' !! (Exiting the current execution)".format(url)+'\033[0m')
            sys.exit()

        print("[INFO] Starting with '{:s}' URL".format(url))
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html5lib')

        # TODO: If the heading is imp. then dont remove h1, h2, h3, h4, h5, h6
        # "Further reading", "Publications", "See also", "Others", "Works cited" = class(div-col columns column-width)
        
        # Remove unwanted blocks // HTML preprocessing.
        html_tags = ['script', 'style', 'footer', 'img', 'noscript', 'svg', 'link', 'audio', 'video',
                    'code', 'figcaption', 'figure', 'iframe', 'map', 'picture', 'h1', 'h2', 'h3', 'h4',
                    'h5', 'h6', 'abbr', 'blockquote']
        div_class_list = ["reflist", "hatnote", "mw-indicators", "authority-control", "thumbinner",
                        "noprint", "navbox", "div-col columns column-width", "printfooter",
                        "sistersitebox", "metadata"]
        div_id_list = ["mw-navigation", "toc", "siteSub", "siteNotice", "catlinks", "mwe-popups-svg",
                        "mw-data-after-content"]

        for remove_block in soup.find_all(html_tags):
            remove_block.decompose()
        for remove_block in soup.find_all('div', id=div_id_list):
            remove_block.decompose()
        for remove_block in soup.find_all('div', {"class":div_class_list}):
            remove_block.decompose()
        for remove_block in soup.find_all('a', {"class":["mw-jump-link"]}):
            remove_block.decompose()
        # "biography" is the main table which contains the imp data and "wikitable" holds some notable data.
        for remove_block in soup.find_all('table', {"class":["sistersitebox", "nowraplinks", "biography", "metadata", "wikitable"]}):
            remove_block.decompose()

        # remove sup having reference class
        for remove_block in soup.find_all('sup', {"class":["reference"]}):
            remove_block.decompose()
        
        # remove li having external links at the bottom of the page
        for remove_block in soup.find_all('li'):
            for remove_ele in remove_block.find_all('a', {"class":["external text"]}):
                remove_block.find_parent().decompose()
                break
        
        # remove li having cite tag
        for remove_block in soup.find_all('li'):
            for ele in remove_block.contents:
                if(ele.name == 'cite'):
                    remove_block.find_parent().decompose()
                    break
        
        for remove_block in soup.find_all('p'):
            if(remove_block.contents[0].string in ["Footnotes", "Citations"]):
                remove_block.decompose()
        
        # print(soup.body)
        # with open("./textual_data/test.html", 'w', encoding='utf8') as f:
        #     f.write(str(soup.body))

        content = str(soup.body)
        text = self.text_maker.handle(content)  # html to textual form 
        return text


if __name__ == "__main__":
    page_obj = FetchWikipage()
    print(page_obj.generateHTML2text("https://en.wikipedia.org/wiki/Albert_Einstein")) # => html2txt data