from dataclasses import dataclass
from classes import AudioResponse
from kokoro import KPipeline
import sounddevice as sd
from rich.console import Console
from rich.text import Text
from rich.live import Live
import threading
import time

console = Console()
pipeline = KPipeline(lang_code='a')
responses = [] # Updated when generating audio
done = False

def generate_audio_thread(text, voice='af_heart'):
    global done
    generator = pipeline(text, voice=voice)
    for i, (gs, ps, audio) in enumerate(generator):
        responses.append(AudioResponse(i=i, gs=gs, ps=ps, audio=audio))
    done = True

def play_audio_for(text, voice='af_heart'):
    threading.Thread(target=generate_audio_thread, args=(text, voice), daemon=True).start()
    
    while not responses:
        time.sleep(0.1)
        
    while not done:
        if not responses:
            time.sleep(0.1)
            continue
        
        response = responses.pop(0)
        i = response.i
        gs = response.gs
        ps = response.ps
        audio = response.audio
        
        sd.play(audio, 24000)
        
        audio_length = len(audio) / 24000
        char_count = len(gs)
        
        if char_count > 0:
            char_delay = (audio_length - 2) / char_count
            
            with Live("", auto_refresh=False, console=console) as live:
                for idx in range(len(gs) + 1):
                    start_time = time.time()
                    styled_text = Text()
                    styled_text.append(gs[:idx])
                    if idx < len(gs):
                        styled_text.append(gs[idx:], style="dim")
                    
                    live.update(styled_text, refresh=True)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    if char_delay - elapsed_time > 0:
                        time.sleep(char_delay - elapsed_time)
        
        print("\n")
        sd.wait()