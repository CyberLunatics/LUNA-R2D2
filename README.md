###  Kinect a la Luna
###### build docker image
```
sudo docker build -t kinect/luna
```
###### run docker container
```
sudo chmod +x /scripts/run.sh
sudo ./run.sh [option] image_name
```
###### configuration on host machine:
```
xhost +local:docker
```

