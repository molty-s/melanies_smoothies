# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col;

# Write directly to the app.
st.title(":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

title = st.text_input('Name on Smoothie:')
st.write('The current movie title is', title)

cnx = st.connection("Snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

options = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

if options :
    options_str = ''

    for fruit_chose in options:
        options_str += fruit_chose + ' '

    my_insert_stmt = " insert into smoothies.public.orders(ingredients,name_on_order) values ('" + options_str + "','" + title + "')"

    time_to_insert = st.button('Submit Order')

    # st.write(my_insert_stmt)
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
