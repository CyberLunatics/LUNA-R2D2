# Expose the X server on the host.
sudo xhost +local:root
# --rm: Make the container ephemeral (delete on exit).
# -it: Interactive TTY.
# --gpus all: Expose all GPUs to the container.
sudo docker run \
  --rm \
  -it \
  --gpus all --privileged \
  -v /srv/r2d2/mkv:/mkv \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  $1 \
  bash
