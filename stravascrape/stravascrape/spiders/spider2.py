from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
import json
import os
from stravascrape.login import my_email, my_password #This is my own file with the login credentials
import pandas as pd
from stravascrape.items import RidePageItem


# import requests as proxy_requests

# proxies = {'http': 'http://user:pass@10.10.1.10:3128/'}
# proxy_requests.get('http://example.org', proxies=proxies)

        
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
        print("<<<<<<<<<<<<<LOG IN >>>>>>>>>>>>>>>>>>>> ")
        
        token = response.xpath('//*[@id="login_form"]/input[2]/@value').extract_first() #name in form is authenticity_token
        # token = 'EuGLXAGTwmOSkSGdkim1CtPPhgFmqbmTTjmzs1gcDfahTWNfu5SKp/yfvfvSe8oVHdIbXSJ815JCpryTGLQEDw=='
        return FormRequest.from_response(response,formdata={

                'authenticity_token': token,
                'email': my_email ,
                'password': my_password


            }, callback = self.prep_ride_list) #redirects to /dashboard

    def prep_ride_list(self,response):

        rides_df = pd.read_csv("spider1_output.csv")
        start_idx = 0 #because of request limits, I am having to run this script in parts.
        ride_id_list = rides_df['ride_id']
        #ride_id_list = [1733394373]
        self.ride_id_list = ride_id_list
        self.n_pages=len(ride_id_list)
        target = self.base_url+str(ride_id_list[start_idx])

        yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':start_idx})


    def scrape_page(self,response,list_idx):
        print("<<<<<<<<<<<<<<<<<<<SCRAPING INDEX"+str(list_idx)+">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


        item = RidePageItem()
        item['ride_id'] = self.ride_id_list[list_idx]
        
        #top block data
        distance = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[1]/strong/text()').extract_first()
        if distance is not None:
            item['distance']=distance.strip().strip('"').replace(",",'')

        item['time'] = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[2]/strong/text()').extract_first()

        elevation = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[1]/li[3]/strong/text()').extract_first()
        if elevation is not None:
            item['elevation'] = elevation.strip().strip('"').replace(",",'')


        kJ = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[2]/strong/text()').extract_first()
        if kJ is not None:
            item['kJ'] = kJ.strip().strip('"').replace(",",'')

        avg_weighted_watts = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[1]/strong/text()').extract_first()
        if avg_weighted_watts is not None:
            item['avg_weighted_watts'] = avg_weighted_watts.strip().strip('"').replace(",",'')


        watts_type = response.xpath('//*[@id="heading"]/div/div/div[2]/ul[2]/li[1]/div/span/text()').extract_first() #need strip because there is \n in beginning and end
        if watts_type is not None:
            item['watts_type'] = watts_type.strip()

        #end of top block data


        #additional data
        avg_speed=response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[1]/tr/td[1]/text()').extract_first()
        if avg_speed is not None:
            avg_speed.strip(" ")#strip white space
            avg_speed.strip('"') #strip quotes
            item['avg_speed'] = avg_speed

        max_speed =response.xpath('//*[@id="heading"]/div/div/div[2]/div[1]/table/tbody[1]/tr/td[2]/text()').extract_first()
        if max_speed is not None:
            max_speed.strip(" ")
            max_speed.strip('"')
            item['max_speed'] = max_speed

        showmore_block = response.xpath('//*[@id="heading"]/div/div[1]/div[2]/div[1]/table/tbody[2]')

        #Don'w what data exactly will show up. So parse the table based on row names
        showmore_dict = {}
        showmore_dict['Cadence']=[None,None]
        showmore_dict['Calories']=[None,None]
        showmore_dict['Temperature']=[None,None]
        showmore_dict['Power']=[None,None]


        rows = showmore_block.xpath("./tr")
        for row in rows:
            name = row.xpath("./th/text()").extract_first()
            val1 = row.xpath("./td[1]/text()").extract_first()
            if val1 is not None:
                val1 = val1.strip().strip('"').replace(",",'')

            val2 = row.xpath("./td[2]/text()").extract_first()
            if val2 is not None:
                val2 = val2.strip().strip('"').replace(",",'')


            showmore_dict[name] = []
            showmore_dict[name].append(val1)
            showmore_dict[name].append(val2)


        item['avg_cad'] = showmore_dict['Cadence'][0]
        item['max_cad'] = showmore_dict['Cadence'][1]
        item['Calories'] = showmore_dict['Calories'][0]
       
        item['avg_temp'] = showmore_dict['Temperature'][0] #this may have an error because contents has a <abbr> for the F/C

        item['raw_avg_watts'] = showmore_dict['Power'][0] #this may throw an error because of the W
        item['max_watts'] = showmore_dict['Power'][1]

        #end of addtional data


        yield item
     
        next_idx = list_idx+1
        
        if(next_idx < self.n_pages):
            target = self.base_url+str(self.ride_id_list[next_idx])
            yield Request(url=target, callback=self.scrape_page, cb_kwargs={'list_idx':next_idx})


        
        




    
        




        
