import warnings
warnings.filterwarnings("ignore")
from featureExtraction.utils import pss_extraction_utils_updated
from featureExtraction.utils import pss_extraction_utils_updated, taskqueue_utils
from taskqueue import TaskQueue
from taskqueue import queueable
from functools import partial
import sys
import json
import numpy as np
from caveclient import CAVEclient
import pandas as pd


config_file = (sys.argv[2])
threshold = 65000

#setup connection
with open(config_file) as f:
      cfg = json.load(f)
client = CAVEclient(cfg['dataset_name'],auth_token_file=cfg['auth_token_file'])


#get cells
if sys.argv[1] == "None":
    fname = '/usr/local/allen/programs/celltypes/workgroups/em-connectomics/analysis_group/soma_paper/all_minnie_soma_features_v117_w_labels_filtered_010421.pkl'
    fname = '/usr/local/allen/programs/celltypes/workgroups/em-connectomics/analysis_group/soma_paper/minnie_w_errors_classified_060322.pkl'
    cells_minnie = pd.read_pickle(fname)
    cells_minnie = cells_minnie.query('soma_object_preds !=0 & soma_soma_merge==False & frac_zeros < 0.2 & cell_merged == True')
    cells_minnie = cells_minnie.query('soma_neuron_class_preds == 1')
    #allcells = cells_minnie.query('new_pred_1 == 1').pt_root_id.values[1400:5000] #NEURONS # jobs that were sent on cloud
    #allcells = cells_minnie.query('new_pred_1 == 1').pt_root_id.values[5010:5100] #NEURONS # 
    allcells = cells_minnie[11:12].pt_root_id.values
    #print(allcells)

else:
    f = open(sys.argv[1])
    input = json.load(f)    
    allcells = input['cells']

tasks = (partial(pss_extraction_utils_updated.myprocessingTask_cellid_feature,config_file,cellid) for cellid in allcells)
tq = TaskQueue('sqs://sharmi_pss', region_name="us-west-2", green=False)
tq.insert(tasks)

