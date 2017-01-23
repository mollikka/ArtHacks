from kuukuosigeneraattori import *


if __name__ == "__main__":

    def angle_function1(i,j,h_repeat,v_repeat):
        d1 = dist(i-10.5, j-18.5)
        d2 = dist(i-25.5, j-53.5)
        ang1 = atan2(j, i)
        ang2 = atan2(j-v_repeat, i-h_repeat)
        angle = (ang1*d2 + ang2*d1)/10

        return angle

    def phase_function1(i,j,h_repeat,v_repeat):
        d1 = dist(i-10.5, j-18.5)
        d2 = dist(i-25.5, j-53.5)
        ang1 = atan2(j, i)
        ang2 = atan2(j-v_repeat, i-h_repeat)
        phase = round(d1*d2/300,1,)

        return phase

    create("kuukuosi1_3840x2160_left.svg",       3840,2160,64,5,angle_function1,phase_function1,
            skip_top_rows=1, i_offset=-64)
    create("kuukuosi1_3840x2160_center.svg",       3840,2160,64,5,angle_function1,phase_function1,
            skip_top_rows=1, i_offset=0)
    create("kuukuosi1_3840x2160_right.svg",       3840,2160,64,5,angle_function1,phase_function1,
            skip_top_rows=1, i_offset=64)
    create("kuukuosi1_1366x768.svg",        1366,768, 50,2,angle_function1,phase_function1,
            skip_top_rows=1)


    def angle_function2(i,j,h_repeat,v_repeat):
        return 0

    def phase_function2(i,j,h_repeat,v_repeat):
        x,y = i/h_repeat, j/v_repeat
        return round((i/27+(0.21*j**4 + 0.47463*j**3 + 0.912*j**2 + 0.52*j + 0.1245)/12)+1, 1)

    create("kuukuosi2_1920x1080.svg",         1920,1080,32,10,angle_function2,phase_function2)
    create("kuukuosi2_1366x768.svg",  1366,768, 32, 0,angle_function2,phase_function2)


    def angle_function3(i,j,h_repeat,v_repeat):
        midx = h_repeat/2
        midy = v_repeat/2
        
        return atan2(j-midy,i-midx)

    def phase_function3(i,j,h_repeat,v_repeat):
        midx = h_repeat/2
        midy = v_repeat/2
        
        return round(log(1+dist(i-midx,j-midy)/min(h_repeat,v_repeat)),1) + 0.5 

    create("kuukuosi3_600x600.svg",         600, 600, 32,0,angle_function3,phase_function3)
    create("kuukuosi3_1366x768.svg",  1366,768, 32,-5,angle_function3,phase_function3)


    def angle_function4(i,j,h_repeat,v_repeat):
        return 0

    def phase_function4(i,j,h_repeat,v_repeat):
        return round((i/h_repeat * -j%2)*10)/10

    create("kuukuosi4_600x600.svg",         600, 600, 32,0,angle_function4,phase_function4)


    def angle_function5(i,j,h_repeat,v_repeat):
        return (i+j)*3.14159/h_repeat*4

    def phase_function5(i,j,h_repeat,v_repeat):
        return (i+0.5)/h_repeat

    create("kuukuosi5_600x600.svg",         600, 600, 32,2,angle_function5,phase_function5)


    def angle_function6(i,j,h_repeat,v_repeat):
        return 0

    def phase_function6(i,j,h_repeat,v_repeat):
        return round(sin(i/h_repeat*pi)**1.2 + sin(j/v_repeat*pi)**1.2,1)

    create("kuukuosi6_600x600.svg",         600, 600, 30,2,angle_function6,phase_function6)

