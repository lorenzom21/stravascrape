from scrapy import Spider
from scrapy.utils.markup import remove_tags 
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.http import TextResponse
from scrapy.shell import inspect_response
import json
import os
from stravascrape.login import my_email, my_password #This is my own file with the login credentials
#from westworld.items import WestworldItem
        
class Spider1(Spider):
    name = "strava_spider1"
    allowed_urls = ["https://www.strava.com"]
    start_urls = ["https://www.strava.com/login"]


    def parse(self,response):
        print("<<<<<<START PARSE >>>>>>>>>> ")
        print(os.getcwd())
        token = response.xpath('//*[@id="login_form"]/input[2]/@value').extract_first() #name in form is authenticity_token
        return FormRequest.from_response(response,formdata={

                'authenticity_token': token,
                'email': my_email ,
                'password': my_password


            }, callback = self.go_to_data)

    def go_to_data(self,response):

        print("<<<< IN go_to_data >>>>>>>>>>>>>>>")
        data_page = 'https://www.strava.com/athlete/training'
        request = Request(url=data_page, callback=self.get_data)

        yield request


       
    def get_data(self,response):

        print("<<<<<<<<<<<START get_data >>>>>>>>>> ")
        #in /dashboard
        token = response.xpath("/html/head/meta[@name='csrf-token']/@content").extract_first()
        print("token found is: "+token)
        page_n = 1
        data_page = 'https://www.strava.com/athlete/training_activities?keywords=&activity_type=&workout_type=&commute=&private_activities=&trainer=&gear=&new_activity_only=false&page='+str(page_n)
        headers = {
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

        yield Request(url=data_page, headers=headers, callback=self.start_scraping)


    def start_scraping(self,response):
        print("\n\n<<<<<<<<< START start_scraping>>>>>>>>>>>\n\n")
        resp_obj = json.loads(response.text) #How do I write this to a csv file?
        i=1;
        for ride in resp_obj['models']:
            print(str(i)+": "+str(ride['id']))
            i+=1

        

 
        print("<<<<<<END OF SCRAP FUNCTION>>>>>>>>>>")

    
        




        
