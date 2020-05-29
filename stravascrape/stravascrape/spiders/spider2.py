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
from stravascrape.items import RidePageItem

        
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

        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IN go_to_data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(os.getcwd())

        rides_df = pd.read_csv("spider1_output.csv")
        ride_id_list = rides_df['ride_id']
        self.ride_id_list = ride_id_list
        self.n_pages=len(ride_id_list)
        target = self.base_url+str(ride_id_list[0])

        yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':0})


    def scrape_page(self,response,list_idx):
        print("<<<<<<<<<<<<<<<<<<<Scraping index "+str(list_idx)+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


        item = RidePageItem()
        item['ride_id'] = self.ride_id_list[list_idx]
        item['avg_watts'] = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[1]/strong/text()').extract_first()

        watts_type = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[1]/div/span/text()').extract_first() #need strip because there is \n in beginning and end
        if watts_type is not None:
            item['watts_type'] = watts_type.strip()

        max_watts = response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[2]/tr[2]/td[2]/text()').extract_first()

        if max_watts is not None:
            item['max_watts'] = max_watts.strip()
            
        item['distance'] = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[1]/strong/text()').extract_first()
        item['time'] = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[2]/strong/text()').extract_first()
        item['elevation'] = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[3]/strong/text()').extract_first()
        item['kJ']=response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[2]/strong/text()').extract_first()
        item['avg_speed']=response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[1]/tr/td[1]/text()').extract_first()
        item['max_speed']=response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[1]/tr/td[2]/text()').extract_first()
        item['avg_cad'] = response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[2]/tr[1]/td[1]/text()').extract_first()

        max_cad = response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[2]/tr[1]/td[2]/text()').extract_first()
        if max_cad is not None:
            item['max_cad'] = max_cad.strip()

        item['Calories'] = response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[2]/tr[3]/td/text()').extract_first()
        item['avg_temp'] = response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[2]/tr[4]/td/text()').extract_first()

        yield item
     
        next_idx = list_idx+1
        
        if(next_idx < self.n_pages):
            target = self.base_url+str(self.ride_id_list[next_idx])
            yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':next_idx})


        
        




    
        




        
