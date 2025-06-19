# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """Choose the fruit you want in your smoothie!
  """
)
name_on_order = st.text_input("Name on smoothie:")
st.write("The name on the smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()   
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients = st.multiselect(
    "Choose upto 5 ingredients:",
    my_dataframe,   
    max_selections=5
)
if ingredients:
        ingredients_string = ''
        for x in ingredients:
            ingredients_string+=x+' '
            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            st.subheader(x+'Nutrition Information')
            smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+x)
            sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = True)

    
        my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""
        # st.write(my_insert_stmt)

        time_to_insert = st.button('Submit order')
        if time_to_insert:
                    session.sql(my_insert_stmt).collect()
                    st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")


