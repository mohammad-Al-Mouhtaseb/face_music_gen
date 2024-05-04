from django.shortcuts import render

# # Create your views here.
# !python3 -m pip install -U git+https://github.com/facebookresearch/audiocraft#egg=audiocraft

from audiocraft.models import musicgen
from audiocraft.utils.notebook import display_audio
import torch


model = musicgen.MusicGen.get_pretrained('medium', device='cuda')
model.set_generation_params(duration=20)

def gen(request):
    res = model.generate([
        'syrian traditional music'
    ], 
        progress=True)
