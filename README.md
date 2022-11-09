###  Kinect a la Luna
###### build docker image
```
sudo docker build . -t kinect/luna
```

###### Nvidia Docker toolkit
```
distribution=ubuntu18.04
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
source: [nvidia-container-toolkit](https://github.com/NVIDIA/nvidia-docker/issues/1186)

###### run docker container
```
sudo chmod +x /scripts/run.sh
sudo ./run.sh [option] image_name
```
###### configuration on host machine:
```
xhost +local:docker
```

