#!/usr/bin/python -W ignore::DeprecationWarning

import os
import urllib.request
import argparse
import praw
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_submissions(subreddit, count, filter):
    r = praw.Reddit(user_agent='Lurker for Reddit')
    sr = r.get_subreddit(subreddit)
    return filter(sr, count)

def get_links(submissions):
    return [sub.url for sub in submissions]

def filter_for_imgur(urls):
    res = []
    for url in urls:
        if any(s in url for s in ["imgur"]):
            if url.endswith('jpg') or url.endswith('gif') or url.endswith('png'):
                res.append(url) # direct link to image
            else:
                try:
                    response = urllib.request.urlopen(url) # try to find a direct link
                except (urllib.request.HTTPError, urllib.request.URLError) as e:
                    print("Error: Could not find '{}'.".format(url))
                    continue
                if "image" in get_content_type(response):
                    res.append(url) # found a direct link to image
                else:
                    print("Found an album! Extracting...")
                    soup = BeautifulSoup(response.read())
                    divs = soup.find_all("div", "item view album-view-image-link")
                    for div in divs:
                        res.append("http:" + div.a['href']) # queue all direct image links from an album
        else:
            try:
                response = urllib.request.urlopen(url)
            except (urllib.request.HTTPError, urllib.request.URLError) as e:
                # print("Error: Could not find '{}'.".format(url))
                continue
            if "image" in get_content_type(response):
                res.append(url) # direct link to image
    return res

def get_content_type(response):
    for header in response.getheaders():
        if header[0].startswith("Content-Type"):
            return header[1]

def get_file_format(content_type):
    short = content_type.split("/")[1]
    return short if short in ["jpg", "jpeg", "gif"] else "png"

def download_images(urls, directory):
    actual = 0
    not_read = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    for i, url in enumerate(urls):
        try:
            response = urllib.request.urlopen(url)
        except (urllib.request.HTTPError, urllib.request.URLError) as e:
            print("Error: Could not download '{}'.".format(url))
            continue
        content_type = get_content_type(response)
        if "image" in content_type:
            directory = directory if directory else "images"
            f = open(directory + "\\"+ str(actual + 1) +"."+get_file_format(content_type), "wb")
            file_size = int(response.getheader('Content-Length'))
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = response.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                progress = int(file_size_dl * 100 / file_size)
                print("\rDownloading [%s/%s]: \t %s \t => \t Downloading: %s%%" % ((str(actual+1)).zfill(2), (str(len(urls))).zfill(2), str(url[-11:-4]), (str(progress)).zfill(3)), end = "")
            f.close()
            print("")
            actual += 1
        else:
            not_read.append(url);
    if(len(not_read) > 0):
        print("Could not read the following urls:")
        for url in not_read:
            print('\t' + url)
    return actual

def get_filters():
    return {"top": lambda r, c: r.get_top(limit=c),
            "top-all": lambda r, c: r.get_top_from_all(limit=c),
            "top-day": lambda r, c: r.get_top_from_day(limit=c),
            "top-hour": lambda r, c: r.get_top_from_hour(limit=c),
            "top-month": lambda r, c: r.get_top_from_month(limit=c),
            "top-week": lambda r, c: r.get_top_from_week(limit=c),
            "top-year": lambda r, c: r.get_top_from_year(limit=c),
            "con": lambda r, c: r.get_controversial(limit=c),
            "con-all": lambda r, c: r.get_controversial_from_all(limit=c),
            "con-day": lambda r, c: r.get_controversial_from_day(limit=c),
            "con-hour": lambda r, c: r.get_controversial_from_hour(limit=c),
            "con-month": lambda r, c: r.get_controversial_from_month(limit=c),
            "con-week": lambda r, c: r.get_controversial_from_week(limit=c),
            "con-year": lambda r, c: r.get_controversial_from_year(limit=c),
            "hot": lambda r, c: r.get_hot(limit=c),
            "new": lambda r, c: r.get_new(limit=c),
            "new-bydate": lambda r, c: r.get_new_by_date(limit=c),
            "new-byrising": lambda r, c: r.get_new_by_rising(limit=c),
            "random": lambda r, c: r.get_random_submission(limit=c),
            "rising": lambda r, c: r.get_rising(limit=c),
    }

def parse_args():
    parser = argparse.ArgumentParser(description="Lurker-Reddit. Downloads all images (filterable) from a given subreddit.")
    parser.add_argument('subreddit', help="The subreddit.")
    parser.add_argument('--count', '-c', default='10', type=int, help="Number of posts to download images from.")
    parser.add_argument('--output', '-o', default=".", action='store', help="The output directory.")
    parser.add_argument('--category', '-t', default="top",
                        choices=["top", "top-all", "top-day", "top-hour", "top-month", "top-month", "top-week",
                                 "top-year", "con", "con-all", "con-day", "con-hour", "con-month", "con-week",
                                 "con-year", "hot", "new", "new-bydate", "new-byrising", "random", "rising"],
                        help="The category filter.")
    return parser.parse_args()

def main():
    args = parse_args()
    print("Contacting Reddit...")
    urls = get_links(get_submissions(args.subreddit, args.count, get_filters()[args.category]))
    print("Found {} reddit threads.".format(str(len(urls))))
    urls = filter_for_imgur(urls)
    print("Found {} image links.".format(str(len(urls))))
    actual = download_images(urls, args.output)
    print("Downloaded {} images to {}.".format(str(actual), '/' + args.output if args.output else "current directory"))

if __name__ == "__main__":
    main()