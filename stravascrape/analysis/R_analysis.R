setwd("~/Google Drive/NYCDSA/webscraping/stravascrape_data")

library(lubridate)
library(dplyr)

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
data_df$kJ_cat[data_df$kJ<=500] = "A) below 500 kJ"
data_df$kJ_cat[500 < data_df$kJ & data_df$kJ<=1000] = "B) 500 to 1000 kJ"
data_df$kJ_cat[1000 < data_df$kJ & data_df$kJ<=1500] = "C) 1,000 to 1,500 kJ"
data_df$kJ_cat[1500 < data_df$kJ] = "D) greater than 1,500 kJ"
data_df$kJ_cat = as.factor(data_df$kJ_cat)
data_df$year = as.factor(year(data_df$start_date))
summary(data_df$kJ_cat)

g_base = ggplot(data=data_df)

#historgram of kJ
hist(data_df$kJ)
g_base + geom_histogram(aes(x=kJ),binwidth=500)

data_df %>% group_by(kJ_cat) %>%
  summarise(.,mean_distance = mean(distancedf2, na.rm=T),sd_distance = sd(distancedf2, na.rm=T),mean_elevation = mean(elevation,na.rm=T),sd_elevation = sd(elevation,na.rm=T))

#Plot distance vs kJ
ggplot(data=data_df,aes(x=distancedf2,y=kJ)) + geom_point(aes(color=watts_type))  + geom_smooth(method='lm') + labs(x="distance in miles", y="Energy in kJ", color='power data source')

#avg weighted power over time by kJ grouping
ggplot(data=data_df, aes(x=start_date,y=avg_weighted_watts))+geom_point(aes(color=watts_type)) + geom_smooth(method='lm') + facet_wrap(~kJ_cat) +labs(x='date', y='avg weighted power', color='power data source')

g_base + geom_bar(aes(x=kJ_cat))
g_base+geom_boxplot(aes(x=kJ_cat,y=distancedf2))

#Calories over time
g_base+geom_point(aes(x=start_date,y=Calories, col=watts_type)) + labs(x='date', y='Calories', color='power data source')
ggplot(data=data_df,aes(x=Calories)) +geom_histogram(binwidth=100) + facet_wrap(~year)
g_base + geom_boxplot(aes(x=kJ_cat,y=Calories))

#histogram of rides by year
ggplot(data=data_df,aes(x=year))+geom_bar()

#slope by year
ggplot(data=data_df[data_df$ft_per_mile<150,],aes(x=ft_per_mile))+geom_histogram(binwidth=5) +facet_wrap(~year) +xlab("feet climb per mile travelled")

