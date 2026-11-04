# count bright slivers along 8 rays from the tap centre (dark theme), median over rays: frames given as args
import sys, numpy as np
from PIL import Image
run=sys.argv[1]; CX,CY=700,290
for f in map(int,sys.argv[2:]):
    a=np.asarray(Image.open(f"qa/demo-r9/frames/{run}/f{f:04d}.png").convert("L"),float)
    bg=np.median(a); n=[];pk=[]
    for th in np.linspace(0.15*np.pi,0.85*np.pi,5):  # downward rays (y down), clear water to r≈400
        r=np.arange(20,int(__import__('os').environ.get('RMAX',226))); v=a[(CY+r*np.sin(th)).astype(int),(CX+r*np.cos(th)).astype(int)]-bg
        p=[i for i in range(1,len(v)-1) if v[i]>12 and v[i]>=v[i-1] and v[i]>v[i+1]]; n.append(len(p)); pk.append(v.max())
    print(f"{run} f{f}: crests>12 levels per ray median {np.median(n):.0f}, peak {np.median(pk):.0f}")
