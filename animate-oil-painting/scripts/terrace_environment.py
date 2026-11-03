import os
from PIL import Image
import numpy as np, subprocess, glob, math
im=Image.open(os.environ['OIL_PAINTING_INPUT']).convert('RGB').resize((1430,1080),Image.Resampling.LANCZOS)
src=np.asarray(im)
s=1430/640
def patch(box):
    l,t,r,b=[round(q*s) for q in box]
    y,x=np.mgrid[t:b,l:r].astype(np.float32)
    u=(x-l)/(r-l-1);v=(y-t)/(b-t-1)
    edge=np.sin(np.pi*u)**2*np.sin(np.pi*v)**2
    return l,t,r,b,x,y,u,v,edge
boxes=[
(89,26,210,111),(420,30,515,127),
(5,185,88,228),(91,188,126,263),(218,185,417,225),(425,190,625,228),(291,215,416,271),
(31,207,61,321),(148,290,181,389),(287,288,346,336),(553,231,606,313),
(294,141,378,176),(437,148,502,175),(519,149,595,179),
(111,99,393,163),(440,105,624,149),
(118,181,219,247),
(211,224,245,277),(252,219,287,276),(438,329,497,388),(272,330,355,395),
(115,305,235,362),(243,307,274,343),(347,405,473,471),(212,389,300,445)]
extra=[(8,218,41,311),(48,229,82,327),(9,322,85,390),(104,386,167,454),(249,301,300,353),(327,289,402,334),(513,248,552,327),(599,229,632,307)]
regions=[patch(b) for b in boxes+extra]
def impulse(t, start, duration):
    progress=np.clip((t-start)/duration,0,1)
    return np.sin(np.pi*progress)**4

def environment_frame(a):
    a = a % (2*np.pi)
    seconds=a*10/(2*np.pi)
    out=src.copy()
    for i,(l,t,r,b,x,y,u,v,e) in enumerate(regions):
        if 17 <= i <= 24:
            continue
        dx=0;dy=0;light=0
        if i>=25 or 7<=i<11:
            j=i-7 if i<11 else i-21
            delay=(j%6)*.21
            gust=impulse(seconds,.35+delay,3.5)
            rebound=impulse(seconds,2.8+delay,1.65)
            light_gust=impulse(seconds,5.55+delay,2.65)
            anchor=np.sin(np.pi*u)**2*np.clip(v*7,0,1)*(1-v)**1.65
            bend=gust-.28*rebound+.62*light_gust
            dx=-s*(7 if j in (0,1,4,5) else 4.7)*anchor*bend
            dy=s*anchor*(1.3*bend+(u-.5)*2.1*light_gust)
        elif i<2:
            anchor=np.clip(u*3,0,1)*np.clip((1-u)*5,0,1)*np.sin(np.pi*v)**2
            wave=np.sin(2*a-7*u+i*1.7)
            dy=s*4.6*anchor*wave
            dx=s*1.8*anchor*np.sin(2*a-8*u+i*1.7)
            light=2.4*anchor*wave
        elif i<7:
            wave=np.sin(3*a+.36*y-.035*x)+.38*np.sin(5*a+.62*y-.066*x)
            dy=s*1.35*e*wave
            dx=s*1.1*e*np.sin(2*a-.08*x+.19*y)
            light=6.5*e*wave
        elif i<16:
            phase=seconds/10
            blend=phase*phase*(3-2*phase)
            smoke=i<14
            travel=20 if smoke else (86 if i==14 else 68)
            opacity=np.clip(e*(2.0 if smoke else 2.8),0,1)[...,None]
            def drift(distance):
                xx=x-distance
                yy=y+(distance*.14 if smoke else 0)
                ix=np.clip(xx.astype(int),0,src.shape[1]-2)
                iy=np.clip(yy.astype(int),0,src.shape[0]-2)
                horizontal=(xx-ix)[...,None]
                vertical=(yy-iy)[...,None]
                upper=src[iy,ix]*(1-horizontal)+src[iy,ix+1]*horizontal
                lower=src[iy+1,ix]*(1-horizontal)+src[iy+1,ix+1]*horizontal
                return upper*(1-vertical)+lower*vertical
            moving=(1-blend)*drift(travel*phase)+blend*drift(travel*(phase-1))
            out[t:b,l:r]=np.clip(np.rint(out[t:b,l:r]*(1-opacity)+moving*opacity),0,255)
            continue
        elif i==16:
            rock=np.sin(2*a+.8)
            dx=s*2.4*e*rock
            dy=s*e*(1.2*np.sin(2*a+1.4)+2*(u-.5)*rock)
        else:
            j=(i-17)%4
            start,duration,direction=[(1.1,3.4,1),(3.05,3.6,-1),(4.25,3.2,1),(2.05,3.9,-1)][j]
            gesture=impulse(seconds,start,duration)
            if i<21:
                angle=direction*.115*gesture
                pivot_x=l+(r-l)*.5
                pivot_y=t+(b-t)*.88
                weight=np.clip(e*2.7,0,1)
                dx=-(y-pivot_y)*angle*weight
                dy=(x-pivot_x)*angle*weight
            else:
                dx=s*direction*1.9*e*gesture
                dy=s*.5*e*gesture
        xx=x+dx; yy=y+dy
        ix=xx.astype(int);iy=yy.astype(int)
        fx=(xx-ix)[...,None];fy=(yy-iy)[...,None]
        layer=out if i>=7 else src
        top=layer[iy,ix]*(1-fx)+layer[iy,ix+1]*fx
        bot=layer[iy+1,ix]*(1-fx)+layer[iy+1,ix+1]*fx
        out[t:b,l:r]=np.clip(np.rint(top*(1-fy)+bot*fy+np.asarray(light)[...,None]),0,255)
    canvas=np.empty((1080,1920,3),np.uint8)
    canvas[:]=[39,51,60]
    canvas[:,245:1675]=out
    return canvas
