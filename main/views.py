from django.shortcuts import render
from . import models
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import requests
Base_url = 'https://chandigarh.craigslist.org/search/sss?query={}'
Base_image_url = 'https://images.craigslist.org/{}_300x300.jpg'
# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url =Base_url.format(quote_plus(search))
    response = requests.get("https://chandigarh.craigslist.org/search/sss?query={}")
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listing = soup.find_all('li',{'class':'result-row'})
    # post_img = post_listing.find("img").get('href')

    final_posting=[]
    for post in post_listing:
        post_title = post.find('a',{"class": "result-title"}).text
        post_url=post.find('a').get('href')
        if post.find('span',{'class':'result-price'}):
            post_price= post.find('span',{'class':'result-price'}).text
        else:
            post_price = 'N/A'
        if post.find('a',{'class':'result-image'}).get('data-ids'):
            post_image_id= post.find('a',{'class':'result-image'}).get('data-ids').split(',')[0].split(':')[1]
            post_image_url = Base_image_url.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_posting.append((post_title,post_url,post_price ,post_image_url))
    # print(post_img)

    stuff_for_frontend = {
        'search': search,
        'final_posting':final_posting
    }
    return render(request,'main/new_search.html' , stuff_for_frontend )