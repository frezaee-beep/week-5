import streamlit as st

from apputil import *


# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
    """
    ## How did survival rates differ by age group and sex across passenger classes?
    """
)
# Generate and display the figure
fig1 = visualize_demographic()
st.plotly_chart(fig1, use_container_width=True)

st.write(
    """
    ## Family Size and Surnames

    The two measures do not agree exactly. Family size is calculated from
    siblings/spouses and parents/children traveling with each passenger,
    while the last-name count simply measures how many passengers share
    the same surname. For example, the largest calculated family size is
    11, while the most common surname, Andersson, appears 9 times.
    """
)
# Generate and display the figure How does average ticket fare vary with family size across passenger classes?
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)


