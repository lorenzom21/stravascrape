from scrapy import Spider
from scrapy.utils.markup import remove_tags 
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.http import TextResponse
from scrapy.shell import inspect_response
import json
import os
from stravascrape.login import my_email, my_password #This is my own file with the login credentials
from stravascrape.items import RideItem
#from westworld.items import WestworldItem
        
class Spider1(Spider):
    name = "strava_spider1"
    custom_settings = {
        'ITEM_PIPELINES': {
            'stravascrape.pipelines.Spider1Pipeline': 1
        }
    }


    allowed_urls = ["https://www.strava.com"]
    start_urls = ["https://www.strava.com/login"]
    base_url = 'https://www.strava.com/athlete/training_activities?keywords=&activity_type=Ride&workout_type=&commute=&private_activities=&trainer=&gear=&new_activity_only=false&page='
    headers = {}



    def parse(self,response):
        print("<<<<<<START PARSE >>>>>>>>>> ")
        print(os.getcwd())
        token = response.xpath('//*[@id="login_form"]/input[2]/@value').extract_first() #name in form is authenticity_token
        return FormRequest.from_response(response,formdata={

                'authenticity_token': token,
                'email': my_email ,
                'password': my_password


            }, callback = self.go_to_data) #redirects to /dashboard

    def go_to_data(self,response):

        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IN go_to_data >>>>>>>>>>>>>>>")
        #starts in /dashboard
        token = response.xpath("/html/head/meta[@name='csrf-token']/@content").extract_first()
        page_n = 1
        self.headers = {
            "authority": "api2.branch.io",
            "accept": "*/*",
            "x-csrf-token": token,
            #"x-csrf-token": "+mhC1Xcn+Ji2hpcaSOeaBzezK/7BAOyytnSBsDxh9BNPlkW+j/qMTF+gfn0iErb6299YpoIPMUGT/uLJTxYqlg==",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://www.strava.com/",
            "accept-language": "en,es;q=0.9",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Accept": "*/*",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Dest": "script",
            "Referer": "https://www.strava.com/",
            "Accept-Language": "en,es;q=0.9",
            "If-None-Match": "W/\"5a-sobOsabTXXL4DkrPrBdu6K5QFv8\"",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.strava.com"
        }

        
        data_page = self.base_url + str(page_n)
        request = Request(url=data_page, headers=self.headers, callback=self.start_scraping, cb_kwargs={'page_n':1})
        #request.cb_kwargs['page_n'] = 1
        yield request


    def start_scraping(self,response,page_n):
        print("\n\n<<<<<<<<< START start_scraping>>>>>>>>>>>\n\n")
     

        #inspect_response(response,self)

        resp_obj = json.loads(response.text) 
        rides = resp_obj['models']

        if(len(rides)>0):
      
            for ride in rides:

                item = RideItem()
                item['ride_id']  = ride['id']
                item['name'] = ride['name']

                item['activity_type_display_name'] = ride['activity_type_display_name']
                item['bike_id'] = ride['bike_id']
                item['calories'] = ride['calories']
                item['distance'] = ride['distance']
                item['distance_raw'] = ride['distance_raw']
                item['elapsed_time'] = ride['elapsed_time']
                item['elapsed_time_raw'] = ride['elapsed_time_raw']
                item['elevation_gain'] = ride['elevation_gain']
                item['elevation_gain_raw'] = ride['elevation_gain_raw']
                item['elevation_unit'] = ride['elevation_unit']
                item['long_unit'] = ride['long_unit']
                item['moving_time'] = ride['moving_time']
                item['moving_time_raw'] = ride['moving_time_raw']
                item['short_unit'] = ride['short_unit']
                item['start_date'] = ride['start_date']
                item['start_date_local_raw'] = ride['start_date_local_raw']
                item['start_day'] = ride['start_day']
                item['start_time']= ride['start_time']
                item['ride_type'] = ride['type'] #response is 'type'
                item['visibility'] = ride['visibility']

                yield item

            next_page = page_n + 1
            data_page = self.base_url+str(next_page)

            print("NEXT PAGE IS "+str(next_page))
            
            yield Request(url=data_page, headers=self.headers, callback=self.start_scraping, cb_kwargs={'page_n':next_page})

    print("<<<<<<END OF START SCRAPING>>>>>>>>>>")

       
    # def get_data(self,response,token):

    #     print("<<<<<<<<<<<START get_data >>>>>>>>>> ")
        
    #     #token = response.xpath("/html/head/meta[@name='csrf-token']/@content").extract_first()
    #     print("token found is: "+token)
    #     page_n = 2
    #     data_page = 'https://www.strava.com/athlete/training_activities?keywords=&activity_type=&workout_type=&commute=&private_activities=&trainer=&gear=&new_activity_only=false&page='+str(page_n)
    #     headers = {
    #         "authority": "api2.branch.io",
    #         "accept": "*/*",
    #         "x-csrf-token": token,
    #         #"x-csrf-token": "+mhC1Xcn+Ji2hpcaSOeaBzezK/7BAOyytnSBsDxh9BNPlkW+j/qMTF+gfn0iErb6299YpoIPMUGT/uLJTxYqlg==",
    #         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    #         "x-requested-with": "XMLHttpRequest",
    #         "sec-fetch-site": "cross-site",
    #         "sec-fetch-mode": "cors",
    #         "sec-fetch-dest": "empty",
    #         "referer": "https://www.strava.com/",
    #         "accept-language": "en,es;q=0.9",
    #         "Connection": "keep-alive",
    #         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    #         "Accept": "*/*",
    #         "Sec-Fetch-Site": "cross-site",
    #         "Sec-Fetch-Mode": "no-cors",
    #         "Sec-Fetch-Dest": "script",
    #         "Referer": "https://www.strava.com/",
    #         "Accept-Language": "en,es;q=0.9",
    #         "If-None-Match": "W/\"5a-sobOsabTXXL4DkrPrBdu6K5QFv8\"",
    #         "content-type": "application/x-www-form-urlencoded",
    #         "origin": "https://www.strava.com"
    #     }

    #     yield Request(url=data_page, headers=headers, callback=self.start_scraping)




    
        




        
