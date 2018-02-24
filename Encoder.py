import os
from pathlib import Path
import threading
import queue
import subprocess
from pprint import pprint

EncoderQueue = queue.Queue()

#ffmpeg's filter input needs to be escaped 3 times (!!!) 
#in order to work with all the special characters
#that will undoubtably be present in this weebiest
#of servers.
def ffmpeg_escape(path):
    path = path.replace('[', '\\[')
    path = path.replace(']', '\\]')
    path = path.replace('\\', '\\\\')
    return path

def ffmpeg_outfile_escape(path):
    path = path.replace('&', '\\&')
    return path


def run():
    while True:
        item = EncoderQueue.get()
        if item is None:
            break
        
        item = os.path.split(item)

        subdir = os.path.join(*item[:-1])

        pprint(f'Subdir:{subdir}')

        item = item[-1]
        
        #Strip file extension
        name = os.path.splitext(item)[0]

        outdir = f'video/{subdir}/{name}'

        #The actual output location.
        #Not passed to the encoder, since we change working directory

        #The path for the empty file indicating 
        # that encoding has completed for the given file
        complete = f'{outdir}/.{name}.complete'

        #Check if outdir exists, which might be fine...
        if(os.path.isdir(outdir)):
            #But if the .complete file exists, we can skip this one.
            if(os.path.isfile(complete)):
                print(f'Skipping {name}')
                EncoderQueue.task_done()
                continue
        else: 
            os.mkdir(outdir)

        print(f'Item:{item}')
        print(f'Name:{name}')
        #name = ffmpeg_outfile_escape(name)
        print(f'Name:{name}')
        sub = ffmpeg_escape(item)

        #subprocess.check_call(['../dash-convert', item, name], cwd='video')
        try:
            out = subprocess.check_output(f'ffmpeg -i "{subdir}/{item}" \
                                 -vf subtitles="{subdir}/{sub}" \
                                 -vcodec libx264       \
                                    -preset slower     \
                                    -tune animation    \
                                 -f dash "{subdir}/{name}/{name}".mpd', 
                                    cwd='video',
                                    encoding='utf-8',
                                    shell=True
                                    )
        except subprocess.CalledProcessError as e:

            #I'm ugly and I'm proud!
            print("Re-running without subtitles")

            try:
                out = subprocess.check_output(f'ffmpeg -i "{subdir}/{item}" \
                                     -vcodec libx264       \
                                        -preset slower     \
                                        -tune animation    \
                                     -f dash "{subdir}/{name}/{name}".mpd', 
                                        cwd='video',
                                        encoding='utf-8',
                                        shell=True
                                        )
            except:
                return

        print(out)
        Path(complete).touch()


threading.Thread(target=run).start()
