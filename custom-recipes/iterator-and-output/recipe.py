
import dataiku
import dataikuapi
import time
from loopinflow.job_utils import ShortJobWaiter

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

input_A_names = get_input_names_for_role('starter_dataset')
input_dataset_name = [name for name in input_A_names][0]

output_A_names = get_output_names_for_role('output_copy')
output_dataset = [name for name in output_A_names][0]
print(output_A_names)

final_ds = get_recipe_config()["final_dataset"]

# get client
client = dataiku.api_client()
current_project = client.get_project(dataiku.default_project_key())

# clear final dataset
dataset = current_project.get_dataset(final_ds)
dataset.clear()

# ensure loop runs only over local setup
input_dataset = current_project.get_dataset(input_dataset_name.split('.')[-1]) #this is an ugly way to get the dataset name
settings = input_dataset.get_settings()
orig_behavior = settings.settings['flowOptions']['rebuildBehavior']
settings.settings['flowOptions']['rebuildBehavior'] = 'EXPLICIT'
settings.save()

# Run the loop a bunch of times
try:
    for i in range(0,int(get_recipe_config()["times_to_build"])):
        start = time.time()

        job = dataset.build(job_type = 'RECURSIVE_FORCED_BUILD', wait= False)
        ShortJobWaiter(job).wait(job)

        end = time.time()
        print("time between runs: " + str(end - start))

    ds = dataiku.Dataset(final_ds, ignore_flow = True)
    df = ds.get_dataframe()

    out = dataiku.Dataset(output_dataset)
    out.write_with_schema(df)
    
finally:
    # return the dataset's build to its default behavior
    settings.settings['flowOptions']['rebuildBehavior'] = orig_behavior
    settings.save()

