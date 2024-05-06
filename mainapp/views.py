from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
import requests

from transformers import AutoProcessor, MusicgenForConditionalGeneration, pipeline
# import scipy

# synthesiser=pipeline("text-to-audio","facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
# import torch
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# device="cpu"
# model.to(device)
# sampling_rate = model.config.audio_encoder.sampling_rate

def gen(request):
    pass
