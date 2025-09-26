import pandas as pd

import sys

file_name = 'krx.csv'
krx_df = pd.read_csv(file_name)

#print(df)

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()

file_path = sys.argv[1]
out_file_name = sys.argv[2]
#print("File path : " + file_path)


mc_df = pd.read_csv(file_path)
#print(df)

name_n_code_list = []
#debug_flag = False
#debug_idx = 0
for name in mc_df['종목명']:
    #print(name)
    for code, cname in zip(krx_df['단축코드'],krx_df['한글 종목약명']):
        if name == cname:
            tmp_list = [code,name]
            name_n_code_list.append(tmp_list)
            #print(code)
            #debug_flag = True
            break

    """
    if not debug_flag:
        print(name, debug_idx)

    debug_idx = debug_idx+1
    debug_flag = False
    """ 

#print(len(name_n_code_list))

with open(out_file_name, 'w') as f:
    for item in name_n_code_list:
        f.write(str(item).split('[')[1].split(']')[0] + '\n')





#print(code_list)
#print(len(code_list))


