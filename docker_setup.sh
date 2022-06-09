
git clone https://github.com/AllenInstitute/featureExtractionParty.git

docker build -t shtaaa/pss_extraction . --no-cache --pull
docker kill shtaaa_pss_extraction
docker rm shtaaa_pss_extraction

#xhost +si:localuser:$(whoami) >/dev/null

#docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi
#docker run --runtime=nvidia --shm-size=1g -e NVIDIA_VISIBLE_DEVICES=0 -d --name sharmi_pointnet_autoe \
nvidia-docker run -d --restart unless-stopped --name shtaaa_pss_extraction \
-v /allen/programs/celltypes/workgroups/em-connectomics/analysis_group/forSharmi/code/Dockertest_github:/usr/local/test \
-v /allen:/usr/local/allen \
-e AWS_ACCESS_KEY_ID=AKIAZE5KZHQ3L56GWEON \
-e AWS_SECRET_ACCESS_KEY=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  \
-e AWS_DEFAULT_REGION=us-west-2 \
-p 9780:9780 \
-e "PASSWORD=$JUPYTERPASSWORD" \
-e DISPLAY \
--privileged \
-i -t shtaaa/pss_extraction  \
/bin/bash -c "sudo initialize-graphics >/dev/null 2>/dev/null; vglrun glxspheres64; jupyter notebook --allow-root ;"

#/bin/bash -c "python popqueue.py ;"

#/bin/bash -c "sudo initialize-graphics >/dev/null 2>/dev/null; vglrun glxspheres64; jupyter notebook --allow-root ; python popqueue.py"

