#!/usr/bin/env python
# coding: utf-8

# In[29]:


import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[30]:


import sqlite3
import pandas as pd
import datetime


# In[31]:


import os
os.getcwd()
os.chdir('/Users/zacharychild/Desktop/')


# In[63]:


get_ipython().system('pip install pillow')
get_ipython().system('pip install wordcloud')
#pillow
#wordcloud


# In[64]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[65]:


from PIL import Image


# In[36]:


conn = sqlite3.connect('/Users/zacharychild/Desktop/chat.db')
cur = conn.cursor()


# In[37]:


# get the names of the tables in the database
# query the database to get all the table names
cur.execute(" select name from sqlite_master where type = 'table' ")

for name in cur.fetchall():
    print(name)


# In[38]:


# create pandas dataframe with all the tables you care about.

## Mac OSX versions below High Sierra
#messages = pd.read_sql_query("select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message", conn) 

## High Sierra and above
messages = pd.read_sql_query('''select *, datetime(date/1000000000 + strftime("%s", "2001-01-01") ,"unixepoch","localtime")  as date_utc from message''', conn) 

handles = pd.read_sql_query("select * from handle", conn)
chat_message_joins = pd.read_sql_query("select * from chat_message_join", conn)


# In[39]:


# these fields are only for ease of datetime analysis (e.g., number of messages per month or year)
messages['message_date'] = messages['date']
messages['timestamp'] = messages['date_utc'].apply(lambda x: pd.Timestamp(x))
messages['date'] = messages['timestamp'].apply(lambda x: x.date())
messages['month'] = messages['timestamp'].apply(lambda x: int(x.month))
messages['year'] = messages['timestamp'].apply(lambda x: int(x.year))


# rename the ROWID into message_id, because that's what it is
messages.rename(columns={'ROWID' : 'message_id'}, inplace = True)

# rename appropriately the handle and apple_id/phone_number as well
handles.rename(columns={'id' : 'phone_number', 'ROWID': 'handle_id'}, inplace = True)


# In[40]:


merge_level_1 = pd.merge(messages[['text', 'handle_id', 'date','message_date' ,'timestamp', 'month','year','is_sent', 'message_id']],  handles[['handle_id', 'phone_number']], on ='handle_id', how='left')

# and then that table with the chats
df_messages = pd.merge(merge_level_1, chat_message_joins[['chat_id', 'message_id']], on = 'message_id', how='left')


print(len(df_messages))
#print(df_messages.head())


# In[41]:


df_messages.to_csv('./imessages_high_sierra.csv', index = False, encoding='utf-8')


# In[165]:


df_messages.columns


# In[42]:


df_messages['date'].min(), df_messages['date'].max()


# In[43]:


plt.plot(df_messages.groupby('date').size())
plt.xticks(rotation='45')


# In[44]:


df_messages.groupby('is_sent').size()


# In[45]:


df_messages.groupby('month').size()
df_messages.groupby('year').size()


# In[46]:


df_messages.columns


# In[227]:


df_messages.head(122300)


# In[ ]:





# In[ ]:





# ### Wife Messages

# In[179]:


wife_messages = df_messages[df_messages['phone_number'] == '+12086803016'].reset_index(drop=True)


# In[72]:


plt.plot(wife_messages.groupby('date').size())
plt.xticks(rotation='45')


# In[73]:


wife_messages.groupby('is_sent').size()


# In[88]:


wife_messages.head(-5)


# In[101]:


len(wife_messages.loc[48512,'text'])


# In[107]:


wife_messages.info()


# In[180]:


#Remove all GIFS
wife_messages = wife_messages[wife_messages['text'].isna()==False].reset_index(drop=True)


# In[181]:


wife_messages = wife_messages[wife_messages['text'].map(len) > 1].reset_index(drop=True)


# In[182]:


wordcloudstr = ' '.join(list(wife_messages['text']))


# In[121]:


wordcloudstr


# In[119]:


text = wife_messages.text[:2]
print(text)


# In[183]:


wordcloud = WordCloud().generate(wordcloudstr)


# In[184]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[185]:


wordcloud.to_file("Taylor_WordCloud.png")


# ### Dad

# In[186]:


dad_messages = df_messages[df_messages['phone_number'] == '+13038084495'].reset_index(drop=True)


# In[187]:


dad_messages.head()


# In[188]:


dad_messages = dad_messages[dad_messages['text'].isna()==False].reset_index(drop=True)


# In[189]:


dad_messages = dad_messages[dad_messages['text'].map(len) > 1].reset_index(drop=True)


# In[190]:


wordcloudstrdad = ' '.join(list(dad_messages['text']))


# In[191]:


wordcloud = WordCloud().generate(wordcloudstrdad)


# In[192]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[193]:


wordcloud.to_file("Dad_WordCloud.png")


# ### Mom 

# In[194]:


mom_messages = df_messages[df_messages['phone_number'] == '+13037041089'].reset_index(drop=True)


# In[195]:


mom_messages = mom_messages[mom_messages['text'].isna()==False].reset_index(drop=True)


# In[196]:


mom_messages = mom_messages[mom_messages['text'].map(len) > 1].reset_index(drop=True)


# In[197]:


wordcloudstrmom = ' '.join(list(mom_messages['text']))


# In[198]:


wordcloud = WordCloud().generate(wordcloudstrmom)


# In[199]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[200]:


wordcloud.to_file("Mom_wordcloud.png")


# ### Kevin 

# In[256]:


kevin_messages = df_messages[df_messages['phone_number'] == '+18018859578'].reset_index(drop=True)


# In[257]:


kevin_messages = kevin_messages[kevin_messages['text'].isna()==False].reset_index(drop=True)


# In[258]:


kevin_messages = kevin_messages[kevin_messages['text'].map(len) > 1].reset_index(drop=True)


# In[259]:


wordcloudstrkevin = ' '.join(list(kevin_messages['text']))


# In[264]:


wordcloudstrkevin = wordcloudstrFamily.replace('Brigham', '')


# In[265]:


wordcloud = WordCloud().generate(wordcloudstrkevin)


# In[266]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[267]:


wordcloud.to_file("Kevin_wordcloud.png")


# In[ ]:





# ### Chloe

# In[209]:


chloe_messages = df_messages[df_messages['phone_number'] == '+18017457460'].reset_index(drop=True)


# In[210]:


chloe_messages = chloe_messages[chloe_messages['text'].isna()==False].reset_index(drop=True)


# In[211]:


chloe_messages = chloe_messages[chloe_messages['text'].map(len) > 1].reset_index(drop=True)


# In[212]:


wordcloudstrchloe = ' '.join(list(chloe_messages['text']))


# In[213]:


wordcloud = WordCloud().generate(wordcloudstrchloe)


# In[214]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[215]:


wordcloud.to_file("chloe_wordcloud.png")


# In[ ]:





# ## Samantha

# In[216]:


sam_messages = df_messages[df_messages['phone_number'] == '+13034761190'].reset_index(drop=True)


# In[217]:


sam_messages = sam_messages[sam_messages['text'].isna()==False].reset_index(drop=True)


# In[218]:


sam_messages = sam_messages[sam_messages['text'].map(len) > 1].reset_index(drop=True)


# In[219]:


wordcloudstrsam = ' '.join(list(chloe_messages['text']))


# In[220]:


wordcloud = WordCloud().generate(wordcloudstrsam)


# In[221]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[222]:


wordcloud.to_file("sam_wordcloud.png")


# ## Family Group Chat

# In[230]:


familyGroup_messages = df_messages[df_messages['chat_id'] == 44.0].reset_index(drop=True)


# In[231]:


familyGroup_messages = familyGroup_messages[familyGroup_messages['text'].isna()==False].reset_index(drop=True)


# In[232]:


familyGroup_messages = familyGroup_messages[familyGroup_messages['text'].map(len) > 1].reset_index(drop=True)


# In[233]:


wordcloudstrFamily = ' '.join(list(familyGroup_messages['text']))


# In[252]:


wordcloudstrFamily = wordcloudstrFamily.replace('Laughed', '')


# In[253]:


wordcloud = WordCloud().generate(wordcloudstrFamily)


# In[254]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[255]:


wordcloud.to_file("Family_wordcloud.png")


# ### Bethan

# In[166]:


bethan_messages = df_messages[df_messages['phone_number'] == '+18014507437'].reset_index(drop=True)


# In[167]:


bethan_messages = bethan_messages[bethan_messages['text'].isna()==False].reset_index(drop=True)


# In[168]:


bethan_messages = bethan_messages[bethan_messages['text'].map(len) > 1].reset_index(drop=True)


# In[172]:


wordcloudstrbethan = ' '.join(list(bethan_messages['text']))


# In[173]:


wordcloud = WordCloud().generate(wordcloudstrbethan)


# In[174]:


plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# In[177]:


wordcloud.to_file("first_review.png")


# In[178]:


bethan_messages.groupby('is_sent').size()


# In[ ]:





# In[ ]:





# In[149]:


df_messages['phone_number'].value_counts()


# In[58]:


df.columns


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[55]:


df.to_csv("TextMessageData.csv",index=False)


# In[56]:


export_excel = df.to_excel (r'C:\Users\zacharychild\Desktop\export_dataframe.xlsx', index = None, header=True)



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




