#!/usr/bin/env python3
"""Build the GitHub profile's lightweight, sequential comic GIF."""
from pathlib import Path
import subprocess
import imageio_ffmpeg
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
SRC=Image.open(ROOT/"assets/asse.png").convert("RGB")
W,H=1100,382
BG=ImageEnhance.Brightness(ImageOps.fit(SRC,(W,H),Image.Resampling.LANCZOS)).enhance(.28).filter(ImageFilter.GaussianBlur(2))
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BIG=ImageFont.truetype(FONT,35)
MED=ImageFont.truetype(FONT,14)
SM=ImageFont.truetype(MONO,11)
GOLD=(255,202,34)
CHAPTERS=[
 ("01  BUILD","EVERY IDEA STARTS SMALL","Late nights. Big ideas."),
 ("02  LAUNCH","LET THE CODE GO PUBLIC","Open source changes everything."),
 ("03  DISCOVER","GET DISCOVERED BY OTHERS","Stars help others find it."),
 ("04  IMPACT","TOGETHER WE BUILD MORE","Your support fuels what is next."),
]
panels=[]
for pos in [.11,.38,.61,.88]:
 cw=int(SRC.width*.26)
 left=max(0,min(SRC.width-cw,int(pos*(SRC.width-1))-cw//2))
 pic=ImageOps.fit(SRC.crop((left,0,left+cw,SRC.height)),(252,203),Image.Resampling.LANCZOS)
 panels.append(ImageEnhance.Brightness(ImageEnhance.Color(pic).enhance(.73)).enhance(.75))
OUT=ROOT/"assets/berserk-comic-banner.gif"
tmp=ROOT/".comic-gif-frames"
tmp.mkdir(exist_ok=True)
STARTS=[.50,2.28,4.06,5.84]
for frame in range(96):
 t=frame/10
 im=BG.copy()
 d=ImageDraw.Draw(im,"RGBA")
 for y in range(0,H,19): d.line((0,y,W,y),fill=(255,199,24,11))
 d.rounded_rectangle((13,12,W-13,H-12),radius=13,outline=(255,193,28,100),width=2)
 d.text((26,19),"BERSERK-HUB150 / THE OPEN SOURCE CHRONICLES",font=SM,fill=GOLD)
 d.text((865,19),"BUILD  >  SHARE  >  IMPACT",font=SM,fill=(231,233,237))
 active=-1
 for i,chapter in enumerate(CHAPTERS):
  x=20+i*270
  y=47
  u=max(0,min(1,(t-STARTS[i])/1.05))
  eased=1-(1-u)**3
  if u>0: active=i
  d.rounded_rectangle((x,y,x+254,y+208),radius=7,fill=(5,8,12,235),outline=(105,98,60,210),width=2)
  if eased>.01:
   cut=int(251*eased)
   im.paste(panels[i].crop((0,0,cut,203)),(x+2,y+2))
   d.rectangle((x+2,y+2,x+cut+2,y+39),fill=(0,0,0,208))
   d.rectangle((x+2,y+152,x+cut+2,y+203),fill=(0,0,0,242))
   if eased<1: d.line((x+2+cut,y+2,x+2+cut,y+204),fill=(255,230,105,230),width=3)
  else:
   d.text((x+100,y+88),"...",font=MED,fill=(94,85,47))
  if u>.2:
   d.text((x+11,y+12),chapter[0],font=MED,fill=GOLD,stroke_width=1,stroke_fill=(0,0,0))
   d.text((x+10,y+163),chapter[1],font=SM,fill=(231,233,237))
   d.text((x+10,y+182),chapter[2],font=SM,fill=GOLD)
  d.rounded_rectangle((x,y,x+254,y+208),radius=7,outline=(*GOLD,235) if i==active else (255,201,44,90),width=3 if i==active else 1)
 d.rounded_rectangle((20,264,W-20,365),radius=11,fill=(1,4,9,245),outline=(255,187,20,166),width=2)
 d.text((38,273),"STAR THE STORY.",font=BIG,fill=(240,242,246))
 d.text((383,273),"FORK THE FUTURE.",font=BIG,fill=GOLD)
 d.text((40,324),"AI SKILL NAVIGATOR   |   SKILLHAWK",font=MED,fill=(240,242,246))
 d.text((40,345),"Real open-source code. If it helps, give it a star so more developers find it.",font=SM,fill=(161,169,176))
 bar=int(max(0,min(1,(t-.4)/7.7))*(W-46))
 if bar>0:d.rectangle((23,369,23+bar,372),fill=GOLD)
 im.save(tmp/f"{frame:04d}.png")
subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-framerate","10","-i",str(tmp/"%04d.png"),"-vf","palettegen=max_colors=128:stats_mode=diff",str(tmp/"palette.png")],check=True)
subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y","-framerate","10","-i",str(tmp/"%04d.png"),"-i",str(tmp/"palette.png"),"-filter_complex","[0:v][1:v]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle","-gifflags","+transdiff+offsetting","-loop","0",str(OUT)],check=True)
print(f"Created {OUT}: {OUT.stat().st_size} bytes")
