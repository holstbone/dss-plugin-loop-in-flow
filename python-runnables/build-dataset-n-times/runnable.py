# This file is the actual code for the Python runnable build-dataset-n-times
from dataiku.runnables import Runnable
from loopinflow.job_utils import ShortJobWaiter
import dataiku
import time



class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        # Create the main handle to interact with the scenario
        client = dataiku.api_client()
        p = client.get_default_project()
        dataset = p.get_dataset(self.config["final_dataset"])
        dataset.clear()
        
        
        # Build a dataset a bunch of times
        for i in range(0,int(self.config["times_to_build"])):
            start = time.time()

            job = dataset.build(job_type = 'RECURSIVE_FORCED_BUILD', wait= True)
            #ShortJobWaiter(job).wait(job)
            
            end = time.time()
            print("time between runs: " + str(end - start))
        return('SUCCESS!!!')
