# ----------------------------------------------------------------------------
# Welcome to the real world, I hope you'll enjoy it!
# Author:           Steve-P42
# Description:      Getting the latest most up-voted HackerNews
# Creation date:    2021-03-13 16:51:39
# Status:           in development
# ----------------------------------------------------------------------------
# %%
import requests
from bs4 import BeautifulSoup

# %%
class TopHackerNews:
    def __init__(self):
        self.source = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/news?p=2']
        self.page_contents = self.get_page_contents()


    def get_page_contents(self):
        res1 = requests.get(self.source[0])
        res2 = requests.get(self.source[1])
        soup = BeautifulSoup(res1.text + res2.text, "html.parser")
        return soup

# %%

x = TopHackerNews()

print(x.page_contents)

# %%

# %%

# %%

# %%

# %%
