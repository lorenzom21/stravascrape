import pandas as pd 


df1 = pd.read_csv("spider1_output.csv", index_col='ride_id')
df2 = pd.read_csv("spider2_output.csv", index_col='ride_id')

joined_df=df1.join(df2, how='inner', lsuffix='df1',rsuffix='df2')

joined_df.to_csv('joined_df.csv')