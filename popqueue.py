from taskqueue import TaskQueue
#import MY_MODULE # MY_MODULE contains the definitions of RegisteredTasks
from taskqueue import queueable
from featureExtraction.utils import pss_extraction_utils_updated, taskqueue_utils
import os
os.environ['NO_GCE_CHECK'] = 'true'

@queueable
def print_task(txt):
  print(str(txt))


def stop_function (executed):
  if executed > 0:
    return True
  else:
    return False

print("About to start processing")
tq = TaskQueue('sqs://sharmi_pss', region_name="us-west-2", green=False)
tq.poll(
  lease_seconds=int(3000),
  verbose=True, # print out a success message
  tally=True, # count number of tasks completed (fq only!)
  stop_fn  = stop_function
)
