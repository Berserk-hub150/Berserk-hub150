#!/usr/bin/env python3
"""Readable sequential comic-book GitHub banner. 4 cinematic chapters, 10fps."""
from pathlib import Path
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Image.open(ROOT/"assets/asse.png").convert("RGB")
W,H=1100,380
OUT=ROOT/"assets/berserk-comic-banner.gif"
TMP=ROOT/".profile-comic-v3-frames"
TMP.mkdir(exist_ok=True)
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
GOLD=(255,203,38);WHITE=(246,246,240);MUTED=(164,167,172)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
F0=ImageFont.truetype(FONT,12)
F1=ImageFont.truetype(FONT,15)
F2=ImageFont.truetype(FONT,18)
F4=ImageFont.truetype(FONT,47)
F5=ImageFont.truetype(FONT,34)
M=ImageFont.truetype(MONO,13)
CH=[
 ("BUILD","IT STARTS WITH ONE IDEA."),
 ("LAUNCH","MAKE IT OPEN SOURCE."),
 ("DISCOVER","GOOD IDEAS GET DISCOVERED."),
 ("IMPACT","WE BUILD SOMETHING BIGGER.")
]
BOXES=[(.00,.04,.39,.88),(.22,.05,.70,.82),(.35,.24,.84,.94),(.66,.03,1.00,.92)]
ART=[]
for x0,y0,x1,y1 in BOXES:
    cut=SOURCE.crop((int(x0*SOURCE.width),int(y0*SOURCE.height),int(x1*SOURCE.width),int(y1*SOURCE.height)))
    cut=ImageOps.fit(cut,(674,231),Image.Resampling.LANCZOS)
    cut=ImageEnhance.Contrast(cut).enhance(1.16)
    ART.append(ImageEnhance.Color(cut).enhance(1.03))

def text3d(d,xy,value,font,fill=WHITE,depth=5):
    x,y=xy
    for z in range(depth,0,-1):
        d.text((x+z,y+z),value,font=font,fill=(75,42,5) if fill==GOLD else (15,18,26),
               stroke_width=1,stroke_fill=(4,4,5))
    d.text((x,y),value,font=font,fill=fill,stroke_width=1,stroke_fill=(4,4,5))

FPS=10
N=96
for n in range(N):
    t=n/FPS
    idx=min(3,int(t/2.4))
    age=t-idx*2.4
    im=Image.new("RGB",(W,H),(8,10,13))
    d=ImageDraw.Draw(im)
    for x in range(0,W,40):d.line((x,0,x,H),fill=(18,18,17))
    for y in range(0,H,40):d.line((0,y,W,y),fill=(17,17,19))
    d.rectangle((0,0,W,5),fill=GOLD)
    d.rectangle((0,H-4,W,H),fill=(135,81,6))
    d.text((26,14),"★  BERSERK-HUB150",font=F2,fill=GOLD)
    d.text((245,18),"THE OPEN SOURCE CHRONICLES",font=M,fill=(209,209,204))
    for i,(name,_) in enumerate(CH):
        x=582+i*128
        active=(i==idx)
        d.rounded_rectangle((x,10,x+119,41),radius=5,fill=(81,57,6) if active else (22,23,24),
                            outline=GOLD if active else (72,66,43),width=2 if active else 1)
        d.text((x+12,17),f"{i+1:02} {name}",font=F0,fill=GOLD if active else (160,155,138))
    d.rounded_rectangle((17,52,702,303),radius=8,fill=(18,18,20),outline=(219,157,22),width=3)
    push=max(0,min(1,age/2.4))
    shifted=ART[idx].resize((686,235),Image.Resampling.BILINEAR)
    pan=int(push*10)
    im.paste(shifted.crop((pan,1,pan+674,232)),(23,58))
    d=ImageDraw.Draw(im,"RGBA")
    d.rectangle((23,58,697,292),outline=(255,226,98,175),width=1)
    for k in range(110):
        d.line((24,184+k,697,184+k),fill=(0,0,0,int(4+2.22*k)),width=1)
    d.rounded_rectangle((38,72,171,109),radius=6,fill=(0,0,0,225),outline=(*GOLD,255),width=2)
    d.text((51,80),f"CH. {idx+1:02} / 04",font=F1,fill=GOLD)
    text3d(d,(39,191),CH[idx][0],F4,GOLD)
    d.text((43,253),CH[idx][1],font=F2,fill=WHITE,stroke_width=1,stroke_fill=(0,0,0))
    d.rounded_rectangle((716,52,1081,303),radius=8,fill=(9,11,15,255),outline=(116,92,33,255),width=2)
    d.text((736,69),"THE MISSION",font=M,fill=GOLD)
    text3d(d,(733,94),"STAR THE",F5,WHITE)
    text3d(d,(733,133),"BUILD.",F5,GOLD)
    d.text((734,178),"If this project helps you,",font=F1,fill=WHITE)
    d.text((734,201),"give it a star so others",font=F1,fill=WHITE)
    d.text((734,224),"can discover it too.",font=F1,fill=WHITE)
    sweep=int(((t%4.0)/4.0)*370)
    d.polygon([(716+sweep,52),(719+sweep,52),(686+sweep,303),(680+sweep,303)],
              fill=(255,218,70,34))
    d.rounded_rectangle((731,256,1065,289),radius=5,fill=(49,38,8,255),outline=(*GOLD,240),width=1)
    d.text((749,262),"★  STAR  •  FORK  •  CONTRIBUTE",font=F1,fill=GOLD)
    d.rounded_rectangle((17,314,1081,367),radius=7,fill=(12,12,13,255),outline=(*GOLD,210),width=2)
    d.text((32,325),"★ AI SKILL NAVIGATOR",font=F2,fill=WHITE)
    d.text((341,325),"★ SKILLHAWK",font=F2,fill=WHITE)
    d.text((680,325),"OPEN CODE. REAL IMPACT.",font=F2,fill=GOLD)
    d.text((33,348),"Adaptive learning for Moodle",font=F0,fill=MUTED)
    d.text((343,348),"AI agent skills security",font=F0,fill=MUTED)
    d.text((681,348),"GIVE A STAR IF IT HELPS.",font=F0,fill=MUTED)
    d.rectangle((23,303,23+int(671*min(1,t/9.6)),306),fill=GOLD)
    if 0<=age<=.3 and idx>0:
        x=23+int(age/.3*674)
        d.rectangle((max(23,x-18),58,min(697,x+6),292),fill=(255,222,65,int(175*(1-age/.3))))
        d.line((x,58,x,291),fill=(255,245,204,200),width=3)
    im.save(TMP/f"{n:04d}.png",compress_level=2)

subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
                "-i",str(TMP/"%04d.png"),"-vf","palettegen=max_colors=192:stats_mode=diff",
                str(TMP/"palette.png")],check=True)
subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-framerate",str(FPS),
                "-i",str(TMP/"%04d.png"),"-i",str(TMP/"palette.png"),"-filter_complex",
                "[0:v][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle",
                "-gifflags","+transdiff+offsetting","-loop","0",str(OUT)],check=True)
print(f"Created {OUT}: {OUT.stat().st_size} bytes, {N} frames")
