import cv2
import numpy as np
import subprocess
import glob
from PIL import Image
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser(description='Render the calibrated Sainte-Adresse reference only.')
parser.add_argument('--input', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--ffmpeg', type=Path)
args = parser.parse_args()
if not args.input.is_file():
    parser.error('Input image does not exist.')
args.output.parent.mkdir(parents=True, exist_ok=True)
os.environ['OIL_PAINTING_INPUT'] = str(args.input.resolve())
from terrace_environment import environment_frame, src, s

# Polygon coordinates follow the painted silhouettes in the 640-pixel reference.
parts = [
    dict(name='woman_upper', points=[(224,238),(228,236),(232,237),(234,241),(233,246),(230,250),(234,253),(237,257),(239,258),(238,262),(236,262),(237,271),(239,275),(234,278),(224,279),(218,277),(219,272),(218,267),(220,256),(223,252),(223,247)], pivot=(228,278), angle=-4.8, timing=(1.2,2.7,4.3,6.0)),
    dict(name='man_upper', points=[(263,229),(267,225),(272,225),(274,230),(277,234),(274,236),(275,242),(281,245),(285,251),(287,260),(287,268),(285,278),(281,281),(279,277),(281,266),(278,272),(278,281),(263,282),(263,270),(261,262),(258,272),(257,280),(253,282),(252,278),(254,267),(257,255),(262,247),(267,243),(266,237),(263,236)], pivot=(270,282), angle=3.8, timing=(3.3,4.4,5.1,7.0)),
    dict(name='seated_upper', points=[(448,340),(456,337),(465,333),(472,334),(478,339),(480,347),(478,355),(474,359),(478,364),(481,371),(480,382),(476,388),(467,391),(453,391),(443,398),(429,402),(419,399),(416,395),(419,391),(425,389),(431,383),(438,375),(443,369),(454,364),(459,362),(455,360),(456,354),(453,349)], pivot=(431,399), angle=-4.8, timing=(3.7,5.7,6.5,9.0)),
    dict(name='parasol', points=[(279,354),(286,347),(288,341),(306,338),(319,334),(331,337),(342,346),(347,357),(348,371),(336,391),(329,390),(317,391),(308,389),(300,385),(290,381),(286,378),(289,369)], pivot=(318,395), angle=2.7, timing=(5.7,6.5,7.0,8.7)),
]

layers=[]
for part in parts:
    points=np.rint(np.array(part['points'])*s).astype(np.int32)
    left,top=points.min(axis=0)-24
    right,bottom=points.max(axis=0)+25
    patch=src[top:bottom,left:right].copy()
    mask=np.zeros(patch.shape[:2],np.uint8)
    cv2.fillPoly(mask,[points-[left,top]],255)
    alpha=cv2.GaussianBlur(mask.astype(np.float32)/255,(3,3),.55)
    background=cv2.inpaint(patch,cv2.dilate(mask,np.ones((3,3),np.uint8)),4,cv2.INPAINT_TELEA)
    layers.append((part,left,top,patch,alpha,background))

def smooth(value):
    value=np.clip(value,0,1)
    return value*value*(3-2*value)

def pose(seconds,timing):
    start,arrive,leave,end=timing
    return smooth((seconds-start)/(arrive-start))*(1-smooth((seconds-leave)/(end-leave)))

def frame(seconds):
    canvas=environment_frame(2*np.pi*(seconds%10)/10)
    for part,left,top,patch,alpha,background in layers:
        amount=pose(seconds%10,part['timing'])
        if amount<.00001:
            continue
        pivot=np.array(part['pivot'])*s-[left,top]
        matrix=cv2.getRotationMatrix2D(tuple(pivot),part['angle']*amount,1)
        height,width=alpha.shape
        moved_alpha=cv2.warpAffine(alpha,matrix,(width,height),flags=cv2.INTER_LINEAR)
        premult=patch.astype(np.float32)*alpha[...,None]
        moved=cv2.warpAffine(premult,matrix,(width,height),flags=cv2.INTER_LINEAR)
        target=canvas[top:top+height,left+245:left+245+width].astype(np.float32)
        # Reveal the restored background only where the original silhouette vacates.
        restored=target*(1-alpha[...,None])+background*alpha[...,None]
        composite=restored*(1-moved_alpha[...,None])+moved
        canvas[top:top+height,left+245:left+245+width]=np.clip(np.rint(composite),0,255)
    return canvas[:,245:1675].copy()

if args.ffmpeg:
    encoder = str(args.ffmpeg.resolve())
else:
    import imageio_ffmpeg
    encoder = imageio_ffmpeg.get_ffmpeg_exe()
temporary = args.output.with_name(args.output.stem + '.partial.mp4')
command = [encoder, '-v', 'error', '-y', '-f', 'rawvideo',
           '-pixel_format', 'rgb24', '-video_size', '1430x1080',
           '-framerate', '30', '-i', '-', '-an', '-c:v', 'libx264',
           '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
           str(temporary)]
process = subprocess.Popen(command, stdin=subprocess.PIPE)
try:
    for index in range(300):
        process.stdin.write(frame(index / 30).tobytes())
finally:
    process.stdin.close()
return_code = process.wait()
if return_code:
    raise RuntimeError(f'Video encoding failed with code {return_code}')
assert np.array_equal(frame(0), frame(10))
subprocess.run([encoder, '-v', 'error', '-i', str(temporary), '-f', 'null', '-'],
               check=True)
temporary.replace(args.output)
print(args.output.resolve())
