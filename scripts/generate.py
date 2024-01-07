import os

import cached_conv as cc
import gin
import torch
import torchaudio
from absl import app, flags, logging

try:
    import rave
except:
    import os
    import sys

    sys.path.append(os.path.abspath("."))
    import rave


FLAGS = flags.FLAGS
flags.DEFINE_string(
    "input_violin", required=True, default=None, help="input signal (violin)"
)
flags.DEFINE_string(
    "input_flute", required=True, default=None, help="input signal (flute)"
)
flags.DEFINE_string("name", required=True, default=None, help="name of the run")
flags.DEFINE_string("model_name", default="best_model.ckpt", help="model name")
flags.DEFINE_string("model_path", default="models", help="model path")
flags.DEFINE_string("out_path", "generations", help="output path")
flags.DEFINE_integer("gpu", default=-1, help="GPU to use")
flags.DEFINE_integer(
    "chunk_size",
    default=None,
    help="chunk size for encoding/decoding (default: full file)",
)


def get_audio_files(path):
    audio_files = []
    valid_exts = rave.core.get_valid_extensions()
    for root, _, files in os.walk(path):
        valid_files = list(
            filter(lambda x: os.path.splitext(x)[1] in valid_exts, files)
        )
        audio_files.extend([(path, os.path.join(root, f)) for f in valid_files])
    return audio_files


def preprocessing(x, sr, model_sr, n_channels, filename):
    if sr != model_sr:
        x = torchaudio.functional.resample(x, sr, model_sr)
    # load file
    if n_channels != x.shape[0]:
        if n_channels < x.shape[0]:
            x = x[:n_channels]
        else:
            print(
                "[Warning] file %s has %d channels, butt model has %d channels ; skipping"
                % (filename, n_channels, n_channels)
            )
    return x


def main(argv):
    torch.set_float32_matmul_precision("high")

    model_path = os.path.join(FLAGS.model_path, FLAGS.name, FLAGS.model_name)
    paths = [FLAGS.input_violin, FLAGS.input_flute]

    # load model
    logging.info("building rave")
    is_scripted = False
    if not os.path.exists(model_path):
        logging.error("path %s does not seem to exist." % model_path)
        exit()
    if os.path.splitext(model_path)[1] == ".ts":
        model = torch.jit.load(model_path)
        is_scripted = True
    else:
        config_path = rave.core.search_for_config(model_path)
        if config_path is None:
            logging.error("config not found in folder %s" % model_path)
        gin.parse_config_file(config_path)
        model = rave.RAVE()
        run = rave.core.search_for_run(model_path)
        if run is None:
            logging.error("run not found in folder %s" % model_path)
        model = model.load_from_checkpoint(run)

    # device
    if FLAGS.gpu >= 0 and torch.cuda.is_available():
        # device = torch.device("cuda:%d" % FLAGS.gpu)
        device = torch.device("cuda")
        print("cuda:%d" % FLAGS.gpu)
        print(device)
        model = model.to(device)
    else:
        device = torch.device("cpu")

    # make output directories
    if FLAGS.name is None:
        FLAGS.name = "_".join(os.path.basename(model_path).split("_")[:-1])
    out_path = os.path.join(FLAGS.out_path, FLAGS.name)
    os.makedirs(out_path, exist_ok=True)

    # parse inputs
    receptive_field = rave.core.get_minimum_size(model)

    cc.MAX_BATCH_SIZE = 8

    f1 = FLAGS.input_violin
    # TODO reset cache
    try:
        x1, sr1 = torchaudio.load(f1)
    except:
        logging.warning("could not open file %s." % f1)
        return -1
    x1 = preprocessing(x1, sr1, model.sr, model.n_channels, f1).to(device)

    f2 = FLAGS.input_flute
    try:
        x2, sr2 = torchaudio.load(f2)
    except:
        logging.warning("could not open file %s." % f2)
        return -1
    x2 = preprocessing(x2, sr2, model.sr, model.n_channels, f2).to(device)

    # Encode each signal
    z1 = model.encode(x1[None])
    z1, _ = z1.chunk(2, 1)
    z2 = model.encode(x2[None])
    z2, _ = z2.chunk(2, 1)

    # Mix in the latent space
    z = (z1 + z2) / 2

    # Decode mixed signal
    out = model.decode(z).cpu()

    # save file
    out_path = os.path.join(FLAGS.out_path, FLAGS.name, "output.wav")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    torchaudio.save(out_path, out[0].cpu(), sample_rate=model.sr)

    logging.info(f"Output generated: {out_path}")


if __name__ == "__main__":
    app.run(main)
