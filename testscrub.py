import os
import urllib
import urllib.request
import re
import requests


import moviepy.editor as mp
import numpy as np
import pandas as panda


from bs4 import BeautifulSoup



url = "http://mms.tveyes.com/PlaybackPortal.aspx?SavedEditID=4c5ca4b5-7713-4497-aee8-beecd45784d4"
geckopath= 'C:\\Users\Stefan\Documents\geckodriver\geckodriver.exe'
searchLine = "Playerlette.aspx"
base_url="http://mms.tveyes.com/"
mp4_base_url = "jmkin.cdn."
download_path = r"C:\Users\Stefan\Desktop\TS Audio\audio_"
mp4_dowloadUrl = [] 
mp4_path = ""


def readExcelLinks():

    file_loc = r"C:\Users\Stefan\Downloads\Broadcast Links.xlsx"
    data_frame = panda.read_excel(file_loc, index_col= None,na_values=['NA'], usecols = "D")

    list_of_weblinks = data_frame['Audio/Video link'].tolist()
    print(list_of_weblinks)

    return list_of_weblinks

def readExcel_createFileNames():

    list_of_folderNames = []
    
    file_loc = r"C:\Users\Stefan\Downloads\Broadcast Links.xlsx"
    data_frame = panda.read_excel(file_loc, index_col= None,na_values=['NA'], usecols = "A:C")

    data_frame['Folder Name']  = data_frame['Date'].astype(str) + '-' + data_frame['Time'].astype(str) + '-' + data_frame['Station']
    list_of_folderTemp = data_frame['Folder Name'].tolist()
    

    for name in list_of_folderTemp:
        new_name = name.replace(":","_")
        list_of_folderNames.append(new_name) 
    print(list_of_folderNames)
    return list_of_folderNames
    
def createDir(file):
    root_path = 'C:Users\Stefan\Documents\MediaEyesData\data'
    path = os.path.join(root_path, file)
    os.makedirs(path)
    return path

def getTranscript(): #extract text data from webpage and writes in to a text file
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    soupTempfile = open(r"soupTemp.txt", "w+")
    soupTempfile.writelines(soup.prettify())
    soupTempfile.close()
    for script in soup(["script", "style"]):

        script.extract()

    strips = list(soup.stripped_strings)

    
    transcript_path = download_path + "Transcript.txt"
    with open(transcript_path, "w+") as file:
     for item in strips:
         file.write("%s\n" % item)

def geDataUrl(): #fetched the data url from the player on the webpage to acces to source of the audio/video
    search = open("soupTemp.txt", "r")
    for line in search.readlines():

        if searchLine in line:
            url_end = re.findall(r'"([^"]*)"',line)
            print(url_end)
            break

    search.close()
    data_url=base_url + str(url_end)[1:-1].replace("'","")



    html1 = urllib.request.urlopen(data_url).read()
    soup1 = BeautifulSoup(html1, "html.parser")
    soupTempfile = open(r"soupTemp.txt", "w+")
    soupTempfile.writelines(soup1.prettify())
    soupTempfile.close()

def getMp4Url(): #fetches url from playlist
    search = open("soupTemp.txt", "r")
    for line in search.readlines():

        if mp4_base_url in line:
            mp4_url = re.findall(r"'([^']+)'", line)
            break
    

    search.close()
    return mp4_url

    
def download_video(video_links): #fetch video from links found on page

    for link in video_links: 

        '''iterate through all links in video_links 
        and download them one by one'''

        # obtain filename by splitting url and getting  
        # last string
        file_name = link.split('/')[-1]
        #remove .mp4 string to get file name (because of string after.mp4 causing error)
        sep = '.mp4'
        file_name_stripped = file_name.split(sep, 1)[0]  

        print("Downloading file:%s"%file_name)

        # create response object 
        r = requests.get(link, stream = True) 

        # download started
        mp4_path = download_path + file_name_stripped + ".mp4" #added .mp4 to get back file type
        with open(mp4_path, 'wb') as f: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    f.write(chunk) 

        print("%s Downloaded!\n"%file_name)

        '''Conversion of video link to audio file in wave format'''
        
        print("%s Converting\n"%file_name)
        videoclip = mp.VideoFileClip(os.path.join(mp4_path))
        wav_path = download_path + file_name_stripped + ".wav" #added .wav to get file type
        videoclip.audio.write_audiofile(os.path.join(wav_path),codec = 'pcm_s16le', verbose = False, logger = None)
        print("%s Converted\n"%file_name)

    print("All videos downloaded and converted!")
    return


''' ----This is the main code area where all code is run (like main in C)----'''
readExcelLinks()
file_names = readExcel_createFileNames()
for name in file_names:
    createDir(name)
    
##getTranscript()
##geDataUrl()
##mp4_dowloadUrl = getMp4Url()
##download_video(mp4_dowloadUrl)


