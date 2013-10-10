from dxfwrite import DXFEngine as dxf
from dxfwrite.const import CENTER

import math as m, time

AUTO_RUN = True
def run():

    details = {
        
	"complexity": ["outline","angleLines","angleMarks","rulerMarks","rulerNums"],
        "degMarkSize": (2,1),
        "degsPerLine":10,
        "degsPerMark":1,
        "description": "rulerNums",
        "mmPerMark":1,
        "rulerClearance":5,
        "rulerMarkSize":(3,) + 4*(0.75,1.5) + (0.75,),
        "rulerMax":65,
	"size": 100,
        "topLeft": (0,0)
        
	}

    name = "tests/test_geoliner_" + details["description"] + "_" + \
           nowStr() + ".dxf"

    drawing = dxf.drawing(name)
    drawGeoliner(drawing,details)
    drawing.save()


def nowStr():
    timeNow = time.gmtime()
    now = c(str(timeNow.tm_year),4) + c(str(timeNow.tm_mon),2) + c(str(timeNow.tm_mday),2) + "_"
    now = now + c(str(timeNow.tm_hour),2) + c(str(timeNow.tm_min),2) + c(str(timeNow.tm_sec),2)
    return now
def c(string, length, char = "0"):
    return char*(length-len(string)) + string

def drawGeoliner(drawing,details):
    oX,oY = details["topLeft"]
    l = details["size"]

    if "outline" in details["complexity"]:
        drawing.add(dxf.line((oX, oY),(oX + l, oY)))
        drawing.add(dxf.line((oX, oY),(oX, oY + l)))
        drawing.add(dxf.line((oX, oY + l),(oX + l, oY)))
    if "angleLines" in details["complexity"]:
        degsPerDevision = details["degsPerLine"]
        maxRads = m.pi

        cX,cY=  (oX + l/2.0,  oY + l/2.0)

        rPD = (degsPerDevision/180.0 * m.pi)
        theta = rPD
        maxD = 0
        while theta < maxRads-0.00001:
            if theta< m.pi/2.0:
                rY = 0
                rX = l*(1 - m.sqrt(0.5)*(m.sin(theta)/m.sin(0.75*m.pi - theta)))

                dX= cX - rX
                dY = cY - rY

                e1 = details["rulerClearance"]
                e2 = e1 /m.tan(theta)

                d2X = m.sqrt(0.5)*e1  - m.sqrt(0.5)*e2
                d2Y = m.sqrt(0.5)*e1  + m.sqrt(0.5)*e2

                
                drawing.add(dxf.line((cX-d2X, cY-d2Y),(oX+rX,oY+rY)))
            else:
                rX = 0
                alpha = m.pi - theta
                rY = l*(1 - m.sqrt(0.5)*(m.sin(alpha)/m.sin(0.75*m.pi - alpha)))
                
                dX= cX - rX
                dY = cY - rY

                e1 = details["rulerClearance"]
                e2 = e1 /m.tan(theta)

                d2X = m.sqrt(0.5)*e1  - m.sqrt(0.5)*e2
                d2Y = m.sqrt(0.5)*e1  + m.sqrt(0.5)*e2

                drawing.add(dxf.line((cX-d2X,cY-d2Y),(oX+rX,oY+rY)))
                
            theta += rPD
    if "wordCircle" in details["complexity"]:
        drawing.add(dxf.circle(radius=10, center=(oX,oY)))
        drawing.add(dxf.circle(radius=11, center=(oX,oY)))
        for i in range(12):
            angle = i*m.pi/6.0
            angleD = i * 30
            rX,rY = oX + 10*m.sin(angle), oY + 10*m.cos(angle)
            drawing.add(dxf.text(str(i),insert = (rX,rY),height=1,rotation = -angleD))
            
    if "angleMarks" in details["complexity"]:
        dPM = details["degsPerMark"]
        maxRads = m.pi

        cX,cY=  (oX + l/2.0,  oY + l/2.0)

        rPM = rad(dPM)
        theta = rPM
        count = 0
        while theta <= maxRads:
            if theta%(rad(details["degsPerLine"])) > 0.00001 and (-theta)%(rad(details["degsPerLine"])) > 0.00001:
                r = details["degMarkSize"][count%len(details["degMarkSize"])]
                if theta< m.pi/2.0:
                    rX = l*(1 - m.sqrt(0.5)*(m.sin(theta)/m.sin(0.75*m.pi - theta)))
                    rY = 0

                    dX= rX - cX
                    dY = rY - cY
                    
                    rX2 = rX + r * (dX/dY)
                    rY2 = rY + r
                    
                    drawing.add(dxf.line((oX+rX2,oY+rY2),(oX+rX,oY+rY)))
                else:
                    rX = 0
                    alpha = m.pi - theta
                    rY = l*(1 - m.sqrt(0.5)*(m.sin(alpha)/m.sin(0.75*m.pi - alpha)))

                    dX= rX - cX
                    dY = rY - cY
                    
                    rX2 = rX+ r
                    rY2 = rY + r * (dY/dX)
                    
                    drawing.add(dxf.line((oX+rX2,oY+rY2),(oX+rX,oY+rY)))
            theta += rPM
            count += 1
    if "rulerMarks" in details["complexity"]:
        cX,cY=  (oX + l/2.0,  oY + l/2.0)
        gap = details["mmPerMark"]
        e2 = gap
        count = 1

        e1 = details["rulerMarkSize"][0]

        dX = m.sqrt(0.5)*e1
        dY = m.sqrt(0.5)*e1

        drawing.add(dxf.line((cX,cY),(cX-dX,cY-dY)))

        while e2 <= (details["rulerMax"]) + 0.00001:
            
            index = count%(len(details["rulerMarkSize"]))
            e1 = details["rulerMarkSize"][index]

            
                
            dX =  - m.sqrt(0.5)*e2
            dY =  + m.sqrt(0.5)*e2

            d2X = m.sqrt(0.5)*e1 - m.sqrt(0.5)*e2
            d2Y = m.sqrt(0.5)*e1 + m.sqrt(0.5)*e2

            drawing.add(dxf.line((cX-d2X,cY-d2Y),(cX-dX,cY-dY)))
            
            if "rulerNums" in details["complexity"] and index == 0:
                
                drawing.add(dxf.text(str(int(e2)),
                                     height=0.9*(details["rulerClearance"]-e1),
                                     rotation = 135,
                                     halign = CENTER,
                                     alignpoint =(cX-d2X,cY-d2Y)))
                
            dX =  + m.sqrt(0.5)*e2
            dY =  - m.sqrt(0.5)*e2

            d2X = m.sqrt(0.5)*e1 + m.sqrt(0.5)*e2
            d2Y = m.sqrt(0.5)*e1 - m.sqrt(0.5)*e2

            drawing.add(dxf.line((cX-d2X,cY-d2Y),(cX-dX,cY-dY)))
            
            if "rulerNums" in details["complexity"] and index == 0:
                
                drawing.add(dxf.text(str(int(e2)),
                                     height=0.9*(details["rulerClearance"]-e1),
                                     rotation = 135,
                                     halign = CENTER,
                                     alignpoint =(cX-d2X,cY-d2Y)))
            e2 += gap
            count += 1
        
    
        
            
        
def rad(deg):
    return (deg/180.0) * m.pi

def drawRectangle(drawing,topLeft,w,h):

    dX,dY = topLeft
    

    drawing.add(dxf.line((dX,dY),(dX + w,dY)))
    drawing.add(dxf.line((dX,dY),(dX,dY + h)))
    drawing.add(dxf.line((dX + w,dY),(dX + w,dY + h)))
    drawing.add(dxf.line((dX,dY + h),(dX + w,dY + h)))

    

def drawBox(drawing, topLeft, size = 0.5):
    

    dX,dY = topLeft
    

    drawing.add(dxf.line((dX,dY),(dX + size,dY)))
    drawing.add(dxf.line((dX,dY),(dX,dY + size)))
    drawing.add(dxf.line((dX + size,dY),(dX + size,dY + size)))
    drawing.add(dxf.line((dX,dY + size),(dX + size,dY + size)))


def drawBoxGrid(drawing,topLeft, n = 6, boxSize = 0.5,gapSize = 0.5):
    dX,dY = topLeft

    for i in range(n):
        drawing.add(dxf.line((dX-gapSize,dY+i*(boxSize+gapSize)),(dX+gapSize,dY+i*(boxSize+gapSize))))
        
        for j in range(n):
            drawBox(drawing,(dX+i*(boxSize+gapSize),dY+j*(boxSize+gapSize)),boxSize)
        

        
    drawing.add(dxf.line((dX,dY-gapSize),(dX,dY+boxSize*(n-1) +gapSize*n)))

def dashWrite(drawing,topLeft,fontHeight,text):
    drawing.add(dxf.line((topLeft),(topLeft[0]+1,topLeft[1])))
    drawing.add(dxf.text(text,insert=(topLeft[0]+1.1,topLeft[1]),height = fontHeight))
    
                


def drawSlotTestH(drawing,topLeft,maximum,minimum,step,gap,slotWidth,fullWidth):

    dX,dY = topLeft

    n = int(round((maximum-minimum)/step)) + 1

    if (slotWidth + (4* gap) > fullWidth):
        complain("full width not big enough")
        
    dX = dX + 2 * gap
    dY = dY + 2 * gap
    for i in range(n):
        h = minimum + i*step
        drawRectangle(drawing,(dX,dY),slotWidth,h)
        drawing.add(dxf.text(str(h),insert = (dX + slotWidth + gap, dY),height = h))
        dY = dY + gap + h

    drawRectangle(drawing,topLeft,fullWidth,dY-topLeft[1])

def drawSlotTestW(drawing,topLeft,maximum,minimum,step,gap,slotHeight,fullWidth):

    dX,dY = topLeft

    n = int(round((maximum-minimum)/step)) + 1

    if (maximum + (4* gap) > fullWidth):
        complain("full width not big enough")
        
    dX = dX + 2 * gap
    dY = dY + 2 * gap
    for i in range(n):
        h = slotHeight
        drawRectangle(drawing,(dX,dY),minimum+i*step,h)
        drawing.add(dxf.text(str(minimum+i*step),insert = (dX + maximum + gap, dY),height = h))
        dY = dY + gap + h

    drawRectangle(drawing,topLeft,fullWidth,dY-topLeft[1])


def drawSlotCube(drawing,topLeft,baseSideLength,slotDepth=0,numSlots=0,cornerdepth=0):
    oX,oY = topLeft
    L = baseSideLength

    squarePositions =[
        (1,0),
        (1,1),
        (0,2),
        (1,2),
        (2,2),
        (1,3)]

    linesDict = {}

    for square in squarePositions:
        dX = oX + square[0]*L
        dY = oY + square[1]*L

        for side in [((0,0),(0,L)),((0,0),(L,0)),((L,L),(0,L)),((L,L),(L,0))]:
            line = ((dX + side[0][0], dY + side[0][1]),(dX + side[1][0], dY + side[1][1]))
            
            if line not in linesDict:
                linesDict[line] = "Single"
            else:
                linesDict[line] = "Double"

    for line in linesDict:
        if linesDict[line] == "Single":
            print line
            drawing.add(dxf.line(line[0],line[1]))
            
if AUTO_RUN:
    run()
