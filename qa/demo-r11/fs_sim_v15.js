    // the surface at half resolution: height, slope (screen axes, y down) and where water shows
    // v1.5: rings stay closed-form; a press-and-drag is no longer a drawn line but a moving pressure on a small
    // stepped height field (GRID below), sampled here and added to the ring slope
    var FS_SIM = HEAD + "uniform sampler2D P,Gt;uniform vec2 vp,gz;uniform vec4 I[" + SLOTS + "],A[16],R[32],K[32],Dm,Cp,Gp;uniform int nR;in vec2 v;out vec4 o;" +
      "float gh(vec2 c){return texture(Gt,c/gz).x;}" +
      "void main(){vec2 p=vec2(v.x,1.-v.y)*vp;float h=0.;vec2 s=vec2(0.);" +
      "for(int i=0;i<16;i++){vec4 a=A[i];float t=dot(a.xy,p)-a.w;h+=a.z*sin(t);s+=a.z*cos(t)*a.xy;}float cv=0.;" +
      "for(int i=0;i<" + SLOTS + ";i++){vec4 q=I[i];if(q.w==0.)continue;vec2 d=p-q.xy;float r=length(d);if(r>=" + RMAX.toFixed(1) + ")continue;" +
      "vec3 e=texture(P,vec2(r*" + ((NR - 1) / NR / RMAX).toFixed(9) + "+" + (0.5 / NR).toFixed(9) + ",q.z)).rgb*q.w;h+=e.x;s+=e.y*d/max(r,.001);cv+=e.z;}" +
      // the height field (cells of Gp.x CSS px): height, central-difference slope and 5-point Laplacian, gain Gp.y
      "if(Gp.y!=0.){vec2 c=p/Gp.x;float c0=gh(c),xa=gh(c+vec2(1.,0.)),xb=gh(c-vec2(1.,0.)),ya=gh(c+vec2(0.,1.)),yb=gh(c-vec2(0.,1.));" +
      "h+=Gp.y*c0;s+=Gp.y*vec2(xa-xb,ya-yb)/(2.*Gp.x);cv+=Gp.y*(xa+xb+ya+yb-4.*c0)/(Gp.x*Gp.x);}" +
      // the finger itself: a dimple held by its meniscus (core dip + a low rim), riding exactly under the pointer
      "if(Dm.z!=0.){vec2 d=p-Dm.xy;float r=length(d),w=Dm.w,c=exp(-r*r/(w*w)),x=(r-1.35*w)/(.16*w),g=exp(-x*x);" +
      "h+=Dm.z*(.1*g-c);s+=Dm.z*(2.*r/(w*w)*c-.1*2.*x/(.16*w)*g)*d/max(r,.001);" +
      "float sg=.16*w;float dz=.5*Dm.z*(.1*(g*(4.*x*x-2.)/(sg*sg)-2.*x*g/(sg*max(r,1.)))-c*(4.*r*r/(w*w*w*w)-4./(w*w)));cv+=dz;}" +
      "float m=1.;for(int i=0;i<32;i++){if(i>=nR)break;vec4 b=R[i];vec2 dd=max(max(b.xy-p,p-b.zw),0.);m=min(m,mix(K[i].x,1.,smoothstep(0.,K[i].y,length(dd))));}" +
      // .x, light: minus the disturbance's Laplacian (the swell left out), positive along each crest.
      // .x, dark (Cp.z): the slope variance this half-res pixel cannot resolve (curvature × pixel, Kaplanyan-style):
      // the composite widens and dims its glints by it instead of drawing detail it would alias
      "float ox=-cv;if(Cp.z>.5)ox=Cp.x*cv*cv;" +
      "o=vec4(ox,s,m);}";
    // v1.5 · the drag wake: a height field (h, v) stepped at a fixed rate on a coarse grid. Each step
    //   v += c²∇²h − β∇⁴h − κh + μ∇²v − pressure;  v *= damping;  h += v
    // so ω² = κ + c²k² + βk⁴: the phase speed has a minimum (c_min ≈ 270 px/s), a pressure moving slower than it
    // just carries its own depression along (no wake), a faster one sheds a V, and the β term makes short ripples
    // run ahead of long ones (capillary-like). The pressure is a capsule along the pointer's path during the step
    // (a raised cosine around the segment), weighted by the time each point spends under it, so a fast flick
    // never prints as a row of beads. Borders absorb (a sponge), the page has no walls.
    var GRID = { c2: 0.30, b: 0.02, k: 0.006, mu: 0.04, damp: 0.986, R: 3.0, rate: 120, life: 2.0, fade: 0.45 };
    var FS_GSTEP = HEAD + "uniform sampler2D Gt;uniform vec4 Sg,Pa;uniform vec2 gz;out vec4 o;" +
      "vec2 f(ivec2 c){return texelFetch(Gt,clamp(c,ivec2(0),ivec2(gz)-1),0).xy;}" +
      "void main(){ivec2 c=ivec2(gl_FragCoord.xy);vec2 q=f(c),l=f(c-ivec2(1,0)),r=f(c+ivec2(1,0)),d=f(c-ivec2(0,1)),u=f(c+ivec2(0,1));" +
      "float s4=l.x+r.x+d.x+u.x,dg=f(c+ivec2(1,1)).x+f(c+ivec2(-1,1)).x+f(c+ivec2(1,-1)).x+f(c+ivec2(-1,-1)).x," +
      "f4=f(c+ivec2(2,0)).x+f(c-ivec2(2,0)).x+f(c+ivec2(0,2)).x+f(c-ivec2(0,2)).x;" +
      "float L=s4-4.*q.x,B=20.*q.x-8.*s4+2.*dg+f4,Lv=l.y+r.y+d.y+u.y-4.*q.y;" +
      "vec2 x=gl_FragCoord.xy,ab=Sg.zw-Sg.xy,ax=x-Sg.xy;float t=clamp(dot(ax,ab)/max(dot(ab,ab),1e-4),0.,1.),dd=length(ax-ab*t);" +
      "float w=dd<Pa.y?.5+.5*cos(3.14159265*dd/Pa.y):0.;" +
      "float e=min(min(x.x,x.y),min(gz.x-x.x,gz.y-x.y)),sp=mix(.82,1.,smoothstep(0.,7.,e));" +
      "float vv=(q.y+" + GRID.c2.toFixed(3) + "*L-" + GRID.b.toFixed(3) + "*B-" + GRID.k.toFixed(4) + "*q.x+" + GRID.mu.toFixed(3) + "*Lv-Pa.x*w)*Pa.z*sp;" +
      "o=vec4(q.x+vv,vv,0.,1.);}";
    // a scroll moves the field with the page (bilinear shift by Pa.w cells)
    var FS_GSHIFT = HEAD + "uniform sampler2D Gt;uniform vec2 gz;uniform float dy;out vec4 o;void main(){o=texture(Gt,(gl_FragCoord.xy+vec2(0.,dy))/gz);}";
