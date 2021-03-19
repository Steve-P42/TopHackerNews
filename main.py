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
from time import gmtime, strftime
import webbrowser
from time import sleep


# %%
class TopHackerNews:
    def __init__(self, page_num=1):
        self.source = ['https://news.ycombinator.com/news', 'https://news.ycombinator.com/news?p=2',
                       'https://news.ycombinator.com/news?p=3', 'https://news.ycombinator.com/news?p=4',
                       'https://news.ycombinator.com/news?p=5']
        self.page_number = page_num
        self.page_contents = self.get_page_contents()
        self.links = self.page_contents.select('.storylink')
        self.subtext = self.page_contents.select('.subtext')
        self.counter = 0
        self.result = self.create_custom_hackernews(self.links, self.subtext)

    def get_page_contents(self):
        """scrape the ycombinator page"""
        res1 = requests.get(self.source[0])
        res2 = requests.get(self.source[1])
        res3 = requests.get(self.source[2])
        res4 = requests.get(self.source[3])
        res5 = requests.get(self.source[4])

        if self.page_number == 1:
            soup = BeautifulSoup(res1.text, "html.parser")
        elif self.page_number == 2:
            soup = BeautifulSoup(res1.text + res2.text, "html.parser")
        elif self.page_number == 3:
            soup = BeautifulSoup(res1.text + res2.text + res3.text, "html.parser")
        elif self.page_number == 4:
            soup = BeautifulSoup(res1.text + res2.text + res3.text + res4.text, "html.parser")
        else:
            soup = BeautifulSoup(res1.text + res2.text + res3.text + res4.text + res5.text, "html.parser")

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

    def return_as_html(self):
        with open("hnews.html", "w") as f:
            count = 1

            f.write(f"""<html> 
                    <head> 
                    <title>HackerNews</title> 
                    </head>

                    <body> 
                    <h2>Most upvoted HackerNews - Stories on {strftime("%d.%m.%Y %H:%M:%S", gmtime())} GMT</h2> 
                    <p>
                    """)

            for element in self.result:
                f.write(f'''
                <ul>
                <li>Story # {count}: {element['title']}</li>
                <br>
                <li>Upvotes: {element['votes']} Link: <a href="{element['link']}">{element['link']}</a></li>
                <br>
                </ul>
                ''')

                count += 1

            f.write(f"""
                    </p>
                    <p>
                    ({len(self.result)} out of {self.counter} stories received 100 or more upvotes.)
                    </p>
                    </body> 
                    </html>
                    """)

        webbrowser.open('hnews.html')


# %%
check = False
while not check:
    try:
        p = int(input('How many pages do you want to scrape? (1-5)'))
        if p in [1, 2, 3, 4, 5]:
            check = True
        else:
            print('Only numbers between 1-5 are allowed.')
    except ValueError:
        print('Only numbers between 1-5 are allowed.')
        pass
print('Browser opens shortly.')
sleep(3)

x = TopHackerNews(p)

x.return_as_html()

# loop = 'hi'
# x.return_pretty_result()
# while loop != 'exit':
#     loop = input()

# %%

# %%

# %%
