from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import requests, scipy, torch, threading, json
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from . models import *

model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)
sampling_rate = model.config.audio_encoder.sampling_rate

@csrf_exempt
def gen_fun(request):
    data = json.loads(request.body)
    desc=data['desc']
    doctor=data['doctor']
    patient=data['patient']
    type=data['type']

    wav_name="mainapp/music/"+type+"/"+desc+".wav"
    inputs = processor(
        text=[desc],
        padding=True,
        return_tensors="pt",
    )
    audio_values = model.generate(**inputs.to(device), do_sample=True, guidance_scale=3, max_new_tokens=256)
    scipy.io.wavfile.write(wav_name, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    music=Music.objects.create(doctor=doctor,patient=patient,music_path=wav_name,type=type)
    music.save()

@csrf_exempt
def gen(request):
    if request.method == 'POST':
        t = threading.Thread(target=gen_fun, args=[request])
        t.setDaemon(True)
        t.start()
        return JsonResponse({"res":"sucsess"})
    else:     
        return JsonResponse({'state':'error request method'}, status=201)

@csrf_exempt
def get_music(request):
    data = json.loads(request.body)
    music_urls=data['url']
    try:
        m = open(music_urls, 'rb')
        response = FileResponse(m)
        return response
    except:
        return JsonResponse({"res":None})

@csrf_exempt
def get_my_list(request):
    data = json.loads(request.body)
    user=data['user']
    m=None
    m=Music.objects.filter(patient=user)
    if len(m)==0:
        m=Music.objects.filter(doctor=user)

    music_urls=[]
    music_names=[]
    for i in m:
        music_urls.append(str(i.music_path))
        n=i.music_path.split('/')
        music_names.append(n[-1])
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

@csrf_exempt
def get_folder_list(request):
    data = json.loads(request.body)
    folder_name=data['folder_name']
    m=Music.objects.all()
    music_urls=[]
    music_names=[]
    for i in m:
        n=i.music_path.split('/')
        if n[2]==folder_name:
            music_urls.append(str(i.music_path))
            music_names.append(n[-1])
    return JsonResponse({"music_names":music_names,"music_urls":music_urls})

@csrf_exempt
def surahList(request):
    url = "https://online-quran-api.p.rapidapi.com/surahs"
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    surahList = response.json()['surahList']
    res=[]
    for i in surahList:
        res.append(i["name"])
    return JsonResponse({"surahList":res})

@csrf_exempt
def surah_audio(request,name):
    url = "https://online-quran-api.p.rapidapi.com/surahs/"+name
    headers = {
        "X-RapidAPI-Key": "4120ca7630msh5566122415863dep16069fjsn207bd1f0e6f4",
        "X-RapidAPI-Host": "online-quran-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return JsonResponse({"audio":response.json()['audio']})