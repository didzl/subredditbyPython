import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


app = Flask("DayEleven")

post = []

@app.route("/")
def home():
  return render_template("home.html", subreddits = subreddits)

@app.route("/read")
def read():
  redit=[]
  for subreddit in subreddits:
    on = request.args.get(subreddit)
    if on == 'on':
      redit.append(subreddit)
      url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"

      result = requests.get(url, headers = headers)
      soup = BeautifulSoup(result.text, "html.parser")
      items = soup.find_all("div", {"class": "Post"})

      for item in items:
        title = item.find("h3").text
        url= item.find("a")
        url_text = f"{url['href']}"
        upvotes_span = item.find("span", {"class", "D6SuXeSnAAagG8dKAb4O4"})
        if upvotes_span == None :
          upvotes = "vote"
        else : 
          upvotes = upvotes_span.text
        post.append(
          {
            "title": title,
            "url": url_text,
            "upvotes": upvotes,
            "category": subreddit,
          }
        )

  return  render_template("read.html", 
      subreddits=subreddits,
      on=on,
      post=post
    )


app.run(host="0.0.0.0")