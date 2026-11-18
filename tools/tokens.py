from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageChops, ImageFont
import math, sys
import os
W=os.environ.get('DOZE_WORK','work'); M=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'assets')
S=512
def white_to_alpha(path,gain=3.2):
    im=Image.open(path).convert('RGBA'); g=ImageOps.grayscale(im)
    a=ImageOps.invert(g).point(lambda v: min(255,int(v*gain)))
    rgb=Image.merge('RGB',[ImageOps.autocontrast(g)]*3)
    out=rgb.convert('RGBA'); out.putalpha(a); return out.crop(a.point(lambda v:255 if v>20 else 0).getbbox())
def redo_lineart():
    """Converte os desenhos a traço (fundo branco) em PNG com transparência. W = pasta com as imagens extraídas do PDF."""
    for k,f in [('boi-da-cara-preta','p23_x438'),('criatura-esboco','p15_x134')]:
        im=white_to_alpha(f'{W}/imgs/{f}.png'); im.thumbnail((1600,1600),Image.LANCZOS); im.save(f'{M}/art/{k}.webp','WEBP',quality=86)
def bg_disc(seed=0):
    bg=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(bg)
    # radial gradient deep purple->black
    for r in range(S//2,0,-2):
        t=r/(S/2); c=(int(40+60*(1-t)*0.3),int(8+10*(1-t)),int(30+40*(1-t)*0.6),255)
        d.ellipse([S/2-r,S/2-r,S/2+r,S/2+r],fill=(int(25+50*t*0.4),int(6+6*t),int(20+30*t*0.5),255) if False else c)
    return bg
def corona(img,cx,cy,r,strength=1.0):
    glow=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(glow)
    for i in range(40,0,-1):
        rr=r+i*2.2; a=int(255*strength*(1-i/40)**2*0.9)
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=(255,236,200,a),width=3)
    glow=glow.filter(ImageFilter.GaussianBlur(4)); img.alpha_composite(glow)
    d=ImageDraw.Draw(img)
    # rays
    for k in range(18):
        ang=k*2*math.pi/18+0.1*(k%3); L=r*(1.25+0.35*((k*7)%5)/4)
        x1=cx+math.cos(ang)*r*0.98; y1=cy+math.sin(ang)*r*0.98; x2=cx+math.cos(ang)*L; y2=cy+math.sin(ang)*L
        d.line([(x1,y1),(x2,y2)],fill=(255,245,225,int(170*strength)),width=2)
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(6,5,8,255))
def frame(img):
    ring=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(ring)
    d.ellipse([4,4,S-4,S-4],outline=(181,101,44,255),width=18)   # rust
    d.ellipse([14,14,S-14,S-14],outline=(232,190,120,255),width=4) # gold inner
    d.ellipse([2,2,S-2,S-2],outline=(20,8,6,255),width=4)
    # small notches like sun rays on ring
    for k in range(24):
        ang=k*2*math.pi/24; r1=S/2-6; r2=S/2-20
        d.line([(S/2+math.cos(ang)*r1,S/2+math.sin(ang)*r1),(S/2+math.cos(ang)*r2,S/2+math.sin(ang)*r2)],fill=(110,45,18,255),width=3)
    img.alpha_composite(ring)
def circle_mask(margin=16):
    m=Image.new('L',(S,S),0); ImageDraw.Draw(m).ellipse([margin,margin,S-margin,S-margin],fill=255); return m
def art_token(name,cx,cy,side,out,lineart=False):
    art=Image.open(f'{M}/art/{name}.webp').convert('RGBA')
    box=(int(cx-side/2),int(cy-side/2),int(cx+side/2),int(cy+side/2))
    canvas=Image.new('RGBA',(box[2]-box[0],box[3]-box[1]),(0,0,0,0))
    canvas.alpha_composite(art,(-box[0],-box[1])) if box[0]<=0 and box[1]<=0 else None
    crop=Image.new('RGBA',(side,side),(0,0,0,0)); crop.paste(art,(-box[0],-box[1]),art)
    crop=crop.resize((S,S),Image.LANCZOS)
    base=bg_disc()
    corona(base,S/2,S*0.42,S*0.26,0.55)
    if lineart:
        parch=Image.open(f'{M}/ui/pergaminho.webp').convert('RGBA').resize((S,S))
        base=parch; 
    base.alpha_composite(crop)
    m=circle_mask(); res=Image.new('RGBA',(S,S),(0,0,0,0)); res.paste(base,(0,0),m)
    frame(res); res.save(f'{M}/tokens/{out}.webp','WEBP',quality=88)
def letter_token(title,out,sub=None):
    base=bg_disc(); corona(base,S/2,S/2,S*0.30,1.0)
    d=ImageDraw.Draw(base)
    f=ImageFont.truetype(f'{M}/fonts/UnifrakturMaguntia-Book.ttf',int(S*0.34))
    t=title[0]; bb=d.textbbox((0,0),t,font=f); w=bb[2]-bb[0]; h=bb[3]-bb[1]
    d.text((S/2-w/2-bb[0],S/2-h/2-bb[1]),t,font=f,fill=(214,64,40,255))
    f2=ImageFont.truetype(f'{M}/fonts/Cinzel-Variable.ttf',int(S*0.058))
    words=title.upper(); bb=d.textbbox((0,0),words,font=f2); w=bb[2]-bb[0]
    if w>S*0.56:
        f2=ImageFont.truetype(f'{M}/fonts/Cinzel-Variable.ttf',int(S*0.058*S*0.56/w)); bb=d.textbbox((0,0),words,font=f2); w=bb[2]-bb[0]
    d.text((S/2-w/2,S*0.765),words,font=f2,fill=(240,215,170,255))
    m=circle_mask(); res=Image.new('RGBA',(S,S),(0,0,0,0)); res.paste(base,(0,0),m); frame(res)
    res.save(f'{M}/tokens/{out}.webp','WEBP',quality=88)
if __name__=='__main__':
    pass
