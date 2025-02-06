# Importing required modules
import pandas as pd
from numerize.numerize import numerize

# Creating a function for formating the values
def change_value_format(value, decimal = True):
    """
    Function for changing the format of the large values

    Parameter:
    - value: The value whose format needs to be changed.
    - decimal: To show values in floating point format.
    """
    if not decimal and value >=1000:
        ending_char = numerize(value)[-1]
        return f"{round(float(numerize(value)[:-1]))}{ending_char}"
    elif not decimal:
        return round(value)
    
    return numerize(value)


# Creating a function for annotating the bars
def annotate_bars(ax, decimal = True):
    """
    Function for annotating the bars.

    Parameter:
    - ax: The axis object of the plot.
    - decimal: To show values in floating point format.
    """

    # Importing numerize for formatting the values
    from numerize.numerize import numerize

    # Looping through each bar
    for bar in ax.patches:
        # Checking if the height of the bar is > 0
        if bar.get_height() > 0:
            # Annotating the bar
            ax.annotate(
                change_value_format(bar.get_height(), decimal),
                (bar.get_x() + bar.get_width()/2, bar.get_height()),
                ha = 'center', va = 'bottom', fontweight = 'bold'
            )


def convert_to_categories(data, column_name, bins, labels, replace=False):
    """
    Converts a continuous column to categorical by binning the values.

    Parameters:
    - data (pd.DataFrame): The DataFrame object.
    - column_name (str): The column name to modify.
    - bins (list): List of bin edges to define the ranges.
    - labels (list): List of labels to assign to the ranges.
    - replace (bool): If True, replace the original column. If False, create a new column.

    Returns:
    - pd.DataFrame: The updated DataFrame with the new categorical column.
    """
    
    if replace:
        data[column_name] = pd.cut(data[column_name], bins=bins, labels=labels)
        data = change_category_order(data, column_name)
    else:
        data[column_name + "_binned"] = pd.cut(data[column_name], bins=bins, labels=labels)
        data = change_category_order(data, column_name + "_binned")

    return data


def change_category_order(data, column_name):
    """
    Function to add new categories and reorder existing categories.
    
    Parameters:
    - Data: The DataFrame object.
    - column_name: The column name to modify.
    
    Returns:
    - Updated DataFrame with modified categorical column.
    """
    
    # Checking if we have null values to add a new category
    if data[column_name].isnull().sum() > 0:
            data[column_name] = data[column_name].cat.add_categories(["N"])                                # Adding new category
            data[column_name] = data[column_name].fillna("N")                                               # Filling the null values with the new category
            new_order = ["N"] +  [cat for cat in list(data[column_name].cat.categories) if cat != "N"]
            data[column_name] = data[column_name].cat.reorder_categories(new_categories = new_order)       # Reordering the categories

    return data

