from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)
sampling_rate = model.config.audio_encoder.sampling_rate

i=0

def gen(request,text):
    inputs = processor(
        text=["80s pop track with bassy drums and synth", "90s rock song with loud guitars and heavy drums"],
        padding=True,
        return_tensors="pt",
    )

    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)
    scipy.io.wavfile.write("mainapp/music/"+i+".wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    
    try:
        m = open("mainapp/music/"+i+".wav", 'rb')
        response = FileResponse(m)
        return response
    except:
        return JsonResponse({"res":None})
    i=i+1
    return HttpResponse(audio_values[0].cpu().numpy())
