from django.shortcuts import render

from .forms import CrawlingForm, CrawlingSubjectForm
from .models import Crawling, CrawlingSubject

from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys

def crawling(request):

    if request.method == 'POST':

        form = CrawlingForm(request.POST)

        if form.is_valid():

            crawling = form.save(commit=False)
            crawling.search = request.POST['search']
            crawling.start_p = request.POST['start_p']
            crawling.end_p = request.POST['end_p']
            crawling.save()
            #search = request.POST['search']
            #start_p = int(request.POST['start_p'])
            #end_p = int(request.POST['end_p'])
            #comment = Crawling(search=search, start_p=start_p, end_p=end_p)
            #comment.save()

            #print(search + str(start_p) + str(end_p))
            print(type(crawling.start_p))
            CrawlingSubject.objects.all().delete()
            #main_crawler(search, start_p, end_p)
            #good("파이썬")
            good_page(crawling.search, int(crawling.start_p), int(crawling.end_p))

            return crawlingsubject(request)
            #return render(request, 'crawling/crawlingsubject.html')

    else:

        form = CrawlingForm()

    context = {'form': form}

    return render(request, 'crawling/crawling.html', context)

def crawlingsubject(request):

    print("hi")
    crawlingsubject_list = CrawlingSubject.objects.order_by('id')
    crawlingsubject_list.distinct().values_list('subject')
    context = {'crawlingsubject_list': crawlingsubject_list}

    return render(request, 'crawling/crawlingsubject.html', context)

def good_page(search, s_p, e_p):

    j = 1
    for i in range(s_p, e_p + 1):

        print("++++" + str(i) + " " + str(j))
        j = good(search, i, j)

def good(search, w, j):

    w = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(w)
    req = requests.get(w)
    html = req.text
    header = req.headers
    status = req.status_code

    if status != 200:

        print("no")

    else:

        print("good")

    soup = BeautifulSoup(html, 'html.parser')
    soup1 = soup.select('ul.list_news > li.bx')
    #print(soup1)

    for i in soup1:

        ii = i.select('div.news_area > a.news_tit')
        ii1 = i.select('div.news_area > a')[0]['title']
        ii2 = i.select('div.news_area > a')[0]['href']
        q = CrawlingSubject(num=j, subject=ii1, ref=ii2)
        print(q.subject)
        q.save()
       # ii1 = ii.find('a')
       # ii2 = ii.select('div.news_dsc')
        print(j)
        print(ii)
        print("-----------")
        print(ii1)
        print(ii2)
        print()
        j = j + 1

    return j

def makePgN(n):

    if n == 1:

        return n

    elif n == 0:

        return n+1

    else:

        return n+9*(n-1)


def makeUrl(s, s_p, e_p):

    if s_p == e_p:

        s_page = makePgN(s_p)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + s + "&start=" + str(s_page)

        return url

    else:

        urls = []

        for i in range(s_p, e_p + 1):

            p = makePgN(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + s + "&start=" + str(p)
            urls.append(url)

        return urls

def news_attrs_crawler(ar, at):

    at_content = []

    for i in ar:

        at_content.append(i.at[at])

    return at_content

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

def articles_crawler(_url):

    main_html = requests.get(_url)

    for i in main_html:

        o_html = i.text
        header = i.headers
        html = BeautifulSoup(o_html, "html.parser")
        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        #url = news_attrs_crawler(url_naver, 'href')

    return url_naver

def makeList(newslist, content):
    for i in content:

        for j in i:
            newslist.append(j)

    return newslist

def main_crawler(s, s_p, e_p):

    url = makeUrl(s, s_p, e_p)

    news_title = []
    news_url = []
    news_content = []
    news_dates = []

    url_num = articles_crawler(url)

    # news_url_1 = []
    # makeList(news_url_1, news_url)

    final_urls = []

    for i in tqdm(range(len(url_num))):

        if "news.naver.com" in url_num[i]:

            final_urls.append(url_num[i])

        else:

            pass

    for i in tqdm(final_urls):

        news = requests.get(i, headers=headers)
        news_html = BeautifulSoup(news.text, "html.parser")

        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")

        content = news_html.select("div#dic_area")
        if content == []:
            content = news_html.select("#articeBody")

        content = ''.join(str(content))

        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')

        news_title.append(title)
        news_content.append(content)

        try:
            html_date = news_html.select_one("div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
            news_date = html_date.attrs['data-date-time']
        except AttributeError:
            news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
            news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))

        news_dates.append(news_date)

# Create your views here.
