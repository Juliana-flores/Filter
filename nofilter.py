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


class DataNoFilter(object):
    def __init__(self, element='', color='b', marker='o'):
        self.element = element
        self._color = color
        absorb_path = os.path.join(
            '/content/filter/', 'data/' + element + '-absorb.txt')
        transm_path = os.path.join(
            '/content/filter/', 'data/' + element + '-transm.txt')
        print("Abrindo o arquivo:", absorb_path)
        self.absorb = pd.read_csv(absorb_path, sep=' ')
        print("Abrindo o arquivo:", transm_path)
        self.transm = pd.read_csv(transm_path, sep=' ')
        self.absorb = self.absorb[['lambda', 'r']]
        self.transm = self.transm[['lambda', 'r']]

    def transform(self):
        print("Transformando para comprimento de onda em nm")
        self.absorb['lambda'] = self.absorb['lambda'].apply(
            lambda x: (1/x)*1e7)
        self.transm['lambda'] = self.transm['lambda'].apply(
            lambda x: (1/x)*1e7)

    def applyNoFilter(self):
        d = {
            'lambda': self.transm['lambda'],
            'r_transm': self.transm['r'],
            'r_absorb': self.absorb['r'],
        }
        print(self.transm.head())
        print(self.absorb.head())
        self.df = pd.DataFrame(d)
        print(self.df.head(n=20))
        self.df['r'] = [getRzao(row.r_transm, row.r_absorb)
                        for row in self.df.itertuples()]
        self.df.drop(columns=['r_transm', 'r_absorb'], inplace=True)

    def saveData(self):
        file_path = os.path.join(
            '/content/filter/', 'out/' + self.element + '-nofilter.txt')
        self.df.fillna(value=0, inplace=True)
        self.df.to_csv(file_path, sep=' ', index=False)

    def getGraph(self):
        file_path = os.path.join(
            '/content/filter/', 'graph/' + self.element + '-nofilter.png')
        print("Criando o gráfico para o elemento: " + self.element)
        fig, ax = plt.subplots()
        ax.plot(self.df['lambda'], self.df['r'])
        ax.set_title(self.element + " reflectância")
        ax.set_xlabel('Comprimento de onda (nm)')
        ax.set_ylabel('Reflectância')
        plt.savefig(file_path)

    def normalize(self):
        min_value = self.df['r'].min()
        max_value = self.df['r'].max()
        self.df['r'] = self.df['r'].apply(
            lambda x: normalizeEquation(x, min_value, max_value))

    def run(self):
        self.transform()
        self.applyNoFilter()
        self.normalize()
        self.saveData()
        self.getGraph()


def normalizeEquation(x, min_value, max_value):
    return ((x - min_value)/(max_value - min_value))


def getRzao(A, T):

    return 1 - (A + T)


def format(tmp, ini, fim):
    tmp = tmp.mean()
    tmp['lambda'] = ((fim - ini)/2) + ini
    tmp['length'] = (fim - ini)/2
    return tmp
