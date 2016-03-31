from PIL import Image
import base64
# 00 ~ 7F まではASCIIと同じだが、 80 ~ FF は難しいのでpngではなくhtmlを返す...

def putBinary(img,fileName,sx,sy):
    putImage = Image.open(fileName,'r')
    img.paste(putImage,(sx,sy))
    return sx + 3 + putImage.size[0]
    
def getBase64Content(fileName):
    with open (fileName,"rb")as f: 
        data = f.read()
    data = base64.b64encode(data)
    return data

def putContent(img,content,sx,sy):
    pushs = [(255,192,192),(255,0,0),(192,0,0)]
    p = 0
    for ic in range(len(content)):
        c = content[len(content)-1-ic]
        for i in range(0,c):img.putpixel((sx,sy+i),pushs[p])
        sx += 1
        p = (p+1) % 3
    img.putpixel((sx,sy),pushs[p])    
    return sx + 3

def WhileNotEmpty(img,sx,sy):
    F = 255
    C = 192
    A1 = [(F,C,C),(C,0,C),(0,C,C),(C,C,0),(C,F,C),(0,0,C),(F,F,C),(C,C,0)]
    for i in range(len(A1)) : img.putpixel((sx+i+1,sy),A1[i])
    img.putpixel((sx+7,sy+1),(C,0,0))       
    img.putpixel((sx+1,sy+2),(C,0,C))       
    img.putpixel((sx,sy+3),(0,0,0))       
    img.putpixel((sx+1,sy+3),(F,C,C))                 
    img.putpixel((sx+6,sy+3),(C,0,C))       
    img.putpixel((sx+7,sy+3),(F,C,C))       
    img.putpixel((sx+7,sy+4),(0,0,0))       
    img.putpixel((sx+8,sy+1),(C,C,0))          
    img.putpixel((sx+9,sy+1),(0,0,0))       
    return sx+8 + 3

def finPiet(img,sx,sy):
    # sy == 0?
    bs = [(0,1),(1,2),(2,2),(3,0),(3,1)]
    rs = [(2,0),(2,1),(1,1)]
    for b in bs: img.putpixel((sx + b[0],sy +b[1]),(0,0,0))
    for r in rs: img.putpixel((sx + r[0],sy +r[1]),(255,0,0))
    return sx + 5 + 3
    

def doByStatusCode(sx,sy,img,status,imgbyte,contentfin):
    sx = putContent(img,status,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    sx = putContent(img,imgbyte,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    sx = putContent(img,contentfin,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    sx = finPiet(img,sx,sy)
    return sx

def getStatusContent(status):
    return  b'HTTP/1.0 '+ status + b'\nContent-type: text/html\n\n<!DOCTYPE html><html lang="ja"><img src="data:image/png;base64,'

if __name__ == "__main__" :
    status_200 = getStatusContent(b"200 OK")
    Img_200 = getBase64Content("200.png")
    status_400 = getStatusContent(b"400 Bad Request")
    Img_400 = getBase64Content("400.png")
    status_451 = getStatusContent(b"451 Unavailable For Legal Reasons")
    Img_451 = getBase64Content("451.png")
    contentfin = b'">'
    
    LEN  = len(status_200)+ len(Img_200)+len(contentfin)
    LEN += len(status_400)+ len(Img_400)+len(contentfin)
    LEN += len(status_451)+ len(Img_451)+len(contentfin)
    img = Image.new("RGB",( 64 * 3 + LEN + 64,25 + 128),(255,255,255))
    sx = putBinary(img,"branch.png",0,0)
    sx = doByStatusCode(sx,25,img,status_400,Img_400,contentfin)
    sx = doByStatusCode(sx,14,img,status_451,Img_451,contentfin)
    sx = doByStatusCode(sx,6,img,status_200,Img_200,contentfin)
    img.save ("htmlserver.png")
