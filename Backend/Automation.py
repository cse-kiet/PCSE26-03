from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt 
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import pythoncom

pythoncom.CoInitialize()

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO SY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb48b gsrt", "sXLa0e", "LWkFKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

client = Groq(api_key=GroqAPIKey)

professional_responses = [

"Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
"I'm at your service for any additional questions or support you may need-don't hesitate to ask.",

]

messages = []

SystemChatBot = [
    {"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, essays, notes, songs, poems, emails, applications, articles ."}
]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user","content":f"{prompt}"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
                
        Answer = Answer.replace("</s>","")
        messages.append({"role":"assistant","content":Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):

    app = app.lower().strip()

    # 🔥 HANDLE COMMON WEBSITES DIRECTLY
    if "youtube" in app:
        webopen("https://www.youtube.com")
        return True

    if "google" in app:
        webopen("https://www.google.com")
        return True

    if "instagram" in app:
        webopen("https://www.instagram.com")
        return True

    if "whatsapp" in app:
        webopen("https://web.whatsapp.com")
        return True

    # 🔥 TRY OPENING LOCAL APP
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:

        # 🔥 SAFE GOOGLE FALLBACK
        def extract_links(html):
            if html is None:
                return []

            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f'https://www.google.com/search?q={query}'
            headers = {'User-Agent': useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            return None

        try:
            html = search_google(app)

            if html:
                links = extract_links(html)

                if links:
                    webopen(links[0])
                else:
                    print("No links found → opening Google search")
                    webopen(f"https://www.google.com/search?q={app}")
            else:
                webopen(f"https://www.google.com/search?q={app}")

        except Exception as e:
            print("Fallback error:", e)
            webopen(f"https://www.google.com/search?q={app}")

        return True
    
def CloseApp(app):

    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False
  # add this import at the top

def System(command):
    command = command.lower().strip()

    def get_volume_interface():
        pythoncom.CoInitialize()
        devices = AudioUtilities.GetSpeakers()
    # Access the underlying COM object
        interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return interface.QueryInterface(IAudioEndpointVolume)

    def mute():
        pythoncom.CoInitialize()
        try:
            get_volume_interface().SetMute(1, None)
        finally:
            pythoncom.CoUninitialize()

    def unmute():
        pythoncom.CoInitialize()
        try:
            get_volume_interface().SetMute(0, None)
        finally:
            pythoncom.CoUninitialize()

    def change_volume(amount):
        pythoncom.CoInitialize()
        try:
            volume = get_volume_interface()
            current = volume.GetMasterVolumeLevelScalar()
            new_level = max(0.0, min(1.0, current + amount))
            volume.SetMasterVolumeLevelScalar(new_level, None)
        finally:
            pythoncom.CoUninitialize()

    def change_brightness(amount):
        current = sbc.get_brightness(display=0)[0]
        new_level = max(0, min(100, current + amount))
        sbc.set_brightness(new_level, display=0)

    print("[DEBUG] Received system command:", command)

    if "mute" in command:
        mute()
    elif "unmute" in command:
        unmute()
    elif "volume" in command:
        if any(x in command for x in ["up", "increase", "raise"]):
            change_volume(0.1)
        elif any(x in command for x in ["down", "decrease", "lower"]):  # ✅ Bug 1 fixed
            change_volume(-0.1)
    elif "brightness" in command:
        if any(x in command for x in ["up", "increase", "raise"]):
            change_brightness(10)
        elif any(x in command for x in ["down", "decrease", "lower"]):  # ✅ Bug 1 fixed
            change_brightness(-10)
    else:
        print(f"No system command matched: {command}")

    return True

async def TranslateAndExecute(commands: list[str]):

    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        else:
            print(f"No function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):
        pass

    return True
    

    
