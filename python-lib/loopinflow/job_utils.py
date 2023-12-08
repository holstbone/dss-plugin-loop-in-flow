import time
import sys
from .utils import DataikuException

class ShortJobWaiter(object):
    """
    Creates a helper to wait for the completion of a job.
    
    :param job: The job to wait for
    :type job: :class:`dataikuapi.dss.job.DSSJob`
    """
    def __init__(self, job):
        self.job = job

    def wait(self, no_fail=False):
        """
        Waits for the job to finish. If the job fails or is aborted,
        an exception is raised unless the `no_fail` parameter is set to True.
        
        :param boolean no_fail: (optional) should an error be raised if the job finished with another status than `DONE` (defaults to **False**)

        :raises DataikuException: when the job does not complete successfully

        :returns: the job state
        :rtype: dict
        """
        job_state = self.job.get_status().get("baseStatus", {}).get("state", "")
        sleep_time = 0.5
        while job_state not in ["DONE", "ABORTED", "FAILED"]:
            sleep_time = 10 if sleep_time >= 10 else sleep_time * 1.1
            time.sleep(int(sleep_time))
            job_state = self.job.get_status().get("baseStatus", {}).get("state", "")

        if no_fail or (job_state == "DONE"):
            return job_state
        
        raise DataikuException("Job run did not finish. Status: %s" % (job_state))