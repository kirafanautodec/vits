import torch

import commons
import numpy
import time
import utils
from io import BytesIO
import lameenc
import base64
import soundfile

from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from schema import TTSRequest, TTSResponse, TTSConfig, TTSResponseData, MarkedSentence, ErrorCode


class TTSService:
    def __init__(self):
        self.hps = utils.get_hparams_from_file('configs/ljs_base.json')
        self.sampling_rate = self.hps.data.sampling_rate
        self.hop_length = self.hps.data.hop_length

        self.net_g = SynthesizerTrn(
            len(symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model).cuda()
        _ = self.net_g.eval()
        _ = utils.load_checkpoint(
            'ckpt/pretrained_ljs.pth', self.net_g, None)

    def get_text(self, text, slow_punctuation_duration):
        text_norm, marked_sentences, attn_punctuations = text_to_sequence(
            text, slow_punctuation_duration)
        if self.hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
            marked_sentences = [(text, (2 * s, 2 * e, p))
                                for text, (s, e, p) in marked_sentences]
            attn_punctuations = commons.intersperse(attn_punctuations, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm, marked_sentences, attn_punctuations

    def syn(self, request: TTSRequest) -> TTSResponse:
        if request is None or request.text is None or len(request.text) == 0:
            return TTSResponse(code=ErrorCode.EmptyText, msg='', data=None)

        text = request.text
        config: TTSConfig = TTSConfig()
        if request.config is not None:
            config = request.config

        stn_tst, marked_sentences, attn_punctuations = self.get_text(
            text, config.slow_punctuation)
        with torch.no_grad():
            x_tst = stn_tst.cuda().unsqueeze(0)
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
            attn_punctuations_tst = torch.LongTensor(
                attn_punctuations).cuda().unsqueeze(0).unsqueeze(0)
            audio_tst, durations_tst = self.net_g.infer(
                x_tst, x_tst_lengths, noise_scale=config.noise_scale, noise_scale_w=config.noise_scale_w, length_scale=config.length_scale, attn_punctuations=attn_punctuations_tst)
            duration_of_tokens = durations_tst[0, 0].data.cpu(
            ).float().numpy() * (1.0 * self.hop_length / self.sampling_rate)
            duration_of_tokens = numpy.insert(duration_of_tokens, 0, 0)
            starttime_of_tokens = numpy.cumsum(duration_of_tokens)
            marked_sentences = [MarkedSentence(content=content, start_time=starttime_of_tokens[s],
                                               end_time=starttime_of_tokens[e], is_punctuation=p) for content, (s, e, p) in marked_sentences]

            audio = audio_tst[0, 0].data.cpu().float().numpy()
            wav_file = BytesIO()
            soundfile.write(wav_file, audio, self.sampling_rate, format='wav')
            encoder = lameenc.Encoder()
            encoder.set_bit_rate(64)
            encoder.set_in_sample_rate(self.sampling_rate)
            encoder.set_channels(1)
            encoder.set_quality(2)
            mp3_data = encoder.encode(wav_file.getvalue())
            mp3_data += encoder.flush()
            wav_file.close()
            audiob64 = base64.b64encode(mp3_data).decode('ascii')
        return TTSResponse(
            code=ErrorCode.OK, msg='',
            data=TTSResponseData(
                marked_sentences=marked_sentences, voice=audiob64)
        )
