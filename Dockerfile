
# base layer
FROM ros:jazzy-perception

SHELL ["/bin/bash", "-c"]

# environment setup
RUN apt-get update && apt upgrade -y && \
	apt-get install python3-pip vim -y

# Install pip packages into system python
# --break-system-packages tells pip to ignore warning to enter into system python manager.
RUN pip3 install --break-system-packages \
    "ultralytics==8.3.0" \
    "numpy>=1.24.0,<2.0.0"

WORKDIR "/ros2_projects/yolodetection_rosws"

CMD ["/bin/bash"]
