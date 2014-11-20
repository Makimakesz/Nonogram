from turtle import *
from random import randint
import sys
Debug=0
width=800
height=600
Len=16#20 = works, seems 16 works too 
X=-1
Y=-1
Lives=3
numBlocks=0
totalBlocks=0
Blocks=[]
World=[]
setCross=[]
forcedCross=[]
numberDrawY=[]
blockColor='#BB00BB'
squareColor='#00FFFF'
numberColor='#FFFFFF'
seperatorColor='#FF0000'
bgColor='#000000'
Title="Nonogram"
dist=10
chance=65
min=5
max=20
def isInt(n):
    if(str(type(n))=="<class 'int'>"):
        return 1
    return 0
def toInt(n):
    try:
        num=int(n)
        return num
    except:
        return n
def Hex(n):
    num=hex(n)[2:]
    if(len(num)<2):
        num='0'+num
    return num
def highestDiv(n):
    ret=-1
    for i in range(2,int(n/2)+1):
        if n%i==0:
            if(n/i==2 and ret>2):
                return ret
            ret=i
    return ret
def setColors():
    global blockColor
    global squareColor
    global bgColor
    min=155
    max=255
    Min=0
    Max=50
    add=50
    r=randint(min,max)
    if(randint(0,2)==1):
        min+=30
    g=randint(min,max)
    if(randint(0,2)==1):
        min+=30
    b=randint(min,max)
    if(r<g and r<b):
        r-=add
    elif(g<r and g<b):
        g-=add
    else:
        b-=add
    R1=randint(Min,Max)
    G1=randint(Min,Max)
    B1=randint(Min,Max)
    if(R1<G1 and R1<B1):
        R1+=add
    elif(G1<R1 and G1<B1):
        G1+=add
    else:
        B1+=add
    R2=255-R1
    G2=255-G1
    B2=255-B1
    blockColor="#%s%s%s"%(Hex(r),Hex(g),Hex(b))
    squareColor="#%s%s%s"%(Hex(R2),Hex(G2),Hex(B2))
    bgColor="#%s%s%s"%(Hex(R1),Hex(G1),Hex(B1))    
setColors()

def generateWorld(x=11,y=11):
    global X
    global Y
    global width
    global height
    global World
    max=14
    if(y<min):
        y=min
    X=x
    Y=y
    if(y>x):
        X=Y
    for y in range(0,Y+1):
        level=""
        for x in range(0,X+1):
            Rand=randint(0,100)
            if(Rand<chance):
                Rand=1
            else:
                Rand=0
            level+=str(Rand)
        World.append(level)
    width=(X*Len)+dist*2+(int((X+2)/2)+1)*Len
    height=(Y*Len)+dist*2+(int((Y+2)/2)+1)*Len
def loadWorld(filename):
    global X
    global Y
    global width
    global height
    global World
    try:
        file=open(filename)
    except:
        print("Failed to load:",filename)
        return -1
    i=0
    test=-1
    while(True):
        a=file.readline()
        if not a: break
        a=a.strip('\n')
        World.insert(0,a)
        X=len(a)
        if(test==-1):
            test=X
        if(test!=X):
            return -1
        i+=1
    file.close()
    Y=i
    if(Y>X):
        for i in range(0,len(World)):
            for j in range(0,Y-X):
                World[i]+=str(randint(0,2))
        X=Y
    
filename="level.txt"
Y=randint(min,max-1)
X=randint(Y,max)
c=0
if len(sys.argv)==1:
    print('Command line arguments: file="(filename)", x=(int), y=(int), chance=(int: 1-100)')
res=-1
for i in range(1,len(sys.argv)):
    arg=sys.argv[i]
    args=arg.split("=")
    if(len(args)==2):
        args[0]=args[0].lower()
        if(args[0]=="file"):
            res=loadWorld(args[1])
            if(res!=-1):
                break
        elif(args[0]=="x"):
            X=toInt(args[1])
        elif(args[0]=="y"):
            Y=toInt(args[1])
        elif(args[0]=="chance"):
            chance=toInt(args[1])
if(res==-1):
    if(X==-1):
        Y=randint(min,max-1)
        X=randint(min,max)
    if(Y==-1):
        Y=randint(min,X)
    if(highestDiv(X)==-1):
        X+=1
    if(highestDiv(Y)==-1):
        Y+=1
    generateWorld(X,Y)
divX=highestDiv(X)
divY=highestDiv(Y)
width=(X*Len)+dist*2+(int((X+2)/2)+1)*Len#+dist*X
height=(Y*Len)+dist*2+(int((Y+2)/2)+1)*Len#+dist*Y
print("Starting game, X:",X,"Y:",Y)
print("You have",Lives,"lives")
#width=500
#height=500
startX=(-1)*(width/2)
startY=(-1)*(height/2)
centerX=(width-(Len*X))-dist
centerY=(height-(Len*Y))-dist
if(Debug==1):
    print("X:",X,"Y:",Y)
    print("Width:",width,"Height:",height)
    print("startX",startX,"startY:",startY)
    print("centerX",centerX,"centerY",centerY)
speed(0)
delay(0)
title(Title)
bgcolor(bgColor)
def isBlock(x,y):
    world=World[y]
    List=list(world)
    if(List[x]=='0'):
        return False
    return True
def getTile(x,y):
    global X
    global Y
    X1=int((startX+x+dist)/Len)
    Y1=int((startY+y+dist)/Len)
    X2=X+X1-1
    Y2=Y-Y1*(-1) -1
    if(Debug):
        print("getTile:",x,y,X2,Y2)
    return (X2,Y2)
def toTile(x,y):
    X=centerX+Len*x
    Y=centerY+Len*y
    Goto(X,Y,0)
    return (X,Y)
def drawBlock(x,y,size,Color='black'):
    color=Color
    fillcolor(Color)
    pencolor(Color)
    Goto(x,y,0)
    begin_fill()
    Goto(x+size,y,1)
    Goto(x+size,y+size,1)
    Goto(x,y+size,1)
    end_fill()
def numberBlock(x,y,size):
    drawBlock(x,y,size,numberColor)
def drawNumber(x,y,num):
    color(numberColor)
    Goto(x+2,y-5,False)
    write(num,font=("Times new roman",7,"normal"))
def cross(x,y):
    color(blockColor)
    global X
    global Y
    (X1,Y1)=getTile(x,y)
    if(X1>=0 and X1<X):
        if(Y1>=0 and Y1<Y):
            (X2,Y2)=toTile(X1,Y1)
            Goto(X2+1,Y2+1,0)
            Goto(X2+Len,Y2+Len,1)
            Goto(X2+1,Y2+Len-1,0)
            Goto(X2+Len,Y2,1)
def block(x,y):
    global X
    global Y
    (X1,Y1)=getTile(x,y)
    if(X1>=0 and X1<X):
        if(Y1>=0 and Y1<Y):
            (X2,Y2)=toTile(X1,Y1)
            drawBlock(X2+2,Y2+2,Len-4,blockColor)
def winGame():
    print("You win!")
    color(bgColor)
    begin_fill()
    Goto(0,0,1)
    Goto(width,0,1)
    Goto(width,height,1)
    Goto(0,height,1)
    Goto(0,0,1)
    end_fill()
    CenterX=(width-X*Len+dist)/2
    CenterY=(height-Y*Len+dist)/2
    color(blockColor)
    beginX=0
    endX=0
    beginY=0
    endY=0
    i=0
    j=0
    for i in range(0,Y):
        if(i==0):
            beginY=CenterY+Len*j
        for j in range(0,X):
            if World[i][j]=='1':
                color(blockColor)
            else:
                color("#000000")
            begin_fill()
            square(CenterX+Len*j,CenterY+Len*i)
            end_fill()
    endX=CenterX+Len*X
    endY=CenterY+Len*Y
    color("#FF0000")
    pensize(2)
    Goto(CenterX,CenterY,0)
    Goto(endX,CenterY,1)
    Goto(endX,endY,1)
    Goto(CenterX,endY,1)
    Goto(CenterX,CenterY,1)
    title("Nonogram - You Win! Click anywhere to exit")
    exitonclick()
class Turtle(Turtle):
    def screensize(self,width,height):
        screensize(width,height)
    def leftclick(self,x,y):
        global Lives
        global numBlocks
        global Blocks
        global setCross
        (X1,Y1) = getTile(x,y)
        if(X1>=0 and X1<X and Y1>=0 and Y1<Y):
            if((X1,Y1) in setCross)==False:
                if(isBlock(X1,Y1)==True):
                    if ((X1,Y1) in Blocks)==False:
                        Blocks.append((X1,Y1))
                        block(x,y)
                        numBlocks+=1
                        if(numBlocks>=totalBlocks):
                            winGame()
                else:
                    if((X1,Y1) in forcedCross)==False:
                        cross(x,y)
                        forcedCross.append((X1,Y1))
                        Lives-=1
                        if(Lives>0):
                            print("Lives left:",Lives)
                            title("Nonogram - Guesses left: %s"%Lives)
                        else:
                            print("Game over!")
                            title("Nonogram - Game Over! Click anywhere to exit")
                            exitonclick()
    def rightclick(self,x,y):
        (X1,Y1) = getTile(x,y)
        if((X1,Y1) in forcedCross)==False:
            if((X1,Y1) in setCross)==True:
                if((X1,Y1) in Blocks)==False:
                    setCross.remove((X1,Y1))
                    (X,Y)=toTile(X1,Y1)
                    drawBlock(X+1,Y+1,Len-2,bgColor)            
            else:
                cross(x,y)
                setCross.append((X1,Y1))
    def middleclick(self,x,y):
        pass
def Goto(x,y,visible):
    if not visible:
        pu()
        goto(startX+x,startY+y)
        pd()
    else:
        pd()
        goto(startX+x,startY+y)
def square(x,y):
    Goto(x,y,0)
    setheading(0)
    forward(Len)
    setheading(90)
    forward(Len)
    setheading(180)
    forward(Len)
    setheading(270)
    forward(Len)
turtle=Turtle()
turtle.screensize(width,height)
if X<12:
    setup(425,height+50)
elif Y<12:
    setup(width+50,400)
else:
    setup(width+50,height+50)
ht()
turtle.ht()
title("Nonogram - Loading...")
for i in range(0,X):
    for j in range(0,Y):
        color(squareColor)
        square(centerX+Len*i,centerY+Len*j) 
        if(j==i):
            world=World[i]
            num=0
            numbers=[]
            for k in range(0,X):
                if(world[k]=='0'):
                    if(num>0):
                        numbers.append(num)
                        num=0
                else:
                    num+=1
            if(num>0):
                numbers.append(num)
            if(len(numbers)==0):
                numbers.append(0)
            for l in range(0,len(numbers)):
                color(squareColor)
                square(centerX-Len*(l+2),centerY+Len*j)
                L=len(numbers)-l-1
                color(numberColor)
                if((L,j) in numberDrawY)==False:
                    drawNumber(centerX-Len*(L+2)+Len/8,centerY+Len*j+Len/2,int(numbers[l]))
                    numberDrawY.append((L,j))
for j in range(0,X):
    num=0
    numbers=[]
    for i in range(0,Y):
        world=World[i]
        Num=int(world[j])
        if(Num==0):
            if(num>0):
                numbers.append(num)
                totalBlocks+=num
                num=0
        else:
            num+=1
    if(num>0):
        numbers.append(num)
        totalBlocks+=num
    if(len(numbers)==0):
        numbers.append(0)
    for k in range(0,len(numbers)):
        color(squareColor)
        square(centerX+Len*j,centerY-Len*(k+2))
        K=len(numbers)-k-1
        color(numberColor)
        drawNumber(centerX+Len*j+Len/8,centerY-Len*(K+2)+Len/2,int(numbers[k]))
if(divX!=-1 and divY!=-1):
    color(seperatorColor)
    for i in range(0,Y+1):
        if(i%divY==0):
            Goto(centerX,centerY+Len*i,0)
            Goto(centerX+Len*X,centerY+Len*i,1)
    for i in range(0,X+1):
        if(i%divX==0):
            Goto(centerX+Len*i,centerY,0)
            Goto(centerX+Len*i,centerY+Len*Y,1)
onscreenclick(turtle.leftclick,1,True)
onscreenclick(turtle.rightclick,3,True)
onscreenclick(turtle.middleclick,2,True)
title("Nonogram - Guesses left: %d"%Lives)
mainloop()
