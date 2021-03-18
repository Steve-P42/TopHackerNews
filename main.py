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
        self.links = self.page_contents.select('.storylink')
        self.subtext = self.page_contents.select('.subtext')
        self.counter = 0
        self.result = self.create_custom_hackernews(self.links, self.subtext)

#todo add possibility to give the number of pages to scrape
    def get_page_contents(self):
        """scrape the ycombinator page"""
        res1 = requests.get(self.source[0])
        res2 = requests.get(self.source[1])
        soup = BeautifulSoup(res1.text + res2.text, "html.parser")

        return soup

    def sort_stories_by_votes(self, hnlist):
        """rank the stories by favourites"""
        return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

    def create_custom_hackernews(self, links, subtext):
        """extract data from page_contents and put into custom list containing title, link and upvotes"""
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
        """this method presents the top-voted stories in a human-readable format"""
        count = 1
        for element in self.result:
            print(f"""
            Story #  {count}:
            Title:   {element['title']}
            Upvotes: {element['votes']}
            Link:    {element['link']}""")

            count += 1

        print(f"""
            ({len(self.result)} out of {self.counter} stories received 100 or more upvotes.)""")



# %%


x = TopHackerNews()

# loop = 'hi'
#
# x.return_pretty_result()
#
# while loop != 'exit':
#     loop = input()

# %%


# %%
import webbrowser

with open("test.html", "w") as f:
    count = 1

    f.write("""<html> 
            <head> 
            <title>Hackernews</title> 
            </head>
             
            <body> 
            <h2>These are the most upvoted Hackernews stories</h2> 
            <p>
            """)

    for element in x.result:
        f.write(f"""
        Story # {count}: {element['title']}
        <br>
        Upvotes: {element['votes']} Link: {element['link']}
        <br>
        """)

        count += 1

    f.write(f"""
            </p>
            <p>
            ({len(x.result)} out of {x.counter} stories received 100 or more upvotes.)
            </p>
            </body> 
            </html>
            """)

    #     f.write('''
    #     <ul>
    #   <li><a href="https://python-forum.io">The best Python forum</a></li>
    #   <li><a href=https://google.com>Google</a></li>
    # </ul>''')

webbrowser.open('test.html')

# %%

# %%
