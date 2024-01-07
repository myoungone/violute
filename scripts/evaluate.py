import torch

try:
    import rave

except ModuleNotFoundError:
    import os
    import sys

    sys.path.append(os.path.abspath("."))
    import rave

import rave.core

import scipy.io.wavfile as wave

# model = rave.core.AudioDistanceV1
model = rave.core.SpectralDistance(
    n_fft=4096, sampling_rate=44100, norm=["L1", "L2"], power=2, normalized=True
)

rate, sig_f = wave.read("inputs/sample_flute.wav")
sig_f = sig_f[:, 0]
rate, sig_v = wave.read("inputs/sample_violin.wav")
sig_v = sig_v[:, 0]

model = rave.core.SpectralDistance(
    n_fft=512, sampling_rate=44100, norm=["L1", "L2"], power=2, normalized=True
)
print(
    f"{float(model.forward(torch.tensor(sig_v/max(abs(sig_v))), torch.tensor(sig_f/max(abs(sig_f))))):.4f}"
)
print("v f v f")
for i in range(11):
    rate, sig = wave.read(f"generations/violute/output_v{i}_f{10-i}.wav")
    diff = sig.shape[0] - sig_f.shape[0]
    sig = sig[diff // 2 : -diff // 2]
    dv = model.forward(
        torch.tensor(sig / max(abs(sig)), dtype=torch.float32),
        torch.tensor(sig_v / max(abs(sig_v)), dtype=torch.float32),
    )
    df = model.forward(
        torch.tensor(sig / max(abs(sig)), dtype=torch.float32),
        torch.tensor(sig_f / max(abs(sig_f)), dtype=torch.float32),
    )
    print(i, 10 - i, f"{dv:.4f} {df:.4f}")
