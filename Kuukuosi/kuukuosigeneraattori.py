from math import sqrt,atan2,pi,sin,log

frontcolor = "#0a0b10"
backcolor = "#1e222f"

def dist(x,y):
    return sqrt(x**2 + y**2)

def get_header(width,height):

    header = """<svg xmlns="http://www.w3.org/2000/svg" width="{0}" height="{1}" viewBox="0 0 {0} {1}">
<rect fill="{2}" width="{0}" height="{1}"/>"""

    return header.format(width,height,backcolor)

def get_footer():
    
    return "</svg>"

def get_moon(x,y,phase,scale,rotation):
    rotation *= 180/pi
    #phase: float from 0(new), to 0.5(full), to 1(new)
    phase = phase%1.0

    if phase<=0.25:
        cp = 50-phase*200
        dp = 50
        cs = 0
        ds = 1
    elif phase<=0.5:
        cp = phase*200-50
        dp = 50
        cs = 1
        ds = 1
    elif phase<=0.75:
        cp = 50
        dp = phase*200-150
        cs = 1
        ds = 1
    else:
        cp = 150-phase*200
        dp = 50
        cs = 1
        ds = 0


        #<circle cx="50" cy="50" r="50" fill="#816452"/>
    return """<g transform="translate({0},{1}) scale({6}) rotate({7},50,50)">
        <path fill="{8}"
                d="M 50,0
                A {3},50 0 0 {5} 50,100
                A {2},50 0 0 {4} 50,0"
        />
    </g>
    """.format(x,y,cp,dp,cs,ds,scale,rotation,frontcolor)

def create(filename, width, height, h_repeat, gap_size,
            angle_function, phase_function,
            skip_top_rows = 0, i_offset=0, j_offset=0):

    v_repeat = int(h_repeat*height/width)

    scale = (height/v_repeat - gap_size)/100

    dx = width/h_repeat
    dy = height/v_repeat

    with open(filename, "w") as output:
        output.write(get_header(width,height))


        for i in range(h_repeat):
            for j in range(skip_top_rows,v_repeat):
                x = i*dx + gap_size/2
                y = j*dy + gap_size/2

                angle = angle_function(i+i_offset,j+j_offset,h_repeat,v_repeat)
                phase = phase_function(i+i_offset,j+j_offset,h_repeat,v_repeat)

                output.write(get_moon(x,y,phase,scale,angle))
        output.write(get_footer())

