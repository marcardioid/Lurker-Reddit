# Lurker-Reddit
Webcrawler for Reddit subreddits. Downloads all images from x posts. Attempts to extract images from Imgur albums.

###Usage  
Run from the command line:

    lurker-reddit.py [-h] [--count COUNT] [--output OUTPUT]
                     [--category {top,top-all,top-day,top-hour,top-month,top-month,top-week,top-year,con,con-all,con-day,con-hour,con-month,con-week,con-year,hot,new,new-bydate,new-byrising,random,rising}]
                     subreddit

Or, execute: `lurker-reddit-gui.exe`

You can get the executable by downloading and extracting `lurker-reddit.zip` in `\dist`.<br>
You can also build it yourself with `setup.py`.

Default download directory: `root/reddit`

###Dependencies

<a href="https://github.com/praw-dev/praw">PRAW</a><br>
<a href="http://www.crummy.com/software/BeautifulSoup">BeautifulSoup 4</a><br>
Both can also be installed using `pip`.
