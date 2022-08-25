###
### To Build:
### docker build -t payload_image <path_to_folder_containing_Dockerfile>
###
### To Run:
### ./scripts/launch_container.sh
###


### Base image for your container
FROM ubuntu:18.04


### Install required packages/dependencies
RUN apt update && apt install -y \
#    python3 \
#    python3-pip \
    curl \
    software-properties-common

### Update sources lists
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    apt-add-repository https://packages.microsoft.com/ubuntu/18.04/multiarch/prod

### Install more
RUN apt update && printf "yes\n" | apt install -y k4a-tools && \
    apt install -y \
    libk4a1.4-dev \
    build-essentials

### Copy source code to container
####COPY src /home/payload/workspace/src
## COPY include /home/payload/workspace/include
####COPY scripts /home/payload/workspace/scripts
####RUN chmod +x /home/payload/workspace/scripts/*.sh

### build payload software (if building is required)
# https://gist.github.com/madelinegannon/c212dbf24fc42c1f36776342754d81bc#installing-sensor-sdk-on-jetson-xavier-nx
#
# RUN mkdir -p /home/payload/workspace/build &&\
#     cd /home/payload/workspace/build &&\
#     cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ../src &&\
#     make &&\
    # make install

### Remove build sources
# RUN rm -rf /home/payload/workspace/build

### Set payload entrypoint
####CMD ["/bin/bash", "/home/payload/workspace/scripts/entrypoint.sh"]

# EOF
