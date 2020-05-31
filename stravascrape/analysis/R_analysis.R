setwd("~/Google Drive/NYCDSA/webscraping/stravascrape_data")

library(lubridate)
library(dplyr)
library(ggplot2)

data_df = read.csv('joined_df.csv', stringsAsFactors = F)
data_df$start_date = mdy(data_df$start_date)
data_df$start_day = as.factor(data_df$start_day)
data_df$elevation = as.numeric(data_df$elevation)

#Have clearer language for watts type
data_df$watts_type[data_df$watts_type=='Estimated Avg Power'] = "Strava estimate"
data_df$watts_type[data_df$watts_type=='Weighted Avg Power'] = "Power meter"
data_df$watts_type = as.factor(data_df$watts_type)

#ft per mile
data_df$ft_per_mile=data_df$elevation/data_df$distancedf2

#classify based on kJ
data_df$kJ_cat = "no cat"
data_df$kJ_cat[data_df$kJ<=250] = "A) up to 250 kJ"
data_df$kJ_cat[250 < data_df$kJ & data_df$kJ<=750] = "B) 250 to 750 kJ"
data_df$kJ_cat[750 < data_df$kJ & data_df$kJ<=1250] = "C) 1,000 to 1,500 kJ"
data_df$kJ_cat[1250 < data_df$kJ] = "D) greater than 1,250 kJ"
data_df$kJ_cat = as.factor(data_df$kJ_cat)
data_df$year = as.factor(year(data_df$start_date))
summary(data_df$kJ_cat)

#find max watts
max(data_df[data_df$start_date>as.Date('2017-09-02'),c('max_watts')],na.rm=T) #1493
data_df %>% filter(.,max_watts==1493) #1400063224

#total distance
sum(data_df$distancedf2) #15249.32


g_base = ggplot(data=data_df)
font_size = theme(text = element_text(size=20))

#historgram of kJ

g_base + geom_histogram(aes(x=kJ),binwidth=500) + font_size

#distance and elevation within the kJ_cat groups
data_df %>% group_by(kJ_cat) %>%
  summarise(.,n=n(),mean_distance = mean(distancedf2, na.rm=T),sd_distance = sd(distancedf2, na.rm=T),mean_elevation = mean(elevation,na.rm=T),sd_elevation = sd(elevation,na.rm=T))

#kJ cat vs distance
g_base + geom_bar(aes(x=kJ_cat))
g_base+geom_boxplot(aes(x=kJ_cat,y=distancedf2))

#Plot distance vs kJ
ggplot(data=data_df,aes(x=distancedf2,y=kJ)) + geom_point(aes(color=watts_type))  + geom_smooth(method='lm') + labs(x="distance in miles", y="Energy in kJ", color='power data source')

#avg weighted power over time by kJ grouping
ggplot(data=data_df, aes(x=start_date,y=avg_weighted_watts))+geom_point(aes(color=watts_type)) + geom_smooth(method='lm') + facet_wrap(~kJ_cat) +labs(x='date', y='avg weighted power', color='power data source') + font_size

#boxplot by year
ggplot(data=data_df, aes(x=year,y=avg_weighted_watts)) + geom_boxplot()+ geom_jitter(shape=1, position=position_jitter(0.2)) + facet_wrap(~kJ_cat) +labs(x='years', y='avg weighted power') + font_size

unique_days = data_df %>% group_by (start_date) %>% summarise(n=n())

unique_days$year = year(unique_days$start_date)
unique_days

#histogram of ride days per year
ggplot(data=unique_days,aes(x=year))+geom_bar() + font_size

#histogram of rides by year
ggplot(data=data_df,aes(x=year))+geom_bar() + font_size

#Calories historgram
ggplot(data=data_df,aes(x=Calories)) +geom_histogram(binwidth=500,aes(fill=start_day)) + labs(fill='day') + font_size


#cadence histogram
ggplot(data = data_df[data_df$avg_cad>60,], aes(x=avg_cad)) + geom_histogram(binwidth=5) + ylab("test") + font_size





