import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

input_A_names = get_input_names_for_role('starter_dataset')
input_dataset = [name for name in input_A_names][0]

output_A_names = get_output_names_for_role('iterated_dataset')
output_dataset = [name for name in output_A_names][0]


final_dataset_in_loop = get_recipe_config()['final_dataset']

input_dataset = dataiku.Dataset(input_dataset)

try:
    total_footage_full_recalcuation = dataiku.Dataset(final_dataset_in_loop, ignore_flow=True)
    print("dataset accessed flow ignored")
    output_df = total_footage_full_recalcuation.get_dataframe()
    print("dataframe accessed")
    print("dataframe size: " + str(len(output_df)))
except:
    print("Output Dataset Doesn't Exist")
    output_df = input_dataset.get_dataframe()

# Write recipe outputs
if_exists = dataiku.Dataset(output_dataset)
if_exists.write_with_schema(output_df)