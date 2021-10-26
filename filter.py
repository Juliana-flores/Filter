#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Filtro para agrotóxicos

@author: diego
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import time 
from sklearn.preprocessing import StandardScaler
class Data(object):
    def __init__(self,element= '', color = 'b',marker = 'o'):
        self.element = element
        self._color = color
        absorb_path = os.path.join('/content/filter/', 'data/' + element +'-absorb.txt')
        transm_path = os.path.join('/content/filter/', 'data/' + element +'-transm.txt')
        print("Abrindo o arquivo:",absorb_path)
        self.absorb = pd.read_csv(absorb_path,sep=' ')
        print("Abrindo o arquivo:", transm_path)
        self.transm = pd.read_csv(transm_path,sep=' ')
        self.absorb = self.absorb[['lambda','r']]
        self.transm = self.transm[['lambda','r']]
        self._interval = [
            {
                'ini': 3660 ,'fim': 3840
            },
            {
                'ini': 4020 ,'fim': 4080
            },
            {
                'ini': 6535 ,'fim': 6895
            },
            {
                'ini': 8400 ,'fim': 8700
            },
            {
                'ini': 9580,'fim': 9880
            },
            {
                'ini': 11770 ,'fim': 12270
            }
        ]
    def transform(self):
        print("Transformando para comprimento de onda em nm")
        self.absorb['lambda'] = self.absorb['lambda'].apply(lambda x: (1/x)*1e7)
        self.transm['lambda'] = self.transm['lambda'].apply(lambda x: (1/x)*1e7)

            
    def applyFilter(self):
        absorb = []
        transm = []
        df = []
        print("Realizando o filtro para separar nas bandas necessárias")
        for i in range(0,len(self._interval)):
            absorb.append( self.absorb.loc[(self.absorb['lambda'] >= self._interval[i]['ini']) & (self.absorb['lambda']<= self._interval[i]['fim'])])
            transm.append( self.transm.loc[(self.transm['lambda'] >= self._interval[i]['ini']) & (self.transm['lambda']<= self._interval[i]['fim'])])
            absorb[i] = format(absorb[i],self._interval[i]['ini'],self._interval[i]['fim'])
            transm[i] = format(transm[i],self._interval[i]['ini'],self._interval[i]['fim']) 
            df.append(absorb[i])
            print("Calculando a reflectância para a banda: " +  str(self._interval[i]['ini']))
            df[i]['r'] = getRzao(absorb[i]['r'],transm[i]['r'])
        self.df = pd.DataFrame(df)
    def saveData(self):
        file_path = os.path.join('/content/filter/', 'out/' + self.element +'.txt')
        print('Save data with filter', file_path)
        self.df.fillna(value=0,inplace= True)
        self.df.to_csv(file_path,sep=' ',index=False)
    def getGraph(self):
        file_path = os.path.join('/content/filter/', 'graph/' + self.element + '.png')
        print("Criando o gráfico para o elemento: " + self.element, file_path)
        fig, ax = plt.subplots()
        ax.plot(self.df['lambda'],self.df['r'])
        ax.set_title(self.element + " reflectância")
        ax.set_xlabel('Comprimento de onda (nm)')
        ax.set_ylabel('Reflectância')
        plt.savefig(file_path)

    def normalize(self):
        #min_value = self.absorb['r'].min()
        #max_value = self.absorb['r'].max()
        #self.absorb['r'] = self.absorb['r'].apply(lambda x: normalizeEquation(x,min_value,max_value))
        #min_value = self.transm['r'].min()
        #max_value = self.transm['r'].max()
        #self.transm['r'] = self.transm['r'].apply(lambda x: normalizeEquation(x,min_value,max_value))
        #print(self.absorb)
        min_value = self.df['r'].min()
        max_value = self.df['r'].max()
        self.df['r'] = self.df['r'].apply(lambda x: normalizeEquation(x,min_value,max_value))

    def run(self):
        self.transform()
        self.applyFilter()
        self.normalize()
        self.saveData()
        self.getGraph()
        
def getRzao(A, T):
  
        return 1 - (A + T)

def normalizeEquation(x,min_value,max_value):
    return ((x - min_value)/(max_value - min_value))
    
def format(tmp, ini, fim):
    tmp = tmp.mean()
    tmp['lambda'] = ((fim - ini)/2) + ini
    tmp['length'] = (fim - ini)/2
    return tmp