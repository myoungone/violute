
build_docker:
	docker build -f ./Dockerfile --rm -t violute .

run_docker:
	docker run -it --ipc=host violute

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

get_data:
	mkdir -p data/sources
	cd data/sources && wget --load-cookies cookies.txt \
	   "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \
	   'https://docs.google.com/uc?export=download&id=1dLADkjp-5Va0OsKfe5EZkZtMdW3gRUTw' \
	   -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1dLADkjp-5Va0OsKfe5EZkZtMdW3gRUTw" -O training_data.tar.gz &&\
	   tar -xzf training_data.tar.gz &&\
	   rm -f cookies.txt &&\
	   rm -f training_data.tar.gz

get_model:
	mkdir -p models/violute
	cd models/violute && wget --load-cookies cookies.txt \
	   "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate \
	   'https://docs.google.com/uc?export=download&id=1-upj6o01NtagaoGftReKB2IXH7OrNQTP' \
	   -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-upj6o01NtagaoGftReKB2IXH7OrNQTP" best_model.cpkt -O &&\
	   rm -f cookies.txt


preprocess:
	python scripts/preprocess.py --input_path=./data/sources --output_path=./data/preprocessed

train:
	python scripts/train.py --name=violute --db_path=./data/preprocessed --max_steps=300000 --save_every=10000 --channels=1 --gpu=0

train_test:
	python scripts/train.py --name=violute --db_path=./data/preprocessed --max_steps=31 --save_every=10 --val_every=15 --channels=1 --gpu=0

generate:
	python scripts/generate.py --name=violute --input_violin=samples/sample_violin.wav --input_flute=samples/sample_flute.wav --gpu=0
