#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 20:08:29 2020

@author: jiaxinli
"""

import re
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def get_soup(url):
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    driver.close()
    return soup


def grab_job_links(soup):
    urls = []
    for link in soup.find_all('h2',{'class':'title'}):
        partial_url = link.a.get('href')
        url = 'https://www.indeed.com' + partial_url
        urls.append(url)
    
    return urls

def get_urls(query,num_pages,location):
    base_url = 'https://www.indeed.com/jobs?q={}&l={}'.format(query,location)
    soup = get_soup(base_url)
    urls = grab_job_links(soup)

    #get the total number of postings found
    posting_count_string = soup.find(name='div',attrs={'id':"searchCount"}).get_text()
    posting_count_string = posting_count_string[posting_count_string.find('of')+2:].strip()
    #print('posting_count_string:{'posting_count_string:{}'.format(posting_count_string))
    
    try:
        posting_count = int(posting_count_string)
    except ValueError:
        posting_count = int(re.search('\d+',posting_count_string).group(0))
    finally:
        posting_count = 330
        pass
    
    #limit number of pages to get
    max_pages = round(posting_count/10)-3
    if num_pages > max_pages:
        print('returning max_pages!!')
        return max_pages
    
    #Additional work is needed when more than 1 page is requested
    if num_pages >= 2:
        for i in range(2,num_pages+1):
            num = (i-1)*10
            base_url = 'https://indeed.com/jobs?q={}&l={}&start={}'.format(query,location,num)
            try:
                soup = get_soup(base_url)
                #combine the results back to the list
                urls += grab_job_links(soup)
            except:
                continue
    return urls
    

def get_posting(url):
    soup = get_soup(url)
    
    #The job title is held in h3 tag
    title = soup.find(name='h3').getText().lower()
    posting = soup.find(name = 'div', attrs = {'class':"jobsearch-JobComponent"}).get_text()
    
    return title,posting.lower()

def get_data(query,num_pages,location='New York'):
    #convert the queried title to Indeed format
    query = '+'.join(query.lower().split())
    
    posting_dict = {}
    urls = get_urls(query,num_pages,location)
    
    #continue only if the requested number of pages is valid
    if isinstance(urls,list):
        num_urls = len(urls)
        for i,url in enumerate(urls):
            try:
                title,posting = get_posting(url)
                posting_dict[i] = {}
                posting_dict[i]['title'],posting_dict[i]['posting'],posting_dict[i]['url']=\
                title,posting,url
            except:
                continue
            
            percent = (i+1)/num_urls
            #print the progress the "end" arg keeps the emssage in the same line
            print("Progress:{:2.0f}%".format(100*percent),end='\n')
            
        #save the dict as json file
        file_name = query.replace('+','_')+'.json'
        with open(file_name,'w') as f:
            json.dump(posting_dict,f)
            
        print('All {} postings have been scraped and saved!'.format(num_urls))
    
    else:
        print("Due to similar results,maximum number of pages is only{}.Please try again!".format(urls))
    
    
#If script is run directly, we'll take input from the user
if __name__ == "__main__":
    queries = ["data scientist","machine learning engineer","data engineer"]
    
    while True:
        query = input("Please enter the title to scrape data for: \n").lower()
        if query in queries:
            break
        else:
            print("Invalid title! Please try again.")
            
    while True:
        num_pages = input("Please enter the number of pages needed(integer only):\n")
        try:
            num_pages = int(num_pages)
            break
        except:
            print("Invalid number of pages! Please try again.")
            
    get_data(query,num_pages,location='New York')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    