import matplotlib.pyplot as plt

import os
import json
import math
import torch
import numpy
import soundfile
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader

import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence

from scipy.io.wavfile import write


def get_text(text, hps):
    text_norm, marked_sentences = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
        marked_sentences = [(text, (2 * s, 2 * e, p)) for text, (s, e, p) in marked_sentences]
    text_norm = torch.LongTensor(text_norm)
    return text_norm, marked_sentences

hps = utils.get_hparams_from_file("./configs/ljs_base.json")
sampling_rate = hps.data.sampling_rate
hop_length = hps.data.hop_length

net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model).cuda()
_ = net_g.eval()
_ = utils.load_checkpoint("ckpt/pretrained_ljs.pth", net_g, None)

stn_tst, marked_sentences = get_text("Folic acid is crucial for proper brain function and plays an important role in mental and emotional health. \nIt aids in the production of DNA and RNA, the body's genetic material, and is especially important when cells and tissues are growing rapidly, such as in infancy, adolescence, and pregnancy.", hps)
with torch.no_grad():
    x_tst = stn_tst.cuda().unsqueeze(0)
    x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
    audio_tst, durations_tst, _1, _2, _3 = net_g.infer(x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1)
    audio = audio_tst[0,0].data.cpu().float().numpy()
    duration_of_tokens = durations_tst[0,0].data.cpu().float().numpy() * (1.0 * hop_length / sampling_rate)
    duration_of_tokens = numpy.insert(duration_of_tokens, 0, 0)
    starttime_of_tokens = numpy.cumsum(duration_of_tokens)
    marked_sentences_times = [(text, (starttime_of_tokens[s], starttime_of_tokens[e], p)) for text, (s, e, p) in marked_sentences]

print(marked_sentences_times) 

soundfile.write("./tmp/sample.wav", audio, sampling_rate, format="wav")