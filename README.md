###  Kinect a la Luna

###### Nvidia Docker toolkit on Ubuntu 18.04 or 20.04
Set distribution variable based on your system's configuration.
```
distribution=ubuntu18.04

distribution=ubuntu20.04
```
```
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
source: [nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-docker/issues/1186)

###### Build payload's Docker image
```
cd LUNA-R2D2/
docker build -t payload_image .
```
* This docker image will install the following key packages:
 * python3 and python3-pip
 * k4a-tools and libk4a1.4-dev
 * software-properties-common, curl, build-essential...etc

###### Run payload's Docker container
```
sudo chmod +x ./scripts/launch_container.sh
sudo ./scripts/launch_container.sh payload_container payload_image
```

###### Configuration on dev host machine:
```
xhost +local:docker
```
