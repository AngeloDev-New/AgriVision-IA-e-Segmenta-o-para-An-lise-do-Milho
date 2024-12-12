# !pip install zipfile
# !sudo apt-get install unrar
# !pip uninstall pillow
# !pip install pillow --upgrade --force-reinstall
# # !pip install pillow
import zipfile
import io
import requests
from PIL import Image
import subprocess
Image.MAX_IMAGE_PIXELS = None
def carregarLocal():
  with open("names.txt","r") as names:
    namelisted = names.readlines()
  for imagen in namelisted:
      with open(imagen.replace("/","//").replace("\n",""),"rb") as image:
        yield image.read()
imagens = []
try:
  for imagenBTS in carregarLocal():
    imagens.append(io.BytesIO(imagenBTS))
# except Exceptin as e:
#   pass
except:
  print("arquivos nao encontrados no local, baixando do drive")
  link = "https://drive.usercontent.google.com/download?id=10CBH3mAWwEw7RLEENgR9SCPpax2Hq9wm&export=download&confirm=t&uuid=60710c25-dc1c-4b9a-8c04-5cb5e30cf482&at=APvzH3o-oEV6bYbNetICf4FTSsvc%3A1733885388620"
  response = requests.get(link)
  response.raise_for_status()
  print(len(response.content),"bytes baixados")
  bts = io.BytesIO(response.content)
  with zipfile.ZipFile(bts) as zf:
    zf.extractall()
    with open("names.txt","w") as names:
      names.write("\n".join(zf.namelist()[1:]))
  for imagenBTS in carregarLocal():
    imagens.append(io.BytesIO(imagenBTS))


def newArea(sections,size,dispercao = (10,10)):
    # sections == tamanho das imagens de saida
    # size == tamanho total do tif
    xdisp,ydisp = dispercao
    largura,altura = sections
    width,height  = size
    for x in range(width):
        for y in range(height):
            if x%xdisp == 0 and y%ydisp == 0:
                left = x
                upper = y
                right = x+largura
                lower = y+altura
                yield (left,upper,right,lower)
def aproved(image,usability):
    if image.mode != "RGBA":
        return True
    width,height  = image.size
    total = width*height
    transparentes = 0
    for x in range(width):
        for y in range(height):
            r,g,b,a = image.getpixel((x,y))
            if a < 10:
                transparentes += 1
                if transparentes > total*usability:
                    return False


def getSegmentos(img,sections,dispercao,USABLE):
  for area in newArea(sections,img.size):
    segmento = img.crop(area)
    if aproved(segmento,USABLE):
      yield segmento

for imagem in imagens:
  with Image.open(imagem,formats=["TIFF"]) as img:
    print(*getSegmentos(
        img=img,sections = (1000,1000),
        dispercao = (10,10),
        USABLE = 0.7),sep="\n")
    print("nSegments")
