# violute

바이올린과 플룻의 음색이 섞인 새로운 음색의 소리를 생성합니다.

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

### Generation

미리 학습한 모델을 활용하여 새로운 음색의 소리를 생성하기 위해, 먼저 다음 명령으로 학습한 모델을 다운로드 받습니다.
(Docker 이미지를 빌드한 경우라면 이미지에 포함되어 있어 다운로드 받지 않고 바로 쓸 수 있습니다.)

    make get_model

주어진 샘플(sample_violin.wav, sample_flute.wav)을 사용하여 결과를 생성하려면 간단히 다음 명령을 사용할 수 있습니다.

    make generate

다른 샘플을 활용하고자 한다면 다음 명령에서 --input_violin 과 --input_flute 를 원하는 샘플 파일로 변경해서 실행합니다.

    python scripts/generate.py --name=violute --input_violin=samples/sample_violin.wav --input_flute=samples/sample_flute.wav --gpu=0

생성한 결과물은 generations/violute/output.wav 에서 확인할 수 있습니다.
