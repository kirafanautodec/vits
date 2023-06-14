import torch

import commons
import numpy
import time
import utils
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

    def run(self, request: TTSRequest) -> TTSResponse:
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
            audio = audio_tst[0, 0].data.cpu().float().numpy()
            duration_of_tokens = durations_tst[0, 0].data.cpu(
            ).float().numpy() * (1.0 * self.hop_length / self.sampling_rate)
            duration_of_tokens = numpy.insert(duration_of_tokens, 0, 0)
            starttime_of_tokens = numpy.cumsum(duration_of_tokens)
            marked_sentences = [MarkedSentence(content=content, start_time=starttime_of_tokens[s], end_time=starttime_of_tokens[e], is_punctuation=p) for content, (s, e, p) in marked_sentences]

        return TTSResponse(code=ErrorCode.OK, msg='', data=TTSResponseData(marked_sentences=marked_sentences, voice=bytes()))


# text = """What are dietary supplements?
# Dietary supplements (also called food supplements or nutritional supplements) are products designed to give you nutrients that might be missing from your diet. They are usually taken as tablets, capsules or powders, or as a liquid.

# Some common examples of supplements include vitamins and minerals (such as vitamin C, iron and calcium), oil supplements (such as fish oil capsules) and herbal supplements.

# Dietary supplements are very popular with Australians. But while supplements have some benefits, most people do not need them. If you are thinking about taking supplements, talk to your doctor first – some can cause more harm than good.

# Why use supplements?
# If your diet lacks a particular nutrient, you might need a supplement to fill that gap.

# Often, you will only need to take a supplement temporarily. For example, if you are pregnant, you might need to take supplements until your baby is born, or until you finish breastfeeding.

# In some other cases, you might need to take a supplement for a longer period, including if you have a chronic health condition.

# Who needs supplements?
# Studies show that many people who take supplements are actually getting enough nutrients from their diet already. In fact, most people who take supplements do not need them. There are, however, some people who find it hard to get the nutrients they need through diet alone.

# You might need to take a supplement if:

# you are pregnant or breastfeeding
# you are elderly, and aren't getting enough nutrition from the food you eat (malnutrition)
# you have a health condition that means your body cannot absorb the nutrients it needs (for example, if you have chronic kidney disease and are on dialysis)
# you have a strong need for a particular nutrient (for example, if you are at risk of osteoporosis and need more calcium)
# you have a restricted diet (for example, if you don't eat meat and aren't getting enough iron)
# you have a nutritional deficiency (for example, a blood test shows you have a vitamin D deficiency)
# What are the risks of using supplements?
# While the body requires a certain amount of each nutrient, higher amounts are not necessarily better. In fact, getting more than you need can sometimes cause harm.

# For example, large doses of vitamin B6 can damage the nervous system, and taking vitamin A, C, or E supplements while you are pregnant can cause serious harm to your baby. Some supplements can also interact with other medicines you are taking.

# The best way to make sure any supplements you plan to take are safe is to check with your pharmacist or doctor.

# What is the alternative to supplements?
# The best way to get all the nutrients you need is to eat a balanced diet. You can get advice about the right amount and kinds of foods to eat from the Australian Dietary Guidelines.

# If you are worried that you are not getting all the nutrients you need, talk to your doctor or consult a dietitian.
# """
# stn_tst, marked_sentences, attn_punctuations = get_text(text, 5.0)
# with torch.no_grad():
#     x_tst = stn_tst.cuda().unsqueeze(0)
#     x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
#     attn_punctuations_tst = torch.LongTensor(
#         attn_punctuations).cuda().unsqueeze(0).unsqueeze(0)
#     audio_tst, durations_tst, _1, _2, _3 = net_g.infer(
#         x_tst, x_tst_lengths, noise_scale=.667, noise_scale_w=0.8, length_scale=1, attn_punctuations=attn_punctuations_tst)
#     audio = audio_tst[0, 0].data.cpu().float().numpy()
#     duration_of_tokens = durations_tst[0, 0].data.cpu(
#     ).float().numpy() * (1.0 * hop_length / sampling_rate)
#     duration_of_tokens = numpy.insert(duration_of_tokens, 0, 0)
#     starttime_of_tokens = numpy.cumsum(duration_of_tokens)
#     marked_sentences_times = [(text, (starttime_of_tokens[s], starttime_of_tokens[e], p))
#                               for text, (s, e, p) in marked_sentences]

# print(marked_sentences_times)

# soundfile.write("./tmp/sample.wav", audio, sampling_rate, format="wav")
