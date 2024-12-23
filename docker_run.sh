#!/bin/bash

# 允许 X server 连接
xhost +

# 检查是否存在名为 pinU20 的容器
container_name="pinU20"
existing_container=$(sudo docker ps -a -q -f name="^/${container_name}$")

if [ -n "$existing_container" ]; then
  echo "Container with name '$container_name' already exists. Stopping and removing it..."
  sudo docker stop "$existing_container"
  sudo docker rm "$existing_container"
fi

# 运行新的容器
sudo docker run -it --privileged --net=host\
  -v /home/lee:/home/lee \
  --device=/dev/dri \
  --group-add video \
  --volume=/tmp/.X11-unix:/tmp/.X11-unix \
  --env="DISPLAY=$DISPLAY" \
  --env="QT_X11_NO_MITSHM=1" \
  --name="$container_name" \
  ubuntu20_pino_cro:v0 /bin/bash
