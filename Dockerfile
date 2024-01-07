FROM hmurari/docker-nvidia-pytorch-opencv-ffmpeg

COPY . ./violute

WORKDIR /violute

RUN make install
