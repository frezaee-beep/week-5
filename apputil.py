from unittest import result

import plotly.express as px
import pandas as pd
import streamlit as st
from apputil import *

# In this section, I want to create a function that can clean the column names as instructed: lowercase and put a underscore between words. 
def clean_column_name(column):
    result = ""

    for i, char in enumerate(column):
        if char.isupper() and i > 0:
            result += "_"

        result += char.lower()

    result = result.replace(" ", "_")
    return result


# This function loads the Titanic dataset and turn it into dataframe and then cleans the column names using the clean_column_name function.
#the second part it creates the age groups using pd.cut and then creates a new column called age_group. Finally, it returns the dataframe.
# then it groups the dataframe by pclass, sex, and age_group and calculates the number of passengers and number of survivors for each group.
def survival_demographics():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

    df = pd.read_csv(url)

    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 12, 19, 59, float("inf")],
        labels=["Child", "Teen", "Adult", "Senior"],
        include_lowest=True
    )
    result = (
        df.groupby(
            ["pclass", "sex", "age_group"],
            observed=False
        )
        .agg(
            n_passengers=("survived", "size"),
            n_survivors=("survived", "sum")
        )
        .reset_index()
    )
    result["survival_rate"] = (
        result["n_survivors"] / result["n_passengers"]
    )

    return result


def visualize_demographic():
    data = survival_demographics()

    fig = px.bar(
        data,
        x="age_group",
        y="survival_rate",
        color="sex",
        facet_col="pclass",
        barmode="group",
        category_orders={
            "age_group": ["Child", "Teen", "Adult", "Senior"]
        },
        labels={
            "age_group": "Age Group",
            "survival_rate": "Survival Rate",
            "sex": "Sex",
            "pclass": "Passenger Class"
        },
        title="Titanic Survival Rates by Age Group, Sex, and Passenger Class"
    )

    return fig


#Exercise 2: Create a function that groups the passengers by family size and calculates the number of passengers and number of survivors for each group.

def family_groups():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

    df = pd.read_csv(url)

    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]

    df["family_size"] = (
        df["sib_sp"] + df["parch"] + 1
    )
    result = (
        df.groupby(
            ["pclass", "family_size"]
        )
        .agg(
            n_passengers=("passenger_id", "size"),
            avg_fare=("fare", "mean"),
            min_fare=("fare", "min"),
            max_fare=("fare", "max")
        )
        .reset_index()
        .sort_values(["pclass", "family_size"])
    )

    return result

def last_names():
    url = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

    df = pd.read_csv(url)

    df.columns = [
        clean_column_name(column)
        for column in df.columns
    ]

    last_names = (
        df["name"]
        .str.split(",")
        .str[0]
        .str.strip()
    )

    return last_names.value_counts()

def visualize_families():
    data = family_groups()

    fig = px.line(
        data,
        x="family_size",
        y="avg_fare",
        color="pclass",
        markers=True,
        labels={
            "family_size": "Family Size",
            "avg_fare": "Average Ticket Fare",
            "pclass": "Passenger Class"
        },
        title="Average Ticket Fare by Family Size and Passenger Class"
    )

    return fig