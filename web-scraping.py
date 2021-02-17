from bs4 import BeautifulSoup
import requests, pandas

"""
Note:
The use of bots to scrap or crawl the web is not allowed from everyone. You should be carefull when you are using web crawlers or scraping data
from web pages.
Many many pages out there will block most of the crawlers unless they provide explicit rules, please look at robots.txt file
that typically leave under the base domain for rules and guidelines.
For example: https://github.com/robots.txt

I'm just gonna scrap my personal portofolio web site to find any broken link.
"""

# Initializing variables
url = "https://stathis-kal.github.io/"
site = requests.get(url) # Making a call to our URL.

# Making a custom DataFrame
cols = ["URL"]
df = pandas.DataFrame(columns = cols)

# Get the html source code of the site
data = site.text
soup = BeautifulSoup(data, features="html.parser")

# Append every URL on the site to a DataFrame
for link in soup.findAll("a", href=True,):
    df = df.append({"URL": link.get("href")}, ignore_index = True)

# Get the data which contains http(s) only.
df = df[df["URL"].str.contains("http") == True]

def reqPerSite(Data):
    result = pandas.DataFrame()
    for url in Data:
        try: # Make a call per URL in our site and append the HTTP status code from the response.
            result = result.append({"URL": url, "Status Code": requests.get(url)}, ignore_index = True)
        except Exception as err:
            print("Error has been occured {err}")
    result.to_csv("report.csv", index = False)

reqPerSite(df["URL"])
