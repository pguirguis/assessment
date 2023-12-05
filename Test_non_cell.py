# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 16:39:59 2023

@author: peter
"""
import math
import numpy as np
from scipy.integrate import solve_ivp
import matlab.engine
# from scipy import stats
# from scipy.optimize import curve_fit
import pandas as pd





algae_data = pd.read_excel(r'Data_main.xlsx', "Algae", engine= 'openpyxl', header= 1)

biomass_data = pd.read_excel(r'Data_main.xlsx', "Biomass", engine= 'openpyxl', header= 1)

outliers = pd.ExcelWriter('Outliers.xlsx')

def is_lnsi(t,temp,t0,temp0):
    
    lnSI_lim = 0.52
    
    lnsi = np.log(t*np.exp(-21000/8.314*(1/(temp+273.15)-1/(700))))

    lnsi0 = np.log(t0*np.exp(-21000/8.314*(1/(temp0+273.15)-1/(700))))

    lnsi_up =  lnsi0 + lnSI_lim
    
    lnsi_down =  lnsi0 -lnSI_lim

    return lnsi_down < lnsi < lnsi_up

def decimalToBinary(n):
    if n == 1:
        num = [1]
    else:
        num = bin(n).replace("0b", "")
        num = [eval(i) for i in str(num)]
    return num

class model:
    def __int__(self, name):
        self.name = name
    def set_fun_str(self,nam_str):  
        self.fun_str = str(nam_str)
    def set_fun_name(self,fun):
        self.fun = fun
        self.poss_ins = []
        self.res = []
        self.rel_res = []
        self.res_biomass = []
        self.rel_res_biomass = []
        self.res_algae = []
        self.rel_res_algae = []
        self.res_intended = []
        self.rel_res_intended = []
        self.mean_res = []
        self.mean_res_algae = []
        self.mean_res_biomass = []
        self.mean_res_intended = []
        self.std_res = []
        self.std_res_algae = []
        self.std_res_biomass = []
        self.std_res_intended = []
        self.ave_res = []
        self.ave_res_algae = []
        self.ave_res_biomass = []
        self.ave_res_intended = []
        self.mape = []
        self.mape_algae = []
        self.mape_biomass = []
        self.mape_intended = []
        self.med_res = []
        self.med_res_algae = []
        self.med_res_biomass = []
        self.med_res_intended = []
        self.med_rel = []
        self.med_rel_algae = []
        self.med_rel_biomass = []
        self.med_rel_intended = []
        self.BIC = []
        self.BIC_algae = []
        self.BIC_biomass = []
        self.BIC_intended = []
        self.AIC = []
        self.AIC_algae = []
        self.AIC_biomass = []
        self.AIC_intended = []
        self.n_points = []
        self.n_points_algae = []
        self.n_points_biomass = []
        self.n_points_intended = []
        self.num_5 = []
        self.num_5_algae = []
        self.num_5_biomass = []
        self.num_5_intended = []
        self.num_10 = []
        self.num_10_algae = []
        self.num_10_biomass = []
        self.num_10_intended = []
        self.num_75 = []
        self.num_75_algae = []
        self.num_75_biomass = []
        self.num_75_intended = []
        self.num_100_rel = []
        self.num_100_rel_algae = []
        self.num_100_rel_biomass = []
        self.num_100_rel_intended = []
    def set_nk(self,nk):
        self.nk = nk
    def set_biomass(self,biomass):
        self.biomass = biomass
    def set_require_input(self,inputs):
        self.require_input = inputs
    def set_require_one(self,inputs):
        self.require_one = inputs
    def set_optional(self,inputs):
        self.optional = inputs
        self.possiblity = len(inputs)
        if self.possiblity == 0:
            num = []
            self.mean_res_biomass.insert(0, [num])
            self.std_res_biomass.insert(0, [num])
            self.res_biomass.insert(0, [num])
            self.rel_res_biomass.insert(0, [num])
            self.poss_ins.insert(0,[num])
            self.ave_res_biomass.insert(0, [num])
            self.mape_biomass.insert(0, [num])
            self.med_res_biomass.insert(0, [num])
            self.med_rel_biomass.insert(0, [num])
            self.BIC_biomass.insert(0, [num])
            self.AIC_biomass.insert(0, [num])
            self.n_points_biomass.insert(0, [num])
            self.num_5_biomass.insert(0, [num])
            self.num_10_biomass.insert(0, [num])
            self.num_75_biomass.insert(0, [num])
            self.num_100_rel_biomass.insert(0, [num])
        else:
            num = []
            self.mean_res_biomass.insert(0, [num])
            self.std_res_biomass.insert(0, [num])
            self.res_biomass.insert(0, [num])
            self.rel_res_biomass.insert(0, [num])
            self.ave_res_biomass.insert(0, [num])
            self.poss_ins.insert(0,[num])
            self.mape_biomass.insert(0, [num])
            self.med_res_biomass.insert(0, [num])
            self.med_rel_biomass.insert(0, [num])
            self.BIC_biomass.insert(0, [num])
            self.AIC_biomass.insert(0, [num])
            self.n_points_biomass.insert(0, [num])
            self.num_5_biomass.insert(0, [num])
            self.num_10_biomass.insert(0, [num])
            self.num_75_biomass.insert(0, [num])
            self.num_100_rel_biomass.insert(0, [num])
            for i in range(1,2**self.possiblity):
                num = decimalToBinary(i)
                if not len(num) == len(inputs):
                    for k in range(len(inputs)-len(num)):
                        num.insert(0,0)
                self.mean_res_biomass.insert(0, [num])
                self.std_res_biomass.insert(0, [num])
                self.res_biomass.insert(0, [num])
                self.rel_res_biomass.insert(0, [num])
                self.poss_ins.insert(0,[num])
                self.ave_res_biomass.insert(0, [num])
                self.mape_biomass.insert(0, [num])
                self.med_res_biomass.insert(0, [num])
                self.med_rel_biomass.insert(0, [num])
                self.BIC_biomass.insert(0, [num])
                self.AIC_biomass.insert(0, [num])
                self.n_points_biomass.insert(0, [num])
                self.num_5_biomass.insert(0, [num])
                self.num_10_biomass.insert(0, [num])
                self.num_75_biomass.insert(0, [num])
                self.num_100_rel_biomass.insert(0, [num])
        for i in self.biomass:
            self.mean_res_biomass.insert(0, [i])
            self.std_res_biomass.insert(0, [i])
            self.res_biomass.insert(0, [i])
            self.rel_res_biomass.insert(0, [i])
            # self.poss_ins.insert(0,[i])
            self.ave_res_biomass.insert(0, [i])
            self.mape_biomass.insert(0, [i])
            self.med_res_biomass.insert(0, [i])
            self.med_rel_biomass.insert(0, [i])
            self.BIC_biomass.insert(0, [i])
            self.AIC_biomass.insert(0, [i])
            self.n_points_biomass.insert(0, [i])
            self.num_5_biomass.insert(0, [i])
            self.num_10_biomass.insert(0, [i])
            self.num_75_biomass.insert(0, [i])
            self.num_100_rel_biomass.insert(0, [i])
    def set_if_avail(self,inputs):
        self.if_avail = inputs
    def set_outputs(self,outputs):
        self.outputs = outputs
        self.res_algae = []
        self.rel_res_algae = []
    def add_res_algae(self,res):
        self.res_algae.insert(0, res)
        self.res.insert(0, res)
    def add_rel_res_algae(self,rel_res):
        self.rel_res_algae.insert(0, rel_res)
        self.rel_res.insert(0, rel_res)
    def add_res_intended(self,res):
        self.res_intended.insert(0, res)
    def add_rel_res_intended(self,rel_res):
        self.rel_res_intended.insert(0, rel_res)
    def add_res_biomass(self,res,poss):
        for r in self.res_biomass:
            if poss[-1] == r[-1] or r[-1] == []:
                r.insert(0, res)
        self.res.insert(0, res)
    def add_rel_res_biomass(self,rel_res,poss):
        for r in self.rel_res_biomass:
            if poss[-1] == r[-1] or r[-1] == []:
                r.insert(0, rel_res)
        self.rel_res.insert(0, rel_res)
    def cal_analysis(self):
        tot_ana = analysis(self.res, self.rel_res, self.nk,len(self.outputs))
        self.mean_res = tot_ana[0]
        self.std_res = tot_ana[1]
        self.ave_res = tot_ana[2]
        self.med_res = tot_ana[3]
        self.mape = tot_ana[4]
        self.med_rel = tot_ana[5]
        self.BIC = tot_ana[6]
        self.AIC = tot_ana[7]
        self.n_points = tot_ana[8]
        self.num_5 = tot_ana[9]
        self.num_10 = tot_ana[10]
        self.num_75 = tot_ana[11]
        self.num_100_rel = tot_ana[12]
        algae_ana = analysis(self.res_algae, self.rel_res_algae, self.nk,len(self.outputs))
        self.mean_res_algae = algae_ana[0]
        self.std_res_algae = algae_ana[1]
        self.ave_res_algae = algae_ana[2]
        self.med_res_algae = algae_ana[3]
        self.mape_algae = algae_ana[4]
        self.med_rel_algae = algae_ana[5]
        self.BIC_algae = algae_ana[6]
        self.AIC_algae = algae_ana[7]
        self.n_points_algae = algae_ana[8]
        self.num_5_algae = algae_ana[9]
        self.num_10_algae = algae_ana[10]
        self.num_75_algae = algae_ana[11]
        self.num_100_rel_algae = algae_ana[12]
        intended_ana = analysis(self.res_intended, self.rel_res_intended, self.nk,len(self.outputs))
        self.mean_res_intended = intended_ana[0]
        self.std_res_intended = intended_ana[1]
        self.ave_res_intended = intended_ana[2]
        self.med_res_intended = intended_ana[3]
        self.mape_intended = intended_ana[4]
        self.med_rel_intended = intended_ana[5]
        self.BIC_intended = intended_ana[6]
        self.AIC_intended = intended_ana[7]
        self.n_points_intended = intended_ana[8]
        self.num_5_intended = intended_ana[9]
        self.num_10_intended = intended_ana[10]
        self.num_75_intended = intended_ana[11]
        self.num_100_rel_intended = intended_ana[12]
        if self.poss_ins == [] or self.poss_ins == [[]]:
            res = self.res[:-1]
            rel_res = self.rel_res[:-1]
            biomass_ana = analysis(res, rel_res, self.nk,len(self.outputs))
            self.mean_res_biomass = [biomass_ana[0],[]]
            self.std_res_biomass = [biomass_ana[1],[]]
            self.ave_res_biomass = [biomass_ana[2],[]]
            self.med_res_biomass = [biomass_ana[3],[]]
            self.mape_biomass = [biomass_ana[4],[]]
            self.med_rel_biomass = [biomass_ana[5],[]]
            self.BIC_biomass = [biomass_ana[6],[]]
            self.AIC_biomass = [biomass_ana[7],[]]
            self.n_points_biomass = [biomass_ana[8],[]]
            self.num_5_biomass = [biomass_ana[9],[]]
            self.num_10_biomass = [biomass_ana[10],[]]
            self.num_75_biomass = [biomass_ana[11],[]]
            self.num_100_rel_biomass = [biomass_ana[12],[]]
        else:
            for p in self.poss_ins:
                if p == []:
                    for che_res in self.res_biomass:
                        if che_res == []:
                            if che_res == p[0]:
                                res = che_res
                        elif che_res[-1] == p[0]:
                            res = che_res[:-1]
                    for che_rel_res in self.rel_res_biomass:
                        if che_rel_res == []:
                            if che_rel_res == p[0]:
                                rel_res = che_rel_res
                        elif che_rel_res[-1] == p[0]:
                            rel_res = che_rel_res[:-1]
                    biomass_ana = analysis(res, rel_res, self.nk,len(self.outputs))
                    for che in self.mean_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[0])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[0])
                    for che in self.std_res_biomass:
                         if che == []:
                             if che == p[0]:
                                 che.insert(0,biomass_ana[1])
                         elif che[-1] == p[0]:
                             che.insert(0,biomass_ana[1])
                    for che in self.ave_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[2])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[2])
                    for che in self.med_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[3])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[3])
                    for che in self.mape_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[4])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[4])
                    for che in self.med_rel_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[5])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[5])
                    for che in self.BIC_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[6])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[6])
                    for che in self.AIC_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[7])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[7])
                    for che in self.n_points_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[8])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[8])
                    for che in self.num_5_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[9])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[9])
                    for che in self.num_10_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[10])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[10])
                    for che in self.num_75_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[11])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[11])
                    for che in self.num_100_rel_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[12])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[12])
                else:
                    for che_res in self.res_biomass:
                        if che_res == []:
                            if che_res == p[0]:
                                res = che_res
                        elif che_res[-1] == p[0]:
                            res = che_res[:-1]
                    for che_rel_res in self.rel_res_biomass:
                        if che_rel_res == []:
                            if che_rel_res == p[0]:
                                rel_res = che_rel_res
                        elif che_rel_res[-1] == p[0]:
                            rel_res = che_rel_res[:-1]
                    biomass_ana = analysis(res, rel_res, self.nk,len(self.outputs))
                    for che in self.mean_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[0])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[0])
                    for che in self.std_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[1])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[1])
                    for che in self.ave_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[2])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[2])
                    for che in self.med_res_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[3])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[3])
                    for che in self.mape_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[4])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[4])
                    for che in self.med_rel_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[5])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[5])
                    for che in self.BIC_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[6])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[6])
                    for che in self.AIC_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[7])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[7])
                    for che in self.n_points_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[8])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[8])
                    for che in self.num_5_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[9])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[9])
                    for che in self.num_10_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[10])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[10])
                    for che in self.num_75_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[11])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[11])
                    for che in self.num_100_rel_biomass:
                        if che == []:
                            if che == p[0]:
                                che.insert(0,biomass_ana[12])
                        elif che[-1] == p[0]:
                            che.insert(0,biomass_ana[12])
    def get_res_biomass(self,poss):
        for r in self.res_biomass:
            if poss == r[-1]:
                res = r
        return res
    def get_anal(self,type_input,ind,poss):
        ana = []
        if ind == []:
            if type_input == []:
                ana = np.append(ana,self.mean_res)
                # ana = np.append(ana,self.std_res)
                ana = np.append(ana,self.ave_res)
                ana = np.append(ana,self.med_res)
                ana = np.append(ana,self.mape)
                ana = np.append(ana,self.med_rel)
                # ana = np.append(ana,self.BIC)
                # ana = np.append(ana,self.AIC)
                ana = np.append(ana,self.n_points)
                ana = np.append(ana,self.num_5)
                ana = np.append(ana,self.num_10)
                # ana = np.append(ana,self.num_75)
                ana = np.append(ana,self.num_100_rel)
            elif type_input == 'intended':
                ana = np.append(ana,self.mean_res_intended)
                # ana = np.append(ana,self.std_res_intended)
                ana = np.append(ana,self.ave_res_intended)
                ana = np.append(ana,self.med_res_intended)
                ana = np.append(ana,self.mape_intended)
                ana = np.append(ana,self.med_rel_intended)
                # ana = np.append(ana,self.BIC_intended)
                # ana = np.append(ana,self.AIC_intended)
                ana = np.append(ana,self.n_points_intended)
                ana = np.append(ana,self.num_5_intended)
                ana = np.append(ana,self.num_10_intended)
                # ana = np.append(ana,self.num_75_intended)
                ana = np.append(ana,self.num_100_rel_intended)
            elif type_input == 'algae':
                ana = np.append(ana,self.mean_res_algae)
                # ana = np.append(ana,self.std_res_algae)
                ana = np.append(ana,self.ave_res_algae)
                ana = np.append(ana,self.med_res_algae)
                ana = np.append(ana,self.mape_algae)
                ana = np.append(ana,self.med_rel_algae)
                # ana = np.append(ana,self.BIC_algae)
                # ana = np.append(ana,self.AIC_algae)
                ana = np.append(ana,self.n_points_algae)
                ana = np.append(ana,self.num_5_algae)
                ana = np.append(ana,self.num_10_algae)
                # ana = np.append(ana,self.num_75_algae)
                ana = np.append(ana,self.num_100_rel_algae)
            elif type_input == 'biomass':
                for i in self.mean_res_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                # for i in self.std_res_biomass:
                #     if i[-1] == poss:
                #         ana = np.append(ana,i[0])
                for i in self.ave_res_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                for i in self.med_res_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                for i in self.mape_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                for i in self.med_rel_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                # for i in self.BIC_biomass:
                #     if i[-1] == poss:
                #         ana = np.append(ana,i[0])
                # for i in self.AIC_biomass:
                #     if i[-1] == poss:
                #         ana = np.append(ana,i[0])
                for i in self.n_points_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                for i in self.num_5_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                for i in self.num_10_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
                # for i in self.num_75_biomass:
                #     if i[-1] == poss:
                #         ana = np.append(ana,i[0])
                for i in self.num_100_rel_biomass:
                    if i[-1] == poss:
                        ana = np.append(ana,i[0])
        else:
            if type_input == []:
                ana = np.append(ana,self.mean_res[ind])
                # ana = np.append(ana,self.std_res[ind])
                ana = np.append(ana,self.ave_res[ind])
                ana = np.append(ana,self.med_res[ind])
                ana = np.append(ana,self.mape[ind])
                ana = np.append(ana,self.med_rel[ind])
                # ana = np.append(ana,self.BIC[ind])
                # ana = np.append(ana,self.AIC[ind])
                ana = np.append(ana,self.n_points[ind])
                ana = np.append(ana,self.num_5[ind])
                ana = np.append(ana,self.num_10[ind])
                # ana = np.append(ana,self.num_75[ind])
                ana = np.append(ana,self.num_100_rel[ind])
            elif type_input == 'intended':
                if np.size(self.ave_res_intended) == 1:
                    ana = np.append(ana,self.mean_res_intended)
                    # ana = np.append(ana,self.std_res_intended)
                    ana = np.append(ana,self.ave_res_intended)
                    ana = np.append(ana,self.med_res_intended)
                    ana = np.append(ana,self.mape_intended)
                    ana = np.append(ana,self.med_rel_intended)
                    # ana = np.append(ana,self.BIC_intended)
                    # ana = np.append(ana,self.AIC_intended)
                    ana = np.append(ana,self.n_points_intended)
                    ana = np.append(ana,self.num_5_intended)
                    ana = np.append(ana,self.num_10_intended)
                    # ana = np.append(ana,self.num_75_intended)
                    ana = np.append(ana,self.num_100_rel_intended)
                else:
                    ana = np.append(ana,self.mean_res_intended[ind])
                    # ana = np.append(ana,self.std_res_intended[ind])
                    ana = np.append(ana,self.ave_res_intended[ind])
                    ana = np.append(ana,self.med_res_intended[ind])
                    ana = np.append(ana,self.mape_intended[ind])
                    ana = np.append(ana,self.med_rel_intended[ind])
                    # ana = np.append(ana,self.BIC_intended[ind])
                    # ana = np.append(ana,self.AIC_intended[ind])
                    ana = np.append(ana,self.n_points_intended[ind])
                    ana = np.append(ana,self.num_5_intended[ind])
                    ana = np.append(ana,self.num_10_intended[ind])
                    # ana = np.append(ana,self.num_75_intended[ind])
                    ana = np.append(ana,self.num_100_rel_intended[ind])
            elif type_input == 'algae':
                if np.size(self.ave_res_algae) == 1:
                    ana = np.append(ana,self.mean_res_algae)
                    # ana = np.append(ana,self.std_res_algae)
                    ana = np.append(ana,self.ave_res_algae)
                    ana = np.append(ana,self.med_res_algae)
                    ana = np.append(ana,self.mape_algae)
                    ana = np.append(ana,self.med_rel_algae)
                    # ana = np.append(ana,self.BIC_algae)
                    # ana = np.append(ana,self.AIC_algae)
                    ana = np.append(ana,self.n_points_algae)
                    ana = np.append(ana,self.num_5_algae)
                    ana = np.append(ana,self.num_10_algae)
                    # ana = np.append(ana,self.num_75_algae)
                    ana = np.append(ana,self.num_100_rel_algae)
                else:
                    ana = np.append(ana,self.mean_res_algae[ind])
                    # ana = np.append(ana,self.std_res_algae[ind])
                    ana = np.append(ana,self.ave_res_algae[ind])
                    ana = np.append(ana,self.med_res_algae[ind])
                    ana = np.append(ana,self.mape_algae[ind])
                    ana = np.append(ana,self.med_rel_algae[ind])
                    # ana = np.append(ana,self.BIC_algae[ind])
                    # ana = np.append(ana,self.AIC_algae[ind])
                    ana = np.append(ana,self.n_points_algae[ind])
                    ana = np.append(ana,self.num_5_algae[ind])
                    ana = np.append(ana,self.num_10_algae[ind])
                    # ana = np.append(ana,self.num_75_algae[ind])
                    ana = np.append(ana,self.num_100_rel_algae[ind])
            elif type_input == 'biomass':
                if len(self.outputs) == 1:
                    for i in self.mean_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    # for i in self.std_res_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0])
                    for i in self.ave_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    for i in self.med_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    for i in self.mape_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    for i in self.med_rel_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    # for i in self.BIC_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0])
                    # for i in self.AIC_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0])
                    for i in self.n_points_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    for i in self.num_5_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    for i in self.num_10_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                    # for i in self.num_75_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0])
                    for i in self.num_100_rel_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0])
                else:
                    for i in self.mean_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    # for i in self.std_res_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0][ind])
                    for i in self.ave_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    for i in self.med_res_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    for i in self.mape_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    for i in self.med_rel_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    # for i in self.BIC_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0][ind])
                    # for i in self.AIC_biomass:
                        # if i[-1] == poss:
                        #     ana = np.append(ana,i[0][ind])
                    for i in self.n_points_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    for i in self.num_5_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    for i in self.num_10_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])
                    # for i in self.num_75_biomass:
                    #     if i[-1] == poss:
                    #         ana = np.append(ana,i[0][ind])
                    for i in self.num_100_rel_biomass:
                        if i[-1] == poss:
                            ana = np.append(ana,i[0][ind])

        return ana





def analysis(Res,rel_Res,N_ks,num_outs):
    if Res == [] :
        mean_Res = [np.NAN] * num_outs
        std_Res = [np.NAN] * num_outs
        ave_Res = [np.NAN] * num_outs
        mape = [np.NAN] * num_outs
        med_res = [np.NAN] * num_outs
        med_rel = [np.NAN] * num_outs
        BIC = [np.NAN] * num_outs
        AIC = [np.NAN] * num_outs
        n_point = [0] * num_outs
        num_5 = [np.NAN] * num_outs
        num_10 = [np.NAN] * num_outs
        num_10 = [np.NAN] * num_outs
        num_75 = [np.NAN] * num_outs
        num_100_rel = [np.NAN] * num_outs
    else:
        try:
            num_col = np.size(Res,1)+1
        except:
            num_col =1
        Res = np.array(Res)
        rel_Res = np.array(rel_Res)
        RSS = np.zeros(num_col)
        mape = np.zeros(num_col)
        med_res = np.zeros(num_col)
        med_rel = np.zeros(num_col)
        AIC = np.zeros(num_col)
        BIC = np.zeros(num_col)
        num_5 = np.zeros(num_col)
        num_10 = np.zeros(num_col)
        num_75 = np.zeros(num_col)
        num_100_rel = np.zeros(num_col)
        if num_col == 1:
            RSS_sum = sum([item*item for item in Res if str(item) != "nan"  and str(item) != "inf" and type(item) != bool ])
            res_col = [item for item in Res if str(item) != "nan"  and str(item) != "inf"  and type(item) != bool]
            abs_res_col = [abs(item) for item in res_col ]
            n_point = len(res_col)
            if n_point == 0:
                mean_Res = np.NAN
                std_Res = np.NAN
                ave_Res = np.NAN
                mape = np.NAN
                med_res = np.NAN
                med_rel = np.NAN
                AIC = np.NAN
                BIC = np.NAN
                num_5 = np.NAN
                num_10 = np.NAN
                num_75 = np.NAN
                num_100_rel = np.NAN
                n_point = np.NAN
            else:
                mean_Res = np.nanmedian(res_col)
                std_Res = np.std(res_col)
                ave_Res = np.nanmean(np.abs(Res))
                mape = np.nanmean(rel_Res)*100
                med_res = np.nanmedian(np.abs(res_col))
                med_rel = np.nanmedian(rel_Res)*100
                AIC = 2*N_ks + np.log(RSS_sum/n_point)*n_point
                BIC = N_ks*np.log(n_point) +np.log(RSS_sum/n_point)*n_point
                abs_res_col = np.reshape(abs_res_col,-1)
                num_5 = len([item for item in abs_res_col  if item <= 5])/n_point*100
                num_10 = len([item for item in abs_res_col if item <= 10])/n_point*100
                num_75 = len([item for item in abs_res_col if item >= 75])/n_point*100
                num_100_rel = len([item for item in rel_Res if item >= 1])/n_point*100
        else:
            mean_Res = np.zeros(num_col)
            std_Res = np.zeros(num_col)
            ave_Res = np.zeros(num_col)
            n_point = np.zeros(num_col)
            abs_res = np.zeros(num_col)
            RSS_sum = np.zeros(num_col)
            for q in range(num_col-1):
                res_col = [item for item in Res[:,q] if str(item) != "nan"  and str(item) != "inf" ] 
                abs_res_col =  [abs(item) for item in res_col ]
                rel_res_col = [item for item in rel_Res[:,q] if str(item) != "nan"  and str(item) != "inf" ] 
                n_point[q] = len(res_col)
                ave_Res[q] = np.nansum(abs_res_col)
                abs_res[q] = np.nansum(np.abs(rel_res_col))
                RSS_sum[q] = np.nansum(np.multiply(res_col,res_col))
                if n_point[q] == 0:
                    mean_Res[q] = np.NAN
                    std_Res[q] = np.NAN
                    ave_Res[q] = np.NAN
                    mape[q] = np.NAN
                    med_res[q] = np.NAN
                    med_rel[q] = np.NAN
                    AIC[q] = np.NAN
                    BIC[q] = np.NAN
                    num_5[q] = np.NAN
                    num_10[q] = np.NAN
                    num_75[q] = np.NAN
                    num_100_rel[q] = np.NAN
                    n_point[q] = np.NAN
                else:
                    mean_Res[q] = np.nanmedian(res_col)
                    std_Res[q] = np.std(res_col)
                    ave_Res[q] = ave_Res[q]/n_point[q]
                    mape[q] = abs_res[q]/n_point[q]*100
                    med_res[q] = np.nanmedian(np.abs(res_col))
                    med_rel[q] = np.nanmedian(np.abs(rel_res_col))*100
                    AIC[q] = 2*N_ks + np.log(RSS_sum[q]/n_point[q])*n_point[q]
                    BIC[q] = N_ks*np.log(n_point[q]) +np.log(RSS_sum[q]/n_point[q])*n_point[q]
                    num_5[q] = len([item for item in abs_res_col if item <= 5])/n_point[q]*100
                    num_10[q] = len([item for item in abs_res_col if item <= 10])/n_point[q]*100
                    num_75[q] = len([item for item in abs_res_col if item >= 75])/n_point[q]*100
                    num_100_rel[q] = len([item for item in rel_res_col if item >= 1])/n_point[q]*100
                    n_point[num_col-1] = np.count_nonzero(~np.isnan(Res))
            mean_Res = np.append(mean_Res,np.nanmedian(Res)/n_point[num_col-1])
            std_Res = np.append(std_Res,np.std(Res))
            ave_Res = np.append(ave_Res,np.nansum(np.abs(Res))/n_point[num_col-1])
            mape[num_col-1] = np.nansum(np.abs(abs_res))/n_point[num_col-1]*100
            med_res[num_col-1] = np.median(np.abs(Res))
            med_rel[num_col-1] = np.median(np.abs(rel_Res))*100
            RSS[num_col-1] = np.sum(RSS_sum)
            AIC[num_col-1] = 2*N_ks + np.log(RSS[num_col-1]/n_point[num_col-1])*n_point[num_col-1]
            BIC[num_col-1] = np.log(n_point[num_col-1])*N_ks + np.log(RSS[num_col-1]/n_point[num_col-1])*n_point[num_col-1]
            pos_Res = abs(Res)
            num_5[num_col-1] = len(pos_Res[pos_Res<=5])/n_point[num_col-1]*100
            num_10[num_col-1] = len(pos_Res[pos_Res<=10])/n_point[num_col-1]*100
            num_75[num_col-1] = len(pos_Res[pos_Res>=75])/n_point[num_col-1]*100
            num_100_rel[num_col-1] = len(rel_Res[rel_Res>=1])/n_point[num_col-1]*100
        mean_Res, std_Res, ave_Res, mape, med_res, med_rel, BIC, AIC, n_point, num_5, num_10, num_75, num_100_rel = np.round(mean_Res, decimals=1), np.round(std_Res, decimals=1), np.round(ave_Res, decimals=1),  np.round(mape, decimals=1), np.round(med_res, decimals=1),np.round(med_rel, decimals=1), np.round(BIC, decimals=1) , np.round(AIC, decimals=1) , n_point, np.round(num_5, decimals=1), np.round(num_10, decimals=1), np.round(num_75, decimals=1), np.round(num_100_rel, decimals=1)
    return mean_Res, std_Res, ave_Res, med_res, mape, med_rel, BIC, AIC, n_point, num_5, num_10, num_75, num_100_rel


def Morse(x, b, T):
    T = T - 273.15
    f = T*(1-np.exp(-b*(x-np.log(1-np.sqrt(25/T))/b)))**2
    return f+ 273.15


def Model_analysis(Fun,if_mat):
    col_1 = 0
    name = pd.Series(['Biomass_type'])
    name.to_excel(outliers,startcol=col_1 ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(['Model'])
    name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Species"])
    name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Carbs wt%"])
    name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Protein wt%"])
    name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Lipids wt%"])
    name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Lignin wt%"])
    name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Temperature (C)"])
    name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Total time (min)"])
    name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
    name = pd.Series(["Output"])
    name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
    nu = pd.DataFrame(["Prediction"])
    nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
    nu = pd.DataFrame(["Experiment"])
    nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
    nu = pd.DataFrame(["Residual"])
    nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
    nu = pd.DataFrame(["Relative Error"])
    nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
    nu = pd.DataFrame(["Data number"])
    nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)
    col_1 = col_1 +1
    
    algae_check = ['Carbs wt%','Protein wt%','Lipids wt%']
    inputs_checks = []
    for i in range(len(algae_data)):
        check_require_one = True
        

        if isinstance(Fun.require_input, str):
            inputs_checks = np.isfinite(algae_data[Fun.require_input][i])
        elif Fun.require_input == []:
            inputs_checks = True
        else:
            inputs_checks = [True for item in Fun.require_input if np.isfinite(algae_data[item][i])]

        if not inputs_checks ==  True:
            if (len(inputs_checks) == len(Fun.require_input)):
                inputs_checks =  True
        require_one = []
        if not Fun.require_one ==[]:
            for k in Fun.require_one:
                check_require_one = False
                for q in k:
                    if np.isfinite(algae_data[q][i]) == True and check_require_one == False:
                        require_one.insert(0, q)
                        check_require_one = True
        if  inputs_checks ==  True and len(require_one) == len(Fun.require_one) :
            count = 0
            opt = Fun.optional
            opt_poss =[]
            
            if not opt == []:
                for me in opt:
                    
                    if inputs_checks == True:
                        if me == 'Hemicellulose wt%' or me == 'Starch wt%':
                            opt_poss.insert(0,'Carbs wt%')
                        elif not me in algae_check:
                            opt_poss.insert(0,'0')
                        else:
                            opt_poss.insert(0,me)
                        opt_poss.reverse()
                        inputs_checks = np.isfinite(algae_data[opt_poss[count]][i])
                    count = count +1
                    intended = True
                    if me in ['Lignin wt%']:
                        intended = False
                all_inputs = all(x in opt_poss for x in algae_check)
            else:
                intended = True
                all_inputs = True 
            if inputs_checks and all_inputs:
                fix_in = [opt_poss,require_one,Fun.require_input,Fun.if_avail]
                

                new_in =[]
                for item in fix_in:
                    if item == []:
                        item
                    elif isinstance(item, list):
                        [new_in.insert(0, item2) for item2 in item]
                    else:
                        new_in.insert(0, item)
                new_in = [algae_data[item][i] for item in new_in]
                new_in.reverse()

                if if_mat == False:

                    result = Fun.fun(new_in)
                else:
                    new_in = np.array(new_in)
                    result = eng.Hietala2021(new_in)
                    try:
                        result = result.real()
                    except:
                        result = result[0]

                res_algae = np.empty(len(Fun.outputs))
                rel_res_algae = np.empty(len(Fun.outputs))

                if  len(Fun.outputs) == 1:
                    if np.isfinite(algae_data[Fun.outputs[0]][i]):
                        res_algae = result -  algae_data[Fun.outputs[0]][i]
                        rel_res_algae = abs((result -  algae_data[Fun.outputs[0]][i])/algae_data[Fun.outputs[0]][i])

                        if ( abs(rel_res_algae) > 1) and (Fun.outputs == 'Biocrude wt%' or Fun.outputs == ['Biocrude wt%']):
                            name = pd.Series(['Algae'])
                            name.to_excel(outliers,startcol=col_1 ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([Fun.fun.__name__])
                            name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Species"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Carbs wt%"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Protein wt%"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Lipids wt%"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Lignin wt%"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Temperature (C)"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([algae_data["Total time (min)"][i]])
                            name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            name = pd.Series([Fun.outputs])
                            name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            nu = pd.DataFrame([result])
                            nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            nu = pd.DataFrame([algae_data[Fun.outputs[0]][i]])
                            nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            nu = pd.DataFrame([res_algae])
                            nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            nu = pd.DataFrame([rel_res_algae])
                            nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            nu = pd.DataFrame([i+3])
                            nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)
                            col_1 = col_1 +1
                    else:
                        res_algae = np.nan
                        rel_res_algae = np.nan
                else:
                    count = 0
                    for o in Fun.outputs:
                        if np.isfinite(algae_data[o][i]) and  np.isfinite(result[count]):
                            res_algae[count] = result[count] -  algae_data[o][i]
                            rel_res_algae[count] = abs((result[count] -  algae_data[o][i])/algae_data[o][i])
                            if ( abs(rel_res_algae[count]) > 1) and (o == 'Biocrude wt%' or o ==['biocrude wt%']):
                                name = pd.Series(['Algae'])
                                name.to_excel(outliers,startcol=col_1  ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([Fun.fun.__name__])
                                name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Species"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Carbs wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Protein wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Lipids wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Lignin wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Temperature (C)"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([algae_data["Total time (min)"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([o])
                                name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([result[count]])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([algae_data[o][i]])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([res_algae[count]])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([rel_res_algae[count]])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([i+3])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                col_1 = col_1 +1
                        else:
                            res_algae[count] = np.nan
                            rel_res_algae[count] = np.nan



                        count = count + 1

                Fun.add_res_algae(res_algae)
                Fun.add_rel_res_algae(rel_res_algae)
                if intended == True:
                    Fun.add_res_intended(res_algae)
                    Fun.add_rel_res_intended(rel_res_algae)
    if Fun.poss_ins == [[[]]]:
        inputs_checks = []
        for i in range(len(biomass_data)):
            check_require_one = True
            if isinstance(Fun.require_input, str):
                inputs_checks = np.isfinite(biomass_data[Fun.require_input][i])
            elif inputs_checks == []:
                inputs_checks = True
            else:
                inputs_checks = [True for item in Fun.require_input if np.isfinite(biomass_data[item][i])]

            if not inputs_checks ==  True:
                if (len(inputs_checks) == len(Fun.require_input)):
                    inputs_checks =  True
            require_one = []
            if not Fun.require_one == []:
                require_one = []
                for k in Fun.require_one:
                    check_require_one = False
                    for q in k:
                        if np.isfinite(biomass_data[q][i]) == True and check_require_one == False:
                            require_one.insert(0, q)
                            check_require_one = True
            if inputs_checks == True and check_require_one == True:
                    fix_in = [require_one,Fun.require_input,Fun.if_avail]
                    new_in =[]
                    for item in fix_in:
                        if item == []:
                            item
                        elif isinstance(item, list):
                            [new_in.insert(0, item2) for item2 in item]
                        else:
                            new_in.insert(0, item)
                    new_in = [biomass_data[item][i] for item in new_in ]
                    new_in.reverse()

                    if if_mat == False:

                        result = Fun.fun(new_in)
                    else:
                        new_in = np.array(new_in)
                        result = eng.Hietala2021(new_in)
                        try:
                             result = result.real()
                        except:
                             result = result[0]
                    res_biomass = np.empty(len(Fun.outputs))
                    rel_res_biomass = np.empty(len(Fun.outputs))
                    if  len(Fun.outputs) == 1:
                        if np.isfinite(biomass_data[Fun.outputs[0]][i]) and  np.isfinite(result):
                            res_biomass = result -  biomass_data[Fun.outputs[0]][i]
                            rel_res_biomass = abs((result -  biomass_data[Fun.outputs[0]][i])/biomass_data[Fun.outputs[0]][i])
                            if ( abs(rel_res_biomass) > 1) and (Fun.outputs == 'Biocrude wt%' or Fun.outputs == ['Biocrude wt%']):
                                name = pd.Series(['Biomass'])
                                name.to_excel(outliers,startcol=col_1  ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([Fun.fun.__name__])
                                name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Species"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Carbs wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Protein wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Lipids wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Lignin wt%"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Temperature (C)"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([biomass_data["Total time (min)"][i]])
                                name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                name = pd.Series([Fun.outputs])
                                name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([result])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([biomass_data[Fun.outputs[0]][i]])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([res_biomass])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([rel_res_biomass])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                nu = pd.DataFrame([i+3])
                                nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)

                                col_1 = col_1 +1
                        else:
                            res_biomass = np.nan
                            rel_res_biomass = np.nan

                    else: 
                        count = 0
                        for o in Fun.outputs:
                            if np.isfinite(biomass_data[o][i]) and  np.isfinite(result[count]):
                                res_biomass[count] = result[count] -  biomass_data[o][i]
                                rel_res_biomass[count] = (result[count] -  biomass_data[o][i])/biomass_data[o][i]
                                if ( abs(rel_res_biomass[count]) > 1) and (o == 'Biocrude wt%' or o == ['Biocrude wt%']):
                                    name = pd.Series(['Biomass'])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([Fun.fun.__name__])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Species"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Carbs wt%"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Protein wt%"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Lipids wt%"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Lignin wt%"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Temperature (C)"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([biomass_data["Total time (min)"][i]])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    name = pd.Series([o])
                                    name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    nu = pd.DataFrame([result[count]])
                                    nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    nu = pd.DataFrame([biomass_data[o][i]])
                                    nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    nu = pd.DataFrame([res_biomass[count]])
                                    nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    nu = pd.DataFrame([rel_res_biomass[count]])
                                    nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                    nu = pd.DataFrame([i+3])
                                    nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)

                                    col_1 = col_1 +1
                            else:
                                res_biomass[count] = np.nan
                                rel_res_biomass[count] = np.nan

                            count = count + 1
                    Fun.add_res_biomass(res_biomass,[[]])
                    Fun.add_rel_res_biomass(rel_res_biomass,[[]])
                    Fun.add_res_intended(res_biomass)
                    Fun.add_rel_res_intended(rel_res_biomass)

    else:
        for p in Fun.poss_ins:
            if not p[0] == [] or p[0] == [[]]:
                inputs_checks = []
                for i in range(len(biomass_data)):
                    check_require_one = True
                    if isinstance(Fun.require_input, str):
                        inputs_checks = np.isfinite(biomass_data[Fun.require_input][i])
                    elif inputs_checks == []:
                        inputs_checks = True
                    else:
                        inputs_checks = [True for item in Fun.require_input if np.isfinite(biomass_data[item][i])]
                    if not inputs_checks ==  True:
                        if (len(inputs_checks) == len(Fun.require_input)):
                            inputs_checks =  True
                    require_one = []   
                    if not Fun.require_one ==[]:
                        for k in Fun.require_one:
                            check_require_one = False
                            for q in k:
                                if np.isfinite(biomass_data[q][i]) == True and check_require_one == False:
                                    require_one.insert(0, q)
                                    check_require_one = True
                    if inputs_checks == True and check_require_one == True:
                        inputs_checks = []
                        poss_val = []
                        poss_option = []
                        opt = Fun.optional

                        if not opt == []:
                            count  = 0
                            all_checks =[]
                            poss_checks = 1
                            for poss_name in ['Protein wt%','Carbs wt%','Lipids wt%','Lignin wt%']:
                                if np.isfinite(biomass_data[poss_name][i]):
                                    if poss_name == 'Carbs wt%':
                                        poss_checks = 0
                                        for k in ['Carbs wt%','Cellulose wt%','Hemicellulose wt%','Starch wt%']:
                                            if k in opt:
                                                poss_checks = 1
                                    elif not poss_name in opt:
                                        poss_checks = 0
                                all_checks.insert(0,poss_checks)
                            for me in opt:
                                if me == "Cellulose wt%" or me == "Hemicellulose wt%" or me == "Starch wt%" :
                                    inputs_checks.insert(0,np.isfinite(biomass_data["Carbs wt%"][i]))
                                    if me == "Hemicellulose wt%" or me == "Starch wt%":
                                        poss_val.insert(0,np.nansum([biomass_data["Carbs wt%"][i],-biomass_data["Cellulose wt%"][i]]))
                                    elif me == "Cellulose wt%":
                                        if np.isfinite(biomass_data[me][i]):
                                            poss_val.insert(0,biomass_data[me][i])
                                        else:
                                            poss_val.insert(0,0)
                                    
                                else:
                                    inputs_checks.insert(0, np.isfinite(biomass_data[me][i]))
                                       
                                    if np.isfinite(biomass_data[me][i]):
                                         poss_option.insert(0,me)
                                         poss_val.insert(0,biomass_data[me][i])
                                    else:
                                         poss_option.insert(0,'0')
                                         poss_val.insert(0,0)
                                count = count +1
                            inputs_checks.reverse()
                            poss_option.reverse()

                        if inputs_checks == p[0] and all(all_checks) :
                            fix_in = [require_one,Fun.require_input,Fun.if_avail]
                            new_in =[]
                            for item in fix_in:
                                if item == []:
                                    item
                                elif isinstance(item, list):
                                    [new_in.insert(0, item2) for item2 in item]
                                else:
                                    new_in = np.array(new_in)
                                    new_in.insert(0, item)
                            new_in = [biomass_data[item][i] for item in new_in ]
                            for item in poss_val:
                                new_in.insert(len(new_in),item)
                            new_in.reverse()
                            
                            if if_mat == False:

                                result = Fun.fun(new_in)
                            else:
                                new_in = np.array(new_in)
                                result = eng.Hietala2021(new_in)
                                try:
                                     result = result.real()
                                except:
                                     result = result[0]     

                            res_biomass = np.empty(len(Fun.outputs))
                            rel_res_biomass = np.empty(len(Fun.outputs))
                            if  len(Fun.outputs) == 1:
                                if np.isfinite(biomass_data[Fun.outputs[0]][i]):
                                    res_biomass = result -  biomass_data[Fun.outputs[0]][i]
                                    rel_res_biomass = abs((result -  biomass_data[Fun.outputs[0]][i])/biomass_data[Fun.outputs[0]][i])
                                    if (abs(rel_res_biomass) > 1) and (Fun.outputs == 'Biocrude wt%' or Fun.outputs == ['Biocrude wt%']):
                                           name = pd.Series(['Biomass'])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([Fun.fun.__name__])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Species"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Carbs wt%"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Protein wt%"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Lipids wt%"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Lignin wt%"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Temperature (C)"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([biomass_data["Total time (min)"][i]])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           name = pd.Series([Fun.outputs])
                                           name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           nu = pd.DataFrame([result])
                                           nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           nu = pd.DataFrame([biomass_data[Fun.outputs[0]][i]])
                                           nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           nu = pd.DataFrame([res_biomass])
                                           nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           nu = pd.DataFrame([rel_res_biomass])
                                           nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                           nu = pd.DataFrame([i+3])
                                           nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)

                                           col_1 = col_1 +1
                                else:
                                    res_biomass = np.nan
                                    rel_res_biomass = np.nan

                            else: 
                                count = 0
                                for o in Fun.outputs:
                                    if np.isfinite(biomass_data[o][i]) and  np.isfinite(result[count]):
                                        res_biomass[count] = result[count] -  biomass_data[o][i]
                                        rel_res_biomass[count] = abs((result[count] -  biomass_data[o][i])/biomass_data[o][i])
                                        if (abs(rel_res_biomass[count]) > 1) and (o == 'Biocrude wt%' or o == ['Biocrude wt%']):
                                            name = pd.Series(['Biomass'])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =0,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([Fun.fun.__name__])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =1,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Species"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =2,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Carbs wt%"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =3,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Protein wt%"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =4,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Lipids wt%"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =5,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Lignin wt%"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =6,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Temperature (C)"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =7,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([biomass_data["Total time (min)"][i]])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =8,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            name = pd.Series([o])
                                            name.to_excel(outliers,startcol=col_1  ,startrow =9,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            nu = pd.DataFrame([result[count]])
                                            nu.to_excel(outliers,startcol=col_1  ,startrow =10,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            nu = pd.DataFrame([biomass_data[o][i]])
                                            nu.to_excel(outliers,startcol=col_1  ,startrow =11,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            nu = pd.DataFrame([res_biomass[count]])
                                            nu.to_excel(outliers,startcol=col_1  ,startrow =12,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            nu = pd.DataFrame([rel_res_biomass[count]])
                                            nu.to_excel(outliers,startcol=col_1  ,startrow =13,index=False,header=False, sheet_name =  Fun.fun.__name__)
                                            nu = pd.DataFrame([i+3])
                                            nu.to_excel(outliers,startcol=col_1  ,startrow =14,index=False,header=False, sheet_name =  Fun.fun.__name__)

                                            col_1 = col_1 +1
                                    else:
                                        res_biomass[count] = np.nan
                                        rel_res_biomass[count] = np.nan

                                    count = count + 1
                            Fun.add_res_biomass(res_biomass,p)
                            Fun.add_rel_res_biomass(rel_res_biomass,p)
                            if all(p[0]):
                                Fun.add_res_intended(res_biomass)
                                Fun.add_rel_res_intended(rel_res_biomass)


    Fun.cal_analysis()


    return



def def_mod(name,nk,req_in,req_one,avail,out,opt,biomass,bo):


    exec('model_'+ name  + ' = model()')

    eval('model_'+ name  + '.set_fun_str(' + str(name) +')')

    eval('model_'+ name + '.set_fun_name('+ name +')')

    eval('model_'+ name + '.set_nk(nk)')

    eval('model_'+ name + '.set_biomass(biomass)')

    eval('model_'+ name + '.set_require_input(req_in)')

    eval('model_'+ name + '.set_require_one(req_one)')

    eval('model_'+ name + '.set_if_avail(avail)')

    eval('model_'+ name + '.set_outputs(out)')

    eval('model_'+ name + '.set_optional(opt)')


    Model_analysis(eval('model_'+ name),bo)

    return eval('model_'+ name)

"""
https://www.sciencedirect.com/science/article/pii/S2211926413000842


Valdez 2013
"""
      
def Valdez2013(const):
    Temp = const[1] + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (85.7, 3.2, 6.6, 4.5, 0)

        def ode(x, t, Temp):
            if np.isfinite(const[2]):
                Temp = Morse(t, const[2], Temp)

            R = 8.314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]

            k1 = math.exp(2.8-(27000/(R*Temp)))
            k2 = math.exp(-0.2-(15000/(R*Temp)))
            k3 = math.exp(6-(41000/(R*Temp)))
            k4 = math.exp(1.8-(26000/(R*Temp)))
            k5 = math.exp(-2.2-(2900/(R*Temp)))
            k6 = math.exp(4-(66000/(R*Temp)))
            k7 = math.exp(1.2-(17000/(R*Temp)))
            k8 = math.exp(0.9-(33000/(R*Temp)))
            k9 = math.exp(-0.8-(4800/(R*Temp)))
            k10 = math.exp(4.7-(45000/(R*Temp)))
            k11 = math.exp(10-(80000/(R*Temp)))

            sol = [-(k1+k2+k3)*x1, -(k4+k5+k6)*x2 + k1*x1 + k7*x3 + k9*x4, -(k7+k8)*x3 + k2 *
                    x1 + k4*x2 + k10*x4, -(k9+k10+k11)*x4 + k3*x1 + k5*x2 + k8*x3, k6*x2 + k11*x4]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]
    if const[0] == 0:
        pred = (85.7, 3.2, 6.6, 4.5, 0)
    else:
        pred = my_ls_func(const[0], Temp)

    Y_Char = pred[0]

    Y_Crude = pred[2] + pred[3]

    Y_LB = pred[2]

    Y_HB = pred[3]

    Y_Aq = pred[1]

    Y_Gas = pred[4]

    Y_Aq_gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_LB, Y_HB, Y_Aq, Y_Gas, Y_Aq_gas

mod_Valdez2013 = def_mod('Valdez2013',22,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Light Biocrude wt%','Heavy Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],[],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0960852414005082

Valdez 2014
"""

def Valdez2014(const):
    Temp = const[4] + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (const[1], const[2], const[0], 0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(const[5]):
                Temp = Morse(t, const[5], Temp)

            R = 8.314

            x1p = x[0]
            x1l = x[1]
            x1c = x[2]
            x2 = x[3]
            x3 = x[4]

            k1p = math.exp(3.347-(24319.1/(R*Temp)))
            k1l = math.exp(1.918-(15972.1/(R*Temp)))
            k1c = math.exp(0.1285-(6223.6/(R*Temp)))
            k2p = math.exp(2.448-(20067.6/(R*Temp)))
            k2c = math.exp(8.177-(49970.7/(R*Temp)))
            k2l = math.exp(7.007-(72834.9/(R*Temp)))
            k3  = math.exp(14.687-(84288.3/(R*Temp)))
            k4  = math.exp(14.836-(86228.5/(R*Temp)))
            k5  = math.exp(3.573-(54801.4/(R*Temp)))
            k6  = math.exp(8.157-(77157.8/(R*Temp)))

            sol = [-(k1p+k2p)*x1p, -(k1l+k2l)*x1l, -(k1c+k2c)*x1c, -(k4+k5)*x2 + k1p*x1p + k1l*x1l +
                    k1c*x1c + k3*x3, -(k3+k6)*x3 + k2p*x1p + k2l*x1l + k2c*x1c + k4*x2, k5*x2 + k6*x3]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if const[3] == 0:
        pred = (const[1], const[2], const[0], 0, 0, 0)
    else:
        pred = my_ls_func(const[3], Temp)

    Y_Char = pred[0] + pred[1] + pred[2]

    Y_Crude = pred[4]

    Y_Aq = pred[3]

    Y_Gas = pred[5]

    Y_Aq_gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_gas

mod_Valdez2014 = def_mod('Valdez2014',20,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S0960852416305545

Hietala 2016
"""

def Hietala2016(const):
    time, T, Lip, b = const
    if not np.isfinite(Lip):
        Lip = 0
    Temp = T + 273
    time = time*60

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (100-12-Lip, Lip, 0, 12, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)
            R = 8.314

            xS = x[0] - 4
            xB = x[1]
            xA = x[3] - 12

            kSB = math.exp(5-(74000/(R*Temp)))
            kSA = math.exp(4-(65000/(R*Temp)))
            kSG = math.exp(3.9-(68000/(R*Temp)))
            kBA = math.exp(3.8-(99000/(R*Temp)))
            kAB = math.exp(1.7-(59000/(R*Temp)))
            kAG = math.exp(2.3-(64000/(R*Temp)))
            kAV = math.exp(7.6-(119000/(R*Temp)))

            sol = [-(kSB+kSA+kSG)*xS, kSB*xS + kAB*xA - kBA*xB, kSG*xS +
                    kAG*xA, kSA*xS + kBA*xB - (kAB + kAG + kAV)*xA, kAV*xA]
            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12
            xS = x[0] + 4

            xA = x[3] + 12
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (100-15-Lip, Lip, 0, 15, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0]

    Y_Crude = pred[1]

    Y_Aq = pred[3]

    Y_Gas = pred[2]

    Y_Loss = pred[4]

    Y_Aq_gas = Y_Aq + Y_Gas

    Y_gas_Loss = Y_Gas + Y_Loss

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Loss, Y_gas_Loss, Y_Aq_gas

mod_Hietala2016 = def_mod('Hietala2016',14,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['Lipids wt%','b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas wt%', 'Loss' ,'Gas + Loss','Aq + Gas wt%'],[],[],False)

"""
https://pubs.acs.org/doi/10.1021/acssuschemeng.6b00226

Luo 2016
"""


""" Protein only """
def Luo2016(const):
    
    prot, time, T, b = const
    
            
    Temp = T + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (72.8, 10.1, 9.23, 0)

        def ode(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314

            xp = x[0]
            xA = x[1]
            xB = x[2]

            k1 = math.exp(-0.75-(9920/(R*Temp)))
            k3 = math.exp(10.37-(58600/(R*Temp)))
            k4 = math.exp(10.83-(57200/(R*Temp)))
            k5 = math.exp(0.38-(29400/(R*Temp)))

            sol = [-k1*xp, -(k3+k5)*xA + k1*xp + k4*xB, k3*xA - k4*xB, k5*xA]
            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (72.8, 10.1, 9.23, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0]

    Y_Crude = pred[2]

    Y_Aq = pred[1]

    Y_Gas = pred[3]

    Y_Aq_gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_gas

mod_Luo2016 = def_mod('Luo2016',8,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Protein wt%'],['Protein wt%'],False)


"""
https://pubs.acs.org/doi/10.1021/acssuschemeng.6b01857

Sheehan 2016
"""

def Sheehan2016(const):

    prot,time, T, b = const

    Temp = T + 273

    time = time*60

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaSheehanation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (55, 43, 0, 2, 0)

        def ode(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 0.008314

            xS = x[0]
            xA1 = x[1]
            xB = x[3]

            kSA1 = math.exp(4.01-(56.0/(R*Temp)))
            kSB  = math.exp(5.34-(68.1/(R*Temp)))
            kSG  = math.exp(5.17-(72.1/(R*Temp)))
            kA1B = math.exp(4.08-(85.1/(R*Temp)))
            kA1G = math.exp(5.33-(125/(R*Temp)))
            kBA2 = math.exp(4.26-(87.2/(R*Temp)))
            kBG  = math.exp(5.28-(111/(R*Temp)))


            sol = [-(kSA1+kSB+kSG)*xS, -(kA1B+kA1G)*xA1 + kSA1*xS, kBA2*xB, -(kBA2+kBG)*xB + kSB*xS + kA1B*xA1, kSG*xS + kA1G*xA1 + kBG*xB]

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode soSheehantion, retuen vaSheehanes for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (85.7, 3.2, 6.6, 4.5, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0]

    Y_Crude = pred[3]

    Y_Aq = pred[1] + pred[2]

    Y_Gas = pred[4]

    Y_Aq_gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_gas

mod_Sheehan2016 = def_mod('Sheehan2016',14,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Protein wt%'],['Protein wt%'],False)

"""
https://www.sciencedirect.com/science/article/pii/S1385894716310506

Vo 2016
"""


def Vo2016(const):
    Temp = const[4] + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (const[2], const[0], const[1],  0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(const[5]):
                Temp = Morse(t, const[5], Temp)

            R = 8.314

            x1p = x[0]
            x1l = x[1]
            x1c = x[2]
            x2 = x[3]
            x3 = x[4]

            k1p = math.exp(3.86-(27200/(R*Temp)))
            k1l = math.exp(1.69-(15100/(R*Temp)))
            k1c = math.exp(3.69-(26500/(R*Temp)))
            k2p = math.exp(6.26-(38900/(R*Temp)))
            k2l = math.exp(5.14-(33000/(R*Temp)))
            k2c = math.exp(7.43-(45500/(R*Temp)))
            k3 = math.exp(3.17-(23700/(R*Temp)))
            k4 = math.exp(4.12-(28000/(R*Temp)))
            k5 = math.exp(8.63-(83600/(R*Temp)))
            k6 = math.exp(7.70-(70300/(R*Temp)))

            sol = [-(k1p+k2p)*x1p, -(k1l+k2l)*x1l, -(k1c+k2c)*x1c, -(k4+k5)*x2 + k1p*x1p + k1l*x1l +
                    k1c*x1c + k3*x3, -(k3+k6)*x3 + k2p*x1p + k2l*x1l + k2c*x1c + k4*x2, k5*x2 + k6*x3]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12
            
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"
        
        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if const[3] == 0:
        pred = (const[1], const[2], const[0], 0, 0, 0)
    else:
        pred = my_ls_func(const[3], Temp)

    Y_Char = pred[0] + pred[1] + pred[2]

    Y_Crude = pred[4]

    Y_Aq = pred[3]

    Y_Gas = pred[5]

    Y_Aq_Gas = Y_Aq + Y_Gas

    return  Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas


mod_Vo2016= def_mod('Vo2016',20,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S0960852417308544

Vo 2017
"""

def Vo2017(const):
    Carb, Prot, Lip,  time, T, b = const
    Temp = T + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Prot, Lip, Carb, 0, 0, 0, 0)

        def ode(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314

            x1p = x[0]
            x1l = x[1]
            x1c = x[2]
            x2 = x[3]
            x3 = x[4]
            x4 = x[5]

            k1p = math.exp(1.19-(19310/(R*Temp)))
            k1l = math.exp(2.6-(24610/(R*Temp)))
            k1c = math.exp(2.12-(22700/(R*Temp)))
            k2p = math.exp(6.22-(56080/(R*Temp)))
            k2l = math.exp(6.7-(49910/(R*Temp)))
            k2c = math.exp(7.24-(68440/(R*Temp)))
            k3p = math.exp(7.52-(46850/(R*Temp)))
            k3l = math.exp(8.8-(39180/(R*Temp)))
            k3c = math.exp(6.92-(77650/(R*Temp)))
            k4  = math.exp(4.59-(37420/(R*Temp)))
            k5  = math.exp(2.38-(26570/(R*Temp)))
            k6  = math.exp(12.58-(94870/(R*Temp)))
            k7  = math.exp(10.84-(70660/(R*Temp)))
            k8  = math.exp(8.54-(59460/(R*Temp)))
            k9  = math.exp(1.22-(20930/(R*Temp)))
            k10 = math.exp(5.13-(43120/(R*Temp)))
            k11 = math.exp(11.38-(82230/(R*Temp)))

            sol = [-(k1p+k2p+k3p)*x1p, -(k1l+k2l+k3l)*x1l, -(k1c+k2c+k3c)*x1c, -(k4+k5+k6)*x2 + k1p*x1p + k1l*x1l + k1c*x1c + k7*x3 + k9*x4, -(k7+k8)
                    * x3 + k2p*x1p + k2l*x1l + k2c*x1c + k4*x2 + k10*x4, -(k9+k10+k11)*x4 + k3p*x1p + k3l*x1l + k3c*x1c + k5*x2 + k8*x3, k6*x2 + k11*x4]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]
    if time == 0:
        pred = (Prot, Lip, Carb, 0, 0, 0, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0] + pred[1] + pred[2]

    Y_LB = pred[4]

    Y_HB = pred[5]

    Y_Crude = Y_LB + Y_HB

    Y_Aq = pred[3]

    Y_Gas = pred[6]

    Y_Aq_Gas = Y_Aq + Y_Gas

    return  Y_Char, Y_LB, Y_HB, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Vo2017= def_mod('Vo2017',17*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Light Biocrude wt%','Heavy Biocrude wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0960852417306521

Sheehan and Savage

"""


def Sheehan2017_1(const):
    
    Carb, Prot, Lip, time, T, b = const
    
    Temp = T + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Prot, Lip, Carb, 0, 0, 0)

        def ode(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314

            x1p = x[0]
            x1l = x[1]
            x1c = x[2]
            x2 = x[3]
            x3 = x[4]

            k1p = 10**5.37* math.exp(-(53300/(R*Temp)))
            k1l = 10**4.15* math.exp(-(57900/(R*Temp)))
            k1c = 10**4.52*math.exp(-(57600/(R*Temp)))
            k2p = 10**5.29*math.exp(-(51900/(R*Temp)))
            k2c = 10**5.25*math.exp(-(78600/(R*Temp)))
            k2l = 10**5.32*math.exp(-(65800/(R*Temp)))
            k3  = 10**3.41*math.exp(-(65600/(R*Temp)))
            k4  = 10**3.52*math.exp(-(66200/(R*Temp)))
            k5  = 10**3.36*math.exp(-(142000/(R*Temp)))
            k6  = 10**4.63*math.exp(-(89800/(R*Temp)))

            sol = [-(k1p+k2p)*x1p, -(k1l+k2l)*x1l, -(k1c+k2c)*x1c, -(k4+k5)*x2 + k1p*x1p + k1l*x1l +
                    k1c*x1c + k3*x3, -(k3+k6)*x3 + k2p*x1p + k2l*x1l + k2c*x1c + k4*x2, k5*x2 + k6*x3]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (Prot, Lip, Carb, 0, 0, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0] + pred[1] + pred[2]

    Y_Crude = pred[4]

    Y_Aq = pred[3]

    Y_Gas = pred[5]

    Y_Aq_Gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Sheehan2017_1 = def_mod('Sheehan2017_1',20,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


def Sheehan2017_2(const):
    
    Carb, Prot, Lip, time, T, b = const
    
    Temp = T + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Prot, Lip, Carb, 0, 0, 0)

        def ode(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314

            x1p = x[0]
            x1l = x[1]
            x1c = x[2]
            x2 = x[3]
            x3 = x[4]

            k1p = 10**5.37*math.exp(-(53300/(R*Temp)))
            k1l = 10**4.15*math.exp(-(57900/(R*Temp)))
            k1c = 10**4.52*math.exp(-(57600/(R*Temp)))
            k2p = 10**5.29*math.exp(-(51900/(R*Temp)))
            k2c = 10**5.25*math.exp(-(78600/(R*Temp)))
            k2l = 10**5.32*math.exp(-(65800/(R*Temp)))
            k3 =  10**3.41*math.exp(-(65600/(R*Temp)))
            k4 =  10**3.52*math.exp(-(66200/(R*Temp)))
            k5 =  10**3.36*math.exp(-(142000/(R*Temp)))
            k6 =  10**4.63*math.exp(-(89800/(R*Temp)))
            k7 =  10**4.33*math.exp(-(63100/(R*Temp)))
            k8 =  10**4.76*math.exp(-(137000/(R*Temp)))
            k9 =  10**2.58*math.exp(-(117000/(R*Temp)))
            k10 = 10**3.09*math.exp(-(54300/(R*Temp)))
            k11 = 10**3.81*math.exp(-(74600/(R*Temp)))
            k12 = 10**-1.11*math.exp(-(84400/(R*Temp)))

            sol = [-(k1p+k2p)*x1p - (k7+k8)*x1p*x1c - (k9+k10)*x1p*x1l, -(k1l+k2l)*x1l - (k9+k10)*x1p*x1l - (k11+k12)*x1c*x1l, -(k1c+k2c)*x1c - (k7+k8)*x1p*x1c - (k11+k12)*x1c*x1l, -(k4+k5)*x2 +
                    k1p*x1p + k1l*x1l + k1c*x1c + k3*x3 + k7*x1p*x1c + k9*x1p*x1l + k12*x1c*x1l, -(k3+k6)*x3 + k2p*x1p + k2l*x1l + k2c*x1c + k4*x2 + k8*x1p*x1c + k10*x1p*x1l + k12*x1c*x1l, k5*x2 + k6*x3]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (Prot, Lip, Carb, 0, 0, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0] + pred[1] + pred[2]

    Y_Crude = pred[4]

    Y_Aq = pred[3]

    Y_Gas = pred[5]

    Y_Aq_Gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Sheehan2017_2 = def_mod('Sheehan2017_2',16*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S1385894719307132

Obeid 2019
"""


def Obeid2019_oil(const):
    
    Lip, time, T, b = const

    Temp = T + 273
    time = time
    
    if time == 0:
        time = 0.001

    def my_ls_func_oil(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_oil = (0, 1, 0)

        def ode_oil(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314
            """
            Oil
            """
            x2 = x[0]
            x3 = x[1]

            k1 = math.exp(6.7-(31100/(R*Temp)))
            k2 = math.exp(6.7-(141100/(R*Temp)))
            k3 = math.exp(5.9-(36700/(R*Temp)))

            sol = [-k2*x2 + k1*x3, -(k1+k3)*x3 + k2*x2, k3*x3]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_oil(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_oil, t_eval=[time], method='Radau')

        pred_oil = np.transpose(r.y)

        return pred_oil[0]

    pred_oil = my_ls_func_oil(time, Temp)*100

    Y_Char = 0

    Y_Crude = pred_oil[1]

    Y_Aq = pred_oil[0]

    Y_Gas = pred_oil[2]

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Obeid2019_oil = def_mod('Obeid2019_oil',3*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Lipids wt%'],['Lipids wt%'],False)


def Obeid2019_carb(const):
    
    Carb, time, T, b = const

    Temp = T + 273
    time = time
    
    if time == 0:
        time = 0.001

    def my_ls_func_Carb(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Carb = (0.952, .48, 0, 0)

        def ode_Carb(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314
            """
            Carb
            """
            x1 = x[0]
            x2 = x[1]
            x3 = x[2]

            k1 = math.exp(4.8-(18600/(R*Temp)))
            k2 = math.exp(7-(25600/(R*Temp)))
            k3 = math.exp(2.6-(4700/(R*Temp)))
            k4 = math.exp(1.1-(4200/(R*Temp)))

            sol = [-k1*x1, -(k3+k4)*x2 + k1*x1 + k2*x3, -k2*x3 + k3*x2, k4*x2]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Carb(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_Carb, t_eval=[time], method='Radau')

        pred_Carb = np.transpose(r.y)

        return pred_Carb[0]

    pred_Carb = my_ls_func_Carb(time, Temp)*100

    Y_Char = pred_Carb[0]

    Y_Crude = pred_Carb[2] 

    Y_Aq =  pred_Carb[1] 

    Y_Gas =  pred_Carb[3] 

    Y_Aq_Gas = Y_Aq + Y_Gas

        
    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Obeid2019_carb = def_mod('Obeid2019_carb',4*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%'],['Carbs wt%'],False)


def Obeid2019_prot(const):
    
    Prot, time, T, b = const
    

    Temp = T + 273
    time = time
    
    if time == 0:
        time = 0.001


    def my_ls_func_Prot(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Prot = (.32, .68, 0, 0)

        def ode_Prot(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314
            """
            Prot
            """
            x1 = x[0]
            x2 = x[1]
            x3 = x[2]

            k1 = math.exp(9.5-(35000/(R*Temp)))
            k2 = math.exp(8.6-(36300/(R*Temp)))
            k3 = math.exp(1.7-(2900/(R*Temp)))
            k4 = math.exp(14.7-(67700/(R*Temp)))

            sol = [-k1*x1, -(k3+k4)*x2 + k1*x1 + k2*x3, -k2*x3 + k3*x2, k4*x2]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Prot(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_Prot, t_eval=[time], method='Radau')

        pred_Prot = np.transpose(r.y)

        return pred_Prot[0]

    pred_Prot = my_ls_func_Prot(time, Temp)*100


    Y_Char = pred_Prot[0]

    Y_Crude = pred_Prot[2]
    
    Y_Aq =  pred_Prot[1]

    Y_Gas = pred_Prot[3]

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Obeid2019_prot = def_mod('Obeid2019_prot',4*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Protein wt%'],['Protein wt%'],False)


def Obeid2019_lig(const):
    
    Lig, time, T, b = const

    Temp = T + 273
    time = time
    
    if time == 0:
        time = 0.001

    def my_ls_func_Lig(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Lig = (.533, .467, 0, 0)

        def ode_Lig(x, t, Tempf):

            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp =Tempf

            R = 8.314
            """
            Lig
            """
            x1 = x[0]
            x2 = x[1]
            x3 = x[2]

            k1 = math.exp(1.2-(4900/(R*Temp)))
            k2 = math.exp(8.6-(39000/(R*Temp)))
            k3 = math.exp(4.8-(27600/(R*Temp)))
            k4 = math.exp(0.7-(7600/(R*Temp)))

            sol = [-k1*x1, -k3*x2 + k1*x1 + k2*x3, -(k2+k4)*x3 + k3*x2, k4*x3]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Lig(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_Lig, t_eval=[time], method='Radau')

        pred_Lig = np.transpose(r.y)

        return pred_Lig[0]

    pred_Lig = my_ls_func_Lig(time, Temp)*100

    Y_Char = pred_Lig[0]

    Y_Crude = pred_Lig[2]

    Y_Aq = pred_Lig[1]

    Y_Gas = pred_Lig[3]

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Obeid2019_lig = def_mod('Obeid2019_lig',4*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Lignin wt%'],['Lignin wt%'],False)


"""
https://www.sciencedirect.com/science/article/pii/S2211926419305090

Palomino et al 2019
"""


def Palomino2019(const):

    Carb, Prot, Lip, Time, Temp, b = const

    R = 8.314
    Tf = Temp + 273

    if np.isfinite(b):
        T = Morse(Time, b, Tf)
    else:
        T =Tf

    kL = 10**5.32*math.exp(-65800/(R*T))
    kP = 10**5.29*math.exp(-51900/(R*T))
    kC = 10**5.25*math.exp(-78600/(R*T))

    Y_Crude = 0.813*Lip*(1-math.exp(-kL*Time)) + 0.397*Prot *(1-math.exp(-kP*Time)) + 0.367*Carb*(1-math.exp(-kC*Time))

    return Y_Crude

mod_Palomino2019 = def_mod('Palomino2019',6,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
https://pubs.acs.org/doi/full/10.1021/acs.energyfuels.9b02936

Obeid 2020
"""

def Obeid2020_poly(const):

    Prot, Lip, Carb, Lig, time, T, b = const

    time = time*60

    Temp = T + 273

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Prot/100, Lip/100, Carb/100, Lig/100, 0, 0, 0, 0)


        def ode(x, t, Tempf):
            if np.isfinite(b):
                Temp = Morse(t, b, Tempf)
            else:
                Temp = Tempf

            R = 8.314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]
            x5 = x[4]
            x6 = x[5]
            x7 = x[6]
            x8 = x[7]

            k1 = math.exp(32.6-(143800/(R*Temp)))
            k2 = math.exp(8.4-(23700/(R*Temp)))
            k3 = math.exp(11-(40000/(R*Temp)))
            k4 = math.exp(9.5-(29300/(R*Temp)))
            k5 = math.exp(11.1-(41200/(R*Temp)))
            k6 = math.exp(9.3-(28000/(R*Temp)))
            k7 = math.exp(7.5-(21300/(R*Temp)))
            k8 = math.exp(12.5-(45900/(R*Temp)))
            k9 = math.exp(22.8-(103800/(R*Temp)))
            k10 = math.exp(21.1-(87900/(R*Temp)))
            k11 = math.exp(31.7-(142300/(R*Temp)))
            k12 = math.exp(24.8-(108100/(R*Temp)))
            k13 = math.exp(29.8-(137800/(R*Temp)))
            k14 = math.exp(4.8-(18100/(R*Temp)))
            k15 = math.exp(23.5-(103200/(R*Temp)))
            k16 = math.exp(15.9-(71200/(R*Temp)))
            k17 = math.exp(15.3-(57600/(R*Temp)))

            sol = [-(k1+k2)*x1, -(k3+k4)*x2, -(k5+k6)*x3, -(k7+k8)*x4, -(k10+k13)*x5 + k3*x2 + k5*x3 + k7*x4 + k9*x6 + k14*x7, -(k9 + k12 + k15) *
                    x6 + k1*x1 + k4*x2 + k6*x3 + k8*x4 + k10*x5 + k11*x7 + k17*x8, -(k11+k14+k16)*x7 + k2*x1 + k12*x6 + k13*x5, -k17*x8 + k15*x6 + k16*x7]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (Prot/100, Lip/100, Carb/100, Lig/100, 0, 0, 0, 0)
    else:

        pred = my_ls_func(time, Temp)

    Y_Char = (pred[0]+pred[1]+pred[2]+pred[3]+pred[4])*100

    Y_Crude = pred[6]*100

    Y_Aq = pred[5]*100

    Y_Gas = pred[7]*100

    Y_Aq_Gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Aq_Gas

mod_Obeid2020_poly= def_mod('Obeid2020_poly',17*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%',"Lignin wt%"],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0306261919319993

Qian 2020
"""


def Qian2020(const):

    time, T, Lip, b = const

    if not np.isfinite(Lip):
        Lip = 0
    Temp = T + 273
    time = time*60

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (100-1.6-Lip, Lip, 0, 1.6, 0)

        def ode(x, t, Temp):
            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 8.314

            xS = x[0] - 10.8
            xB = x[1]
            xA = x[3] - 1.6

            check1 =0
            check2 =0

            if xS < 0:
                xS = 0
                check1 =1
            if xA < 0:
                xA =0
                check2 =1

            k1 = math.exp(3-(60000/(R*Temp)))
            k2 = math.exp(3.6-(66000/(R*Temp)))
            k3 = math.exp(5.9-(94000/(R*Temp)))
            k4 = math.exp(6-(129000/(R*Temp)))
            k6 = math.exp(5.9-(110000/(R*Temp)))
            k5 = math.exp(4.8-(90000/(R*Temp)))

            sol = [-(k1+k2+k3)*xS, k1*xS - k4*xB, k3*xS + k6 *
                    xA, k2*xS + k4*xB - (k6 + k5)*xA, k5*xA]
            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            if check1 ==0:
                xS = x[0] + 10.8

            if check2 ==0:
                xA = x[3] + 1.6


            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (100-1.6-Lip, Lip, 0, 1.6, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = pred[0]

    Y_Crude = pred[1]

    Y_Aq = pred[3]

    Y_Gas = pred[2]

    Y_Loss = pred[4]

    Y_Aq_Gas = Y_Aq + Y_Gas + Y_Loss

    return Y_Char, Y_Crude, Y_Aq, Y_Gas, Y_Loss, Y_Aq_Gas

mod_Qian2020 = def_mod('Qian2020',10,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['Lipids wt%','b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],[],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S1385894720303880

Obeid2020
"""

def Obeid2020_mono_oil(const):

    Lip, time, T, b = const
    
    time = time

    Temp = T + 273
    if time == 0:
        time = 0.00001

    def my_ls_func_oil(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_oil = (0, 0, 1, 0)

        def ode_oil(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 8.314
            """
            Oil
            """

            x1 = x[0]
            x2 = x[1]
            x3 = x[3]

            k1 = math.exp(7.2-(16100/(R*Temp)))
            k2 = math.exp(16.7-(67500/(R*Temp)))
            k3 = math.exp(11.9-(40100/(R*Temp)))
            k4 = math.exp(0.6-(100/(R*Temp)))
            k5 = math.exp(-0.3-(6700/(R*Temp)))

            sol = [-k1*x1 + k4*x3, -k3*x2 + k1*x1 +
                    k2*x3, -(k2+k4+k5)*x3 + k3*x2, k5*x3]

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_oil(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_oil, t_eval=[time], method='Radau')

        pred_oil = np.transpose(r.y)

        return pred_oil[0]

    pred_oil = my_ls_func_oil(time, Temp)*100
   

    Y_Char =  pred_oil[0]

    Y_Crude = pred_oil[2]

    Y_Aq = pred_oil[1]

    Y_Gas = pred_oil[3]

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2020_mono_oil = def_mod('Obeid2020_mono_oil',5*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Lipids wt%'],['Lipids wt%'],False)

def Obeid2020_mono_carb(const):

    Carb, time, T, b = const


    time = time
    
    Temp = T + 273
    if time == 0:
        time = 0.00001
    
    
    def my_ls_func_Carb(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Carb = (1, 0, 0, 0)
    
        def ode_Carb(x, t, Temp):
    
            if np.isfinite(b):
                Temp = Morse(t, b, Temp)
    
            R = 8.314
            """
            Carb
            """
            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
    
            k1 = math.exp(11.7-(46500/(R*Temp)))
            k2 = math.exp(3.8-(18800/(R*Temp)))
            k3 = math.exp(7.8-(29500/(R*Temp)))
            k4 = math.exp(10-(32200/(R*Temp)))
            k5 = math.exp(1.9-(12600/(R*Temp)))
    
            sol = [-k1*x1 + k4*x3, -(k3+k5)*x2 + k1 *
                    x1 + k2*x3, -(k2+k4)*x3 + k3*x2, k5*x2]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Carb(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"
    
        r = solve_ivp(f2, (0, time), x0_Carb, t_eval=[time], method='Radau')
    
        pred_Carb = np.transpose(r.y)
    
        return pred_Carb[0]
    
    pred_Carb = my_ls_func_Carb(time, Temp)*100
    
       
    
    Y_Char = pred_Carb[0]
    
    Y_Crude = pred_Carb[2]
    
    Y_Aq = pred_Carb[1]
    
    Y_Gas = pred_Carb[3]
    
    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2020_mono_carb = def_mod('Obeid2020_mono_carb',5*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%'],['Carbs wt%'],False)

def Obeid2020_mono_prot(const):

    Prot, time, T, b = const


    time = time

    Temp = T + 273
    if time == 0:
        time = 0.00001


    def my_ls_func_Prot(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Prot = (.32, .68, 0, 0)

        def ode_Prot(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 8.314
            """
            Prot
            """
            x1 = x[0]
            x2 = x[1]
            x3 = x[2]

            k1 = math.exp(12-(42100/(R*Temp)))
            k2 = math.exp(12.8-(45400/(R*Temp)))
            k3 = math.exp(10.2-(43800/(R*Temp)))
            k4 = math.exp(2.6-(8500/(R*Temp)))
            k5 = math.exp(-0.8-(1900/(R*Temp)))

            sol = [-k1*x1 + k4*x2, -(k3+k4+k5)*x2 +
                    k1*x1 + k2*x3, -k2*x3 + k3*x2, k5*x2]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Prot(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0_Prot, t_eval=[time], method='Radau')

        pred_Prot = np.transpose(r.y)

        return pred_Prot[0]

    pred_Prot = my_ls_func_Prot(time, Temp)*100


    Y_Char = pred_Prot[0]

    Y_Crude = pred_Prot[2]

    Y_Aq = pred_Prot[1]

    Y_Gas = pred_Prot[3]

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2020_mono_prot = def_mod('Obeid2020_mono_prot',5*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Protein wt%'],['Protein wt%'],False)



def Obeid2020_mono_lig(const):

    Lig, time, T, b = const
    
    time = time
    
    Temp = T + 273
    if time == 0:
        time = 0.00001
    
    
    def my_ls_func_Lig(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0_Lig = (.369, (1-.369), 0)
    
        def ode_Lig(x, t, Temp):
    
            if np.isfinite(b):
                Temp = Morse(t, b, Temp)
    
            R = 8.314
            """
            Lig
            """
            x2 = x[0]
            x3 = x[1]
    
            k1 = math.exp(5.2-(8300/(R*Temp)))
            k2 = math.exp(4.6-(2800/(R*Temp)))
            k3 = math.exp(3.1-(21700/(R*Temp)))
    
            sol = [-k2*x2 + k1*x3, -(k1+k3)*x3 + k2*x2, k3*x3]
            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode_Lig(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"
    
        r = solve_ivp(f2, (0, time), x0_Lig, t_eval=[time], method='Radau')
        pred_Lig = np.transpose(r.y)
    
        return pred_Lig[0]
    
    pred_Lig = my_ls_func_Lig(time, Temp)*100
    
    Y_Char = 0
    
    Y_Crude = pred_Lig[1]
    
    Y_Aq = pred_Lig[0]
    
    Y_Gas = pred_Lig[2]
    
    Y_Aq_Gas = Y_Aq + Y_Gas



    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2020_mono_lig = def_mod('Obeid2020_mono_lig',3*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Lignin wt%'],['Lignin wt%'],False)


"""
https://www.sciencedirect.com/science/article/pii/S1385894721021628

Chacon-Parra 2021
"""

def Chacon_Parra2021(const):
    prot, time, T, b = const
        
    Temp = T + 273
    if time == 0:
        time = 0.01

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (0.32, 0.68, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = .008314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]

            k1F = math.exp(11.4-(59.630/(R*Temp)))
            k2F = math.exp(7.07-(38.100/(R*Temp)))
            try:
                k3F = math.exp(-81.26-(303.920/(R*Temp)))
                if k3F > 10**100:
                    k3F = 0                    
            except:
                k3F = 0
            k4F = math.exp(12.58-(77.080/(R*Temp)))
            k5R = math.exp(-14.76-(-27.940/(R*Temp)))
            k6R = math.exp(-1.15-(10.850/(R*Temp)))
            k7R = math.exp(5.6-(40.810/(R*Temp)))
            k8R = math.exp(9.33-(56.190/(R*Temp)))

            sol = [-(k1F+k2F)*x1 + k5R*x2 + k6R*x3, k1F*x1 + k7R*x3 + k8R*x4 -
                    (k3F+k4F+k5R)*x2, k2F*x1 + k3F*x2 - (k6R+k7R)*x3, k4F*x2 - k8R*x4]
            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"
        

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    def my_ls_funcN(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (0.3, 0.5, 0.15, 0.1, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            xN1 = x[0]
            xN2 = x[1]
            xN3 = x[2]
            xN4 = x[3]
            xN5 = x[4]
            xN6 = x[5]

            if Temp <= 275:
                k1F = math.exp(-1.77)
                k2F = math.exp(-3.19)
                k3F = math.exp(-10.08)
                k4F = math.exp(-3.94)
                k5F = math.exp(-3.55)
                k6F = math.exp(-2.98)
                k7F = math.exp(-5.41)
                k8R = math.exp(-4.66)
                k9R = math.exp(-6.44)
                k10R = math.exp(-11.52)
                k11R = math.exp(-3.83)
                k12R = math.exp(1.14)
                k13R = math.exp(-0.82)
                k14R = math.exp(-9.17)
            elif Temp > 275 and Temp <= 325:
                k1F = math.exp(-0.55)
                k2F = math.exp(-2.25)
                k3F = math.exp(-3.29)
                k4F = math.exp(-2.34)
                k5F = math.exp(-22.7)
                k6F = math.exp(-2.54)
                k7F = math.exp(-5.66)
                k8R = math.exp(-8.71)
                k9R = math.exp(-2.53)
                k10R = math.exp(-3)
                k11R = math.exp(-2.41)
                k12R = math.exp(-3.09)
                k13R = math.exp(-6.42)
                k14R = math.exp(-3.58)
            else:
                k1F = math.exp(-0.19)
                k2F = math.exp(-1.73)
                k3F = math.exp(-5.55)
                k4F = math.exp(-1)
                k5F = math.exp(-8.84)
                k6F = math.exp(-2.75)
                k7F = math.exp(-4.84)
                k8R = math.exp(-8.98)
                k9R = math.exp(-4.32)
                k10R = math.exp(-9.21)
                k11R = math.exp(-0.95)
                k12R = math.exp(-7.78)
                k13R = math.exp(-7.98)
                k14R = math.exp(-2.73)

            sol = [-(k1F+k2F)*xN1 + k8R*xN2 + k9R*xN3, k1F*xN1 + k10R*xN3 + k11R*xN4 - (k3F+k4F+k5F+k7F+k8R)*xN2, k2F*xN1 + k3F *
                    xN2 - (k9R+k10R)*xN3, k4F*xN2 - k11R*xN4, k5F*xN2 + k13R*xN6 - (k12R+k6F)*xN5, k7F*xN2 + k6F*xN5 - (k13R+k14R)*xN6]
            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    pred = my_ls_func(time, Temp)

    Y_Char = pred[0]*100

    Y_Crude = pred[2]*100

    Y_Aq = pred[1]*100

    Y_Gas = pred[3]*100

    pred = my_ls_funcN(time, Temp)

    N_Char = pred[0]*100

    N_Crude = pred[2]*100

    N_Aq = (pred[1] + pred[3] + pred[4])*100

    N_gas = pred[5]*100

    Y_Aq_Gas = Y_Aq + Y_Gas


    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas, N_Char, N_Crude, N_Aq, N_gas

mod_Chacon_Parra2021 = def_mod('Chacon_Parra2021',8*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Protein wt%'],['Protein wt%'],False)


"""
https://www.sciencedirect.com/science/article/pii/S1385894721028096 


Obeid 2022
"""

def Obeid2022_algae(const):

    Carb, Prot, Lip, time, T, b = const

    time = time*60

    Temp = T + 273
    if time == 0:
        time = 0.00001
    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Lip/100, Carb/100, Prot/100, 0, 0, 0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 0.008314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]
            x5 = x[4]
            x6 = x[5]
            x7 = x[6]
            x8 = x[7]

            k1 = math.exp(28.05-(130.76/(R*Temp)))
            k2 = math.exp(3.56-(3.94/(R*Temp)))
            k3 = math.exp(8.84-(26.54/(R*Temp)))
            k4 = math.exp(2.31-(2.31/(R*Temp)))
            k5 = math.exp(25.53-(119.51/(R*Temp)))
            k6 = math.exp(3.24-(0.28/(R*Temp)))
            k7 = 0
            k8 = 0
            k9 = math.exp(27.85-(119.41/(R*Temp)))
            k10 = math.exp(31.6-(140.19/(R*Temp)))
            k11 = math.exp(1.47-(13.85/(R*Temp)))
            k12 = math.exp(9.96-(49.9/(R*Temp)))
            k13 = math.exp(1.47-(13.85/(R*Temp)))
            k14 = math.exp(-0.97-(1.03/(R*Temp)))
            k15 = math.exp(3.63-(3.56/(R*Temp)))
            k16 = math.exp(-0.97-(1.03/(R*Temp)))
            k17 = math.exp(3.9-(8.87/(R*Temp)))

            sol = [-(k1+k2)*x1, -(k3+k4)*x2, -(k5+k6)*x3, -(k7+k8)*x4, -(k10+k13)*x5 + k3*x2 + k5*x3 + k7*x4 + k9*x6 + k14*x7, -(k9 + k12 + k15)*x6 + k1*x1 + k4*x2 + k6*x3 + k8*x4 + k10*x5 + k11*x7 + k17*x8, -(k11+k14+k16)*x7 + k2*x1 + k12*x6 + k13*x5, -k17*x8 + k15*x6 + k16*x7]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            sol = [item if math.isfinite(item) or item < 0 else 0 for item in sol]

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    pred = my_ls_func(time, Temp)

    Y_Char = (pred[0]+pred[1]+pred[2]+pred[3]+pred[4])*100

    Y_Crude = pred[6]*100

    Y_Aq = pred[5]*100

    Y_Gas = pred[7]*100

    Y_Aq_Gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas


mod_Obeid2022_algae = def_mod('Obeid2022_algae',15*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

def Obeid2022_Sludge(const):

    Carb, Prot, Lip, Lig, time, T, b = const

    time = time*60

    Temp = T + 273

    if time == 0:
        time = 0.00001

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Lip/100, Carb/100, Prot/100, Lig/100, 0, 0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 0.008314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]
            x5 = x[4]
            x6 = x[5]
            x7 = x[6]
            x8 = x[7]

            k1 = math.exp(4.21-(0.59/(R*Temp)))
            k2 = math.exp(9.31-(33.25/(R*Temp)))
            k3 = math.exp(4.2-(0.55/(R*Temp)))
            k4 = math.exp(5.8-(8.75/(R*Temp)))
            k5 = math.exp(7.62-(18.53/(R*Temp)))
            k6 = math.exp(5.4-(8.26/(R*Temp)))
            k7 = math.exp(8.61-(24.2/(R*Temp)))
            k8 = math.exp(5.63-(8.07/(R*Temp)))
            k9 = math.exp(1.47-(13.85/(R*Temp)))
            k10 = math.exp(6.08-(31.6/(R*Temp)))
            k11 = math.exp(11.5-(45.2/(R*Temp)))
            k12 = math.exp(6.27-(26.02/(R*Temp)))
            k13 = math.exp(15.4-(71.22/(R*Temp)))
            k14 = math.exp(1.47-(13.85/(R*Temp)))
            k15 = math.exp(18.75-(77.72/(R*Temp)))
            k16 = math.exp(1.47-(13.85/(R*Temp)))
            k17 = math.exp(18.06-(70.22/(R*Temp)))

            sol = [-(k1+k2)*x1, -(k3+k4)*x2, -(k5+k6)*x3, -(k7+k8)*x4, -(k10+k13)*x5 + k3*x2 + k5*x3 + k7*x4 + k9*x6 + k14*x7, -(k9 + k12 + k15) *x6 + k1*x1 + k4*x2 + k6*x3 + k8*x4 + k10*x5 + k11*x7 + k17*x8, -(k11+k14+k16)*x7 + k2*x1 + k12*x6 + k13*x5, -k17*x8 + k15*x6 + k16*x7]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    pred = my_ls_func(time, Temp)

    Y_Char = (pred[0]+pred[1]+pred[2]+pred[3]+pred[4])*100

    Y_Crude = pred[6]*100

    Y_Aq = pred[5]*100

    Y_Gas = pred[7]*100

    Y_Aq_Gas = Y_Aq + Y_Gas

    return  Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2022_Sludge = def_mod('Obeid2022_Sludge',17*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)

def Obeid2022_Pinwood(const):

    Carb, Prot, Lip, Lig, time, T, b = const

    Temp = T + 273

    time = time*60

    if time == 0:
        time = 0.00001

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (Lip/100, Carb/100, Prot/100, Lig/100, 0, 0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 0.008314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]
            x4 = x[3]
            x5 = x[4]
            x6 = x[5]
            x7 = x[6]
            x8 = x[7]

            k1 = math.exp(9.26-(29.38/(R*Temp)))
            k2 = math.exp(1.86-(5.46/(R*Temp)))
            k3 = math.exp(4.2-(0.55/(R*Temp)))
            k4 = math.exp(16.76-(70.02/(R*Temp)))
            k5 = math.exp(22.72-(93.62/(R*Temp)))
            k6 = math.exp(18.55-(78.02/(R*Temp)))
            k7 = math.exp(4.12-(0.08/(R*Temp)))
            k8 = math.exp(15.1-(62.56/(R*Temp)))
            k9 = math.exp(9.37-(29.2/(R*Temp)))
            k10 = math.exp(13.1-(47.45/(R*Temp)))
            k11 = math.exp(-0.04-(5.22/(R*Temp)))
            k12 = math.exp(10.53-(52.54/(R*Temp)))
            k13 = math.exp(1.47-(13.85/(R*Temp)))
            k14 = math.exp(2.52-(1.46/(R*Temp)))
            k15 = math.exp(12.61-(49.11/(R*Temp)))
            k16 = math.exp(1.47-(13.85/(R*Temp)))
            k17 = math.exp(12.46-(45.03/(R*Temp)))

            sol = [-(k1+k2)*x1, -(k3+k4)*x2, -(k5+k6)*x3, -(k7+k8)*x4, -(k10+k13)*x5 + k3*x2 + k5*x3 + k7*x4 + k9*x6 + k14*x7, -(k9 + k12 + k15) *x6 + k1*x1 + k4*x2 + k6*x3 + k8*x4 + k10*x5 + k11*x7 + k17*x8, -(k11+k14+k16)*x7 + k2*x1 + k12*x6 + k13*x5, -k17*x8 + k15*x6 + k16*x7]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    if time == 0:
        pred = (Prot, Lip, Carb, 0, 0, 0, 0)
    else:
        pred = my_ls_func(time, Temp)

    Y_Char = (pred[0]+pred[1]+pred[2]+pred[3]+pred[4])*100

    Y_Crude = pred[6]*100

    Y_Aq = pred[5]*100

    Y_Gas = pred[7]*100

    Y_Aq_Gas = Y_Aq + Y_Gas

    return  Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Obeid2022_Pinwood = def_mod('Obeid2022_Pinwood',17*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)


"""
https://link.springer.com/article/10.1007/s13399-022-03019-6

Saral 2022
"""


def Saral2022(const):

    time, T, b = const

    Temp = T + 273

    if time == 0:
        time = 0.00001

    def my_ls_func(time, Temp):
        """definition of function for LS fit
            x gives evaluation points,
            teta is an array of parameters to be varied for fit"""
        x0 = (1, 0, 0, 0)

        def ode(x, t, Temp):

            if np.isfinite(b):
                Temp = Morse(t, b, Temp)

            R = 0.008314

            x1 = x[0]
            x2 = x[1]
            x3 = x[2]

            k1 = math.exp(-0.16-(9.87/(R*Temp)))
            k2 = math.exp(-1.60-(11.15/(R*Temp)))
            k3 = math.exp(0.85-(10.39/(R*Temp)))
            k4 = math.exp(0.66-(10.12/(R*Temp)))
            k5 = math.exp(4.22-(47.37/(R*Temp)))
            k6 = math.exp(-4.42-(17.69/(R*Temp)))

            sol = [-(k1+k2)*x1, k1*x1 + k3*x3 - (k4+k5)*x2, k2*x1 + k4*x2 - (k3+k6) *x3, k5*x2 + k6*x3]

            # S1 , S2, B1, B2, B12, Aq1, Aq2, Aq12, G1, G2, G12, S_new1, S_new2, S_new12

            return sol
        # create an alias to f which passes the optional params
        def f2(t, y): return ode(y, t, Temp)
        # calculate ode solution, retuen values for each entry of "x"

        r = solve_ivp(f2, (0, time), x0, t_eval=[time], method='Radau')

        pred = np.transpose(r.y)

        return pred[0]

    pred = my_ls_func(time, Temp)

    Y_Char = pred[0]*100

    Y_Crude = pred[2]*100

    Y_Aq = pred[1]*100

    Y_Gas = pred[3]*100

    Y_Aq_Gas = Y_Aq + Y_Gas

    return Y_Char, Y_Crude, Y_Aq, Y_Gas,  Y_Aq_Gas

mod_Saral2022 = def_mod('Saral2022',6*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],[],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S1385894720331351

Hietala et al 2021
"""

def Hietala2021():
    return

eng = matlab.engine.start_matlab()

eng.eval("warning off", nargout=0)

mod_Hietala2021 = def_mod('Hietala2021',16*2,['Temperature (C)','Solid content (w/w) %'],[['Total time (min)','Holding Time (min)']],['Ash wt%','b'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas wt%','Loss','Gas + Loss','Aq + Gas wt%','C% B','N% B','C% S','N% S'],['Carbs wt%','Protein wt%','Lipids wt%'],[],True)

eng.quit()

"""
https://www.sciencedirect.com/science/article/pii/S0960852410010096

Biller et al 2011
"""


def Biller2011(const):

    t_0 = 60

    temp_0 = 350

    Carb, Prot, Lip, time, temp = const

    if is_lnsi(time,temp,t_0,temp_0):

        k = [ 0.8, 0.18, 0.06]

        Y_Crude = k[0]*Lip + k[1]*Prot + k[2]*Carb

    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Biller2011 = def_mod('Biller2011',3,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://pubs.acs.org/doi/10.1021/ef501760d

Teri et al 2014
"""

def Teri2014_3(const):

    Carb,  Prot, Lip, Time, Temp = const

    SI_lim = 0.52
 
    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))
 
    SI_min = np.log(20*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_max = np.log(60*np.exp(-21000/8.314*(1/(350+273.15)-1/(700))))
 
    xL,xC,xP = Lip/100,Carb/100,Prot/100
 
    if SI >= SI_min - SI_lim and SI < (SI_min+SI_max)/2 :
 
        k = [ 95.1, 5.8, 33.4, -1.6, 27.1, -1.9]
 
        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP
 
    elif SI <= SI_max + SI_lim and SI > (SI_min+SI_max)/2:
 
        k = [ 93.8, 12.2, 34.7, -0.3, -20.5, 40.2]
 
        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP
    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Teri2014_3 = def_mod('Teri2014_3',6*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


def Teri2014_4(const):

    Carb,  Prot, Lip, Time, Temp = const

    SI_lim = 0.52

    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(20*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_max = np.log(60*np.exp(-21000/8.314*(1/(350+273.15)-1/(700))))

    xL,xC,xP = Lip/100,Carb/100,Prot/100

    if SI >= SI_min - SI_lim and SI < (SI_min+SI_max)/2 :

        k = [ 94.9, 6.1, 31.6, -21.2, 35.9, 3.8]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP

    elif SI <= SI_max + SI_lim and SI > (SI_min+SI_max)/2:

        k = [ 85.2, 11.9, 34.0, 10.2, -2.4, 33.6]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP

    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Teri2014_4 = def_mod('Teri2014_4',6*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

def Teri2014_1(const):

    Carb,  Prot, Lip, Time, Temp = const

    SI_lim = 0.52

    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(20*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_max = np.log(60*np.exp(-21000/8.314*(1/(350+273.15)-1/(700))))

    xL,xC,xP = Lip/100,Carb/100,Prot/100

    if SI >= SI_min - SI_lim and SI < (SI_min+SI_max)/2 :

        k = [ 95.1, 5.8, 33.4, 0, 0, 0]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP

    elif SI <= SI_max + SI_lim and SI > (SI_min+SI_max)/2:

        k = [ 93.8, 12.2, 34.7, 0, 0, 0]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP
    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Teri2014_1 = def_mod('Teri2014_1',3*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


def Teri2014_2(const):

    Carb,  Prot, Lip, Time, Temp = const

    SI_lim = 0.52

    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(20*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_max = np.log(60*np.exp(-21000/8.314*(1/(350+273.15)-1/(700))))

    xL,xC,xP = Lip/100,Carb/100,Prot/100

    if SI >= SI_min - SI_lim and SI < (SI_min+SI_max)/2 :

        k = [ 94.9, 6.1, 31.6, 0, 0, 0]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP

    elif SI <= SI_max + SI_lim and SI > (SI_min+SI_max)/2:

        k = [ 85.2, 11.9, 34.0, 0, 0, 0]

        Y_Crude = k[0]*xL + k[1]*xC + k[2]*xP + k[3]*xL*xC + k[4]*xL*xP + k[5]*xC*xP

    else:
        Y_Crude = np.nan

    return Y_Crude


mod_Teri2014_2 = def_mod('Teri2014_2',3*2,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://pubs-rsc-org.ezaccess.libraries.psu.edu/en/content/articlelanding/2015/GC/C5GC00574D

Leow et al 2015
"""


def Leow2015(const):

    Carb, Prot, Lip, time, temp, N_biomass = const

    if is_lnsi(time, temp, 30, 300):

        k = [ 0.97, 0.42, 0.17]

        Y_Crude = k[0]*Lip + k[1]*Prot + k[2]*Carb

        if np.isfinite(N_biomass):
            N_Crude = 0.726*N_biomass
        else:
            N_Crude = np.nan
    else:
        Y_Crude, N_Crude = np.nan, np.nan


    return Y_Crude, N_Crude

mod_Leow2015 = def_mod('Leow2015',3,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['N%'],['Biocrude wt%',"N% B"],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
https://link.springer.com/article/10.1007/s12649-016-9726-7

Déniel et al 2017

"""


def Deniel2017(const):

    Cell, Prot, Lip, lig, time, temp = const

    if is_lnsi(time, temp, 30, 300):

        x1, x2, x3, x4 = Cell/100,Prot/100, lig/100, Lip/100

        Y_Crude = (0.05*x1 + 0.95*x4 + 0.18*x1*x2 + 0.79*x1*x3 + 0.45*x1*x4 + 0.23*x2*x3 + 0.44*x2*x4 - 0.3*x3*x4)*100

        Y_char = (0.33*x1 + 0.64*x3)*100

        Y_gas = (0.1*x1 + 0.05*x2 + 0.04*x3 + 0.32*x1*x2 + 0.16*x1*x3 - 0.03*x1*x4 + 0.16*x2*x3 - 0.02*x2*x4 + 0.01*x3*x4)*100

        Y_Aq = (0.48*x1 + 0.05*x2 + 0.68*x3 + 0.95*x4 + 0.5*x1*x2 + 0.94*x1*x3 + 0.42*x1*x4 + 0.39*x2*x3 + 0.42*x2*x4 - 0.28*x3*x4)*100

        Y_Aq_gas = Y_gas + Y_Aq

    else:
        Y_char, Y_Crude, Y_Aq, Y_gas, Y_Aq_gas = np.nan,np.nan,np.nan,np.nan,np.nan

    return  Y_char, Y_Crude, Y_Aq , Y_gas, Y_Aq_gas

mod_Deniel2017 = def_mod('Deniel2017',8,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%'],['Carbs wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)


"""
https://pubs.rsc.org/en/content/articlehtml/2017/gc/c6gc03294j

Li et al 2017
"""

def Li2017(const):

    C, P, L, t, temp, A, C_mass, H_mass, O_mass, N_mass, HHV_mass = const


    if is_lnsi(t, temp, 30, 300):

        Y_Crude = 0.85*L + 0.45*P + 0.22*C

        Y_char = 0.41*C + 0.18*A

        Y_gas = 0.07*P + 0.46*C

        Y_Aq = 0.24*P + 0.86*A

        N_Crude = 0.133*P

        TOC_Aq = 478*P/1000

        TN_Aq = 251*P/1000

        C_char = 1.75*C

        check = True

        for i in C_mass, H_mass, O_mass, N_mass:
            if not np.isfinite(i):
                check = False

        if check == True:

            AOS_c = (3*N_mass/14 + 2*O_mass/16 - H_mass)/(C_mass/12)

            C_Curde = -8.37*AOS_c + 68.55

            H_Crude = -2.61*AOS_c + 8.2

            O_Crude = 100-(C_Curde+H_Crude+N_Crude)

            HHV_Crude = 30.74 -8.52*AOS_c + 0.024*P

        else:
            C_Curde = np.nan

            H_Crude = np.nan

            O_Crude = np.nan

            HHV_Crude = np.nan

        if check == True and np.isfinite(HHV_mass):

            ER_Crude = (0.85*L + 0.45*P + 0.22*C)*HHV_Crude/HHV_mass

        else:

            ER_Crude = np.nan

        Y_Aq_gas = Y_Aq + Y_gas

    else:
        Y_char, Y_Crude, Y_Aq, Y_gas, Y_Aq_gas, C_Curde, H_Crude, O_Crude, N_Crude, TOC_Aq, TN_Aq, C_char, HHV_Crude, ER_Crude = np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, np.nan, np.nan, np.nan, np.nan,np.nan, np.nan, np.nan, np.nan

    return Y_char, Y_Crude, Y_Aq, Y_gas, Y_Aq_gas, C_Curde, H_Crude, O_Crude, N_Crude, TOC_Aq, TN_Aq, C_char, HHV_Crude, ER_Crude

mod_Li2017 = def_mod('Li2017',3,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],['Ash wt%','C%','H%','O%','N%','HHV Biomass'],['Solids wt%','Biocrude wt%','Aquous wt%','Gas + Loss','Aq + Gas wt%','C% B','H% B','O% B','N% B','TOC mg/L','TN mg /L','C% S','HHV Bio','Energy Recovery'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S0960852417311409

Shakya et al 2017
"""

def Shakya2017(const):
    C, P, L, time, Temp = const

    SI_lim = 0.52

    SI = np.log(time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(30*np.exp(-21000/8.314*(1/(280+273.15)-1/(700))))
    SI_max = np.log(30*np.exp(-21000/8.314*(1/(320+273.15)-1/(700))))

    if SI >= SI_min - SI_lim and SI < (SI_min+SI_max)/2 :

        Y_Crude = 0.9*L + 0.22*C + 0.32*P
    elif SI <= SI_max + SI_lim and SI > (SI_min+SI_max)/2:
        Y_Crude = 0.96*L + 0.3*C + 0.43*P
    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Shakya2017 = def_mod('Shakya2017',6,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S2211926417305477

Hietala et al 2017

"""


def Hietala2017(const):

    C,P,L, t, temp = const


    L , P, C =  L/100 , P/100, C/100

    if is_lnsi(t, temp, 20, 250):
        r_sat = 0.394

        r_mon = 0.158

        sat = L*r_sat

        mon = L*r_mon

        pol = L*(1-(r_sat+r_mon))

        k = [ 10.7, 575,0,0,0,0,0,-4130,0,65, 51.2,223,0,0,-1170,0,0,316,-514,547,0]

        Y_crude = k[0] + k[1]*sat + k[2]*mon + k[3]*pol + k[4]*P + k[5]*C + k[6]*sat**2 + k[7]*mon**2 + k[8]*pol**2 + k[9]*P**2 + k[10]*C**2 + k[11]*sat*mon + k[12]*sat*pol + k[13]*sat*P + k[14]*sat*C + k[15]*mon*pol + k[16]*mon*P + k[17]*mon*C + k[18]*pol*P + k[19]*pol*C + k[20]*P*C 

        k = [ 1.43, 0,0,0,0,0,0,148,0,0, -0.198,-134,0,0,5.7,0,0,0,0,0,0]

        H_C_crude = k[0] + k[1]*sat + k[2]*mon + k[3]*pol + k[4]*P + k[5]*C + k[6]*sat**2 + k[7]*mon**2 + k[8]*pol**2 + k[9]*P**2 + k[10]*C**2 + k[11]*sat*mon + k[12]*sat*pol + k[13]*sat*P + k[14]*sat*C + k[15]*mon*pol + k[16]*mon*P + k[17]*mon*C + k[18]*pol*P + k[19]*pol*C + k[20]*P*C 

        k = [ 4.16, 0, 87.2, 0, 0, 0, 0, -1070, 0, 0, -3.08, 0, 195, 0, -11.3, 0, -183, 0, 0, 0, 11.4 ]

        N_crude = k[0] + k[1]*sat + k[2]*mon + k[3]*pol + k[4]*P + k[5]*C + k[6]*sat**2 + k[7]*mon**2 + k[8]*pol**2 + k[9]*P**2 + k[10]*C**2 + k[11]*sat*mon + k[12]*sat*pol + k[13]*sat*P + k[14]*sat*C + k[15]*mon*pol + k[16]*mon*P + k[17]*mon*C + k[18]*pol*P + k[19]*pol*C + k[20]*P*C 

        k = [ 18.6, 0, -761, 0, 0, 0, 0, 2140, 0, 0, 0, 0, 0, 0, 0, 0, 912, 765, 33.2, 0, -37.5]

        O_crude = k[0] + k[1]*sat + k[2]*mon + k[3]*pol + k[4]*P + k[5]*C + k[6]*sat**2 + k[7]*mon**2 + k[8]*pol**2 + k[9]*P**2 + k[10]*C**2 + k[11]*sat*mon + k[12]*sat*pol + k[13]*sat*P + k[14]*sat*C + k[15]*mon*pol + k[16]*mon*P + k[17]*mon*C + k[18]*pol*P + k[19]*pol*C + k[20]*P*C 

        k = [ 35.8, 49.3, 0, -82.8, 0, 0, -642, 0, 0, -14.5, 0, 0, 0, 0, 0, 0, 0, 0, 208, 0, 0]

        HHV_crude = k[0] + k[1]*sat + k[2]*mon + k[3]*pol + k[4]*P + k[5]*C + k[6]*sat**2 + k[7]*mon**2 + k[8]*pol**2 + k[9]*P**2 + k[10]*C**2 + k[11]*sat*mon + k[12]*sat*pol + k[13]*sat*P + k[14]*sat*C + k[15]*mon*pol + k[16]*mon*P + k[17]*mon*C + k[18]*pol*P + k[19]*pol*C + k[20]*P*C

    else:
        Y_crude, H_C_crude, N_crude, O_crude, HHV_crude = np.nan, np.nan, np.nan, np.nan, np.nan

    return Y_crude, H_C_crude, N_crude, O_crude, HHV_crude

mod_Hietala2017 = def_mod('Hietala2017',10,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%','H/C% B','N% B','O% B','HHV Bio'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0306261918310110

Yang et al 2018
"""


def Yang2018(const):

    Cell, Hemi, Prot, Lip, Lig,t,temp  = const

    if is_lnsi(t, temp, 10, 290):

        x1, x2, x3, x4, x5 = Prot/100, Hemi/100, Cell/100, Lig/100, Lip/100

        Y_Crude = 19.88*x1 + 4.29* x2 + 12* x3 + 2.13*x4 + 95.18*x5 + 59.04*x2*x5 + 37.94*x3*x5

        Y_char = 5.88*x1 + 21.04* x2 + 31.65* x3 + 39.29*x4 + 0.57*x5 - 86.33*x3*x4

    else:
        Y_char, Y_Crude = np.nan, np.nan

    return Y_char, Y_Crude

mod_Yang2018 = def_mod('Yang2018',7,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Solids wt%','Biocrude wt%'],['Cellulose wt%','Hemicellulose wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)


"""
https://pubs.acs.org/doi/10.1021/acssuschemeng.8b03156

Lu et al 2018
"""

def Lu2018(const):

    Cell, Hemi, Prot, Lip, Lig, t, temp  = const

    if is_lnsi(t, temp, 10, 290):

        Lip, Prot, Cell, Hemi, Lig = Lip/100, Prot/100, Cell/100, Hemi/100, Lig/100

        Y_Crude = 82*Lip + 21.1*Prot + 4.57*Cell + 6.57*Hemi + 1.39*Lig - 73.9*Lip*Lig + 47.9*Prot*Cell + 46.2*Prot*Hemi + 45.6*Prot*Lig + 111.1*Cell*Lig + 67.5*Hemi*Lig

        C_Crude = 75.6*Lip + 74.3*Prot + 72.8*Cell + 73.2*Hemi + 70.1*Lig + 6.5*Lip*Cell + 9.24*Lip*Lig + 9.01*Prot*Cell + 8.63*Prot*Hemi + 8.49*Cell*Hemi + 24.9*Cell*Lig + 13.1*Hemi*Lig

        H_Crude = 11.7*Lip + 9.41*Prot + 6.84*Cell + 6.48*Hemi + 7.48*Lig + 3.11*Lip*Prot + 7.57*Lip*Cell + 9.25*Lip*Hemi + 4.45*Lip*Lig  + 2.33*Cell*Hemi

        N_Crude = 0.22*Lip + 6.34*Prot + 0.23*Cell + 0.12*Hemi + 0.29*Lig + 14.5*Prot*Cell + 14.9*Prot*Hemi + 3.5*Prot*Lig

        O_Crube = 100- (C_Crude+ H_Crude+ N_Crude)

    else: 
        Y_Crude, C_Crude, H_Crude, O_Crube, N_Crude = np.nan, np.nan, np.nan, np.nan, np.nan

    return Y_Crude, C_Crude, H_Crude, O_Crube, N_Crude

mod_Lu2018 = def_mod('Lu2018',11,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%', 'C% B', 'H% B', 'O% B', 'N% B'],['Cellulose wt%','Hemicellulose wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0960852417313160

Sheng et al 2018
"""

def Sheng2018(const):

    Carb, Prot, Lip, t, temp = const


    if is_lnsi(t, temp, 60, 280):
        xL, xP, xC = Lip, Prot, Carb
        if xL == 0 or xP == 0 or xL-xP == 0 :
            LP = 0
        else:
            LP =  0.052*xL*xP/abs(xL-xP)

        if xL == 0 or xC == 0 or xL-xC == 0 :
            LC = 0
        else:
            LC =   0.093*xL*xC/abs(xL-xC)

        if xP == 0 or xC == 0 or xP-xC == 0 :
            PC = 0
        else:
            PC =   0.003*xP*xC/abs(xP-xC)
        Y_Crude = 0.9*xL + 0.385*xP + 0.025*xC + LP + LC + PC

    else:
        Y_Crude = np.nan

    return Y_Crude



mod_Sheng2018 = def_mod('Sheng2018',6,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S0960852416300906

Wagner et al 2016
"""

def Wagner2016(const):

    C, P, L,t, Temp = const

    SI_lim = 0.52

    SI = np.log(t*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min  = np.log(30*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_mid1 = np.log(30*np.exp(-21000/8.314*(1/(320+273.15)-1/(700))))
    SI_mid2 = np.log(30*np.exp(-21000/8.314*(1/(340+273.15)-1/(700))))
    SI_max  = np.log(30*np.exp(-21000/8.314*(1/(360+273.15)-1/(700))))


    if SI >= SI_min - SI_lim and SI < (SI_min+SI_mid1)/2 :
        Y_Crude = 0.96*L + 0.024*C + 0.161*P
    elif SI > (SI_min+SI_mid1)/2 and SI < (SI_mid1+SI_mid2)/2:  
        Y_Crude = 1.001*L + 0.033*C + 0.244*P
    elif SI > (SI_mid2+SI_mid1)/2 and SI < (SI_mid2+SI_max)/2:  
        Y_Crude = 1.006*L + 0.040*C + 0.210*P
    elif SI <= SI_max + SI_lim and SI > (SI_mid2+SI_max)/2:  
        Y_Crude = 1.013*L + 0.036*C + 0.286*P
    else:
        Y_Crude = np.nan

    return Y_Crude


mod_Wagner2016 = def_mod('Wagner2016',6,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

"""
# https://www.sciencedirect.com/science/article/pii/S096014811930655X

# Zhang et al 2019
# """

# def Zhang2019(const):

#     Time, Temp, Loading = const

#     if Time <= 60 and Time >= 10 and Temp <= 350 and Temp >= 280 and Loading >= 7  and Loading <= 20:

#         x1 = (2*Temp -350-280)/(350-280)
#         x2 = (2*Time -60 - 10)/(60-10)
#         x3 = (2*Loading -20-7)/(20-7)


#         Y_Crude = 9.49 + 1.64*x1 + 2.67*x2 + 5.680e-4*x3 + 1.38*x1*x2 + 0.37*x1*x3 - 0.8*x2*x3 + 0.66*x1**2                - 1.58*x1**2*x3

#         Y_Char = 27.67 - 5.29*x1 - 5.96*x2 + 8.96*x3     - 1.9*x1*x2  - 0.46*x1*x3 - 5.3*x2*x3 - 2.33*x1**2 + 7.3*x1**2*x2 - 12.34*x1**2*x3

#     else:
#         Y_Char,Y_Crude = np.nan, np.nan

#     return  Y_Char,Y_Crude


# mod_Zhang2019 = def_mod('Zhang2019',9,['Temperature (C)','Solid content (w/w) %'],[['Total time (min)','Holding Time (min)']],[],['Solids wt%','Biocrude wt%'],[],[],False)


"""
# https://www.sciencedirect.com/science/article/pii/S1743967118301788

# Zhuang et al 2019
# """

# def Zhuang2019(const):

#     Time, Temp,Loading = const

#     if Time <= 60 and Time >= 20 and Temp <= 300 and Temp >= 240 and Loading >= 5  and Loading <= 15:

#         xT = (2*Temp-300-240)/(300-240)
#         xD = (2*Time-60-20)/(60-20)
#         xR = (2*Loading-15-5)/(15-5)

#         ER = 28.70 + 11.45*xT + 2.09*xD + 1.92*xR - 1.15*xT*xD + 0.038*xT*xR + 0.61*xD*xR - 2.29*xT**2 + 1.54*xD**2 -0.004859*xR**2

#     else:
#         ER = np.nan
#     return ER

# mod_Zhuang2019 = def_mod('Zhuang2019',10,['Temperature (C)','Solid content (w/w) %'],[['Total time (min)','Holding Time (min)']],[],['Energy Recovery'],[],[],False)


"""
https://www.sciencedirect.com/science/article/pii/S0306261918315903

Yang et al 2019
"""

def Yang2019(const):

    Carb, Prot, Lip, Lig, Time, Temp, Loading = const

    water_ratio = (100-Loading)/Loading 
    
    SI_lim = 0.52
    
    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(5*np.exp(-21000/8.314*(1/(270+273.15)-1/(700))))
    SI_max = np.log(20*np.exp(-21000/8.314*(1/(320+273.15)-1/(700))))

    if SI >= SI_min - SI_lim and SI <= SI_max + SI_lim:
        x1, x2, x3, x4, x5, x6, x7 = Prot/100, Carb/100, Lig/100, Lip/100, (2*Temp-320-270)/(320-270), (2*Time-20-5)/(20-5), (2*water_ratio-12-6)/(12-6)
        
        Y_Crude = 19.99*x1 + 9.75* x2 + 1.75* x3 + 97.37*x4 - 33.1*x1*x4 + 26.4*x2*x3 + 59.8*x2*x4 - 65.6*x3*x4 -25.46*x3*x4*x5 - 18.93*x1*x4*x6 - 38.63*x1*x4*x7
        
        Y_char = (2.184*x1 + 5.396* x2 + 5.514* x3 + 0.87*x4 + 6.025*x1*x3 - 2.051*x2*x3 + 4.349*x3*x4 + 0.455*x3*x5 - 2.957*x1*x2*x5 - 3.396 * x2*x3*x5 - 1.838*x1*x2*x6 - 0.339*x2*x7 - 0.359*x3*x7)**2
    else:
        Y_Crude = np.nan
        Y_char = np.nan
    return  Y_char, Y_Crude

mod_Yang2019 = def_mod('Yang2019',11,['Temperature (C)','Solid content (w/w) %'],[['Total time (min)','Holding Time (min)']],[],['Solids wt%','Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)


"""

https://www.sciencedirect.com/science/article/pii/S0960852419304353?via%3Dihub

Aierzhati et al 2019
"""

def Aierzhati2019(const):

    C,P,L,Time,Temp = const

    SI_lim = 0.52

    SI = np.log(Time*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(10*np.exp(-21000/8.314*(1/(280+273.15)-1/(700))))
    SI_max = np.log(60*np.exp(-21000/8.314*(1/(360+273.15)-1/(700))))

    if SI >= SI_min - SI_lim and SI <= SI_max + SI_lim:

        Y_Crude = 1.61*L - 0.558*P - 0.00625*Time**2 + 0.00565*P**2 + 0.00324*Time*Temp + 0.0108*L*C - 0.00273*L*Temp - 0.00465*L*Time - 0.00772*C*Time
    else:
        Y_Crude = np.nan

    return Y_Crude

mod_Aierzhati2019 = def_mod('Aierzhati2019',9,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Carbs wt%','Protein wt%','Lipids wt%'],[],False)

# """ 
# https://www.sciencedirect.com/science/article/pii/S0048969720367474

# Hong et al 2021
# """

# def Hong2021(const):

#     Time ,Temp,Loading = const

#     if Time <= 180 and Time >= 80 and Temp <= 315 and Temp >= 260 and Loading >= 12  and Loading <= 18:

#         x1,x2,x3 = (Temp-280)/20,(Time-180)/60,(Loading-15)/3

#         k = [25.43, 0.46, -0.09, -0.52, 1.76, 0.18, -0.97, -2.08, -0.78]

#         Y_Crude = k[0] + k[1]*x1 + k[2]*x2 + k[3]*x1*x2 + k[4]*x1*x3 + k[5]*x2*x3 + k[6]*x1**2 + k[7]*x2**2 + k[8]*x3**2
#     else:
#         Y_Crude = np.nan

#     return Y_Crude



# mod_Hong2021 = def_mod('Hong2021',9,['Temperature (C)','Solid content (w/w) %'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],[],[],False)

"""
https://pubs.acs.org/doi/full/10.1021/acssuschemeng.1c04810

Subramanya et al 2021
"""


def Subramanya2021(const):

    Cell,Starch,Prot,Lip,Lig,t,Temp = const

    Cell,Lig,Starch,Prot,Lip = Cell/100,Lig/100,Starch/100,Prot/100,Lip/100

    SI_lim = 0.52

    SI = np.log(t*np.exp(-21000/8.314*(1/(Temp+273.15)-1/(700))))

    SI_min = np.log(30*np.exp(-21000/8.314*(1/(300+273.15)-1/(700))))
    SI_mid = np.log(30*np.exp(-21000/8.314*(1/(350+273.15)-1/(700))))
    SI_max = np.log(30*np.exp(-21000/8.314*(1/(425+273.15)-1/(700))))

    if  (SI_min - SI_lim) <= SI <= (SI_max + SI_lim):
        if SI < (SI_min+SI_mid)/2 :

            if Prot == 0 or Cell == 0:
                PC = 0
            else:
                PC = 0.0139*Prot*Cell/((Prot + Cell)**2) *Prot*Cell

            Y_Crude = 9.15*Cell + 5.24*Lig + 11.71*Starch + 24.66*Prot + 86.84*Lip + PC*100*100 + 0.00331*Starch*Prot*100*100 + 0.00459*Cell*Lig*100*100 + 0.00071*Starch*Lig*100*100 + 0.0023*Lip*Lig*100*100

        elif SI > (SI_max+SI_mid)/2 :

            Y_Crude = 3.27*Cell + 1.3*Lig + 4.26*Starch + 33.27*Prot + 11.85*Lip + 0.00128*Prot*Cell*100*100 + 0.00085*Starch*Prot*100*100 + 0.00591*Cell*Lig*100*100 + 0.00161*Starch*Lig*100*100 + 0.00153*Lip*Lig*100*100

        else:

            Y_Crude = 8.95*Cell + 3.54*Lig + 14.83*Starch + 27.8*Prot + 86.32*Lip + 0.00533*Prot*Cell*100*100 + 0.00218*Starch*Prot*100*100 + 0.00834*Cell*Lig*100*100 + 0.00028*Starch*Lig*100*100 - 0.00267*Lip*Lig*100*100

    else:
        Y_Crude = np.nan
    return Y_Crude


mod_Subramanya2021 = def_mod('Subramanya2021',30,['Temperature (C)'],[['Total time (min)','Holding Time (min)']],[],['Biocrude wt%'],['Cellulose wt%','Starch wt%','Protein wt%','Lipids wt%','Lignin wt%'],[],False)

"""
https://www.sciencedirect.com/science/article/pii/S0360544222014645

Yan et al 2022
"""
def Yan2022(const):

    Cell,Hemi,Lip,Lig,Temp = const

    x1,x2,x3,x4 = Cell/100,Hemi/100,Lig/100,Lip/100

    if  Temp <= 396 and Temp >= 268:
        x5 = ((Temp+273)-621)/48 #[-1,1] or [300,396]

        k = [ 27.71, -0.26, 26.27, -0.27, 35.11, -0.22, 44, -0.48, -7.73, 9.94, -0.45, 5.76, 2.02, 4.19, 16.25, 14.41, 0.81, 47.2, 0.57, -346]

        Y_Crude = k[0]*x1*(1+k[1]*x5) + k[2]*x2*(1+k[3]*x5)+ k[4]*x3*(1+k[5]*x5)+ k[6]*x4*(1+k[7]*x5) + k[8]*x1*x2*x5 + k[9]*x1*x3*(1+k[10]*x5) + k[11]*x1*x4*(1+k[12]*x5) + k[13]*x2*x3 + k[14]*x2*x4*x5 + k[15]*x3*x4*(1+k[16]*x5) + k[17]*x1*x2*x4*(1+k[18]*x5) + k[19]*x1*x2*x3*x5

        k2 = [ -0.15, 0, 0.77, 0, 13.18, -7.93/13.18, 6.77, 6.3/6.77, 0, -3.95, 0, 22.19, -20.85/22.19, 20.48, -22.57, 16.34, 20.39/16.34, 0, 0, 0]

        Y_solids = k2[0]*x1*(1+k2[1]*x5) + k2[2]*x2*(1+k2[3]*x5)+ k2[4]*x3*(1+k2[5]*x5)+ k2[6]*x4*(1+k2[7]*x5) + k2[8]*x1*x2*x5 + k2[9]*x1*x3*(1+k2[10]*x5) + k2[11]*x1*x4*(1+k2[12]*x5) + k2[13]*x2*x3 + k2[14]*x2*x4*x5 + k2[15]*x3*x4*(1+k2[16]*x5) + k2[17]*x1*x2*x4*(1+k2[18]*x5) + k2[19]*x1*x2*x3*x5

    else:
        Y_solids,Y_Crude = np.nan, np.nan
    return Y_solids,Y_Crude

mod_Yan2022 = def_mod('Yan2022',20,['Temperature (C)'],[],[],['Solids wt%','Biocrude wt%'],['Cellulose wt%','Hemicellulose wt%','Lipids wt%','Lignin wt%'],[],False)


out = pd.ExcelWriter('Data_out.xlsx')
def pri_vals(mod,test_in,test_out,biomass_in,exclu_biomass,col_n):
    if test_in == []:
        she_name = "All_res"
        she2_name = 'All_analysis'
        name = mod.fun.__name__
        name = pd.Series([name])
        name.to_excel(out,startcol=col  ,startrow =0,index=False,header=False,sheet_name = she_name)
        if test_out in mod.outputs:
            if len(mod.outputs) ==1:
                mod_res = [item for item in mod.res if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
                mod_res.to_excel(out,startcol=col ,startrow =1,index=False,header=False,sheet_name = she_name)
                anal = mod.get_anal(test_in,[],biomass_in)
                name.to_excel(out,startcol=0  ,startrow =col,index=False,header=False,sheet_name = she2_name)
                anal = pd.DataFrame(data=anal)
                anal = anal.T
                anal = anal.round(1)
                anal.to_excel(out, startcol=1  ,startrow =col,index=False,header=False,sheet_name = she2_name)
            else:
                mod_res = np.reshape(mod.res,(-1,len(mod.outputs)))
                ind = mod.outputs.index(test_out)
                mod_res = [item for item in mod_res[:,ind] if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
                mod_res.to_excel(out,startcol=col ,startrow =1,index=False,header=False,sheet_name = she_name)
                anal = mod.get_anal(test_in,ind,biomass_in)
                name.to_excel(out,startcol=0  ,startrow =col,index=False,header=False,sheet_name = she2_name)
                anal = pd.DataFrame(data=anal)
                anal = anal.T
                anal = anal.round(1)
                anal.to_excel(out, startcol=1  ,startrow =col,index=False,header=False,sheet_name = she2_name)
    elif test_in == "intended":
        she_name = test_in + '_res'
        she2_name =  test_in +'_analysis'
        name = mod.fun.__name__
        name = pd.Series([name])
        name.to_excel(out,startcol=col  ,startrow =0,index=False,header=False,sheet_name = she_name)
        if test_out in mod.outputs:
            ind = mod.outputs.index(test_out)
            mod_res = np.reshape(mod.res_intended,(-1,len(mod.outputs)))
            if len(mod.outputs) == 1:
                mod_res = [item for item in mod_res if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
            else:
                mod_res = [item for item in mod_res[:,ind] if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
            mod_res.to_excel(out,startcol=col ,startrow =1,index=False,header=False,sheet_name = she_name)
            anal = mod.get_anal(test_in,ind,biomass_in)
            name.to_excel(out,startcol= 0  ,startrow =col,index=False,header=False,sheet_name = she2_name)
            anal = pd.DataFrame(data=anal)
            anal = anal.T
            anal = anal.round(1)
            anal.to_excel(out, startcol= 1  ,startrow =col,index=False,header=False,sheet_name = she2_name)

    elif test_in == "algae":
        she_name = test_in + '_res'
        she2_name =  test_in +'_analysis'
        name = mod.fun.__name__
        name = pd.Series([name])
        name.to_excel(out,startcol=col  ,startrow =0,index=False,header=False,sheet_name = she_name)
        if test_out in mod.outputs:
            ind = mod.outputs.index(test_out)
            mod_res = np.reshape(mod.res_algae,(-1,len(mod.outputs)))
            if len(mod.outputs) == 1:
                mod_res = [item for item in mod_res if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
            else:
                mod_res = [item for item in mod_res[:,ind] if str(item) != "nan"  and str(item) != "inf" ] 
                mod_res = pd.DataFrame(data=mod_res)
            mod_res.to_excel(out,startcol=col ,startrow =1,index=False,header=False,sheet_name = she_name)
            anal = mod.get_anal(test_in,ind,biomass_in)
            name.to_excel(out,startcol= 0  ,startrow =col,index=False,header=False,sheet_name = she2_name)
            anal = pd.DataFrame(data=anal)
            anal = anal.T
            anal = anal.round(1)
            anal.to_excel(out, startcol= 1  ,startrow =col,index=False,header=False,sheet_name = she2_name)

    elif test_in == "biomass":
        for mass in biomass_in:
            if mass in mod.optional:
                ind = mod.optional.index(mass)
                p = np.zeros(len(mod.optional))
                p[ind] = 1
                she_name = test_in + '_' + mass + '_res'
                she2_name =  test_in + '_' + mass +'_analysis'
                name = mod.fun.__name__
                name = pd.Series([name])
                name.to_excel(out,startcol=col ,startrow =0,index=False,header=False,sheet_name = str(she_name))
                all_mod_res = mod.res_biomass
                for w in all_mod_res:
                    if w[-1] == p:
                        mod_res = w[:-1]
                if test_out in mod.outputs:
                    ind = mod.outputs.index(test_out)
    
                    if len(mod.outputs) == 1 or len(mod_res) == 0:
                        mod_res = [item for item in mod_res if str(item) != "nan"  and str(item) != "inf" ] 
                        mod_res = pd.DataFrame(data=mod_res)
                    else:
                        mod_res = np.reshape(np.array(mod_res),(-1,len(mod.outputs)))
                        mod_res = [item for item in mod_res[:,ind] if str(item) != "nan"  and str(item) != "inf" ] 
                        mod_res = pd.DataFrame(data=mod_res)
    
                    mod_res.to_excel(out,startcol=col ,startrow =1,index=False,header=False,sheet_name = str(she_name))
                    anal = mod.get_anal(test_in,ind,p)
                    name.to_excel(out,startcol=0  ,startrow =col,index=False,header=False,sheet_name = str(she2_name))
                    anal = pd.DataFrame(data=anal)
                    anal = anal.T
                    anal = anal.round(1)
                    anal.to_excel(out, startcol=1  ,startrow =col,index=False,header=False,sheet_name = str(she2_name))


Test_in = [[],'intended','algae']
Test_out = 'Biocrude wt%'
biomass_in = [[]]
exclu_biomass = []

col = 0
# for i in [mod_Subramanya2021]:
for i in [mod_Biller2011,mod_Teri2014_1,mod_Teri2014_2,mod_Leow2015,mod_Wagner2016,mod_Li2017,mod_Shakya2017,mod_Teri2014_3,mod_Teri2014_4,mod_Deniel2017,mod_Yang2018,mod_Lu2018,mod_Sheng2018,mod_Subramanya2021,mod_Hietala2017,mod_Yang2019,mod_Aierzhati2019,mod_Yan2022]:
    for l in Test_in:

        pri_vals(i,l,Test_out,biomass_in,exclu_biomass,col)
    col = col +1

col = col + 4

for i in [mod_Luo2016,mod_Sheehan2016,mod_Obeid2019_prot,mod_Obeid2020_mono_prot,mod_Chacon_Parra2021,mod_Obeid2019_carb,mod_Obeid2020_mono_carb,mod_Obeid2019_oil,mod_Obeid2020_mono_oil,mod_Obeid2019_lig,mod_Obeid2020_mono_lig,mod_Valdez2013,mod_Saral2022,mod_Hietala2016,mod_Qian2020,mod_Valdez2014,mod_Vo2016,mod_Vo2017,mod_Sheehan2017_1,mod_Palomino2019,mod_Obeid2022_algae,mod_Sheehan2017_2,mod_Hietala2021,mod_Obeid2020_poly,mod_Obeid2022_Sludge,mod_Obeid2022_Pinwood]:
# # for i in [mod_Luo2016,mod_Sheehan2016,mod_Obeid2019_prot,mod_Obeid2020_mono_prot,mod_Chacon_Parra2021,mod_Obeid2019_carb,mod_Obeid2020_mono_carb,mod_Obeid2019_oil,mod_Obeid2020_mono_oil,mod_Obeid2019_lig,mod_Obeid2020_mono_lig,mod_Valdez2013,mod_Saral2022,mod_Hietala2016,mod_Qian2020,mod_Valdez2014,mod_Vo2016,mod_Vo2017,mod_Sheehan2017_1,mod_Palomino2019,mod_Obeid2022_algae,mod_Sheehan2017_2,mod_Obeid2020_poly,mod_Obeid2022_Sludge,mod_Obeid2022_Pinwood]:
    for l in Test_in:
        pri_vals(i,l,Test_out,biomass_in,exclu_biomass,col)
    col = col +1 

out.close()
outliers.close()