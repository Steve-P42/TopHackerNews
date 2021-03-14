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
import pprint

# %%
class TopHackerNews:
    def __init__(self):
        self.source = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/news?p=2']
        self.page_contents = self.get_page_contents()
        self.links = self.page_contents.select('.storylink')
        self.subtext = self.page_contents.select('.subtext')
        self.counter = 0
        self.result = self.create_custom_hackernews(self.links, self.subtext)


    def get_page_contents(self):
        res1 = requests.get(self.source[0])
        res2 = requests.get(self.source[1])
        soup = BeautifulSoup(res1.text + res2.text, "html.parser")

        return soup

    def sort_stories_by_votes(self, hnlist):
        return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

    def create_custom_hackernews(self, links, subtext):
        hn = []
        for idx, item in enumerate(links):
            title = item.getText()
            href = item.get('href', None)  # None is a default, in case there's no href
            vote = subtext[idx].select('.score')
            if len(vote):
                vts = int(vote[0].getText().replace(' points', ''))
                # print(vts)
                if vts > 99:
                    hn.append({'title': title, 'link': href, 'votes': vts})

            self.counter += 1

        return self.sort_stories_by_votes(hn)


    def return_pretty_result(self):
        pprint.pprint(self.result)
        print(self.counter)

# %%


x = TopHackerNews()

x.return_pretty_result()

# %%

# %%

# %%

# %%

# %%
