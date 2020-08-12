# -*- coding: utf-8 -*-
"""

This code is developed by Muhammad Abrar.
Horizontal-Sliced Permuted Partition (H-SPP) Anatomy based Algorithm
Command Line Usage : python HSPP_Anatomy.py Dataset[a|i] Attributes[7|14] Partitions{p} L-Diversity[L]   
Example usage: python Hspp_Anatomy.py a 7 50 10"

Dataset = INFORMS | Adults
No of Attributes = 7 | 14
partitions= Number of L-Diverse Tables


"""

import random
import pandas as pd
import numpy as np
import time
from utils.read_informs_data_2 import read_data as read_informs
from utils.read_data_2 import read_data
from utils.read_data import read_data as read_data_7
from utils.read_informs_data import read_data as read_informs_7
import sys





"the code you want to test stays here"
                     # Reading the dataset

def preproccess_Informs():
    label=['PID','DOBMM','DOBYY','SEX','RACEX','RACEAX','RACEBX', 'RACEWX', 'RACETHNX', 'HISPANX', 'HISPCAT','EDUCYEAR','marry','SAFP']
    cvslabel=['PID','DOBMM','DOBYY','SEX','RACEX','RACEAX','RACEBX', 'RACEWX', 'RACETHNX', 'HISPANX', 'HISPCAT','EDUCYEAR','marry']
    DATA=()
    DATA = read_informs()
                           #""" STEP 1 : MERGING DATASET """
    dataset=pd.DataFrame((DATA[0:58568]),columns=['PID','DOBMM','DOBYY','SEX','RACEX','RACEAX','RACEBX', 'RACEWX','RACETHNX', 'HISPANX', 'HISPCAT','EDUCYEAR','marry','SAFP','Conditional'])    
    newdata =dataset.drop(dataset.columns[-1] ,axis=1,inplace=False)

    cvs_data=newdata.copy();
    cvs_data.reset_index(inplace=True)
    cvs_data.drop(cvslabel,axis=1,inplace=True)
    
    newdata.drop(['SAFP'],axis=1,inplace=True)
    newdata.reset_index(inplace=True);
    newdata.rename({'index': 'UID'}, axis=1, inplace=True);

    return newdata , cvs_data

def preprocess_adults():
    I_Label=['age', 'workcalss', 'final_weight', 'education', 'education_num', 'matrital_status','relationship', 'race','sex','capital_gain', 'capital_loss','hours_per_week','native_country','SA']
    label=['age', 'workcalss', 'final_weight', 'education', 'education_num', 'matrital_status', 'relationship', 'race','sex','capital_gain', 'capital_loss','hours_per_week','native_country','SAFP']
    cvslabel=['age', 'workcalss', 'final_weight', 'education', 'education_num', 'matrital_status', 'relationship', 'race','sex','capital_gain', 'capital_loss','hours_per_week','native_country']
    DATA=()
    DATA = read_data()
   
    dataset=pd.DataFrame((DATA[0:40000]),columns=I_Label)
    dataset['SAFP'] = dataset.groupby(['age', 'workcalss', 'final_weight', 'education', 'education_num', 'matrital_status','relationship', 'race','sex','capital_gain', 'capital_loss','hours_per_week','native_country'])['SA'].transform('sum')
    cvs_data=dataset.copy();
    cvs_data.drop_duplicates(subset=cvslabel,inplace=True)
    cvs_data.reset_index(inplace=True)
    cvs_data.drop(cvslabel,axis=1,inplace=True)
    
    newdata= dataset.drop_duplicates(subset=['age', 'workcalss', 'final_weight', 'education', 'education_num', 'matrital_status','relationship', 'race','sex','capital_gain', 'capital_loss','hours_per_week','native_country'])
    newdata.drop(['SA'],axis=1,inplace=True)
    
    newdata.drop(['SAFP'],axis=1,inplace=True)
    newdata.reset_index(inplace=True);
    newdata.rename({'index': 'UID'}, axis=1, inplace=True);    
    return newdata,cvs_data

""" STEP 2 :  do partition such that there are L distinct SAFPs in each partiton.
                        Inputs p => partition , L=> L diversity  nunique() """
                        
                        
def preprocess_adults_7():
    I_Label=['age','workclass','education','matrital_status','race','sex','native_country','SA']
    label=['age','workclass','education','matrital_status','race','sex','native_country','SAFP']
    cvslabel=['age','workclass','education','matrital_status','race','sex','native_country']
    DATA=()
    DATA = read_data_7()
  
    dataset=pd.DataFrame((DATA[0:40000]),columns=I_Label)
    dataset['SAFP'] = dataset.groupby(['age','workclass','education','matrital_status','race','sex','native_country'])['SA'].transform('sum')
    cvs_data=dataset.copy();
    cvs_data.drop_duplicates(subset=cvslabel,inplace=True)
    cvs_data.reset_index(inplace=True)
    cvs_data.drop(cvslabel,axis=1,inplace=True)
    
    
    newdata= dataset.drop_duplicates(subset=['age','workclass','education','matrital_status','race','sex','native_country'])
    newdata.drop(['SA'],axis=1,inplace=True)
    
    newdata.drop(['SAFP'],axis=1,inplace=True)
    newdata.reset_index(inplace=True);
    newdata.rename({'index': 'UID'}, axis=1, inplace=True);  
    return newdata,cvs_data


def preprocess_Informs_7():
    
    DATA=()
    DATA = read_informs_7()
    
                                #""" STEP 1 : MERGING DATASET """
    label=['DOBMM','DOBYY','RACEX','EDUCYEAR','marry','SAFP']
    cvslabel=['DOBMM','DOBYY','RACEX','EDUCYEAR','marry']
    dataset=pd.DataFrame((DATA[0:58568]),columns=['DOBMM','DOBYY','RACEX','EDUCYEAR','marry','SAFP','Conditional'])

    newdata =dataset.drop(dataset.columns[-1] ,axis=1,inplace=False)
    
    cvs_data=newdata.copy();
    cvs_data.reset_index(inplace=True)
    cvs_data.drop(cvslabel,axis=1,inplace=True)
    
    newdata.drop(['SAFP'],axis=1,inplace=True)
    newdata.reset_index(inplace=True);
    newdata.rename({'index': 'UID'}, axis=1, inplace=True);
    
    return newdata,cvs_data

def sp_anatomy(data,p,L):
    
    newdata=data
    z=1;
    size = int((len(newdata))/p)

    list_of_dfs = [newdata.loc[i:i+size-1,:] for i in range(0, len(newdata),size)]  #PARTITIONS list containing all the dataframes/partitions

    print(newdata.shape[1])
    print(size)
    length=len(list_of_dfs)
    alldata=pd.DataFrame();
    Qpt=pd.DataFrame()
    a=list_of_dfs
    guid=0;
    start_row1=0;
    start_row2=0;
    start_row3=0;
    start_row4=0;
#L IT=pd.DataFrame((DATA[0:length]),columns=['UID','GUID'])
     
    
    lit= [];
#""" STEP 3 QA Permuted Partitions for key, value in dict.iteritems():
#    temp = [key,value]
#    dictlist.append(temp)"""

#    writer = pd.ExcelWriter('SP_Anatomy.xlsx', engine='xlsxwriter')
    writer = pd.ExcelWriter('MST_TAble.xlsx', engine='xlsxwriter')
    for i in range(length): 
    
        df=pd.DataFrame.from_records(list_of_dfs[i])
    
    #df['SAFP'] = np.roll(df['SAFP'], random.randint(0,df['SAFP'].nunique())) #permuting Sensitive Attribute Randomly (Not mentioned in the algorithm)

    #if df['SAFP'].nunique() > L:   #Checking L-Diversity in each partition
        #print(df['SAFP'].nunique())
        rand=random.randint(0,(df.shape[1]-1))   # randomly selecting Quassi Identifier in the dataset        
        df.iloc[:,rand]= np.random.permutation(df.iloc[:,rand]) #iloc to index dataframe with integer , randomly permuting the selected quassi identifier
    
        df.reset_index(inplace=True);

        df.rename({'index': 'Guid'}, axis=1, inplace=True);
        df['Guid']=guid;
        guid=guid+1;
    
        FL=random.randint(0,(len(df)-1))
        SL=random.randint(0,(len(df)-1))
        if FL==SL :
            SL=random.randint(0,(len(df)))
            print("SL",(SL))
            print("FL",(FL))
                                                         #   Splitting into two separate Tables
        lit=df.iloc[FL,0:2]
        lit=lit.reset_index()
        lit.columns = ['','First Leader']
    
        lit1=df.iloc[SL,0:2]
        lit1=lit1.reset_index()
        lit1.columns = ['','Second Leader']
    #litt=pd.DataFrame.from_records(lit)          
   
    #Qpt = df.drop(df.columns[0:-1] ,axis=1,inplace=False)       # Drop all columns of df except SAFP and store that SAFP column in QPT 
        
    #Qpt['count'] = Qpt.groupby(['SAFP'])['SAFP'].transform('count')     # Add another column of count that counts    
        
    #df.drop(df.columns[-1],axis=1,inplace=True)
        
        
       
        df.to_excel(writer,sheet_name=('Validation Table'), index=False , startrow=start_row1)
        
        start_row1 = start_row1 + len(df) + 20;
        alldata=alldata.append(df,True);
        df.drop(df.columns[0],axis=1,inplace=True)
    
    
   
        df.to_excel(writer,sheet_name=('MST'), index=False , startrow=start_row2)  #, startcol=df.shape[1]+3)
        
        start_row2 = start_row2 + len(df) + 20;
        columns=['firstleader',2];
        lit.to_excel(writer,sheet_name=('LIT'), index=False ,header=True, startrow=start_row3) 
        start_row3 = start_row3 + 4;
        columns=['secondleader',2];
        lit1.to_excel(writer,sheet_name=('LIT'), index=False ,header=True, startrow=start_row4, startcol=lit.shape[1]+10) 
        start_row4 = start_row4 + 4;       
    writer.save()
    writer = pd.ExcelWriter('Alldata.xlsx', engine='xlsxwriter')
    alldata.to_excel(writer,sheet_name=('Alldata'), index=False , startrow=0)
    writer.save()
    return alldata,length,size

def cvs(cvs_data,alldata,length,size,csii):
    fl=pd.DataFrame();
    start_row1=0;
    start_row2=0;
    start_row3=0;
    start_row4=0;
    start_row5=0;
    fl=alldata
    
    csi=pd.DataFrame();
    sl=pd.DataFrame();
    a=pd.DataFrame();
    writer = pd.ExcelWriter('SLandFL_Datasets.xlsx', engine='xlsxwriter')    
    dataset=cvs_data;
    
    fl['SAFP']=dataset['SAFP']
    for i in range(csii): 
        csi[i]=np.random.permutation(dataset.SAFP)
        if i > 0 :
            csi[0]=csi[0].str.cat(csi[[i]],sep=',')           # make i number of columns containing permuted SA values from data frame (dataset)
            csi.drop([i],axis=1,inplace=True)  #concatinate each column in 0 and delete other columns
 
    fl['SAFP']=fl['SAFP'].str.cat(csi[[0]],sep=',') 
     
    sl['UID']=fl['UID']
    sl['CSI']=csi;


    list_of_dfs_fl = [fl.loc[i:i+size-1,:] for i in range(0, len(fl),size)]
    list_of_dfs_sl = [sl.loc[i:i+size-1,:] for i in range(0, len(sl),size)]
    for i in range(length): 
    
        dfl=pd.DataFrame.from_records(list_of_dfs_fl[i])
        dsl=pd.DataFrame.from_records(list_of_dfs_sl[i])

        dsa=dfl['SAFP'].str.split(pat = ",",n=1,expand=True)
    
        dfl.to_excel(writer,sheet_name=('FL_Daset'), index=False , startrow=start_row1)
        start_row1 = start_row1 + len(dfl) + 50;
        dsl.to_excel(writer,sheet_name=('SL_dataset'), index=False , startrow=start_row2)
        start_row2 = start_row2 + len(dsl) + 50;
    
        #dfl['SAFP']=dsa[0]
        spt = dsa.drop(dsa.columns[-1] ,axis=1,inplace=False)
        #lit=df.iloc[FL,0:2]
        #spt=spt.reset_index()
        dfl.drop(dfl.columns[-1],axis=1,inplace=True)
        spt.columns = ['SA']
        #spt.groupby('SA').count()
        spt['Count'] = spt.groupby('SA')['SA'].transform('count')
        #spt['Unique']=spt['SA'].unique()
        spt.drop_duplicates(subset=['SA'],inplace=True)

        #spt=spt.groupby('Unique')['SA'].apply(','.join).reset_index();
   

    
    
  
#    a['value']=a.unique.nunique()
    
   #spt.groupby(['Unique'], as_index = False).agg({'SA': ','.join})
    
        dfl.to_excel(writer,sheet_name=('Final_dataset'), index=False , startrow=start_row3) #,startcol=dfl.shape[1]+3)
        start_row3 = start_row3 + len(dfl) + 50;
    
        spt.to_excel(writer,sheet_name=('Final_dataset'), index=False , startrow=start_row4 , startcol=dfl.shape[1]+5) #,startcol=dfl.shape[1]+3)
        start_row4 = start_row4 + len(dfl) + 50;
  # a.to_excel(writer,sheet_name=('SPT'), index=False , startrow=start_row5) #,startcol=dfl.shape[1]+3)
  #  start_row5 = start_row5 + len(dfl) + 50;
    writer.save()

        
       
        
if __name__ == '__main__':
    
    LEN_ARGV = len(sys.argv)
    try:
        Data=   (sys.argv[1])
        Att=    int(sys.argv[2])
        p =     int(sys.argv[3])
        csii =   int(sys.argv[4])
    except IndexError:
       print("Command Line Usage : python HSPP.py Dataset[a|i] Attributes[7|14] Partitions{p} Counterfeit_Sensitive_Values [CSI]   Example usage: python Hspp.py a 7 50 2")
    if Data=='a':
        if Att==7:
            print("7 Attributes | Adults Dataset")
            [newdata,cvs_data]=preprocess_adults_7()
        else:
            print("14 Attributes | Adults Dataset")
            [newdata,cvs_data]=preprocess_adults()
            
    else:
        if Att==7:
            print("7 Attributes | Informs Dataset")
            [newdata,cvs_data]=preprocess_Informs_7()
        else:
            print("14 Attributes | Informs Dataset")
            [newdata,cvs_data]=preproccess_Informs()
    
        
    start = time.time()   
    [alldata,length,size]=sp_anatomy(newdata,p,L);
    cvs(cvs_data,alldata,length,size,csii)
    end = time.time()
    print("Total Execution Time", (end - start), "sec", sep=' ')
    print("output is generated in MST.xlsx file")
        