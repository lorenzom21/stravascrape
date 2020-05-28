from scrapy import Spider
from scrapy.utils.markup import remove_tags 
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.http import TextResponse
from scrapy.shell import inspect_response
import json
import os
from stravascrape.login import my_email, my_password #This is my own file with the login credentials
import pandas as pd
#from stravascrape.items import RideItem

        
class Spider2(Spider):
    name = "strava_spider2"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stravascrape.pipelines.Spider2Pipeline': 1
        }
    }

    allowed_urls = ["https://www.strava.com"]
    start_urls = ["https://www.strava.com/login"]
    base_url = 'https://www.strava.com/activities/'
    n_pages = 0
    ride_id_list = []



    def parse(self,response):
        print("<<<<<<START PARSE >>>>>>>>>> ")
        
        token = response.xpath('//*[@id="login_form"]/input[2]/@value').extract_first() #name in form is authenticity_token
        return FormRequest.from_response(response,formdata={

                'authenticity_token': token,
                'email': my_email ,
                'password': my_password


            }, callback = self.prep_ride_list) #redirects to /dashboard

    def prep_ride_list(self,response):

        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IN go_to_data >>>>>>>>>>>>>>>")
        print(os.getcwd())

        rides_df = pd.read_csv("spider1_output.csv")
        ride_id_list = rides_df['ride_id'][0:5]
        self.ride_id_list = ride_id_list
        self.n_pages=len(ride_id_list)
        target = self.base_url+str(ride_id_list[0])

        yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':0})


    def scrape_page(self,response,list_idx):
        print("<<<<<<<<<<<<<<<<<<<Scraping index "+str(list_idx)+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
        title = response.xpath('//*[@id="heading"]/div/div/div[1]/div/div/h1/text()').extract_first()
        print(title)
        next_idx = list_idx+1
        

        if(next_idx < self.n_pages):
            target = self.base_url+str(self.ride_id_list[next_idx])
            yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':next_idx})


        
        




    
        




        
