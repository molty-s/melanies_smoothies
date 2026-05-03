# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col;
import requests  

# Write directly to the app.
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

title = st.text_input('Name on Smoothie:')
st.write('The current movie title is', title)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

options = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

if options :
    options_str = ''

    for fruit_chose in options:
        options_str += fruit_chose + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chose, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chose,' is ', search_on, '.')
      
        st.subheader(fruit_chose + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = " insert into smoothies.public.orders(ingredients,name_on_order) values ('" + options_str + "','" + title + "')"

    time_to_insert = st.button('Submit Order')

    # st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

