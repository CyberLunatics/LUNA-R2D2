###
### To Build:
### docker build -t payload_image <path_to_folder_containing_Dockerfile>
###
### To Run:
### ./scripts/run.sh
###

### Base image for your container
FROM nvidia/cuda:11.4.0-base-ubuntu18.04

### Install required packages/dependencies
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    curl \
    software-properties-common

### Update sources lists
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    apt-add-repository https://packages.microsoft.com/ubuntu/18.04/multiarch/prod

### Install more
RUN apt update && ACCEPT_EULA=y apt install -y k4a-tools && \
    apt install -y \
    libk4a1.4-dev \
    build-essential

### Copy source code to container
COPY src /home/payload/workspace/src
## COPY include /home/payload/workspace/include
####COPY scripts /home/payload/workspace/scripts
####RUN chmod +x /home/payload/workspace/scripts/*.sh

### build payload software (if building is required)
RUN gcc -g -Wall  /home/payload/workspace/src/check-device.cpp -o /usr/local/bin/check-device -lk4a -lstdc++; \
    gcc -g -Wall  /home/payload/workspace/src/capture-stream.c -o /usr/local/bin/capture-stream -lk4a; \
    gcc -g -Wall /home/payload/workspace/src/capture-disk.c -o /usr/local/bin/capture-disk -lk4a

# Dependencies for glvnd and X11.
RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
  && rm -rf /var/lib/apt/lists/*

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

# RUN mkdir -p /home/payload/workspace/build &&\
#     cd /home/payload/workspace/build &&\
#     cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local ../src &&\
#     make &&\
#     make install

### Remove build sources
# RUN rm -rf /home/payload/workspace/build

### Set payload entrypoint
####CMD ["/bin/bash", "/home/payload/workspace/scripts/entrypoint.sh"]

# EOF
