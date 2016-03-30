from PIL import Image
import base64
# 00 ~ 7F まではASCIIと同じだが、 80 ~ FF は難しいのでpngではなくhtmlを返す...

def getPngData(fileName,requireW,requireH):
    data = []
    Max = 0
    l = 0
    with open (fileName,"rb")as f: 
        rdata = f.read()
    rdata = base64.b64encode(rdata)
    print(rdata)
    for d in rdata:
        data.append(d)
        Max = max(Max,d)
        if d == 0: l += 4
        else :l += 1
    data.reverse() 
    img = Image.new("RGB",( l + requireW, Max + requireH),(255,255,255))
    return (img,data)

def getBase64Content(fileName):
    with open (fileName,"rb")as f: 
        data = f.read()
    data = base64.b64encode(data)
    return data

def putBinary(img,data,sx,sy):
    pushs = [(255,192,192),(255,0,0),(192,0,0)]
    nots  = [(0,192,0),(192,255,192),(0,255,0)]
    p = 0
    for d in data:
        if d == 0:
            img.putpixel((sx,sy),pushs[p])
            sx += 1
            p = (p+1) %3
            img.putpixel((sx,sy),pushs[p])
            sx += 1
            img.putpixel((sx,sy),nots[p]) 
            sx += 1
            img.putpixel((sx,sy),(255,255,255))
        else :
            for i in range(0,d): img.putpixel((sx,sy+i),pushs[p])
        sx += 1
        p = (p+1) % 3
    img.putpixel((sx,sy),pushs[p])
    return sx + 3

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
    # sy == 0
    bs = [(0,1),(1,2),(2,2),(3,0),(3,1)]
    rs = [(2,0),(2,1),(1,1)]
    for b in bs: img.putpixel((sx + b[0],sy +b[1]),(0,0,0))
    for r in rs: img.putpixel((sx + r[0],sy +r[1]),(255,0,0))

if __name__ == "__main__" :
    sx,sy = 0,0
    #content = b"HTTP/1.0 200 OK\nContent-type: image/png\n\n"
    #content = b'HTTP/1.0 200 OK\nContent-type: text/html\n\n<!DOCTYPE html><html lang="ja"><img src="index.png"></html>'
    #img,data = getPngData("index.png",len(content)+len(contentfin) + 100,sy) 
    #sx = putBinary(img,data,sx,sy)
    #sx = WhileNotEmpty(img,sx,sy)
    #いろ変えるかい？
    content = b'HTTP/1.0 200 OK\nContent-type: text/html\n\n<!DOCTYPE html><html lang="ja"><script>window.location.href="data:image/png;base64,'
    content64 = getBase64Content("index.png")
    contentfin = b'";</script>'
    LEN  = len(content)+ len(content64)+len(contentfin)
    img = Image.new("RGB",( 64 + LEN , 128),(255,255,255))
    sx = putContent(img,content,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    sx = putContent(img,content64,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    sx = putContent(img,contentfin,sx,sy)
    sx = WhileNotEmpty(img,sx,sy)
    finPiet(img,sx,sy)
    img.save ("htmlserver.png")