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



    def parse(self,response):
        print("<<<<<<START PARSE >>>>>>>>>> ")
        
        token = response.xpath('//*[@id="login_form"]/input[2]/@value').extract_first() #name in form is authenticity_token
        return FormRequest.from_response(response,formdata={

                'authenticity_token': token,
                'email': my_email ,
                'password': my_password


            }, callback = self.go_to_data) #redirects to /dashboard

    def go_to_data(self,response):

        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IN go_to_data >>>>>>>>>>>>>>>")
        print(os.getcwd())

        rides_df = pd.read_csv("spider1_output.csv")
        ride_id_list = rides_df['ride_id']
        
        




    
        




        
