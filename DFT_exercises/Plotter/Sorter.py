import os
import time
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib
from matplotlib import transforms as tr
import matplotlib.pyplot as plt
from mendeleev import element
from termcolor import colored
import pyfiglet

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset



def get_parser():

    parser = argparse.ArgumentParser(description = 'Plotting script')

    parser.add_argument('-ip',
                        dest='inputp',
                        type=str,
                        help='input prolate directory')

    parser.add_argument('-io',
                        dest='inputo',
                        type=str,
                        help='input oblate directory')
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
                        'MS_neutron': [],
                        'MS_proton': [],
                        'MS_total': [],
                        'IS': [],
                        'Qdef': [],
                        'Qdef_p': [],
                        'Qdef_n': [],
                        'B20_n':[],
                        'B20_p':[],
                        'B20_t':[],
                        'B20': [],
                        'B40_n':[],
                        'B40_p':[],
                        'B40_t':[],
                        'B40': [],
                        'B60': [],
                        'B60_n':[],
                        'B60_p':[],
                        'B60_t':[],
                        'Skin': []
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
            MS_neutron = 0
            MS_proton = 0
            MS_total = 0
            IS = 0
            Qdef = 0
            B20_n = 0 
            B20_p = 0 
            B20_t = 0 
            B20 = 0
            B40 = 0
            B40_n = 0 
            B40_p = 0 
            B40_t = 0 
            B60 = 0
            B60_n = 0 
            B60_p = 0 
            B60_t = 0 
            Qdef_n = 0 
            Skin = 0
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
                if 'ms  radius (fm2) :' in line:
                    tmp_string = line.replace('ms  radius (fm2) :','')
                    MS_neutron = float(tmp_string.split()[0])
                    MS_proton  = float(tmp_string.split()[1])
                    MS_total   = float(tmp_string.split()[2])
                if 'Q20        (fm2) :' in line:
                    tmp_string = line.replace('Q20        (fm2) :','')
                    Qdef_n = float(tmp_string.split()[0])
                    Qdef_p = float(tmp_string.split()[1])
                    Qdef = float(tmp_string.split()[2])
                if 'beta20           :' in line:
                    tmp_string = line.replace('beta20           :','')
                    B20_n = float(tmp_string.split()[0])
                    B20_p = float(tmp_string.split()[1])
                    B20_t = float(tmp_string.split()[2])
                    B20 = B20_p

                if 'beta40           :' in line:
                    tmp_string = line.replace('beta40           :','')
                    B40 = float(tmp_string.split()[1])
                    B40_n = float(tmp_string.split()[0])
                    B40_p = float(tmp_string.split()[1])
                    B40_t = float(tmp_string.split()[2])
                if 'beta60           :' in line:
                    tmp_string = line.replace('beta60           :','')
                    B60 = float(tmp_string.split()[1])
                    B60_n = float(tmp_string.split()[0])
                    B60_p = float(tmp_string.split()[1])
                    B60_t = float(tmp_string.split()[2])
                if 'skin       (fm)  :' in line:
                    tmp_string = line.replace( 'skin       (fm)  :','')
                    Skin = float (tmp_string)
                    

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
            sorted_output['MS_neutron'].append(MS_neutron)
            sorted_output['MS_proton'].append(MS_proton)
            sorted_output['MS_total'].append(MS_total)
            sorted_output['IS'].append(IS)
            sorted_output['Qdef'].append(Qdef)
            sorted_output['Qdef_n'].append(Qdef_n)
            sorted_output['Qdef_p'].append(Qdef_p)
            sorted_output['B20_p'].append(B20_p)
            sorted_output['B20_n'].append(B20_n)
            sorted_output['B20_t'].append(B20_t)
            sorted_output['B40_p'].append(B40_p)
            sorted_output['B40_n'].append(B40_n)
            sorted_output['B40_t'].append(B40_t)
            sorted_output['B60_p'].append(B60_p)
            sorted_output['B60_n'].append(B60_n)
            sorted_output['B60_t'].append(B60_t)
            sorted_output['B20'].append(B20)
            sorted_output['B40'].append(B40)
            sorted_output['B60'].append(B60)
            sorted_output['Skin'].append(Skin)

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
    EV8_Data_oblate = dict()
    EV8_Data_prolate = dict()


    #-----retrieve data from dataset-----#
    if args.inputo is not None:
        print('--Sorting oblate ',colored('EV8', 'green'),' Data--')
        EV8_Data_oblate = EV8_Extractor(args.inputo)
    
    if args.inputp is not None:
        print('--Sorting prolate ',colored('EV8', 'green'),' Data--')
        EV8_Data_prolate = EV8_Extractor(args.inputp)

    if args.inputp is None and args.inputo is None:
        print(colored('ERROR :', 'red'), ' EV8 Data not provided')
        raise SystemExit

    size = 25
    plt.rcParams['font.size']=size
    fig_iter, axs_iter = plt.subplots(figsize=(16,9), dpi=100)
    # anchor = tr.Bbox.from_extents(400,450,1000,1200)
    # axins_oblate = zoomed_inset_axes(axs_iter, 3, bbox_to_anchor=anchor, bbox_transform = axs_iter.transAxes)#, loc=7)
    # axins_oblate.set_xlim(400, 500)
    # axins_oblate.set_ylim(1780, 1800)
    # # mark_inset(axs_iter, axins_oblate, loc1=1, loc2=2, fc="none", ec="0.5")
    # # plt.xticks(visible=False)
    # plt.yticks(visible=False)
    # axins_prolate = zoomed_inset_axes(axs_iter, 3, loc=4) # zoom = 2
    # axins_prolate.set_xlim(400, 500)
    # axins_prolate.set_ylim(1790, 1800)
    # # mark_inset(axs_iter, axins_prolate, loc1=1, loc2=2, fc="none", ec="0.5")
    # # plt.xticks(visible=False)
    # plt.yticks(visible=False)


    for i,iso in enumerate(EV8_Data_prolate['ISO']):
        if iso == 146 : 
            axs_iter.plot(EV8_Data_prolate['Iterations'][i]['it'],np.abs(EV8_Data_prolate['Iterations'][i]['Etot']),"y-",label='Prolate',linewidth=2)

            print(np.abs(EV8_Data_prolate['Etotal'][i])*1000/238)
            print(np.abs(EV8_Data_oblate['Etotal'][i])*1000/238)
    for i,iso in enumerate(EV8_Data_oblate['ISO']):
        if iso == 146 : 
            axs_iter.plot(EV8_Data_oblate['Iterations'][i]['it'],np.abs(EV8_Data_oblate['Iterations'][i]['Etot']),"b-",label='Oblate',linewidth=2)

            print(np.abs(EV8_Data_prolate['Etotal'][i])*1000/238)
            print(np.abs(EV8_Data_oblate['Etotal'][i])*1000/238)
            # axins_oblate.plot(EV8_Data_prolate['Iterations'][i]['it'],np.abs(EV8_Data_prolate['Iterations'][i]['Etot']),"y-",label='Prolate')
            # axins_oblate.plot(EV8_Data_prolate['Iterations'][i]['it'],np.abs(EV8_Data_prolate['Iterations'][i]['Etot']),"y-",label='Prolate')
            # axins_prolate.plot(EV8_Data_oblate['Iterations'][i]['it'],np.abs(EV8_Data_oblate['Iterations'][i]['Etot']),"b-",label='Oblate')
            # axins_prolate.plot(EV8_Data_oblate['Iterations'][i]['it'],np.abs(EV8_Data_oblate['Iterations'][i]['Etot']),"b-",label='Oblate')

    axs_iter.set_xlabel('Iteration')
    axs_iter.set_ylabel('Binding Energy [MeV]')
    # axs_iter.set_xlim(200,500)
    # axs_iter.set_ylim(1790,1798.5)

    fig, axs = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data_prolate['ISO']):
        axs.plot(EV8_Data_prolate['Iterations'][i]['it'],EV8_Data_prolate['Iterations'][i]['Etot'],"-",label=str(iso))
    axs.set_xlabel('iteration')
    axs.set_ylabel('Energy [MeV]')
    # axs.set_yscale('log')

    figB20, axsB20 = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data_prolate['ISO']):
        if iso == 146 : 
            print(i)
            axsB20.plot(EV8_Data_prolate['Iterations'][i]['it'],EV8_Data_prolate['Iterations'][i]['B20'],"y-",label='Prolate',linewidth=2)
            axsB20.plot(EV8_Data_oblate['Iterations'][i]['it'],EV8_Data_oblate['Iterations'][i]['B20'],"b-",label='Oblate',linewidth=2)

    axsB20.set_xlabel('iteration')
    axsB20.set_ylabel(r'$\beta_{20}$')
    plt.legend()

    figB20.savefig('iterationB20.pdf',transparent=True)

    figB22, axsB22 = plt.subplots(figsize=(16,9), dpi=100)    
    for i,iso in enumerate(EV8_Data_prolate['ISO']):
        axsB22.plot(EV8_Data_prolate['Iterations'][i]['it'],EV8_Data_prolate['Iterations'][i]['B22'],"-",label=str(iso))
    axsB22.set_xlabel('iteration')
    axsB22.set_ylabel(r'$\beta_{22}$')

    iso_exp = 141,142,143,144,146
    rms_exp = 5.8203,5.8291,5.8337,5.8431,5.8571
    rms_sig_exp = 0.0049	,0.0052	,0.0041	,0.0038	,0.0033	
    

    ms_sig_exp = 0.001 ,0.001 ,0.0002 ,0.0002, 0
    ms_exp = -0.435 ,-0.334 ,-0.2803 ,-0.1676 , 0

    figRMS, axsRMS = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data_prolate['ISO']):
    axsRMS.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['RMS_proton'],"o",label = 'prolate')
    axsRMS.plot(EV8_Data_oblate['ISO'],EV8_Data_oblate['RMS_proton'],"o",label = 'oblate')
    # axsRMS.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['RMS_neutron'],"o",label = 'neutron')
    # axsRMS.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['RMS_total'],"o",label = 'total')
    # axsRMS.errorbar(x=iso_exp,y=rms_exp,yerr=rms_sig_exp,fmt='o-',markersize = 5,label='exp')
    axsRMS.set_xlabel('neutron number')
    axsRMS.set_ylabel('r$_{RMS}$ [fm]')
    plt.legend()
    figRMS.savefig('rms_comparison.pdf',transparent=True)


    figRMS_iso, axsRMS_iso = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data_prolate['ISO']):
    axsRMS_iso.plot(EV8_Data_prolate['ISO'],[ms-EV8_Data_prolate['MS_proton'][10] for ms in EV8_Data_prolate['MS_proton']],"o",label = 'calculation')
    # axsRMS_iso.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['RMS_neutron'],"o",label = 'neutron')
    # axsRMS_iso.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['RMS_total'],"o",label = 'total')
    axsRMS_iso.errorbar(x=iso_exp,y=ms_exp,yerr=ms_sig_exp,fmt='o-',markersize = 5,label='exp')
    axsRMS_iso.set_xlabel('neutron number')
    axsRMS_iso.set_ylabel(r'$\delta \langle r^2 \rangle ^{A-238}$ [fm$^2$]')
    plt.legend()
    figRMS_iso.savefig('ms.pdf',transparent=True)

    figQ20, axsQ20 = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data_prolate['ISO']):
    axsQ20.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['Qdef'],"o",label = 'total')
    axsQ20.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['Qdef_n'],"o",label = 'neutron')
    axsQ20.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['Qdef_p'],"o",label = 'proton')
    axsQ20.set_xlabel('neutron number')
    axsQ20.set_ylabel('Q$_{20}$ [fm$^2$]')
    plt.legend()

    figEtot, axsEtot = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data_prolate['ISO']):
    axsEtot.plot(EV8_Data_prolate['ISO'],[  abs(1000*EV8_Data_prolate['Etotal'][i])/(92+iso) -abs(1000*EV8_Data_oblate['Etotal'][i])/(92+iso)  for i,iso in enumerate(EV8_Data_prolate['ISO'])],"o")
    
    axsEtot.set_xlabel('neutron number')
    axsEtot.set_ylabel('Binding Energy difference [keV/A]')
    figEtot.savefig('bindingenergies.pdf',transparent=True)
    iso_exp = 138, 140, 142, 144 ,146 
    beta_exp = 0.262,0.264,0.2718,0.2821,0.2863
    beta_sig_exp =  0.016,0.013,0.0026,0.0018,0.0024 

    figBETA, axsBETA = plt.subplots(figsize=(16,9), dpi=100)    
    # for i,iso in enumerate(EV8_Data_prolate['ISO']):
    axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B20'],"o",label = r'$\beta_{20} -proton$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B40'],"o",label = r'$\beta_{40} proton$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B60'],"o",label = r'$\beta_{60} proton$')
    axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B20_n'],"o",label = r'$\beta_{20} -neutron$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B40_n'],"o",label = r'$\beta_{40} neutron$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B60_n'],"o",label = r'$\beta_{60} neutron$')
    axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B20_t'],"o",label = r'$\beta_{20} -total$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B40_t'],"o",label = r'$\beta_{40} total$')
    # axsBETA.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['B60_t'],"o",label = r'$\beta_{60} total$')

    # axsBETA.errorbar(x=iso_exp,y=beta_exp,yerr=beta_sig_exp,fmt='o-',markersize = 5,label='exp')

    axsBETA.set_xlabel('neutron number')
    axsBETA.set_ylabel(r'$\beta$ deformation')
    plt.legend()
    figBETA.savefig('beta_comp.pdf',transparent=True)

    figSkin, axsSkin = plt.subplots(figsize=(16,9), dpi=100)    
    axsSkin.plot(EV8_Data_prolate['ISO'],EV8_Data_prolate['Skin'],"o")
    axsSkin.set_xlabel('neutron number')
    axsSkin.set_ylabel(r'neutron skin [fm]')
    figSkin.savefig('skin.pdf',transparent=True)
    plt.show()

    return
if __name__ == '__main__':
    main()
