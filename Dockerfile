FROM hmurari/docker-nvidia-pytorch-opencv-ffmpeg

COPY . ./violute

WORKDIR /violute

RUN make install
RUN make get_model
