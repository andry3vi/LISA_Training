import os
import time
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
from mendeleev import element
from termcolor import colored
import pyfiglet


def get_parser():

    parser = argparse.ArgumentParser(description = 'Plotting script')

    parser.add_argument('-i',
                        dest='input',
                        type=str,
                        help='input directory')

    # parser.add_argument('-Fluka',
    #                     dest='Flukafolder',
    #                     type=str,
    #                     help='Fluka simulation folder')

    # parser.add_argument('-PACE',
    #                     dest='PACEfolder',
    #                     type=str,
    #                     help='PACE4 simulation folder')

    # parser.add_argument('-EXFOR',
    #                     dest='EXFORfolder',
    #                     type=str,
    #                     help='EXFOR experimental data folder')

    parser.add_argument('-o',
                        dest='output',
                        type=str,
                        help='output directory')


    args = parser.parse_args()

    return args, parser

def EV8_Extractor(input):

    isotope_list = dict()
    
    sorted_output = {   'ISO' : [],
                        'Iterations': [],
                        'Etotal': [],
                        'RMS_neutron': [],
                        'RMS_proton': [],
                        'RMS_total': [],
                        'IS': [],
                        'Qdef': [],
                        'Qdef_p': [],
                        'Qdef_n': [],
                        'B20': [],
                        'B40': [],
                        'B60': []
                    }
    for file in os.listdir(input):
        if '.ev8.' in file:
            isotope_list[int(file[:3])] = input+'/'+file

    # print(isotope_list)
    for iso in tqdm(isotope_list.keys()):
        
        with open(isotope_list[iso], 'r') as evout_file:
            # text = evout_file.read()
            iteration_counter = {'it':[],
                                 'line':[],
                                 'Etot':[],
                                 'B20' :[],
                                 'B22' :[]}
            Etotal = 0
            RMS_neutron = 0
            RMS_proton = 0
            RMS_total = 0
            IS = 0
            Qdef = 0
            B20 = 0
            B40 = 0
            B60 = 0
            Qdef_n = 0 
            Qdef_p = 0 

            lines = evout_file.readlines()
            for i,line in enumerate(lines):
                if 'Sum. it  : Iter   =' in line:
                    iteration_counter['it'].append(int(line.split('=')[-1]))
                    iteration_counter['line'].append(i)
                if 'total energy (Lagrange)' in line:
                    Etotal = float(line.split('total energy (Lagrange)')[-1])
                if 'rms radius (fm)  :' in line:
                    tmp_string = line.replace('rms radius (fm)  :','')
                    RMS_neutron = float(tmp_string.split()[0])
                    RMS_proton  = float(tmp_string.split()[1])
                    RMS_total   = float(tmp_string.split()[2])
                if 'Q20        (fm2) :' in line:
                    tmp_string = line.replace('Q20        (fm2) :','')
                    Qdef_n = float(tmp_string.split()[0])
                    Qdef_p = float(tmp_string.split()[1])
                    Qdef = float(tmp_string.split()[2])
                if 'beta20           :' in line:
                    tmp_string = line.replace('beta20           :','')
                    B20 = float(tmp_string.split()[2])

                if 'beta40           :' in line:
                    tmp_string = line.replace('beta40           :','')
                    B40 = float(tmp_string.split()[2])
                if 'beta60           :' in line:
                    tmp_string = line.replace('beta60           :','')
                    B60 = float(tmp_string.split()[2])

            for index, line_i in enumerate(iteration_counter['line']):

                tmp_str=lines[line_i+1].replace('Etot   =','*')
                tmp_str=tmp_str.replace('dE      =','*')
                iteration_counter['Etot'].append(float(tmp_str.split('*')[1]))
                
                tmp_str=lines[line_i+3].replace('B20    =','*')
                tmp_str=tmp_str.replace('B22     =','*')
                iteration_counter['B20'].append(float(tmp_str.split('*')[1]))
                iteration_counter['B22'].append(float(tmp_str.split('*')[2]))
            sorted_output['ISO'].append(iso)
            sorted_output['Iterations'].append(iteration_counter)
            sorted_output['Etotal'].append(Etotal)
            sorted_output['RMS_neutron'].append(RMS_neutron)
            sorted_output['RMS_proton'].append(RMS_proton)
            sorted_output['RMS_total'].append(RMS_total)
            sorted_output['IS'].append(IS)
            sorted_output['Qdef'].append(Qdef)
            sorted_output['Qdef_n'].append(Qdef_n)
            sorted_output['Qdef_p'].append(Qdef_p)
            sorted_output['B20'].append(B20)
            sorted_output['B40'].append(B40)
            sorted_output['B60'].append(B60)

#  Sum. it  : Iter   =    5
#  Sum. E   : Etot   = -1495.776 dE      = 0.893E-01
#  Sum. Quad: Qxx    = -1113.953 Qy      = -1113.953 Qz      =  2227.907
#  Sum. Beta: B20    =    12.333 B22     =     1.306
#  Sum. Misc: Sum D2H= 0.109E+01 dFermi N=

    return sorted_output



def clear():
    os.system('clear')

def menu():
        strs = ('Enter 1 for plotting Segre production charts\n'
                'Enter 2 for plotting EXFOR data comparison\n'
                'Enter 3 for plotting Simulated production Cross Sections comparison\n'
                'Enter 4 for plotting Simulated production Cross Sections CODE separated\n'
                'Enter 5 for plotting Recoil spectra\n'
                'Enter 6 for sorting production cross section\n'
                'Enter 7 for Talys dedicated plot\n'
                'Enter 8 for Talys isotope chain xsec as a function of energy\n'
                'Enter 9 to exit : ')
        choice = input(strs)
        return int(choice)


def main():

    clear()
    ascii_banner = pyfiglet.figlet_format("EV8 Data Plotter")
    print(ascii_banner)
    #-----Getting parser-----#
    args, parser = get_parser()

    #-----Define data containers-----#
    EV8_Data = dict()


    #-----retrieve data from dataset-----#
    if args.input is not None:
        print('--Sorting ',colored('EV8', 'green'),' Data--')
        EV8_Data = EV8_Extractor(args.input)
    else:
        print(colored('ERROR :', 'red'), ' EV8 Data not provided')
        raise SystemExit

    size = 25
    plt.rcParams['font.size']=size

    fig, axs = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data['ISO']):
        axs.plot(EV8_Data['Iterations'][i]['it'],EV8_Data['Iterations'][i]['Etot'],"-",label=str(iso))
    axs.set_xlabel('iteration')
    axs.set_ylabel('Energy [keV]')
    # axs.set_yscale('log')

    figB20, axsB20 = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data['ISO']):
        axsB20.plot(EV8_Data['Iterations'][i]['it'],EV8_Data['Iterations'][i]['B20'],"-",label=str(iso))
    axsB20.set_xlabel('iteration')
    axsB20.set_ylabel(r'$\beta_{20}$')


    figB22, axsB22 = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data['ISO']):
        axsB22.plot(EV8_Data['Iterations'][i]['it'],EV8_Data['Iterations'][i]['B22'],"-",label=str(iso))
    axsB22.set_xlabel('iteration')
    axsB22.set_ylabel(r'$\beta_{22}$')

    iso_exp = 141,142,143,144,146
    rms_exp = 5.8203,5.8291,5.8337,5.8431,5.8571
    rms_sig_exp = 0.0049	,0.0052	,0.0041	,0.0038	,0.0033	
    
    figRMS, axsRMS = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data['ISO']):
    axsRMS.plot(EV8_Data['ISO'],EV8_Data['RMS_proton'],"o",label = 'proton')
    axsRMS.plot(EV8_Data['ISO'],EV8_Data['RMS_neutron'],"o",label = 'neutron')
    axsRMS.plot(EV8_Data['ISO'],EV8_Data['RMS_total'],"o",label = 'total')
    axsRMS.errorbar(x=iso_exp,y=rms_exp,yerr=rms_sig_exp,fmt='o-',markersize = 5,label='exp')
    axsRMS.set_xlabel('neutron number')
    axsRMS.set_ylabel('r$_{RMS}$ [fm]')
    plt.legend()

    figQ20, axsQ20 = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data['ISO']):
    axsQ20.plot(EV8_Data['ISO'],EV8_Data['Qdef'],"o",label = 'total')
    axsQ20.plot(EV8_Data['ISO'],EV8_Data['Qdef_n'],"o",label = 'neutron')
    axsQ20.plot(EV8_Data['ISO'],EV8_Data['Qdef_p'],"o",label = 'proton')
    axsQ20.set_xlabel('neutron number')
    axsQ20.set_ylabel('Q$_{20}$ [fm$^2$]')
    plt.legend()

    figEtot, axsEtot = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data['ISO']):
    axsEtot.plot(EV8_Data['ISO'],EV8_Data['Etotal'],"o")
    axsEtot.set_xlabel('neutron number')
    axsEtot.set_ylabel('Energy [keV]')

    iso_exp = 138, 140, 142, 144 ,146 
    beta_exp = 0.262,0.264,0.2718,0.2821,0.2863
    beta_sig_exp =  0.016,0.013,0.0026,0.0018,0.0024 

    figBETA, axsBETA = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data['ISO']):
    axsBETA.plot(EV8_Data['ISO'],EV8_Data['B20'],"o",label = r'$\beta_{20}$')
    axsBETA.plot(EV8_Data['ISO'],EV8_Data['B40'],"o",label = r'$\beta_{40}$')
    axsBETA.plot(EV8_Data['ISO'],EV8_Data['B60'],"o",label = r'$\beta_{60}$')
    axsBETA.errorbar(x=iso_exp,y=beta_exp,yerr=beta_sig_exp,fmt='o-',markersize = 5,label='exp')

    axsBETA.set_xlabel('neutron number')
    axsBETA.set_ylabel(r'$\beta$ deformation')
    plt.legend()
    
    plt.show()
if __name__ == '__main__':
    main()
