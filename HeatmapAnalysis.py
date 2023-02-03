import csv
import os
import numpy as np
import re

# Função para calcular a dispersão espacial
def spatial_disp(xy):
    mean_pos = np.mean(xy,axis=0)
    disp = np.sum(np.linalg.norm(xy - mean_pos,axis=1)) / len(xy)
    
    mean_disp = (mean_pos,disp)
    return(mean_disp) 

n = 86+1 # numero de testes
lst = [ [[a], []] for a in range(n)]

for i,t in enumerate(lst):
    dta_im=[]
    m=[l for l in os.listdir(os.getcwd()+"/hmap_gpos") if l.endswith('.csv') and l.find(f"p{i+1}.") != -1]
    im=[l for l in os.listdir(os.getcwd()+"/hmap_gpos") if l.endswith('.png') and l.find(f"p{i+1}.") != -1]

    for i,y in enumerate(m):
        dta_im.append((y,im[i]))   
    lst[t[0][0]][1] = dta_im

with open("dados.csv",'w') as f:
    with open("line.csv",'w') as o:
        for i,dta_im in lst:
            f.write(f"{i[0]+1},")
            print(i[0]+1)

            for dta,fimg in dta_im:
                i[0]=i[0]+1
                n=dta[dta.find("ce_")+3:re.search("_p\d",dta).start()]
                if i[0] == 6:
                    o.write(f"med_x ({n}),med_y ({n}), disp ({n}),")


                t_data = []

                data = open(os.getcwd()+f"/hmap_gpos/{dta}",encoding="utf-8")
                csv_data = csv.reader(data,delimiter=',')
                data_lines = list(csv_data)
                # remove indexes
                remove= [0,1,2,5,6,7,8]

                for line in data_lines:
                    if line[-2] == "True":
                        new_line = [float(h) for g, h in enumerate(line) if g not in remove]
                        t_data.append(new_line)
                arr=np.array(t_data)

                m_d=spatial_disp(arr) #(mean_pos,disp)
                f.write(f"{m_d[0][0]},{m_d[0][1]},{m_d[1]},")
            f.write("\n")
