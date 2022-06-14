from featureExtraction.utils import pss_extraction_utils_updated
from featureExtraction import extract_pss,create_histograms_updated
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from caveclient import CAVEclient
import warnings
warnings.filterwarnings("ignore")


allids = []
allhists = []
allpreds = []
allscores = []
allpsssholl = []
index = 0
sholl_radii_upper = range(15000,60000,15000)
sholl_radii_lower = range(0,45000,15000)

sholl_bins = 4
bin_size = 15000
min_bin = 0

client = CAVEclient('minnie65_phase3_v1',auth_token_file='/usr/local/featureExtractionParty/chunkedgraph-secret.json')
#nuc_df = client.materialize.query_table('allen_v1_column_types_slanted',
#                                        filter_out_dict={'classification_system':['aibs_coarse_unclear','aibs_coarse_error','aibs_coarse_nonneuronal']},materialization_version=117)

     

cluster_center_file = 'cluster_centers_V3_30binsmanualordered.pkl'
cluster_centers = pd.read_pickle(cluster_center_file)
kmeans = KMeans(n_clusters=30, init='k-means++', max_iter=3000, n_init=10, random_state=0)
kmeans.fit(cluster_centers)
kmeans.cluster_centers_ = np.array(cluster_centers)

celllist = [864691135644671215]
all_histograms = []
for cell_id in celllist:

#   read and query    
    data_synapses = client.materialize.query_table('synapses_pni_2',
                                        filter_in_dict={'post_pt_root_id':['%d'%cell_id]},materialization_version=117)
    file_prefix = '/usr/local/allen/programs/celltypes/workgroups/em-connectomics/analysis_group/forSharmi/psstestoutput/'
    filename = file_prefix + '%d.pkl'%cell_id
    pss_only = pd.read_pickle(filename)
    origpss = pss_only.merge(data_synapses,on='id')
    pss = origpss[origpss['PSSfeatures'].map(len) > 1]
    
    #shape features and bins
    featureslist = list(pss['PSSfeatures'].values)
    features=np.stack( featureslist, axis=0 )
    labels = kmeans.predict(features)
    score = kmeans.score(features)
    hist,f = np.histogram(labels,bins=30)
    print("This is hist")
    print(hist)

    #sholl
    cell_center =client.materialize.query_table('nucleus_detection_v0',filter_in_dict={'pt_root_id':['%d'%cell_id]}, materialization_version = 117)['pt_position'].values[0] * [4,4,40]
    synapse_pts =pss['ctr_pt_position'].values
    synapse_pts = synapse_pts.transpose()
    synapse_pts = np.stack(synapse_pts)*[4,4,40]
    dists = np.linalg.norm(synapse_pts  - cell_center, axis = 1)

    #create histogram
    pss_sholl = []
    for lab in range(0,30):
        labind = np.where(labels==lab)
        mydist = dists[labind]

        sholl = []
        cur_bin = min_bin
        for r in range(sholl_bins):
            lower = cur_bin
            upper = lower + bin_size
            sholl.append(len(np.where((mydist<upper) & (mydist>=lower))[0]))
            cur_bin = upper
    
        pss_sholl.extend(sholl)

    print("This is pss_sholl:")
    print(pss_sholl)
    all_histograms.append(pss_sholl)


#final histogram containing all sholl features: allhistograms

#to visualize it : 
#just one of them:
hist = np.reshape( np.array(all_histograms[0]), (30, 4))
hist = hist.transpose()
print(hist[:,2])

import seaborn as sns
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(20, 5), dpi=50)
fig.patch.set_facecolor((1.0,1.0,1.0))

cmap = sns.light_palette("gray", as_cmap=True)

plt.subplot(411)
sns.heatmap([hist[3,:]],linewidths=.5, cmap = cmap,cbar=False)
plt.yticks([])
plt.xticks([])

plt.subplot(412)
sns.heatmap([hist[2,:]],linewidths=.5, cmap = cmap,cbar=False)
plt.yticks([])
plt.xticks([])


plt.subplot(413)
sns.heatmap([hist[1,:]],linewidths=.5, cmap = cmap,cbar=False)
plt.yticks([])
plt.xticks([])


plt.subplot(414)
sns.heatmap([hist[0,:]],linewidths=.5, cmap = cmap,cbar=False)
plt.yticks([])
plt.xticks([])
plt.xticks(fontsize= 20)

fig.savefig('/usr/local/allen/programs/celltypes/workgroups/em-connectomics/analysis_group/forSharmi/code/featureExtractionParty/Sharmitestdump/temp.png', dpi=fig.dpi)