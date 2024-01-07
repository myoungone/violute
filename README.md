# violute

## Install

### Docker

다음 명령을 사용하여 Docker 이미지를 빌드하고 실행할 수 있습니다.

    docker build -f ./Dockerfile --rm -t violute .
    docker run -it --ipc=host violute

간단히 make 를 사용하여 다음과 같이 같은 동작을 수행할 수 있습니다.

    make build_docker
    make run_docker

### Conda

다음 명령으로 필요한 파일을 설치할 수 있습니다.

    pip install --upgrade pip && pip install -r requirements.txt

모델 학습이 필요하다면 데이터 전처리에 ffmpeg 소프트웨어가 필요합니다. 다음 명령으로 설치해 줍니다.

    conda install ffmpeg

## Usage

