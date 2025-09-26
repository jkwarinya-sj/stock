import pandas as pd

"""
file_name = 'kor_co2.xlsx'
df = pd.read_excel(file_name)


file_name1 = 'kor_di.xlsx'
df1 = pd.read_excel(file_name1)

#print(df1)


name_list = []
for name in zip(df1['종목명']):
    #print(str(name).split(',')[0].split('(')[1])
    name_list.append(str(name).split(',')[0].split('(')[1].split("'")[1])


idx_list = []
for code, name in zip(df['단축코드'],df['한글 종목약명']):
    idx = 0
    for c_name in name_list:
        if c_name == name:
            print(code, name)
            del name_list[idx]
            break
            #idx_list.append(idx)
        idx = idx+1

#print(idx_list)

#for idx in idx_list:
#    print(name_list[idx])

print(name_list)
"""

file_name = 'kor_di.xlsx'
df = pd.read_excel(file_name)

#print(df[['종목명','수익률 (%)']])

df_div = df[['종목명','수익률 (%)']]




file_name = 'kor_co2.xlsx'
df = pd.read_excel(file_name)

print(df)

code_list = []
for name in df_div['종목명']:
    #print(name)
    for code, cname in zip(df['단축코드'],df['한글 종목약명']):
        if name == cname:
            code_list.append(code)
            break

print(len(code_list))

df_div['code'] = code_list

#df_div.to_excel('di_list.xlsx')



import marcap

df = marcap.marcap_data('2024-01-01', '2024-12-31')

print(df)



