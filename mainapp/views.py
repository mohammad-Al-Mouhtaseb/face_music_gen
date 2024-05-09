from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

# import warnings
# warnings.simplefilter(action='ignore', category=FutureWarning)

# from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small", force_download=True)
# processor = AutoProcessor.from_pretrained("facebook/musicgen-small", force_download=True)

# import torch
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# model.to(device)
# sampling_rate = model.config.audio_encoder.sampling_rate


from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch
device = "cuda" if torch.cuda.is_available() else "cpu"
model = musicgen.MusicGen.get_pretrained('medium', device=device)
model.set_generation_params(duration=8)

def gen(request,text):
    # inputs = processor(
    #     text=["80s pop track with bassy drums and synth", "90s rock song with loud guitars and heavy drums"],
    #     padding=True,
    #     return_tensors="pt",
    # )
    res = model.generate([
        'crazy EDM, heavy bang'
    ], 
        progress=True)
    display_audio(res, 32000)
    # audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)
    scipy.io.wavfile.write("mainapp/music/m1.wav", data=res)
    return JsonResponse({"res":"sucsess"})

def get(request,text):
    try:
        m = open("mainapp/music/m1.wav", 'rb')
        response = FileResponse(m)
        return response
    except:
        return JsonResponse({"res":None})