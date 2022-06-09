FROM shtaaa/pss_feature_extract:v19

RUN apt-get install  git
#RUN apt-get install  openssh-server -y

WORKDIR /root/.cloudvolume/secrets
COPY google-secret.json .

#WORKDIR /usr/local/featureExtractionParty/external/pointnet_spine_ae
#COPY pointnet_spine_ae/ .

#WORKDIR /usr/local/featureExtractionParty/featureExtraction
#COPY featureExtraction /usr/local/featureExtractionParty/featureExtraction

WORKDIR /usr/local/
COPY featureExtractionParty /usr/local/featureExtractionParty


WORKDIR /usr/local/featureExtractionParty/
RUN pip install  -e .
COPY chunkedgraph-secret.json .


WORKDIR /usr/local/test

