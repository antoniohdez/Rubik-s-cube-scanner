import subprocess
from rubik import Rubik
def standar_colors(color):
    return {
        'R':'U',
        'W':'F',
        'Y':'B',
        'O':'D',
        'B':'L',
        'G':'R'
    }[color]

def rubik_to_args(rubik, command):
    out = [ command,
        standar_colors(rubik.faces['U'][0][1]) + standar_colors(rubik.faces['F'][2][1]), #UF
        standar_colors(rubik.faces['U'][1][2]) + standar_colors(rubik.faces['R'][1][2]), #UR
        standar_colors(rubik.faces['U'][2][1]) + standar_colors(rubik.faces['B'][0][1]), #UB
        standar_colors(rubik.faces['U'][1][0]) + standar_colors(rubik.faces['L'][1][0]), #UL
        standar_colors(rubik.faces['D'][2][1]) + standar_colors(rubik.faces['F'][0][1]), #DF
        standar_colors(rubik.faces['D'][1][2]) + standar_colors(rubik.faces['R'][1][0]), #DR
        standar_colors(rubik.faces['D'][0][1]) + standar_colors(rubik.faces['B'][2][1]), #DB
        standar_colors(rubik.faces['D'][1][0]) + standar_colors(rubik.faces['L'][1][2]), #DL
        standar_colors(rubik.faces['F'][1][2]) + standar_colors(rubik.faces['R'][2][1]), #FR
        standar_colors(rubik.faces['F'][1][0]) + standar_colors(rubik.faces['L'][2][1]), #FL
        standar_colors(rubik.faces['B'][1][2]) + standar_colors(rubik.faces['R'][0][1]), #BR
        standar_colors(rubik.faces['B'][1][0]) + standar_colors(rubik.faces['L'][0][1]), #BL
        standar_colors(rubik.faces['U'][0][2]) + standar_colors(rubik.faces['F'][2][2]) + standar_colors(rubik.faces['R'][2][2]), #UFR
        standar_colors(rubik.faces['U'][2][2]) + standar_colors(rubik.faces['R'][0][2]) + standar_colors(rubik.faces['B'][0][2]), #URB
        standar_colors(rubik.faces['U'][2][0]) + standar_colors(rubik.faces['B'][0][0]) + standar_colors(rubik.faces['L'][0][0]), #UBL
        standar_colors(rubik.faces['U'][0][0]) + standar_colors(rubik.faces['L'][2][0]) + standar_colors(rubik.faces['F'][2][0]), #ULF
        standar_colors(rubik.faces['D'][2][2]) + standar_colors(rubik.faces['R'][2][0]) + standar_colors(rubik.faces['F'][0][2]), #DRF
        standar_colors(rubik.faces['D'][2][0]) + standar_colors(rubik.faces['F'][0][0]) + standar_colors(rubik.faces['L'][2][2]), #DFL
        standar_colors(rubik.faces['D'][0][0]) + standar_colors(rubik.faces['L'][0][2]) + standar_colors(rubik.faces['B'][2][0]), #DLB
        standar_colors(rubik.faces['D'][0][2]) + standar_colors(rubik.faces['B'][2][2]) + standar_colors(rubik.faces['R'][0][0])  #DBR
    ]
    #print out
    #print "                    UF    UR    UB    UL    DF    DR    DB    DL    FR    FL    BR    BL    UFR    URB    UBL    ULF    DRF    DFL    DLB    DBR"
    return out

def solve(rubik):
    return subprocess.Popen(rubik_to_args(rubik, "bin/Solver.bin"), stdout=subprocess.PIPE).communicate()[0].split()


#input_arg = "UF/ UR/ UB/ UL/ DF/ DR/ DB/ DL/ FR/ FL/ BR/ BL/ UFR/ URB/ UBL/ ULF/ DRF/ DFL/ DLB/ DBR";
if __name__ == '__main__':
    rubik = Rubik()
    rubik.scramble()
    rubik.describe()
    print solve(rubik)
