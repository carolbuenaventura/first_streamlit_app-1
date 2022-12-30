import streamlit
import snowflake.connector
import pandas
# --2b import requests
from urllib.error import URLError


streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmel')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice  streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error("Please select a fruit to get information.")
  else:
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     streamlit.dataframe(fruityvice_normalized)
      
      
      
      
      
      

# Display the table on the page

#--1a fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
fruit_choice = streamlit.text_input('What fruit would you like information about?')
streamlit.write('The user entered ', fruit_choice)






fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)



# --3c take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# --4d output it the screen as a table
streamlit.dataframe(fruityvice_normalized)



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# --1 my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
# --2 streamlit.text("Hello from Snowflake:")
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('The user entered ', add_my_fruit)



streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")



#don't run anything past here while we troubleshoot
streamlit.stop()
