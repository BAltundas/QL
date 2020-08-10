# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 17:32:19 2018

@author: BAltundas
"""


import sys 
if sys.version_info < (3, 0):
  from Tkinter import *
  from tkFileDialog  import askopenfile, asksaveasfile
  import Tkinter
  import tkMessageBox,ttk
  import cPickle as pickle
  from ttk import Notebook, Label, Entry, Labelframe, Combobox
  from Tkinter import Radiobutton, Text, Scale,  Scrollbar,StringVar, BooleanVar, Checkbutton, Button, Frame
else:
  from tkinter import *
  import tkinter as Tkinter
  from tkinter.filedialog  import askopenfile, asksaveasfile
  import tkinter.ttk as ttk
  import tkinter.messagebox as tkMessageBox
  from tkinter.ttk import Notebook, Label, Entry, Labelframe, Combobox, Frame
  from tkinter import Radiobutton, Scale, Text,  Scrollbar,StringVar, BooleanVar, Checkbutton, Button
  import pickle as pickle

  
#from Tkinter import * #  from tkinter import *
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg', warn=False)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from  mpl_toolkits.axes_grid1 import  make_axes_locatable
import numpy as np
from scipy.integrate import odeint
import webbrowser
import math
import scipy
import os
#################################
# -*- coding: utf-8 -*-


def Plot_Properties_SwTL(fr, title,  unit, xlabel, ylabel,FunCalc,indx): 
#    file_path='C:/Program Files/Quick_Look/DelSwat.p'
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/DelSwat.p'

    plt.close('all')
    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    ColorList = PlotList.ColorList
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight    
    ax = figure.add_subplot(111)
    Yarray= [] 
    YarrayOld= [] 
    DeltaYarray= [] 
    sw_array=Calculated.sw_array
    length=len(sw_array)
    zeros=np.zeros(length)
    YarrayOld= zeros
    DeltaYarray=zeros
    so=Input.soil
    for i in range(0, length):
        Input.swat=sw_array[i]
        Input.sgas=max(0, 1.0 - so - Input.swat)  
        tmp=FunCalc()
        Yarray.append( tmp )    
    array_dimX=len(sw_array)
    i=0
    if(not IsActiveF.flgPlotHold):  
        ax.cla()
    if(IsActiveF.flgTLbaseline):
        ylabel=ylabel + '[%]'
        title = title +'[%]'
        YarrayOld= pickle.load( open( file_path, "rb" ) )
        Yarray=np.concatenate((YarrayOld,Yarray), axis=0)
        array_dimY=len(Yarray)
        for i in range(array_dimX, array_dimY, array_dimX): 
            DeltaYarray= 100*(Yarray[i:i+array_dimX]-Yarray[0:array_dimX])/Yarray[0:array_dimX]
            ax.plot(sw_array, DeltaYarray,ColorList[i//array_dimX],label=str (i//array_dimX))    
    else:
        ylabel=ylabel + unit
        title = title + unit
        ax.plot(sw_array, Yarray,ColorList[i], label=str (0))  
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame1 = Tkinter.Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))

            
def Plot_Properties_PressureTL(fr, title,  unit, xlabel, ylabel,FunCalc,indx):
#    file_path='C:/Program Files/Quick_Look/DelPressure.p'
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/DelPressure.p'

    plt.close('all')
    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight   
    ColorList = PlotList.ColorList
    ax = figure.add_subplot(111)
    Yarray= [] 
    YarrayOld= [] 
    DeltaYarray= [] 
    
    pressure_array=Calculated.pressure_array
    length=len(pressure_array)
    zeros=np.zeros(length)
    YarrayOld= zeros
    DeltaYarray=zeros
    for i in range(0, length):
        Input.pressure=pressure_array[i]
        tmp=FunCalc()
        Yarray.append(tmp)
    array_dimX=len(pressure_array)
    i=0
    if(not IsActiveF.flgPlotHold):   
        ax.cla()
    if(IsActiveF.flgTLbaseline):
        ylabel=ylabel + '[%]'
        title = title + '[%]'
        YarrayOld= pickle.load( open( file_path, "rb" ) )
        Yarray=np.concatenate((YarrayOld,Yarray), axis=0)
        array_dimY=len(Yarray)
        for i in range(array_dimX, array_dimY, array_dimX):
            DeltaYarray= 100*(Yarray[i:i+array_dimX]-YarrayOld[0:array_dimX])/YarrayOld[0:array_dimX]
            ax.plot(pressure_array, DeltaYarray,ColorList[i//array_dimX],label=str (i//array_dimX))    
    else:
        ylabel=ylabel + unit
        title = title + unit
        ax.plot(pressure_array, Yarray,ColorList[i], label=str (0))   
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame1 = Tkinter.Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))


def Plot_Properties_TemperatureTL(fr, title,  unit, xlabel, ylabel,FunCalc,indx):
#    file_path='C:/Program Files/Quick_Look/DelTemperature.p'
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)
            
    file_path=file_path+'/DelTemperature.p'

    plt.close('all')
    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    ColorList = PlotList.ColorList
    ax = figure.add_subplot(111)
    Yarray= [] 
    YarrayOld= [] 
    DeltaYarray= [] 
    temperature_array=Calculated.temperature_array
    length=len(temperature_array)
    zeros=np.zeros(length)
    YarrayOld= zeros
    DeltaYarray=zeros
    for i in range(0, length):
        Input.temperature=temperature_array[i]
        tmp=FunCalc()
        Yarray.append( tmp )
    array_dimX=len(temperature_array)
    i=0
    if(not IsActiveF.flgPlotHold):
        ax.cla()
    if(IsActiveF.flgTLbaseline):
        ylabel=ylabel + '[%]'
        title = title +'[%]'
        YarrayOld= pickle.load( open( file_path, "rb" ) )
        Yarray=np.concatenate((YarrayOld,Yarray), axis=0)
        array_dimY=len(Yarray)
        for i in range(array_dimX, array_dimY, array_dimX):
            DeltaYarray= 100*(Yarray[i:i+array_dimX]-Yarray[0:array_dimX])/Yarray[0:array_dimX]
            ax.plot(temperature_array, DeltaYarray,ColorList[i//array_dimX],label=str (i//array_dimX))    
    else:
        ylabel=ylabel + unit
        title = title + unit
        ax.cla()
        ax.plot(temperature_array, Yarray,ColorList[i], label=str (0))    
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame1 = Tkinter.Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))


def Plot_Properties_SwSgTL(fr, title, unit, xlabel, ylabel, funCalc,indx):
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/DelSwSgTL.p'

    f = Figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    plt.close()
    a = f.add_subplot(111)
    xedges= [] 
    yedges= [] 
    Zarray= [] 

    yedges = Calculated.sg_array
    xedges = Calculated.sw_array
    lenX=len(xedges)
    lenY=len(yedges)
    Mat=np.zeros((lenX, lenY))
    DelMat=np.zeros((lenX, lenY))
    X, Y = np.meshgrid(xedges, yedges)
    indx=1       
    emptyValue=9999999999999999999.9
    for i in range (0, lenX):
        sw=xedges[i]
        for j in range(0, lenY):
            if(xedges[i]+yedges[j]<=1.0):
                sg=yedges[j]
                Input.swat = sw
                Input.sgas = sg
                Input.soil=1.0- sw- sg
                tmp=funCalc()
            else:
                tmp=emptyValue           
            Zarray.append( tmp )
            Mat[j,i]=tmp        
    if indx==0:
        Mat= 0.0     
    cmin=Mat.min()
    Mat=np.where(Mat==emptyValue, cmin, Mat)
    cmax=Mat.max()
    if(IsActiveF.flgTLbaseline):
        TitleName = title +'[%]'
        MatOld= pickle.load( open( file_path, "rb" ) )
        Mat=np.concatenate((MatOld, Mat),axis=0)
        rown=len(Mat)
        for i in range(0, rown, lenX):
            DelMat=100*(Mat[i:i+lenX,0:lenY]-Mat[0:lenX,0:lenY])/Mat[0:lenX,0:lenY]
            cmax=DelMat.max()
            cmin=DelMat.min()
            im=a.pcolormesh(X, Y,DelMat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    else:
        TitleName = title + unit
        im=a.pcolormesh(X, Y,Mat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    a.set_aspect('equal')
    a.set_xlim(xedges[0], xedges[-1])
    a.set_ylim(yedges[0], yedges[-1])
    divider= make_axes_locatable(a)
    ca=divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im,cax=ca)
    a.set_xlabel('$S_w$', fontsize=txtsize)
    a.set_ylabel('$S_g$', fontsize=txtsize)
    a.set_title(TitleName,fontsize=txtsize)  
    a.grid(True, which='minor', axis='both', linestyle='-', color='k')
    canvas = FigureCanvasTkAgg(f,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1) 
    toolbar_frame2 = Tkinter.Frame(fr)
    toolbar_frame2.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame2 )
    pickle.dump( Mat, open(file_path, 'wb'))


def Plot_Properties_PT_TL(fr, title, unit, xlabel, ylabel, funCalc,indx):
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/DelPT_TL.p'

    f = Figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    plt.close()
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight 
    a = f.add_subplot(111)
    xedges= [] 
    yedges= [] 
    xedges = Calculated.pressure_array # X-->P 
    yedges = Calculated.temperature_array # Y-->T    
    lenX=len(xedges)
    lenY=len(yedges)
    Mat=np.zeros((lenX, lenY))
    DelMat=np.zeros((lenX, lenY))
    X, Y = np.meshgrid(xedges, yedges)
#    indx=1       
    for i in range (0, lenX):
        Input.pressure = xedges[i]
        for j in range(0, lenY):
            Input.temperature = yedges[j]
            tmp=funCalc()          
            Mat[j,i]=tmp            
    cmin=Mat.min()
    Mat=np.where(Mat<0, cmin, Mat)
    cmax=Mat.max()
    if(IsActiveF.flgTLbaseline):
        TitleName = title +'[%]'
        MatOld= pickle.load( open( file_path, "rb" ) )
        Mat=np.concatenate((MatOld, Mat),axis=0)
        rown=len(Mat)
        for i in range(0, rown, lenX):
            DelMat=100*(Mat[i:i+lenX,0:lenY]-Mat[0:lenX,0:lenY])/Mat[0:lenX,0:lenY]
            cmax=DelMat.max()
            cmin=DelMat.min()
            im=a.pcolormesh(X, Y,DelMat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    else:
        TitleName = title + unit
        im=a.pcolormesh(X, Y,Mat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    a.set_aspect('auto')
    a.set_xlim(xedges[0], xedges[-1])
    a.set_ylim(yedges[0], yedges[-1])  
    divider= make_axes_locatable(a)
    ca=divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im,cax=ca)  
#    cbar=plt.colorbar(im,cax=ca)  
    a.set_ylabel('Temperature[$^{o}$C]', fontsize=txtsize)
    a.set_xlabel('Pressure[bar]', fontsize=txtsize)
    a.set_title(TitleName,fontsize=txtsize)
    a.grid(True, which='minor', axis='both', linestyle='-', color='k')
    canvas = FigureCanvasTkAgg(f,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)   
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1) 
    toolbar_frame2 = Tkinter.Frame(fr)
    toolbar_frame2.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame2 )
    pickle.dump( Mat, open( file_path, 'wb'))


def Plot_Properties_Pressure(fr, title, unit, xlabel, ylabel, FunCalc,indx):
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/TempFilePressure.p'

    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    ColorList = PlotList.ColorList
    ax = figure.add_subplot(111)
    ylabel=ylabel+unit
    Yarray= [] 
    Yarray0= [] 
    pressure_array=Calculated.pressure_array
    length=len(pressure_array)
    zeros=np.zeros(length)
    Yarray0= zeros
    for i in range(0, length):
        Input.pressure=pressure_array[i]
        tmp=FunCalc()
        Yarray.append( tmp )
    if indx==0:
        Yarray= zeros      
    array_dimX=len(pressure_array)
    i=0
    ax.cla()
    if(IsActiveF.flgPlotHold):
        Yarray0= pickle.load( open( file_path, "rb" ) )
        array_dimY0=len(Yarray0)
        number_array=array_dimY0 // array_dimX
        if number_array>0:
            for i in range(0, array_dimY0, array_dimX):
                ax.plot(pressure_array, Yarray0[i:i+array_dimX],ColorList[i//array_dimX],label=str (i//array_dimX))    
            ax.plot(pressure_array, Yarray,ColorList[1+i//array_dimX],label=str (i//array_dimX+1)) 
            Yarray=np.concatenate((Yarray0, Yarray), axis=0)
        else :  
            ax.cla()
            ax.plot(pressure_array, Yarray,ColorList[i],label=str (0)) 
    else:
        ax.cla()
        ax.plot(pressure_array, Yarray,ColorList[i], label=str (0))       
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame1 = Tkinter.Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))


def Plot_Properties_Temperature(fr, title,unit, xlabel, ylabel, FunCalc,indx):
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/TempFileTemperature.p'

    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    ylabel=ylabel+unit
    ColorList = PlotList.ColorList
    ax = figure.add_subplot(111)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    Yarray= [] 
    Yarray0= [] 
    temperature_array=Calculated.temperature_array
    length=len(temperature_array)
    zeros=np.zeros(length)
    Yarray0= zeros
    for i in range(0, length):
        Input.temperature=temperature_array[i]
        tmp=FunCalc()
        Yarray.append( tmp )
    if indx==0:
        Yarray= zeros      
    array_dimX=len(temperature_array)
    i=0
    ax.cla()
    if(IsActiveF.flgPlotHold):
        Yarray0= pickle.load( open( file_path, "rb" ) )
        array_dimY0=len(Yarray0)
        number_array=array_dimY0 // array_dimX
        if number_array>0:
            for i in range(0, array_dimY0, array_dimX):
                ax.plot(temperature_array, Yarray0[i:i+array_dimX],ColorList[i//array_dimX],label=str (i//array_dimX))    
            ax.plot(temperature_array, Yarray,ColorList[1+i//array_dimX],label=str (i//array_dimX+1)) 
            Yarray=np.concatenate((Yarray0, Yarray), axis=0)
        else :  
            ax.cla()
            ax.plot(temperature_array, Yarray,ColorList[i],label=str (0)) 
    else:
        ax.cla()
        ax.plot(temperature_array, Yarray,ColorList[i], label=str (0))        
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
#    canvas.show()
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame1 = Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))
    

def Plot_Properties_Sw(fr, title,  unit, xlabel, ylabel,FunCalc,indx): 
#    file_path='C:/Program Files/Quick_Look/TempFileSw.p'
    file_path='C:/temp'
    if(os.path.isdir(file_path)):
        file_path ='C:/temp/Quick_Look'
        if(not os.path.isdir(file_path)):
            os.mkdir(file_path)
    else:
        file_path ='C:/temp/Quick_Look'
        os.mkdir(file_path)

    file_path=file_path+'/TempFileSw.p'

    figure = plt.figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    ColorList = PlotList.ColorList
    ax = figure.add_subplot(111)
    ylabel=ylabel+unit 
    Yarray= [] 
    Yarray0= [] 
    so=Input.soil
    sw_array=Calculated.sw_array
    length=len(sw_array)
    zeros=np.zeros(length)
    Yarray0= zeros
    for i in range(0, length):
        Input.swat = sw_array[i]
        Input.sgas=max(0, 1.0 - so - Input.swat)  
        tmp=FunCalc()
        Yarray.append( tmp )
    if indx==0:
        Yarray= zeros      
    array_dimX=len(sw_array)
    ax.cla()
    i=0
    if(IsActiveF.flgPlotHold):
        Yarray0= pickle.load( open( file_path, "rb" ) )
        array_dimY0=len(Yarray0)
        number_array=array_dimY0 // array_dimX
        if number_array>0:
            for i in range(0, array_dimY0, array_dimX):
                ax.plot(sw_array, Yarray0[i:i+array_dimX],ColorList[i//array_dimX],label=str (i//array_dimX))    
            ax.plot(sw_array, Yarray,ColorList[1+i//array_dimX],label=str (i//array_dimX+1)) 
            Yarray=np.concatenate((Yarray0, Yarray), axis=0)
        else :  
            ax.cla()
            ax.plot(sw_array, Yarray,ColorList[i],label=str (0)) 
    else:
        ax.cla()
        ax.plot(sw_array, Yarray,ColorList[i], label=str (0))    
    title = title + unit
    ax.set_title(title)
    ax.set_xlabel(xlabel,fontsize=txtsize)
    ax.set_ylabel(ylabel,fontsize=txtsize)#, fontweight='bold')     
    ax.grid(True)  
    ax.legend( title=ylabel, shadow=True,fancybox=True)
    canvas = FigureCanvasTkAgg(figure,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    
    toolbar_frame1 = Tkinter.Frame(fr)
    toolbar_frame1.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame1)
    pickle.dump( Yarray, open( file_path, 'wb'))


def Plot_Properties_SwSg(fr, title, unit, xlabel, ylabel, funCalc,indx):
    f = Figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight
    a = f.add_subplot(111)
    xedges= [] 
    yedges= [] 
    Zarray= [] 
    
    xedges = Calculated.sw_array
    yedges = Calculated.sg_array

    lenX=len(xedges)
    lenY=len(yedges)
    Mat=np.zeros((lenX, lenY))
    X, Y = np.meshgrid(xedges, yedges)
    indx=1
    TitleName = title+unit
    for i in range (0, lenX):
        sw=xedges[i]
        for j in range(0, lenY):
            if(xedges[i]+yedges[j]<=1.0):
                sg=yedges[j]
                Input.swat = sw
                Input.sgas = sg
                Input.soil = 1.0- sw- sg
                tmp=funCalc()
            else:
                tmp=99999.0           
            Zarray.append( tmp )
            Mat[j,i]=tmp       
    if indx==0:
        Mat= 0.0
    cmin=Mat.min()
    Mat=np.where(Mat==99999.0, cmin, Mat)
    cmax=Mat.max()
    im=a.pcolormesh(X, Y,Mat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    a.set_aspect('equal')
    a.set_xlim(xedges[0], xedges[-1])
    a.set_ylim(yedges[0], yedges[-1])  
    divider= make_axes_locatable(a)
    ca=divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im,cax=ca) 
    a.set_xlabel('$S_w$', fontsize=txtsize)
    a.set_ylabel('$S_g$', fontsize=txtsize)
    a.set_title(TitleName,fontsize=txtsize)
    a.grid(True, which='minor', axis='both', linestyle='-', color='k')
    canvas = FigureCanvasTkAgg(f,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight)  
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)   
    toolbar_frame2 = Tkinter.Frame(fr)
    toolbar_frame2.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame2 )

    
def Plot_Properties_PT(fr, title, unit, xlabel, ylabel, funCalc,indx):
    f = Figure(figsize=(1, 1), dpi=80, facecolor='w', edgecolor='r', tight_layout=True)
    txtsize=PlotAux.fontsize
    cwidth=PlotAux.canvWidth
    cheight=PlotAux.canvHeight    
    a = f.add_subplot(111)

    xedges1= [] 
    yedges1= [] 
    
    xedges1 = Calculated.pressure_array        
    yedges1 = Calculated.temperature_array

    lenX=len(xedges1)
    lenY=len(yedges1)
    Mat=np.zeros((lenX, lenY))
    X, Y = np.meshgrid(xedges1, yedges1)
#    indx=1    
    TitleName = title+unit    
    for i in range (0, lenX):
        Input.pressure=xedges1[i]
        for j in range(0, lenY):
            Input.temperature=yedges1[j]
            tmp=funCalc()            
            Mat[j,i]=tmp
    cmin=Mat.min()
    Mat=np.where(Mat<0, cmin, Mat)
    cmax=Mat.max()
    im=a.pcolormesh(X, Y,Mat, cmap=plt.cm.bwr, vmin=cmin, vmax=cmax)
    a.set_aspect('auto')
    a.set_xlim(xedges1[0], xedges1[-1])
    a.set_ylim(yedges1[0], yedges1[-1]) 
    divider= make_axes_locatable(a)
    ca=divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(im,cax=ca)  
    
    a.set_ylabel('Temperature[$^{o}$C]', fontsize=txtsize)
    a.set_xlabel('Pressure[MPa]', fontsize=txtsize)

    a.set_title(TitleName,fontsize=txtsize)    
    a.grid(True, which='minor', axis='both', linestyle='-', color='k')
    canvas = FigureCanvasTkAgg(f,master=fr)
    canvas.get_tk_widget().config(width=cwidth,height=cheight) 
    canvas.draw()
    canvas.get_tk_widget().grid(column=1, row=1)
    toolbar_frame2 = Tkinter.Frame(fr)
    toolbar_frame2.grid(row=3,column=1,columnspan=2) 
    NavigationToolbar2TkAgg( canvas, toolbar_frame2 )

    
def Scalar2Array(ValueMin, ValueMax, numVal):
  DelValue= (ValueMax-ValueMin)/numVal
  a= [] 
  a.insert(0,ValueMin)
  i=1
  while (i <= numVal-1):
     ValueNew=ValueMin + i* DelValue
     a.append(ValueNew)
     i=i+1
  return a
def Scalar2ArrayWithRes(ValueMin, ValueMax):
  numVal=Input.resolutionN
  res = (ValueMax-ValueMin)/numVal
  a= [] 
  a.insert(0,ValueMin)
  i=1
  while (i <= numVal):
     ValueNew=ValueMin + i* res
     a.append(ValueNew)
     i=i+1
  return a  


def Calculate_Water_Density(pressureMPa, TCelcius, salinity):    
  '''
  These equations could be check with the numerical values from : http://www.crewes.org/ResearchLinks/ExplorerPrograms/FlProp/FluidProp.htm
  Output:
  densityBrine[kg/m3]
  '''
  densityW = 1.0e+3*(1.0 + 1.0E-6*\
   (-80.0*TCelcius - 3.3*math.pow(TCelcius, 2) + 0.00175*math.pow(TCelcius, 3) + 489.0*pressureMPa - 2.0*TCelcius*pressureMPa +\
   0.016*math.pow(TCelcius, 2)*pressureMPa - 1.3E-5*math.pow(TCelcius, 3)*pressureMPa - 0.333*math.pow(pressureMPa, 2) -\
   0.002*TCelcius*math.pow(pressureMPa, 2)))
  term1=80.0 + 3.0*TCelcius - 3300.0*salinity - 13.0*pressureMPa + 47.0*pressureMPa*salinity
  term2= 300.0*pressureMPa - 2400.0*pressureMPa*salinity +TCelcius*term1
  IsCalculated.Brine_density= True
  densityBrine= densityW + 1.0E+3*salinity*(0.668 + 0.44*salinity + 1.0E-6*term2)
  Calculated.brine_density= densityBrine
#  print('Rho_b', densityBrine)
  return densityBrine


def Calculate_Brine_Bulkmodulus(pressureMPa, TCelcius, salinity):
     '''
     Calculate water bulkmodulus 
     output:
     RhoBrine[kg/m3]
     velocityA[m/s]
     KBrine[MPa]'''
     Calculated.brine_density=Calculate_Water_Density(pressureMPa, TCelcius, salinity)
     brine_density=Calculated.brine_density
     velocityA = ComputeVelocityA(pressureMPa, TCelcius, salinity)  
     IsCalculated.Brine_bulkmodulus= True
     KBrine= brine_density*math.pow(velocityA, 2)/1.0E6
     Calculated.Brine_bulkmodulus=KBrine
#     print('kBrine=',KBrine)
     return KBrine


def ComputeVelocityA(pressureMPa, TCelcius, salinity):
#'''
## Calculate water sound speed
## These equations could be check with the numerical values from : http://www.crewes.org/ResearchLinks/ExplorerPrograms/FlProp/FluidProp.htm
## Output:
##   velocityBrine[m/s]'''
 velocityW = 1402.85 + 1.524*pressureMPa + 3.437E-3*math.pow(pressureMPa, 2) - 1.197E-5*math.pow(pressureMPa, 3) +\
                            TCelcius*(4.871 - 0.0111*pressureMPa + 1.739E-4*math.pow(pressureMPa, 2) - 1.628E-6*math.pow(pressureMPa, 3)) +\
                            math.pow(TCelcius, 2)*(-0.04783 + 2.747E-4*pressureMPa - 2.135E-6*math.pow(pressureMPa, 2) + 1.237E-8*math.pow(pressureMPa, 3)) +\
                            math.pow(TCelcius, 3)*(1.487E-4 - 6.503E-7*pressureMPa - 1.455E-8*math.pow(pressureMPa, 2) + 1.327E-10*math.pow(pressureMPa, 3)) +\
                            math.pow(TCelcius, 4)*(-2.197E-7 + 7.987E-10*pressureMPa + 5.23E-11*math.pow(pressureMPa, 2) - 4.614E-13*math.pow(pressureMPa, 3))
 
 velocityBrine=  velocityW + salinity*(1170.0 - 9.6*TCelcius + 0.055*math.pow(TCelcius, 2) - 8.5E-5*math.pow(TCelcius, 3) +\
                                         2.6*pressureMPa - 0.0029*TCelcius*pressureMPa - 0.0476*math.pow(pressureMPa, 2)) +\
                   math.pow(salinity, 1.5)*(780.0 - 10.0*pressureMPa + 0.16*math.pow(pressureMPa, 2)) - 1820.0*math.pow(salinity, 2)                         
 return velocityBrine


def ComputeBrineConductivity(TCelcius, salinity):
    a1 = 7.15743
    a2 = -2.77595
    b1 = 2.94568
    b2 = -10.0649
    b3 = 33.6676
    sigma_water = 0.0000055 # //S/m
    sigma_as = 27.0 # // S/m fully saturated (NaCl) @25C
    amb_TC = 25.0 # // ambient temp TC 
    ws = salinity
    ws2 = ws * ws
    sig_aq_n = (a1 * ws + a2 * ws2) / (1.0 + b1 * ws + b2 * ws2 + b3 * ws2 * ws)
    CondW = (sigma_as * sig_aq_n + sigma_water) * (TCelcius + 21.5) / (amb_TC + 21.5) # with temperature correction from ambient (25 C) to reservoir tempC
    return CondW


def showError(text):
    print("Error:", text)
    return 1


def Validate():
  """To Validate the GUI Inputs"""
  global er, propS
  er = 1  
  # Check pressure
  PMPa = Input.pressure
  if (PMPa<Input.pressureMin or PMPa>Input.pressureMax):
      er = "Invalid pressure value, "+ str(PMPa)
      tkMessageBox.showerror("Error",er)    
      showError(er)
      return 1
# Check Temperature
  TDegC = Input.temperature
  if (TDegC<Input.temperatureMin or TDegC>Input.temperatureMax):
      er = "Invalid temperature value," + str(TDegC)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check Soil
  soil = Input.soil
  if (soil<0.0 or soil>1.0):
      er = "Invalid So value, "+ str(soil)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check Sgas
  sgas = Input.sgas
  if (sgas<0.0 or sgas>1.0):
      er = "Invalid Sgas value, "+ str(sgas)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check Swat
  swat = Input.swat
  if (swat<0.0 or swat>1.0):
      er = "Invalid Sgas value, "+ str(swat)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check water saturation     
  if(sgas+soil+swat>1.0):
      Input.swat=1.0-sgas-soil
      isActive()
      er = "Sum of oil, water, and gas saturations can not be more than 1.0. Sw is set as 1-soil-sgas "
      tkMessageBox.showerror("Error",er)        
      return 1   
# Check Salinity
  salinity = Input.salinity
  if (salinity <0 or salinity >=.3):
      er = "Invalid salinity value [>0.3]), "+ str(salinity)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check api
  api = Input.api
  if (api <Input.apiMin or api >Input.apiMax ):
      er = "Invalid api value, "+ str(api)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check specgravity
  specGravity = Input.gas_specific_gravity
  if (specGravity <Input.gas_specific_gravityMin or specGravity >Input.gas_specific_gravityMax ):
      er = "Invalid gas specific gravity value, "+str(specGravity)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check GOR
  GOR = Input.gasoil_ratio
  if (  GOR <Input.gasoil_ratioMin or GOR >Input.gasoil_ratioMax ):
      er = "Invalid GOR value, "+str(GOR)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check NTG
  NTG =  Input.net_to_gross
  if (NTG <Input.net_to_grossMin or NTG > Input.net_to_grossMax):
      er = "Invalid NTG value, " +str(NTG)
      tkMessageBox.showerror("Error",er)        
      return 1
# Rock Properties
# Check Rock Density    
  RhoRock =  Input.rockdensity
  if (RhoRock <Input.rockdensityMin or RhoRock>Input.rockdensityMax ):
      er = "Invalid rock density value, "+str(RhoRock)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check POR
  POR =  Input.porosity
  er = "Valid gas oil ratio"
  if (POR <0 or POR>1):
      er = "Invalid porosity value, "+str(POR)
      tkMessageBox.showerror("Error",er)  
      return 1
# Check cPOR
  CPOR =  Input.critical_porosity
  er = "Valid critical porosity value"
  if (CPOR <0 or CPOR<Input.porosity):
      er = "Invalid critical porosity value, "+str(CPOR)
      tkMessageBox.showerror("Error",er)  
      return 1
# Check vug fraction
  fv =  Input.vugfraction
  er = "Valid vug fraction value"
  
  if((RockPhysicModels.DryRockModelName=="Forward carbonate advisor") and (fv>0.2 or fv>=Input.porosity) ):
      er = "Invalidvug fraction value, "+str(fv)
      er = er + "\n Vugular porosity (fv) can not be larger than 0.2"+\
           "\n and has to be smaller than the porosity"
      tkMessageBox.showerror("Error",er) 
      return 1
# Krief exponent
  KriefExponent =  Input.KriefExponent
  er = 'Valid ' + InputPropNames.KriefExponent
  if (KriefExponent <1.0 or KriefExponent > 4.0 ):
      er = "Invalid exponent for Krief model, "+str(KriefExponent)
      tkMessageBox.showerror("Error",er)        
      return 1
# Input Kdry
  Kdry =  Input.Kdry
  er = 'Valid ' + InputPropNames.Kdry
  if (Kdry <=0.0 ):
      er = "Invalid value entered for Kdry, "+str(Kdry)
      tkMessageBox.showerror("Error",er)        
      return 1
# Input Gdry
  Gdry =  Input.Gdry
#  print("Gdry[GPa]=",Gdry)
  er = 'Valid ' + InputPropNames.Gdry
  if (Gdry <=0.0):
      er = "Invalid value entered for Gdry, "+str(Gdry)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check bulkmodulus
  Km =  Input.bulkmodulus
  er = "Valid bulkmodulus"
  if (Km <Input.bulkmodulusMin or Km>Input.bulkmodulusMax):
      er = "Invalid bulkmodulus value, "+str(Km)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check shearmodulus
  Gm =  Input.shearmodulus
  er = "Valid shearmodulus"
  if (Gm <Input.shearmodulusMin or Gm>Input.shearmodulusMax ):
      er = "Invalid shearmodulus value, "+str(Gm)
      tkMessageBox.showerror("Error",er)        
      return 1
# Aspect ratio1
  aratio1 =  Input.aratio1
  er = 'Valid ' + InputPropNames.aratio1
  if (aratio1 <0  ):
      er = "Invalid aspect ratio (1) value, "+str(aratio1)
      tkMessageBox.showerror("Error",er)        
      return 1
## aspect ratio2
#  aratio2 =  Input.aratio2
#  er = 'Valid ' + InputPropNames.aratio2
#  if (aratio2 <0 ):
#      er = "Invalid aspect ratio (2) value, "+str(aratio2)
#      tkMessageBox.showerror("Error",er)        
#      return 1
# Bulk moduli of inclusions
  K_inclusion1 =  Input.K_inclusion1
  er = 'Valid ' + InputPropNames.K_inclusion1
  if (K_inclusion1 <0):
      er = "Invalid volume fraction value, "+str(K_inclusion1)
      tkMessageBox.showerror("Error",er)        
      return 1
## Volume fraction 2
#  K_inclusion2 =  Input.K_inclusion2
#  er = 'Valid ' + InputPropNames.K_inclusion2
#  if (K_inclusion2 <0 ):
#      er = "Invalid volume fraction value, "+str(K_inclusion2)
#      tkMessageBox.showerror("Error",er)        
#      return 1
# Volume fraction1
  volfrac1 =  Input.volfrac1
  er = 'Valid ' + InputPropNames.volfrac1
  if (volfrac1 <0 or volfrac1>1.0 ):
      er = "Invalid volume fraction value, "+str(volfrac1)
      tkMessageBox.showerror("Error",er)        
      return 1
## Volume fraction 2
#  volfrac2 =  Input.volfrac2
#  er = 'Valid ' + InputPropNames.volfrac2
#  if (volfrac2 <0 or volfrac2>=1.0 ):
#      er = "Invalid volume fraction value, "+str(volfrac2)
#      tkMessageBox.showerror("Error",er)        
#      return 1
## Validate volfrac and K_inclusion
#  if (volfrac1 + volfrac2 + Input.porosity> 1.0 and (K_inclusion2>0.0 or  K_inclusion1>0.0) ):  # this is true only if inclusions are considered
#      er = "Void fractions can not be more than the unity, "+str(volfrac1 + volfrac2 + Input.porosity)
#      tkMessageBox.showerror("Error",er)        
#      return 1      
# Validate volfrac and K_inclusion
  if (volfrac1 + Input.porosity> 1.0 and (K_inclusion1>0.0) ):  # this is true only if inclusions are considered
      er = "Void fractions can not be more than the unity, "+str(volfrac1 + Input.porosity)
      tkMessageBox.showerror("Error",er)        
      return 1   
# Confining pressure effect on Kdry
# Check  confining_pressure
  Pconf= Input.confining_pressure
  er = "Valid confining pressure"
  if (Pconf <0 ):
      er = "Confining pressure, "+str(Pconf)
      tkMessageBox.showerror("Error",er)        
      return 1      
# Check  poisson ratio
  poisson_ratio= Input.poisson_ratio 
  er = "Valid poisson ratio"
  if (poisson_ratio <0 or poisson_ratio>0.5):
      er = "Poisson ratio, "+str(poisson_ratio)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check  coordintation number
  C= Input.coord_number
  er = "Valid coordination number"
  if (C <2 ):
      er = "coordination number, "+str(C)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check  coefficient for effective pressure
  CoefEffPres= Input.effPresCoef 
  er = "Valid effective pressure coefficient"
  if (CoefEffPres <0 ):
      er = "effective pressure coefficient, "+str(CoefEffPres)
      tkMessageBox.showerror("Error",er)        
      return 1    
# Check  coefficient for effective pressure
  Linear_CoefAG= Input.Linear_CoefAG 
  er = "Valid coefficient CoefAG"
  if (Linear_CoefAG <0 ):
      er = "Coefficient Linear_CoefAG, "+str(Linear_CoefAG)
      tkMessageBox.showerror("Error",er)        
      return 1
  Linear_CoefAK= Input.Linear_CoefAK 
  er = "Valid coefficient CoefAK"
  if (Linear_CoefAK <0 ):
      er = "Coefficient Linear_CoefAK, "+str(Linear_CoefAK)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check saturation exponent
  m =  Input.mExp
  er = "Valid cementation exponent"
  if (m <0 or m>3.0 ):
      er = "Cementation exponent, "+str(m)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check tortuosity
  tortuosity =  Input.tortuosity
  er = "Valid saturation exponent"
  if (tortuosity <0 or tortuosity>1.0 ):
      er = "Cementation exponent, "+str(tortuosity)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check saturation
  n =  Input.nExp
  er = "Valid saturation exponent"
  if (n <0 or n>3.0 ):
      er = "Cementation exponent, "+str(n)
      tkMessageBox.showerror("Error",er)        
      return 1
# Check cec
  cec =  Input.QvCEC
  er = "Valid CEC"
  if (cec <0 ):
      er = "Cementation exponent, "+str(cec)
      tkMessageBox.showerror("Error",er)        
      return 1
#
  rock_sigma_capture =  Input.rock_sigma_capture
  er = "Valid rock sigma-capture"
  if (rock_sigma_capture <0 ):
      er = "Rock sigma-capture, "+str(rock_sigma_capture)
      tkMessageBox.showerror("Error",er)        
      return 1
#  oil_sigma_capture =  Input.oil_sigma_capture
#  er = "Valid oil sigma-capture"
#  if (oil_sigma_capture <0 ):
#      er = "Oil sigma-capture, "+str(oil_sigma_capture)
#      tkMessageBox.showerror("Error",er)        
#      return 1
## Check 
#  brine_sigma_capture =  Input.brine_sigma_capture
#  er = "Valid brine sigma-capture"
#  if (brine_sigma_capture <0 ):
#      er = "Brine sigma capture, "+str(brine_sigma_capture)
#      tkMessageBox.showerror("Error",er)        
#      return 1
#  return 1
 
    
def ReinitializeIsCalculated():
    IsCalculated.Brine_density = False
    IsCalculated.Oil_density = False
    IsCalculated.Gas_density = False
    
    IsCalculated.brine_bulkmodulus = False
    IsCalculated.oil_bulkmodulus = False
    IsCalculated.gas_bulkmodulus = False
    
    IsCalculated.Fld_density = False 
    IsCalculated.Fld_bulkmodulus = False
    IsCalculated.Fld_vp = False 
    IsCalculated.Fld_ip = False
# rock_frame
    IsCalculated.Rock_FarmeBulkmodulus = False
    IsCalculated.Rock_FrameShearmodulus = False
    IsCalculated.poisson_ratio=False
     
    IsCalculated.poisson_ratio = False
    IsCalculated.DryRock_Density = False
    IsCalculated.DryRock_Bulkmodulus = False
    IsCalculated.DryRock_Shearmodulus= False
    
    IsCalculated.DryRock_vp=False
    IsCalculated.DryRock_ip=False
    IsCalculated.DryRock_vs=False
    IsCalculated.DryRock_is=False
# Effective
    IsCalculated.Eff_Density=False
    IsCalculated.Eff_Bulkmodulus=False
    IsCalculated.Eff_Shearmodulus=False
    IsCalculated.Eff_vp=False
    IsCalculated.Eff_vs=False
    IsCalculated.Eff_ip=False
    IsCalculated.Eff_is=False
    IsCalculated.Eff_Pressure=False
    
    IsCalculated.Eff_porosity=False

    IsCalculated.Eff_conductivity=False
    IsCalculated.Eff_resistivity=False 
    IsCalculated.Eff_neutron_sigma=False
    return 1


class IsActiveF():
    Fld_Rho=False
    Rock_Rho=False
    Dry_Rho=False
    Eff_Rho=False
    
    Fld_Kb=False  
    Rock_Kb=False  
    Dry_Kb=False 
    Eff_Kb=False   

    Rock_Gb=False     
    Dry_Gb=False 
    Eff_Gb=False   

    Rock_Vp=False        
    Fld_Vp=False    
    Dry_Vp=False     
    Eff_Vp=False
    
    Rock_Vs=False 
    Dry_Vs=False 
    Eff_Vs=False  
    Eff_VpVs=False  

    Rock_Ip=False    
    Fld_Ip=False
    Dry_Ip=False
    Eff_Ip=False    
    
    Rock_Is=False    
    Dry_Is=False
    Eff_Is=False
    Eff_PMod= False
    flgPMod= False
  
# Reflection
    Eff_Rpp=False
    Eff_Rps=False
    Fld_conductivity=False
    Eff_conductivity=False
    Fld_resistivity=False 
    Eff_resistivity=False 
    Eff_neutron_sigma=False
    CO2Dissolution = False
    flg2Dplot = False
    flgPlotHold = False
    flgCheckTLA = False
    flgTLbaseline= False
    Hs_pls= False
    Hs_pls_ave= False

 
class IsChecked():
    DPlot_2D_is_checked=False

  
class InputPropNames():
    pressure='Pressure'
    temperature='Temperature'
    soil='Oil saturation'
    sgas='Gas saturation'
    swat='Water saturation'
    salinity='Salinity'
    api='API of oil'
    gas_specific_gravity ='Gas specific gravity'
    gasoil_ratio='Gas oil ratio'
    net_to_gross='NTG'
    rockdensity='Rock density'
    porosity='Total porosity'
    critical_porosity='Critical porosity'
    bulkmodulus='Bulk modulus'
    shearmodulus='Shear modulus'
    vugfraction='Vug fraction(m3/m3)'
    KriefExponent='Krief exponent'
    Kdry='Input Kdry[GPa]'
    Gdry='Input Gdry[GPa]'
    
    aratio1='Aspect ratio 1'
    aratio2='Aspect ratio 2'
    volfrac1='volume fraction 1'
    volfrac2='volume fraction 2'
    K_inclusion1='bulkmod_inclusion1'
    K_inclusion2='bulkmod_inclusion2'
    confining_pressure= 'Confining pressure'
    poisson_ratio = 'Poisson ratio'
    coord_number='Corrdination number'
    effPresCoef = 'effective pressure coefficient'
# EM
    nExp='Cementation Exponent(n)'
    mExp='Cementation Exponent(m)'
    tortuosity='Tortuosity'
    QvCEC= 'CEC'
#   Nuclear
    rock_sigma_capture='Sigma-Capture (rock)'
#    oil_sigma_capture='Sigma-Capture (oil)'
#    brine_sigma_capture='Sigma-Capture(brine)'
#    gas_sigma_capture='Sigma-Capture(gas)'
# Reflection coefficients
    VpTop = 'Vp (top layer)'
    VsTop = 'Vs (top layer)'
    RhoTop = 'Density (top layer)'
    IncidentAngle='Incident angle' 


class Input(): 
    '''
    Input tab
    Fluid properties
    '''
    api=28.0    
    Ave_weight_frac =0.5     
    resolutionN = 20

    confining_pressure= 15 #
    pressure=10.0  
    pressureMin=9.0   
    pressureMax=25.0
    pressureResolution=5.0
    
    temperature=100.0    
    temperatureMin=35.0
    temperatureMax=250.0 
    temperatureResolution=5.0

    soil=0.4    
    soilMin=0.0    
    soilMax=1.0     
    soilResolution=0.05    

    sgas=0.05  
    sgasMin=0.0    
    sgasMax=1.0
    sgasResolution=0.05

    swat = 0.55
    swatMin=0.0    
    swatMax=1.0
    swatResolution=0.05
    salinity=0.0
    salMin=0.0
    salMax=0.3
    salResolution=0.05

    apiMin=10.0
    apiMax=200.0
    apiResolution=0.5

    gas_specific_gravityMin=0.0
    gas_specific_gravityMax=5.0
    gas_specific_gravityResolution=0.1

    gasoil_ratioMin=0.0 
    gasoil_ratioMax=200.0   
    gasoil_ratioResolution=0.5
    gas_specific_gravity=0.7     
    gasoil_ratio= 20.0
    
    net_to_gross=1.0  
    net_to_grossMin=0.0
    net_to_grossMax=1.0
    net_to_grossResolution=0.05

    CO2Flag="co2"
# rock frame 
    rockdensity=2650.0
    rockdensityMin=2000.0
    rockdensityMax=5000.0
    rockdensityResolution=10.0

    bulkmodulus=37.0
    bulkmodulusMin=0.0
    bulkmodulusMax=50.0
    bulkmodulusResolution=0.1

    shearmodulus=44.0   
    shearmodulusMin=0.0
    shearmodulusMax=50.0
    shearmodulusResolution=0.1    

    poisson_ratio = 0.01

    tortuosity = 0.1
    coord_number=9.0
    critical_porosity= 0.99
    
    K_inclusion1=2.25
    K_inclusion2=2.25

    aratio1=1.0
    aratio2= 0.01
    
    volfrac1=0.29
    volfrac2=0.01
    
    Linear_CoefAK=10.0
    Linear_CoefAG=10.0
    
# dry rock
    porosity= 0.3
    porosityMin=0.0
    porosityMax=1.0
    porosityResolution=0.05

    KriefExponent = 3.0
    Kdry = 20.0
    Gdry = 20.0

    MacBeth_Pk=1.0
    MacBeth_Ek=1.0
    MacBeth_Pg=1.0
    MacBeth_Eg=1.0    
    
    vugfraction=min(0.19,porosity*0.6)
# other
    CementSat=0.1
    GCement=3.0
    KCement=2.0
    CementPatchiness=0.1   
#    GClay=4.0
#    KClay=5.0
#    
    DeltaN1=0.4
    DeltaN2=0.1

    effPresCoef = 1.0
    eff_porosity= 1.0
# reclection coefficent
    RhoTop=2280.0
    IncidentAngle=30.0  
    VpTop=1850.0
    VsTop=1100.0
#resistivity
    nExp=2.0    
    mExp=2.0
    QvCEC=0.1
# nuclear capture
    rock_sigma_capture= 10.0
#    gas_sigma_capture=0.0
#    brine_sigma_capture= 100.0
#    oil_sigma_capture= 20.0    
# weights for the ave HS and voigt-Reuss
    HSRockFrameTable=[]

  
class Calculated():
# Fluid
    brine_density = 0.0
    oil_density = 0.0
    gas_density = 0.0
    bulk_fluid_density =0.0   
    
    RhoG_Mat=0   
    brine_bulkmodulus = 1.0
    oil_bulkmodulus = 1.0
    gas_bulkmodulus = 1.0
    fluid_density = 1.0    
    fluid_bulkmodulus=1.0
    brine_conductivity=0.0
    brine_resitivity=0.0
    
    fluid_vp =1.0
    fluid_ip =1.0
#  rock frame with inclusion
    rockframe_bulkmodulus =1.0
    rockframe_shearmodulus =1.0
    rockframe_density =1.0
    rockframe_vp =1.0
    rockframe_vs =1.0
    rockframe_Ip =1.0
    rockframe_Is =1.0
    poisson_ratio = 1.0
#Dry rock    
    DryRock_Density=1000.0
    DryRock_Bulkmodulus=1000.0
    DryRock_Shearmodulus=1000.0
    DryRock_vp=1000.0
    DryRock_vs=1000.0
    DryRock_ip=1000.0
    DryRock_is=1000.0
#Dry rock 
    Eff_porosity=Input.porosity*Input.net_to_gross 

    Eff_Density=1000.0
    Eff_Pressure=0.0
    Eff_Bulkmodulus=1000.0
    Eff_Shearmodulus=1000.0
    Eff_vp=1000.0
    Eff_vpvS=1.0
    Eff_vp_List=1000.0
    Eff_vs=1000.0
    Eff_ip=1000.0
    Eff_is=1000.0   
    Eff_Rpp=0.0
    Eff_Rps=0.0
    Eff_PModulus=0.0    
# reflection coef
    Eff_Rpp =0.0
    Eff_Rps =0.0
    theta1= 0.0
    theta2=0.0
    phi1=0.0
    phi2=0.0
    pratio =1.0  
    Eff_conductivity=0.0
    Eff_resistivity=0.0 
    Eff_neutron_sigma=0.0
# arrays    
    soilarray=0 
    apiarray=0 
    P_array = 1.0
    T_array = 1.0 
    So_array = 1.0 
    Sg_array = 1.0   

    sw_array=[]
    sg_array=[]
    so_array= []
    pressure_array= []
    temperature_array=[]       

    Salinity_array = 1.0
    Api_array = 1.0
    GOR_array = 1.0    
    NTG_array = 1.0
    GasSpeGrav_array = 1.0 

    
class IsCalculated():
    porosity = False
    Brine_density = False
    Oil_density = False
    Gas_density = False
    brine_bulkmodulus = False
    brine_conductivity=False
    brine_resistivity=False
    oil_bulkmodulus = False
    gas_bulkmodulus = False  
    
    Fld_density = False 
    Fld_bulkmodulus = False
    Fld_vp = False 
    Fld_ip = False
# rock frame
    Rock_Density = False
    Rock_FrameBulkmodulus = False
    Rock_FrameShearmodulus= False
    Rock_Framevp=False
    Rock_FrameIp=False
    Rock_FrameVs=False
    Rock_FrameIs=False
    poisson_ratio = False
# Dry
    DryRock_Density = False
    DryRock_Bulkmodulus = False
    DryRock_Shearmodulus= False
    DryRock_vp=False
    DryRock_ip=False
    DryRock_vs=False
    DryRock_is=False
# Effective
    Eff_Density=False
    Eff_Pressure=False
    Eff_PressureOnce=False    
    Eff_Bulkmodulus=False
    Eff_Shearmodulus=False
    Eff_vp=False
    Eff_vs=False
    Eff_ip=False
    Eff_is=False 
    Eff_Rpp=False
    Eff_Rss=False
    
    Eff_porosity=False

    Eff_conductivity=False
    Eff_resistivity=False 
    Eff_neutron_sigma=False
    

class RockPhysicModels():
    FSM_GassmannModel='Gassmann Model'
    FSM_PatcyModel='Patchy Saturation Model'
    FSM_HTI_0_PC11_SshC44='Gassmann [HTI(0):P-C11,Ssh-C44]'
    FSM_HTI_0_PC11_SsvC66='Gassmann [HTI(0):P-C11,Ssv-C66]'
    FSM_HTI_0_PC33_SC44='Gassmann [HTI(90):P-C33,S-C44]'
    FSM_ORTH_PC33_SC44='Gassmann [Orthorh:P-C33,S-C44]'
    FSM_ORTH_PC33_SC55='Gassmann [Orthorh:P-C33,S-C55]'
               
    effRockModelName={}
    DryRockModelName={}
    RockFrameModelName={}
    ConfiningPModelName={}
    FSMName={}
    RefCoefName={}
# EM model
    EMModelName={}

 
class PlotList():
    PlotName={}
    ColorList = ['ro-', 'b-o', 'g-o', 'k-o', 'r-*', 'b-*', 'g-*', 'k-*']


class PlotAux():
    varp='saturation'
    varp2D='Sw-Sg'
    varTL_Fwd='Forward'
    var1D_2DPlot='1D plot'
    fontsize=15
    canvWidth=450#380
    canvHeight=400#400
    

class InputVar():
    def __init__(self):
        self.api=StringVar(value=str(Input.api))
        self.aratio1=StringVar(value=str(Input.aratio1))
        self.aratio2=StringVar(value=str(Input.aratio2))
        self.Ave_weight_frac =StringVar(value=str(Input.Ave_weight_frac))
        
        self.bulkmodulus=StringVar(value=str(Input.bulkmodulus))
#        self.brine_sigma_capture=StringVar(value=str(Input.brine_sigma_capture))

        self.CementSat=StringVar(value=str(Input.CementSat))
        self.CementPatchiness=StringVar(value=str(Input.CementPatchiness))
        self.confining_pressure=StringVar(value=str(Input.confining_pressure))
        self.coord_number=StringVar(value=str(Input.coord_number)) 
        self.critical_porosity=StringVar(value=str(Input.critical_porosity))
        self.CO2Dissolution =  BooleanVar (value=IsActiveF.CO2Dissolution)
        self.CO2Flag = StringVar(value=Input.CO2Flag)
        self.DeltaN1=StringVar(value=str(Input.DeltaN1))
        self.DeltaN2=StringVar(value=str(Input.DeltaN2))

        self.effPresCoef=StringVar(value=str(Input.effPresCoef))
        self.eff_porosity=StringVar(value=str(Input.eff_porosity))
        self.gas_specific_gravity=StringVar(value=str(Input.gas_specific_gravity))

#        self.gas_sigma_capture=StringVar(value=str(Input.gas_sigma_capture))        
        self.gasoil_ratio=StringVar(value=str(Input.gasoil_ratio))
        self.GCement=StringVar(value=str(Input.GCement))
#        self.GClay=StringVar(value=str(Input.GClay))

        self.IncidentAngle=StringVar(value=str(Input.IncidentAngle))
        self.KCement=StringVar(value=str(Input.KCement))
#        self.KClay=StringVar(value=str(Input.KClay))

        self.K_inclusion1=StringVar(value=str(Input.K_inclusion1))
        self.K_inclusion2=StringVar(value=str(Input.K_inclusion2))        

        self.Linear_CoefAG=StringVar(value=str(Input.Linear_CoefAG))
        self.Linear_CoefAK=StringVar(value=str(Input.Linear_CoefAK))

        self.mExp=StringVar(value=str(Input.mExp))
        self.mExp=StringVar(value=str(Input.mExp))
        self.MacBeth_Pk=StringVar(value=str(Input.MacBeth_Pk))
        self.MacBeth_Ek=StringVar(value=str(Input.MacBeth_Ek))
        self.MacBeth_Pg=StringVar(value=str(Input.MacBeth_Pg))
        self.MacBeth_Eg=StringVar(value=str(Input.MacBeth_Eg))

        self.net_to_gross=StringVar(value=str(Input.net_to_gross))
        self.nExp=StringVar(value=str(Input.nExp))

#        self.oil_sigma_capture=StringVar(value=str(Input.oil_sigma_capture))

        self.poisson_ratio=StringVar(value=str(Input.poisson_ratio))
        self.porosity=StringVar(value=str(Input.porosity))
        self.pressure=StringVar(value=str(Input.pressure))

        self.QvCEC=StringVar(value=str(Input.QvCEC))

        self.RhoTop=StringVar(value=str(Input.RhoTop))
        self.rockdensity=StringVar(value=str(Input.rockdensity))
        self.rock_sigma_capture=StringVar(value=str(Input.rock_sigma_capture))

        self.sgas=StringVar(value=str(Input.sgas))
        self.shearmodulus=StringVar(value=str(Input.shearmodulus))
        self.soil=StringVar(value=str(Input.soil))
        self.swat=StringVar(value=str(Input.swat))
        self.salinity=StringVar(value=str(Input.salinity))

        self.temperature=StringVar(value=str(Input.temperature))
        self.tortuosity=StringVar(value=str(Input.tortuosity))

        self.volfrac1=StringVar(value=str(Input.volfrac1))
        self.volfrac2=StringVar(value=str(Input.volfrac2))
        self.VpTop=StringVar(value=str(Input.VpTop))
        self.VsTop=StringVar(value=str(Input.VsTop))
        self.vugfraction=StringVar(value=str(Input.vugfraction))
        self.KriefExponent=StringVar(value=str(Input.KriefExponent))
        self.Kdry=StringVar(value=str(Input.Kdry))
        self.Gdry=StringVar(value=str(Input.Gdry))

        
        self.RockFrameMod=StringVar()
        self.ConfMod=StringVar()
        self.FSMMod=StringVar()
        self.EMMod=StringVar()
        self.PlotMod=StringVar()
        self.DryMod=StringVar()
        self.ReflectionCoefMod=StringVar()

        self.flgRhoF= BooleanVar(False) 
        self.flgKbF= BooleanVar(False) 
        self.flgVpF= BooleanVar(False) 
        self.flgIpF= BooleanVar(False) 

        self.flgRhoR= BooleanVar(False) 
        self.flgKbR= BooleanVar(False) 
        self.flgGbR= BooleanVar(False) 
        self.flgVpR= BooleanVar(False) 
        self.flgVsR= BooleanVar(False) 
        self.flgIpR= BooleanVar(False) 
        self.flgIsR= BooleanVar(False) 

        self.flgRhoD= BooleanVar(False) 
        self.flgKbD= BooleanVar(False) 
        self.flgGbD= BooleanVar(False) 
        self.flgVpD= BooleanVar(False) 
        self.flgVsD= BooleanVar(False) 
        self.flgIpD= BooleanVar(False) 
        self.flgIsD= BooleanVar(False) 
        self.flgRhoE= BooleanVar(False) 
        self.flgKbE= BooleanVar(False) 
        self.flgGbE= BooleanVar(False) 
        self.flgVpE= BooleanVar(False) 
        self.flgVsE= BooleanVar(False) 
        self.flgVpVsE= BooleanVar(False) 
        self.flgIpE= BooleanVar(False) 
        self.flgIsE= BooleanVar(False) 
        
        self.flgCondE= BooleanVar(False) 
        self.flgResE= BooleanVar(False) 
        self.flgRppE= BooleanVar(False) 
        self.flgRpsE= BooleanVar(False) 
        self.flgNeutron= BooleanVar(False) 
        self.flgCheckTLA= BooleanVar(False) 
        self.flgPlotHold= BooleanVar(False) 
        self.flgPMod= BooleanVar(False)
        self.Eff_Rpp= BooleanVar(False)
        self.Eff_Rps= BooleanVar(False)
        self.Fld_conductivity= BooleanVar(False)
        self.Eff_conductivity= BooleanVar(False)
        self.Fld_resistivity= BooleanVar(False)
        self.Eff_resistivity= BooleanVar(False)
        self.Eff_neutron_sigma= BooleanVar(False)
        self.flg2Dplot =  BooleanVar(False)
        self.flgPlotHold =  BooleanVar(False)
        self.flgCheckTLA =  BooleanVar(False)
        self.flgTLbaseline=  BooleanVar(False)
        self.Hs_pls=  BooleanVar(False)
        self.Hs_pls_ave=  BooleanVar(False)

        
    def getvalue(self, propname):
        if(propname==InputPropNames.pressure):
            return self.pressure.get()
        elif(propname==InputPropNames.temperature):
            return self.temperature.get()
        elif(propname==InputPropNames.soil):
            return self.soil.get()
        elif(propname==InputPropNames.sgas):
            return self.sgas.get()
        elif(propname==InputPropNames.swat):
            return self.swat.get()
        elif(propname==InputPropNames.salinity):
            return self.salinity.get()
        elif(propname==InputPropNames.api):
            return self.api.get()
        elif(propname==InputPropNames.gas_specific_gravity):
            return self.gas_specific_gravity.get()
        elif(propname==InputPropNames.gasoil_ratio):
            return self.gasoil_ratio.get()
        elif(propname==InputPropNames.net_to_gross):
            return self.net_to_gross.get()


    def setvalue(self,propname, value):
        if(propname==InputPropNames.pressure):
            self.pressure.set(value=str(value))
        elif(propname==InputPropNames.temperature):
            self.temperature.set(value=str(value))
        elif(propname==InputPropNames.soil):
            self.soil.set(value=str(value))
        elif(propname==InputPropNames.sgas):
            self.sgas.set(value=str(value))
        elif(propname==InputPropNames.swat):
            self.swat.set(value=str(value))
        elif(propname==InputPropNames.salinity):
            self.salinity.set(value=str(value))
        elif(propname==InputPropNames.api):
            self.api.set(value=str(value))
        elif(propname==InputPropNames.gas_specific_gravity):
            self.gas_specific_gravity.set(value=str(value))
        elif(propname==InputPropNames.gasoil_ratio):
            self.gasoil_ratio.set(value=str(value))
        elif(propname==InputPropNames.net_to_gross):
            self.net_to_gross.set(value=str(value))
    

class SimpleTableInput(Frame):
    def __init__(self, parent, rows, columns):
        Frame.__init__(self, parent) 
        self._entry = {}
        self.rows = rows
        self.columns = columns
        print(columns)
        # register a command to use for validation
        self.vcmd = (self.register(self._validate), "%P")
        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = Entry(self, validate="key", width=13,  validatecommand=self.vcmd)
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)
        
        
    def append(self):
     row = self.rows
     for column in range(self.columns):
         index = (row, column)
         e = Entry(self, validate="key", width=8, validatecommand=self.vcmd)
         e.grid(row=row, column=column, stick="nsew")
         self._entry[index] = e
     self.rows += 1
     
     
    def delete(self):
        row = self.rows - 1
        for column in range(self.columns):
            index = (row, column)
            self._entry[index].grid_remove()
        self.rows -= 1   
    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                current_row.append(self._entry[index].get())
            result.append(current_row)
        return result
    def _validate(self, P):
        '''Perform input validation. 
        Allow only an empty value, or a value that can be converted to a float
        '''
        return True
        if P.strip() == "":
            return True
        try:
            f = float(P)
            print(f)
        except ValueError:
            self.bell()
            return False
        return True


class CreateTable(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        filename= "addRow.png"
        try:
            imgAdd = Image.open(filename)
        except (OSError, IOError):
#            er = "File addRow2.png not found"
            tkMessageBox.showinfo("File not found",filename)
        imgAdd = imgAdd.resize((20, 20), Image.ANTIALIAS)
        self.imageAdd = ImageTk.PhotoImage(imgAdd)    
        self.label1= Label(self,text='Name   ', justify='center')
        self.label1.grid(column=0,row=0, padx=2)      
        self.label2= Label(self,text='Vol.Frac', justify='center')
        self.label2.grid(column=2,row=0,  padx=8)       
        self.label3= Label(self,text='Density(kg/m3)',justify='center')
        self.label3.grid(column=3,row=0, padx=4)
# u'CO\u2082'
#u'Ks/m\u00B3'
        self.label4= Label(self,text='Ks(GPa)   ', justify='center')
        self.label4.grid(column=7,row=0)       
        self.label5= Label(self,text='Gs(GPa)    ',  justify='center')
        self.label5.grid(column=12,row=0)       
        filename= "Cancel.png"
        try:
            imgDel = Image.open(filename)
        except (OSError, IOError):
#            er = "File addRow2.png not found"
            tkMessageBox.showinfo("File not found",filename)            
        imgDel = imgDel.resize((20, 20), Image.ANTIALIAS)
        self.imageDel = ImageTk.PhotoImage(imgDel)     
        self.table = SimpleTableInput(self, 1, 5)
        self.submit = Button(self, text="Apply", command=self.on_submit)      
        self.table.grid(column=0,row=1, columnspan=15)# pack(side="top", fill="both", expand=True)
        self.addrow = Button(self,text="Add row", image=self.imageAdd, command=self.addrow)
        self.addrow.grid(column=0,row=2)
  #      self.addrow.config(image=self.imageAdd,width="25",height="25")       
        self.delterow = Button(self,image=self.imageDel, command=self.deleterow)
        self.delterow.grid(column=1,row=2)
        self.submit.grid(column=3,row=2) 


    def on_submit(self):
        Input.HSRockFrameTable= self.table.get()
        print(Input.HSRockFrameTable)


    def addrow(self):
        self.table.append()        


    def deleterow(self):
        self.table.delete()  


"""
Created on Thu Nov 17 16:09:55 2016

@author: BAltundas 
"""


def Calculate_Fluid_Bulkdensity():#(kg/m3)
    PMPa=Input.pressure
    TCelcius= Input.temperature
    Salinity=Input.salinity
    API=Input.api
    GOR=Input.gasoil_ratio
    GasSpecGravity=Input.gas_specific_gravity    
    so=Input.soil
    sg=Input.sgas
    sw=Input.swat     
    Calculated.brine_density=Calculate_Water_Density(PMPa, TCelcius, Salinity)
    Calculated.oil_density=Calculate_Oil_Density(PMPa, TCelcius, API, GOR,GasSpecGravity)
#    print('Oil density', Calculated.oil_density)
    if (Input.CO2Flag=="co2"):
        Calculated.gas_density=Calculate_CO2_Density(PMPa, TCelcius)
        Calculated.oil_density=Calculate_Oil_Density(PMPa, TCelcius, API, 0.0,GasSpecGravity)
        if(IsActiveF.CO2Dissolution):
             tkMessageBox.showerror("Error:", "CO2 Dissolution to be implelemented")          
    else:
        Calculated.oil_density=Calculate_Oil_Density(PMPa, TCelcius, API, GOR,GasSpecGravity)
        Calculated.gas_density=Calculate_HCGas_Density(PMPa, TCelcius, GasSpecGravity)
#    print('gas density', Calculated.gas_density)        
    IsCalculated.Fld_density=True
    Calculated.fluid_density= sw*Calculated.brine_density+so* Calculated.oil_density+sg*Calculated.gas_density
    return Calculated.fluid_density

   
def Calculate_Fluid_Kf(): #(MPa)
    PMPa=Input.pressure
    TCelcius= Input.temperature
    Salinity=Input.salinity
    API=Input.api
    GOR=Input.gasoil_ratio
    GasSpecGravity=Input.gas_specific_gravity
    so=Input.soil
    sg=Input.sgas
    sw=Input.swat   
    Calculated.brine_bulkmodulus=Calculate_Brine_Bulkmodulus(PMPa, TCelcius, Salinity)  
    if (Input.CO2Flag=="co2"):
        Calculated.gas_bulkmodulus= Calculate_CO2_Bulkmodulus(PMPa, TCelcius)
        Calculated.oil_bulkmodulus=Calculate_Oil_Bulkmodulus(PMPa, TCelcius, API, 0.0,GasSpecGravity)  
        if(IsActiveF.CO2Dissolution):
                tkMessageBox.showerror("Error:", "CO2 Dissolution to be implelemented")   
    else:
        Calculated.gas_bulkmodulus=Calculate_HCGas_Bulkmodulus(PMPa, TCelcius, GasSpecGravity)
        Calculated.oil_bulkmodulus=Calculate_Oil_Bulkmodulus(PMPa, TCelcius, API, GOR,GasSpecGravity)  
#    print('gas K', Calculated.gas_bulkmodulus) 
    term = sw/Calculated.brine_bulkmodulus+so/Calculated.oil_bulkmodulus + sg/Calculated.gas_bulkmodulus
    Calculated.fluid_bulkmodulus= 1.0/term
    IsCalculated.Fld_bulkmod=True
    return  Calculated.fluid_bulkmodulus

   
def Calculate_Fluid_Vp():#(m/s)
     k_f=Calculate_Fluid_Kf()    
     rho_f =Calculate_Fluid_Bulkdensity()
     Calculated.bulk_fluid_density=rho_f
     Calculated.fluid_bulkmodulus = 1.0E+3*k_f
     Calculated.fluid_vp= 1.0E+3*math.sqrt(k_f/rho_f)
     IsCalculated.Fld_vp=True
     return Calculated.fluid_vp

    
def Calculate_Fluid_Ip():
   vp_f=Calculate_Fluid_Vp()    
   Calculated.fluid_vp= vp_f
   rho_f =Calculate_Fluid_Bulkdensity()
   Calculated.bulk_fluid_density= rho_f
   IsCalculated.Fld_ip =True
   Calculated.fluid_ip = vp_f*rho_f/1.0E+6
   return Calculated.fluid_ip


class StdoutRedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area


    def write(self, str):
        self.text_area.update_idletasks()
        self.text_area.insert('end', str)
        self.text_area.see('end')

         
def CalculateOutput(output_frame):
  old_stdout = sys.stdout    
  textWindow = Text(output_frame, height=15, width=2,wrap='word', relief="sunken")
  scrollb = Scrollbar(output_frame)  
  textWindow.focus_set()
  textWindow.grid(column=0,row=9,columnspan=3,padx=2,pady=2,sticky="nsew") 
  scrollb.grid(row=9, column=5,columnspan=5)
  scrollb.config(command=textWindow.yview)
  textWindow.config(yscrollcommand=scrollb.set)
  sys.stdout = StdoutRedirector(textWindow)
  print("Output properties:")
  print("----------------------------------------")  
# Fluid properties  
  if(IsActiveF.Fld_Rho):  
      Calculated.bulk_fluid_density=Calculate_Fluid_Bulkdensity()
      print("Rho_fluid[kg/m3] = {0:.3f}".format(Calculated.bulk_fluid_density))
  if(IsActiveF.Fld_Kb):
      Calculated.fluid_bulkmodulus=Calculate_Fluid_Kf()
      print("K_fluid[MPa]     = {0:.3f}".format(Calculated.fluid_bulkmodulus))      
  if(IsActiveF.Fld_Vp):  
      Calculated.fluid_vp=Calculate_Fluid_Vp()
      print("Vp_fluid[m/s]    = {0:.3f}".format(Calculated.fluid_vp))
  if(IsActiveF.Fld_Ip):  
      Calculated.fluid_ip=Calculate_Fluid_Ip()
      print("Ip_fluid[kPa.s/m]= {0:.3f}".format(Calculated.fluid_ip))
      
# Rockframe properties
  if(IsActiveF.Rock_Rho):  
      Calculated.rockframe_density= Calculate_RockFrame_Density()
      print("Rho_rock[kg/m3]  = {0:.3f}".format(Calculated.rockframe_density))
# {0:.3f}.'.format(math.pi)
  if(IsActiveF.Rock_Kb):
      Calculated.rockframe_bulkmodulus=Calculate_RockFrame_Bulkmodulus()
      print("Ks_rock[GPa]     = {0:.3f}".format(Calculated.rockframe_bulkmodulus))
  if(IsActiveF.Rock_Gb):  
      Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
      print("Gs_rock[GPa]     = {0:.3f}".format(Calculated.rockframe_shearmodulus))
  if(IsActiveF.Rock_Vp):
      Calculated.rockframe_density =Calculate_RockFrame_Density()
      Calculated.rockframe_bulkmodulus=Calculate_RockFrame_Bulkmodulus()
      Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
      Calculated.rockframe_vp = math.sqrt(1.0E+9*(Calculated.rockframe_bulkmodulus + (4.0/3.0)*Calculated.rockframe_shearmodulus)/ Calculated.rockframe_density)
      print("Vp_rock[m/s]     = {0:.3f}".format(Calculated.rockframe_vp))
  if(IsActiveF.Rock_Vs):
      Calculated.rockframe_density =Calculate_RockFrame_Density()
      Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
      Calculated.rockframe_vs = math.sqrt(1.0E+9*Calculated.rockframe_shearmodulus/ Calculated.rockframe_density)
      print("Vs_rock[m/s]     = {0:.3f}".format(Calculated.rockframe_vs))
  if(IsActiveF.Rock_Ip):  
      Calculated.rockframe_density =Calculate_RockFrame_Density()
      Calculated.rockframe_bulkmodulus=Calculate_RockFrame_Bulkmodulus()
      Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
      Calculated.rockframe_vp = math.sqrt(1.0E+9*(Calculated.rockframe_bulkmodulus + (4.0/3.0)*Calculated.rockframe_shearmodulus)/ Calculated.rockframe_density)
      Calculated.rockframe_Ip = Calculated.rockframe_vp *  Calculated.rockframe_density/1000.0
      print("Ip_rock[kPa.s/m] = {0:.3f}".format(Calculated.rockframe_Ip))
  if(IsActiveF.Rock_Is):  
      Calculated.rockframe_density =Calculate_RockFrame_Density()
      Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
      Calculated.rockframe_vs = math.sqrt(1.0E+9*Calculated.rockframe_shearmodulus/ Calculated.rockframe_density)
      Calculated.rockframe_Is = Calculated.rockframe_vs *  Calculated.rockframe_density/1000.0
      print("Is_rock[kPa.s/m] = {0:.3f}".format(Calculated.rockframe_Is))
# Dry properties
  if(IsActiveF.Dry_Rho):
    Calculated.DryRock_Density = Calculate_DryRock_Density()
    print("Rho_dry[kg/m3]   = {0:.3f}".format(Calculated.DryRock_Density))
  if(IsActiveF.Dry_Kb):
    Calculated.DryRock_Bulkmodulus=Calculate_Dry_Rock_Bulkmodulus()
    print("Kdry[MPa]        = {0:.3f}".format(Calculated.DryRock_Bulkmodulus))
  if(IsActiveF.Dry_Gb):
    Calculated.DryRock_Shearmodulus=Calculate_Dry_Rock_Shearmodulus()
    print("Gdry[MPa]        = {0:.3f}".format(Calculated.DryRock_Shearmodulus))
  if(IsActiveF.Dry_Vp):
    Calculated.DryRock_vp=Calculate_VpDry()
    print("Vp_dry[m/s]      = {0:.3f}".format( 1.0E+3*Calculated.DryRock_vp))
  if(IsActiveF.Dry_Vs):
    Calculated.DryRock_vs=Calculate_VsDry()
    print("Vs_dry[m/s]      = {0:.3f}".format( 1.0E+3*Calculated.DryRock_vs))
  if(IsActiveF.Dry_Ip):
    Calculated.DryRock_Ip=Calculate_IpDry()
    print("Ip_dry[kPa.s/m]  = {0:.3f}".format(Calculated.DryRock_Ip))
  if(IsActiveF.Dry_Is):
    Calculated.DryRock_is=Calculate_IsDry()
    print("Is_dry[kPa.s/m]  = {0:.3f}".format( Calculated.DryRock_is))
# Effective properties
  if(IsActiveF.Eff_Rho):
    Calculated.Eff_Density=Calculate_Effective_Density()
    print("Rho_eff[kg/m3]   = {0:.3f}".format( Calculated.Eff_Density))
  if(IsActiveF.Eff_Kb):
    Calculated.Eff_Bulkmodulus=Calculate_Effective_Bulkmodulus()
    print("Kb_eff[MPa]      = {0:.3f}".format( Calculated.Eff_Bulkmodulus))
  if(IsActiveF.Eff_Gb):
    Calculated.Eff_Shearmodulus=Calculate_Effective_Shearmodulus()
    print("Gb_eff[MPa]      = {0:.3f}".format( Calculated.Eff_Shearmodulus))
  if(IsActiveF.Eff_Vp):
    Calculated.Eff_vp=Calculate_Effective_Vp()
    print("Vp_eff[m/s]      = {0:.3f}".format( Calculated.Eff_vp))
  if(IsActiveF.Eff_Vs):
    Calculated.Eff_vs=Calculate_Effective_Vs()
    print("Vs_eff[m/s]      = {0:.3f}".format(Calculated.Eff_vs))
  if(IsActiveF.Eff_VpVs):
    Calculated.Eff_vp=Calculate_Effective_Vp()
    Calculated.Eff_vs=Calculate_Effective_Vs()
    Calculated.Eff_vpvs=Calculated.Eff_vp/Calculated.Eff_vs
    print("Vp/Vs            = {0:.3f}".format(Calculated.Eff_vpvs))
  if(IsActiveF.Eff_Ip):
    Calculated.Eff_ip=Calculate_Effective_Ip()
    print("Ip_eff[kPa.s/m]  = {0:.3f}".format( Calculated.Eff_ip))
  if(IsActiveF.Eff_Is):
    Calculated.Eff_is=Calculate_Effective_Is()
    print("Is_eff[kPa.s/m]  = {0:.3f}".format(Calculated.Eff_is))
  if(IsActiveF.Eff_PMod):
    Calculated.Eff_PMod=Calculate_Effective_Pmodulus()
    print("M-Mod_eff[MPa]   = {0:.3f}".format(Calculated.Eff_PMod))   
# reflection coefficient  
  if (IsActiveF.Eff_Rpp or IsActiveF.Eff_Rps):
    Calculate_RPP_RPS_SetParameters()
  if(IsActiveF.Eff_Rpp):
    Calculated.Eff_Rpp=Calculate_Effective_Rpp()
    print("Rpp[]            = {0:.3f}".format(Calculated.Eff_Rpp))
  if(IsActiveF.Eff_Rps):
    Calculated.Eff_Rpp=Calculate_Effective_Rps()
    print("Rps[]            = {0:.3f}".format(Calculated.Eff_Rps))
# EM properties
  if(IsActiveF.Eff_conductivity):
    Calculated.Eff_conductivity=Calculate_Effective_Conductivity()
    IsCalculated.Eff_conductivity=True
    print("Conductivity_eff[S/m] ={0:.3f}".format(Calculated.Eff_conductivity))
  if(IsActiveF.Eff_resistivity):
    Calculated.Eff_resistivity=Calculate_Effective_Resistivity()
    print("Resistivity_eff[ohm.m]={0:.3f}".format( Calculated.Eff_resistivity))
# RST properties      
  if(IsActiveF.Eff_neutron_sigma):
    Calculated.Eff_neutron_sigma=Calculate_Effective_neutron_sigma()
    print("Neutron sigma_eff[c.u]={0:.3f}".format( Calculated.Eff_neutron_sigma ))
  sys.stdout = old_stdout
  return 1

  
def Calculate_CO2_Density(PressureMPa, TCelcius): 

# Ouput:
#   RhoCO2[g/cc]    
  co2DensityRef = 467.0
  co2CriticalPressure = 7.3773
  co2CriticalTemp = 304.1284   
  TKelvin= TCelcius + 273.15
  inverseTempR = co2CriticalTemp/TKelvin
  pressureR = PressureMPa/co2CriticalPressure
  
  a0 = (-6.4297*inverseTempR + 1.2478*math.pow(inverseTempR, 3))/(1.0 +\
      12.787*math.pow(inverseTempR, 2))
  a1 = (69.810 - 56.079*inverseTempR)/(1.0 - 0.9948*math.pow(inverseTempR, 2))
  a2 = (4.8232 - 11.6367*inverseTempR)/(1.0 - 0.9974*inverseTempR)
  a3 = 3.8632 + 14.6565*math.pow(inverseTempR, 2)
  a4 = (0.046*inverseTempR)/(1.0 - 0.9097*inverseTempR)
  a5 = (0.014 + 0.0159*math.pow(inverseTempR, 3))/(1.0 - 0.9158*inverseTempR)
  co2DensityR = a0*math.atan2(a1 + a2*pressureR, 1.0 + a3*pressureR) - \
       a0*math.atan(a1) + a4*pressureR/(1.0 + a5*pressureR)
  RCO2=co2DensityR*co2DensityRef # in kg/m3
  return RCO2
#
# Bulk Modulus of CO2
####################################
def Calculate_CO2_Bulkmodulus(PressureMPa, TCelcius): 
# Output:
#   KCO2[MPa]
  densityCO2 = Calculate_CO2_Density(PressureMPa, TCelcius) # in g/cc  
  co2Gamma=Calculate_CO2_Heatcapacity_ratio(PressureMPa, TCelcius)
  co2Compressibility_iso=Calculate_ISO_CO2_Compressibility(PressureMPa, TCelcius)
  KCO2= co2Gamma*(densityCO2/co2Compressibility_iso)/1000.0  
  return KCO2
#######################################################################
# Calculates Bulk Modulus of CO2
####################################
# Input: Pressure[MPa], Temperature[C], CO2 Density[g/cc]
# Output: Bulk modulus of CO2[MPa]
def Calculate_CO2_BulkmodulusWDen(PressureMPa, TCelcius, densityCO2): 
  co2Gamma=Calculate_CO2_Heatcapacity_ratio(PressureMPa, TCelcius)
  co2Compressibility_iso=Calculate_ISO_CO2_Compressibility(PressureMPa, TCelcius)
  KCO2= co2Gamma*(densityCO2/co2Compressibility_iso)    
#  print("KCO2= ",KCO2)
  return KCO2  
#######################################################################
# Calculates adiabatic compressibility of CO2
####################################
# Input: Pressure[MPa], Temperature[C]
# Output: Bulk modulus of CO2[MPa]
def Calculate_ISO_CO2_Compressibility(PressureMPa, TCelcius): 
  co2DensityRef = 0.467
  co2CriticalPressure = 7.3773
 
  co2CriticalTemp = 304.1284
  TKelvin= TCelcius + 273.15
  inverseTempR = co2CriticalTemp/TKelvin
  inverseTempR2=inverseTempR*inverseTempR
  inverseTempR3=inverseTempR2*inverseTempR
  pressureR = PressureMPa/co2CriticalPressure
  
  a0 = (0.046*inverseTempR)/(1.0 - 0.9097*inverseTempR)
  
  a1 = (0.014 + 0.0159*inverseTempR3)/(1.0 - 0.9158*inverseTempR)
  a2 = (-6.4297*inverseTempR + 1.2478*inverseTempR3)/(1.0 +\
        12.787*inverseTempR2)
  a3 = (4.8232 - 11.6367*inverseTempR)/(1.0 - 0.9974*inverseTempR)
  a4 = (69.81 - 56.079*inverseTempR)/(1.0 - 0.9948*inverseTempR2)
  a5 = 3.8632 + 14.6565*inverseTempR2
  drhodp= (a0/math.pow(1.0 + a1*pressureR, 2) + \
      a2*(a3 - a4*a5)/(1.0 + math.pow(a4, 2) + 2.0*a4*a3*pressureR + \
      2.0*a5*pressureR + math.pow(a3*pressureR, 2) + \
      math.pow(a5*pressureR, 2)))
  co2Compressibility_iso = co2DensityRef*drhodp/co2CriticalPressure   
  return co2Compressibility_iso  
#######################################################################
# Calculates heat ca[acity ratio of CO2
####################################
# Input: Pressure[MPa], Temperature[C]
# Output: Bulk modulus of CO2[MPa]
def Calculate_CO2_Heatcapacity_ratio(PressureMPa, TCelcius): 
  co2CriticalPressure = 7.3773 
  co2CriticalTemp = 304.1284  

  tempRinC = TCelcius/(co2CriticalTemp - 273.15)    # Tc/30.97

  pressureR = PressureMPa/co2CriticalPressure
  pressureR2=pressureR*pressureR
  pressureR3=pressureR2*pressureR
  
  tempRinC2=tempRinC*tempRinC
  tempRinC3=tempRinC2*tempRinC
  
  c0 = (1.80054 + 2.16216*pressureR)/(1.0 + 0.311519*pressureR2)
  c1 = (-11.9979 - 12.9002*pressureR + 3.51493*pressureR2)/(1.0 + \
       2.59049*pressureR2)
  c2 = (13.9135 - 1.69808*pressureR)/(1.0 + 1.53221*pressureR2 + \
        1.71231*pressureR3)
  c3 = (-3.85853 - 3.26199*pressureR)/(1.0 + 3.16209*pressureR2 + \
       0.169326*pressureR3)
  c4 = (27.0555 - 18.3289*pressureR + 5.17922*pressureR2)/(1.0 + \
        35.5424*pressureR2)
  c5 = (77.9646 - 5.70987*pressureR2)/(1.0 + 68.2891*pressureR2 +\
       207.209*pressureR3)
  co2Gamma = (c0 + c1*tempRinC + c2*tempRinC2)/(1.0 + c3*tempRinC+\
       c4*tempRinC2 + c5*tempRinC3)  
  return co2Gamma  
# Enf of the file
########################################
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 01 14:56:26 2017

@author: BAltundas
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 19:18:20 2016

@author: BAltundas
"""

#
#from MyGlobalClasses import  Input,   Calculated, IsCalculated
#import EffectiveProperties
#import DryRockProperties
#
def Get_RockFrame_BulkModulus():
    if(IsCalculated.Rock_FrameBulkmodulus):
        Ks= Calculated.rockframe_bulkmodulus
    else:
        Ks=Calculate_RockFrame_Bulkmodulus()
    Calculated.rockframe_bulkmodulus = Ks
    IsCalculated.Rock_FrameBulkmodulus = True
    return Ks
def Get_RockFrame_ShearModulus():
    if(IsCalculated.Rock_FrameShearmodulus):
        Gs= Calculated.rockframe_shearmodulus
    else:
        Gs=Calculate_RockFrame_Shearmodulus()
    Calculated.rockframe_shearmodulus = Gs
    IsCalculated.Rock_FrameShearmodulus = True
    return Gs    
def Calculate_Poisson_Ratio():   
    if(IsCalculated.poisson_ratio):
        poisson_ratio=Calculated.poisson_ratio
    else:
        Gs= Get_RockFrame_ShearModulus()
        Ks= Get_RockFrame_BulkModulus()
        poisson_ratio = (3.0*Ks -2.0*Gs)/(6.0*Ks+2.0*Gs)
        IsCalculated.poisson_ratio = True
        Calculated.poisson_ratio = poisson_ratio    
    return poisson_ratio
def Calculate_Kdry_with_Hertz_Mindlin():
    por =Calculate_Effective_Porosity()
    pressure = Calculate_Effective_Pressure()   
    poisson_ratio=Calculate_Poisson_Ratio()          
    C= Input.coord_number
    Gs= Get_RockFrame_ShearModulus()
    fac = C * (1.0 - por) * Gs / (math.pi * (1.0 - poisson_ratio))
    fac = fac * fac / 18.0
    Kdry = math.pow(fac * pressure, (1.0 / 3.0))
    Calculated.DryRock_Bulkmodulus = Kdry
    IsCalculated.DryRock_Bulkmodulus = True
    return Kdry

def Calculate_Gdry_with_Hertz_Mindlin():
    por =Calculate_Effective_Porosity()
    poisson_ratio=Calculate_Poisson_Ratio()       
    pressure = Calculate_Effective_Pressure()   
    C= Input.coord_number
    Gs = Get_RockFrame_ShearModulus()
    fac = C * (1.0 - por) * Gs / (math.pi * (1.0 - poisson_ratio))
    fac = 3.0 * fac * fac / 2.0
    Gdry = ((5.0 - 4 * poisson_ratio) / (5.0 * (2.0 - poisson_ratio))) * math.pow(fac * pressure, 1.0 / 3.0)
    Calculated.DryRock_Shearmodulus = Gdry
    IsCalculated.DryRock_Shearmodulus = True
    return Gdry

def Calculate_Kdry_with_Hertz_Mindlin_HSL():
    por =Calculate_Effective_Porosity()
    cpor = Input.critical_porosity    
    GHM = Calculate_Gdry_with_Hertz_Mindlin() 
    KHM = Calculate_Kdry_with_Hertz_Mindlin()
    Km = Calculated.rockframe_bulkmodulus   
    rel_por = por / cpor
    GHM_term = (4.0 / 3.0) * GHM
    fac = rel_por / (KHM + GHM_term) + (1.0 - rel_por) / (Km + GHM_term)
    return math.pow(fac, -1.0) - GHM_term

def Calculate_Gdry_with_Hertz_Mindlin_HSL():
    por =Calculate_Effective_Porosity()
    cpor = Input.critical_porosity
    GHM = Calculate_Gdry_with_Hertz_Mindlin() 
    KHM = Calculate_Kdry_with_Hertz_Mindlin()
    Gm = Calculated.rockframe_shearmodulus
    rel_por = por / cpor
    z_term = (GHM / 6.0) * (9.0 * KHM + 8.0 * GHM) / (KHM + 2.0 * GHM)
    fac = rel_por / (GHM + z_term) + (1.0 - rel_por) / (Gm + z_term)
    return math.pow(fac, -1.0) - z_term

def Calculated_Kdry_Linear(k_dry):   
    coefAK = Input.Linear_CoefAK
    effpres  = Calculate_Effective_Pressure()
    return k_dry +  coefAK * effpres

def Calculated_Gdry_Linear(g_dry):   
    coefAG = Input.Linear_CoefAG
    effpres  = Calculate_Effective_Pressure()
#    effpres = PresConfin - N * PressurePore
    return g_dry + coefAG * effpres

def Calculated_Kdry_McBeth():     
    effpres  = Calculate_Effective_Pressure()
#    effpres = PresConfin - N * PressurePore  
    ModuliInfty=12.0 # update this
    
    Pkm = Input.MacBeth_Pk
    Ekm = Input.MacBeth_Ek
    return ModuliInfty / (1.0 + Ekm * math.exp(-effpres / Pkm))
    
def Calculated_Gdry_McBeth():     
    effpres  = Calculate_Effective_Pressure()
#    effpres = PresConfin - N * PressurePore  
    ModuliInfty=12.0 # update this
    Pkm = Input.MacBeth_Pg
    Ekm = Input.MacBeth_Eg
    return ModuliInfty / (1.0 + Ekm * math.exp(-effpres / Pkm))

# Contact cement model begin
def CalculateBulkModulus_HSAverage(Vcl, Kq,  Gq,  Kcl,  mucl):
    Ksplus = Kq + Vcl / (1.0 / (Kcl - Kq) + (1.0 - Vcl) / (Kq + (4.0 / 3.0) * Gq))
    Ksminus = Kcl + (1.0 - Vcl) / (1.0 / (Kq - Kcl) + Vcl / (Kcl + (4.0 / 3.0) * mucl))
    Ks = (Ksminus + Ksplus) / 2.0
    return Ks

def CalculateBulkModulus_withConfiningPressure( Mus, Pressure,  n,  nu,  phi0):
#        { // Hertz-Mindlin
    pi = 1.0 * math.pi
    Ku1 = math.pow((n * n * (1.0 - phi0) * (1.0 - phi0) * Mus * Mus * Pressure) / (18.0 * pi * pi * (1.0 - nu) * (1.0 - nu)), 1.0 / 3.0)
    return Ku1

def Dvorkin_Nur_Coefficeints( nu,  nuc,  G,  Gc,  alpha):
#        {
#         //   double nuc = nu;
    pi = 1.0 * math.pi
#            // equations in the Appendix
#            // G-shear modulus of grain
#            // Gc- shear modulus of cement
#            // poison ratio of the cement
    Ln = (2.0 * Gc / (pi * G)) * ((1.0 - nu) * (1.0 - nuc)) / (1.0 - 2.0 * nuc)
    Lt = Gc / (pi * G)
    At = -1.0E-2 * (2.26 * nu * nu + 2.07 * nu + 2.3) * math.pow(Lt, (0.079 * nu * nu + 0.1754 * nu - 1.342))
    Bt = (0.0573 * nu * nu + 0.0937 * nu + 0.202) * math.pow(Lt, (0.0274 * nu * nu + 0.0529 * nu - 0.8765))
    Ct = (1.0/10000.0) * (9.654 * nu * nu + 4.945 * nu + 3.1) * math.pow(Lt, (0.01867 * nu * nu + 0.4011 * nu - 1.8186))
    An = -0.024153*math.pow(Ln, -1.3646)
    Bn = 0.20405 *math.pow(Ln, (-0.89008))
    Cn = 0.00024649 * math.pow(Ln, (-1.9864))
    Sn = An * alpha * alpha + Bn * alpha + Cn
    St = At * alpha * alpha + Bt * alpha + Ct
    return Ln,  Lt,  At,  Bt,  Ct, An, Bn, Cn, Sn, St

def Calculate_Kdry( n,  Mc,  phi0,  Sn):
#        { // Mc, Gc, compresional and shear moduli of cement
#            // Eq.1- Effective bulk modulus of dry rock with cement grains 
            return (1.0 / 6.0) * n * (1.0 - phi0) * Mc * Sn

def CalculateShearModulus_HSAverage(Vcl, Kq, Gq, Kcl,Gcl):
    Gplus = Kq + Vcl / (1.0 / (Gcl - Gq) + (2.0 * (1.0 - Vcl) * (Kq + 2.0 * Gq)) / (5.0 * Gq * (Kq + (4.0 / 3) * Gq)))
    Gminus = Gcl + (1.0 - Vcl) / (1.0 / (Gq - Gcl) + (2.0 * Vcl * (Kcl + 2.0 * Gcl)) / (5.0 * Gcl * (Kcl + (4.0 / 3.0) * Gcl)))
    Gs = (Gminus + Gplus) / 2.0
    return Gs
            
def CalculateShearModulus_withConfiningPressure(Mus,  Pressure,  n, nu, phi0):
#        { // Hetrz-Mindlin
    pi = 1.0 * math.pi;
    muu1 = ((5.0 - 4.0 * nu) / (5.0 * (2.0 - nu))) * math.pow((3.0 * n * n * (1.0 - phi0) *(1.0 - phi0) * Mus * Mus *Pressure) / (2.0 * pi * pi * (1.0 - nu) * (1.0 - nu)), 1.0 / 3.0)
    return muu1

def Calculate_Gdry( n,  Kc, Gc,  phi0,  St):
#            // Mc, Gc, compresional and shear moduli of cement
#            // Kc:- effective bulk modulus of dry rock under confining pressure
#            // Eq.1- Effective shear modlus of dry rock with cement grains 
    return (3.0 / 5.0) * Kc + (3.0 / 20.0) * n * (1.0 - phi0) * Gc * St

# main
def Calculate_Kdry_ContactCement():
    
    effStress = Calculate_Effective_Pressure()

    porosity =Calculate_Effective_Porosity()
    criticalPorosity = Input.critical_porosity
    coordinationNumber = Input.coord_number 
    
    Gc = Input.GCement
    Kc = Input.KCement
#    Gcl = Input.GClay
#    Kcl = Input.KClay
    
    cementSaturation = Input.CementSat
    CementPatchiness = Input.CementPatchiness
    
#    ntg = Input.net_to_gross
#    Vcl = 1.0 - ntg
    
    poisson_ratio=Calculate_Poisson_Ratio()       

    Gs = Calculated.rockframe_shearmodulus
    Ks = Calculated.rockframe_bulkmodulus
    
#    Ks = CalculateBulkModulus_HSAverage(Vcl, Km, Gm, Kcl, Gcl)# HS+- averaged bulk modulus of rock grian 
#    Gs = CalculateShearModulus_HSAverage(Vcl, Km, Gm, Kcl, Gcl) # // HS+- averaged shear modulus of rock grian  

    Ks1 = CalculateBulkModulus_withConfiningPressure(Gs, effStress, coordinationNumber, poisson_ratio, criticalPorosity);
    Gs1 = CalculateShearModulus_withConfiningPressure(Gs, effStress, coordinationNumber, poisson_ratio, criticalPorosity);
    
    alpha = 2.0 * math.pow(cementSaturation * criticalPorosity / (3.0 * coordinationNumber * (1 - criticalPorosity)), 0.25);                 
    poisson_ratio_cement = (3.0 * Kc - Gc) / (6.0 * Kc + 2.0 * Gc);
    
    Ln,  Lt,  At,  Bt,  Ct, An, Bn, Cn, Sn, St =Dvorkin_Nur_Coefficeints(poisson_ratio, poisson_ratio_cement, Gs, Gc, alpha)
    
    Kdry_c = Calculate_Kdry(coordinationNumber, Kc, criticalPorosity, Sn)
    Gdry_c = Calculate_Gdry(coordinationNumber, Kdry_c, Gc, criticalPorosity, St)
    
    # HS- bound using patchiness of clay
    Kdry_clay = Kdry_c + (1.0 - CementPatchiness) / (1.0 / (Ks1 - Kdry_c) + CementPatchiness / (Kdry_c + (4.0 / 3.0) * Gdry_c));
    Gdry_clay = Gdry_c + (1.0 - CementPatchiness) / (1.0 / (Gs1 - Gdry_c) + 2.0 * CementPatchiness * (Kdry_c + 2.0 * Gdry_c) / (5.0 * Gdry_c * (Kdry_c + (4.0 / 3.0) * Gdry_c)));
    #               // Eq 5
    phirel = porosity / criticalPorosity
    
    Kdry = 1.0 / (phirel / (Kdry_clay + (4.0 / 3.0) * Gdry_clay) + (1.0 - phirel) / (Ks + (4.0 / 3.0) * Gdry_clay)) - (4.0 / 3.0) * Gdry_clay
    return Kdry  # MPa

def Calculate_Gdry_ContactCement():
# main
    effStress = Calculate_Effective_Pressure()
    
    porosity =Calculate_Effective_Porosity()
    criticalPorosity = Input.critical_porosity
    coordinationNumber = Input.coord_number
    
    Gc = Input.GCement
    Kc = Input.KCement
#    Gcl = Input.GClay
#    Kcl = Input.KClay
    
    cementSaturation = Input.CementSat
    CementPatchiness = Input.CementPatchiness
    
#    ntg= Input.net_to_gross
    
#    Vcl = 1.0 - ntg

    poisson_ratio=Calculate_Poisson_Ratio()     
    poisson_ratio_cement = (3.0 * Kc - Gc) / (6.0 * Kc + 2.0 * Gc);

    Gs = Calculated.rockframe_shearmodulus
#    Ks = Calculated.rockframe_bulkmodulus

#
#    Gm = Get_RockFrame_ShearModulus()
#    Km = Get_RockFrame_BulkModulus()
 
#    Gs = CalculateShearModulus_HSAverage(Vcl, Km, Gm, Kcl, Gcl) # // HS+- averaged shear modulus of rock grian  
    
    Ks1 = CalculateBulkModulus_withConfiningPressure(Gs, effStress, coordinationNumber, poisson_ratio, criticalPorosity)
    Gs1 = CalculateShearModulus_withConfiningPressure(Gs, effStress, coordinationNumber, poisson_ratio, criticalPorosity)
    
    alpha = 2.0 * math.pow(cementSaturation * criticalPorosity / (3.0 * coordinationNumber * (1 - criticalPorosity)), 0.25)
        
    Ln,  Lt,  At,  Bt,  Ct, An, Bn, Cn, Sn, St =Dvorkin_Nur_Coefficeints(poisson_ratio, poisson_ratio_cement, Gs, Gc, alpha)
    
    Kdry_c = Calculate_Kdry(coordinationNumber, Kc, criticalPorosity, Sn)
    Gdry_c = Calculate_Gdry(coordinationNumber, Kdry_c, Gc, criticalPorosity, St)
                    
    # HS- bound using patchiness of clay
    Kdry_clay = Kdry_c + (1.0 - CementPatchiness) / (1.0 / (Ks1 - Kdry_c) + CementPatchiness / (Kdry_c + (4.0 / 3.0) * Gdry_c));
    Gdry_clay = Gdry_c + (1.0 - CementPatchiness) / (1.0 / (Gs1 - Gdry_c) + 2.0 * CementPatchiness * (Kdry_c + 2.0 * Gdry_c) / (5.0 * Gdry_c * (Kdry_c + (4.0 / 3.0) * Gdry_c)))
    #
    #               // Eq 5
    phirel = porosity / criticalPorosity
    term1=Gdry_clay + (Gdry_clay / 6.0) * ((9 * Kdry_clay + 8.0 * Gdry_clay) / (Kdry_clay + 2.0 * Gdry_clay))
    term2=Gs + (Gdry_clay / 6.0) * ((9.0 * Kdry_clay + 8.0 * Gdry_clay) / (Kdry_clay + 2.0 * Gdry_clay))
    term3=(9.0 * Kdry_clay + 8.0 * Gdry_clay) / (Kdry_clay + 2.0 * Gdry_clay)
    Gdry = 1.0 / (phirel / (term1) + (1 - phirel) / (term2 )) -  (Gdry_clay / 6.0) * (term3 )
    return Gdry # MPa
# contact cement end
#########################################
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 16:42:57 2016

@author: BAltundas
"""

#from MyGlobalClasses import IsCalculated, Calculated, Input, RockPhysicModels
#import DryRockProperties
#import EffectiveProperties
#
#from SolveDEM import Calculate_KGFrame_with_DEM   
#from WaterProperties import Calculate_Water_Density
#import ConfiningPressureEffect 

########################### Rock fram properties
def Calculate_RockFrame_Density():
    val=0

    if(RockPhysicModels.RockFrameModelName=="User input"):
        val= Input.rockdensity
    elif (RockPhysicModels.RockFrameModelName=="DEM" or 
        RockPhysicModels.RockFrameModelName=="Self-consistent" or 
        RockPhysicModels.RockFrameModelName=="Kuster-Toksoz"):
        
        f=Input.volfrac1  # volume fraction of bulk rock frame
#        f2=Input.volfrac2  # volume fraction of bulk rock frame
        # if there is any cinlsuion, rock frame density is updated with the assumption that
        # inclusions are filled with brine at P and T provided     
        pressureMPa = Input.pressure
        TCelcius = Input.temperature
        salinity = Input.salinity        
        RhoBrine=Calculate_Water_Density(pressureMPa, TCelcius, salinity)        
#        val= Input.rockdensity*(1- f1 - f2) + (f1+f2)*RhoBrine
        val= Input.rockdensity*(1- f ) + f*RhoBrine
    elif(RockPhysicModels.RockFrameModelName == "HS+" or   
    RockPhysicModels.RockFrameModelName == 'HS-' or
    RockPhysicModels.RockFrameModelName == "Voigt" or
    RockPhysicModels.RockFrameModelName == 'Reuss' or
    RockPhysicModels.RockFrameModelName == 'HSAve' or
    RockPhysicModels.RockFrameModelName == 'Voigt-Reuss'):
        val=0.0
        table=np.matrix(Input.HSRockFrameTable)
        colN=len(table[:,0])
        for i in range(0, colN):
            frac=float(table[i,1])
            den= float(table[i,2])
 #           print('i=',i, table[i,1],table[i,2], frac*den)
            val = val + frac*den        
    Calculated.rockframe_density =  val   
    return Calculated.rockframe_density

        
def Calculate_RockFrame_Bulkmodulus():
    # output Km [GPa]
    val1=0.0
    val2=0.0
    
    if(RockPhysicModels.RockFrameModelName=="DEM"):
        [val1,val2]= Calculate_KGFrame_with_DEM()
    elif( RockPhysicModels.RockFrameModelName=="Self-consistent"):
        [val1,val2]=Calculate_KGFrame_SelfConsistent()
    elif (RockPhysicModels.RockFrameModelName=="Kuster-Toksoz"):
        [val1,val2]=Calculate_KGFrame_KT()
    elif (RockPhysicModels.RockFrameModelName == "HS+"):   
        val1=Calculate_Km_HSPlus()
    elif (RockPhysicModels.RockFrameModelName == 'HS-'):
        val1=Calculate_Km_HSMinus()
    elif (RockPhysicModels.RockFrameModelName == "Voigt"):
        val1=Calculate_KsGs_Voigt(3)
    elif (RockPhysicModels.RockFrameModelName == 'Reuss'):
        val1=Calculate_KsGs_Reuss(3) 
    elif (RockPhysicModels.RockFrameModelName == 'HSAve' ):
        weigthFrac= Input.Ave_weight_frac
        val1=Calculate_Km_HSPlus()
        val2=Calculate_Km_HSMinus()
        val1=val1*weigthFrac + val2*(1.0-weigthFrac)
    elif (RockPhysicModels.RockFrameModelName == 'Voigt-Reuss'):
        weigthFrac= Input.Ave_weight_frac
        val1=Calculate_KsGs_Voigt(3) # 3 for K, 4 for G
        val2=Calculate_KsGs_Reuss(3)
        val1=val1*weigthFrac + val2*(1.0-weigthFrac)
    elif (RockPhysicModels.RockFrameModelName == 'VR-HS'):
        print('add this later')
    else:
        val1=Input.bulkmodulus
    Calculated.rockframe_bulkmodulus=val1
    
    IsCalculated.Rock_FrameBulkmodulus=True    
    return Calculated.rockframe_bulkmodulus   # GPa
#

def Calculate_RockFrame_Shearmodulus():
    if(RockPhysicModels.RockFrameModelName=="DEM"):
        [val1,val2]= Calculate_KGFrame_with_DEM()  # val1->K, val2->g
    elif( RockPhysicModels.RockFrameModelName=="Self-consistent"):
        [val1,val2]=Calculate_KGFrame_SelfConsistent()  # val1->K, val2->g
    elif (RockPhysicModels.RockFrameModelName=="Kuster-Toksoz"):
        [val1,val2]=Calculate_KGFrame_KT()  # val1->K, val2->g
    elif (RockPhysicModels.RockFrameModelName == "HS+"):   
        val2=Calculate_Gm_HSPlus()
    elif (RockPhysicModels.RockFrameModelName == 'HS-'):
        val2=Calculate_Gm_HSMinus()
    elif (RockPhysicModels.RockFrameModelName == "Voigt"):
        val2= Calculate_KsGs_Voigt(4)
    elif (RockPhysicModels.RockFrameModelName == 'Reuss'):
        val2=Calculate_KsGs_Reuss(4)
    elif (RockPhysicModels.RockFrameModelName == 'HSAve' ):
        weigthFrac= Input.Ave_weight_frac
        val1=Calculate_Gm_HSPlus()
        val2=Calculate_Gm_HSMinus()
        val2=val1*weigthFrac + val2*(1.0-weigthFrac)
    elif (RockPhysicModels.RockFrameModelName == 'Voigt-Reuss'):
        weigthFrac= Input.Ave_weight_frac
        val1=Calculate_KsGs_Voigt(4) # 3 for K, 4 for G
        val2=Calculate_KsGs_Reuss(4)
        val2=val1*weigthFrac + val2*(1.0-weigthFrac)
    elif (RockPhysicModels.RockFrameModelName == 'VR-HS'):
        print('add this later')
    else:
        val2=Input.shearmodulus        
    Calculated.rockframe_shearmodulus =val2
    IsCalculated.Rock_FarmeBulkmodulus=True    
    return Calculated.rockframe_shearmodulus  # GPa
    
#HsPlus
def Calculate_Km_HSPlus():
    table=np.matrix(Input.HSRockFrameTable)
    maxGm, minGm=MaxMin(table,4)
    Calculated.rockframe_bulkmodulus=Calculate_Km_HSPlusMinus(table,maxGm)
    return Calculated.rockframe_bulkmodulus
#HsPlus
def Calculate_Km_HSMinus():
    table=np.matrix(Input.HSRockFrameTable)
    maxGm, minGm=MaxMin(table,4) # 4 for G, 3 for K
    Calculated.rockframe_bulkmodulus=Calculate_Km_HSPlusMinus(table,minGm)
    return Calculated.rockframe_bulkmodulus
    
def MaxMin(table,indx):
    colN=len(table[:,0])
    maxval=0.0
    minval=1.0E+16
    for i in range(0, colN):
        val=float(table[i,indx])
        if (maxval<val):
            maxval=val
        if (minval>val):
            minval=val
    return maxval,minval
#HsMinus
def Calculate_Km_HSPlusMinus(table, maxminGm):
    val=0.0
    colN=len(table[:,0])
    for i in range(0, colN):
        frac=float(table[i,1])
        km= float(table[i,3])
        val =  val + frac/(km + 4.0*maxminGm/3.0 )        
    Calculated.rockframe_bulkmodulus = 1.0/val - 4.0*maxminGm/3.0 # in GPa
    return Calculated.rockframe_bulkmodulus
    
#HsPlus
def Calculate_Gm_HSPlus():
    table=np.matrix(Input.HSRockFrameTable)
    maxKm, minKm=MaxMin(table,3)
    maxGm, minGm=MaxMin(table,4)
    zmax=zeta(maxKm, maxGm)
    Calculated.rockframe_bulkmodulus=Calculate_Gm_HSPlusMinus(table,zmax)
    return Calculated.rockframe_bulkmodulus
#HsPlus
def Calculate_Gm_HSMinus():
    table=np.matrix(Input.HSRockFrameTable)
    maxKm, minKm=MaxMin(table,3)
    maxGm, minGm=MaxMin(table,4)
    zmin=zeta(minKm, minGm)
    Calculated.rockframe_bulkmodulus=Calculate_Gm_HSPlusMinus(table,zmin)
    return Calculated.rockframe_bulkmodulus
    
def Calculate_Gm_HSPlusMinus(table, z):
    val=0.0
    colN=len(table[:,0])
    for i in range(0, colN):
        frac=float(table[i,1])
        gm= float(table[i,4])
        if(gm==0.0 and z==0):
            continue
        val =  val + frac/(gm + z ) 
    Calculated.rockframe_bulkmodulus = 1.0/val - z # in GPa
    return Calculated.rockframe_bulkmodulus
    
def zeta(k, g):
    return g*((9.0*k+8.0*g)/(k+2.0*g))/6.0

def Calculate_KsGs_Reuss(indx):
    sumV=0.0
    table=np.matrix(Input.HSRockFrameTable)
    colN=len(table[:,0])
    for i in range(0, colN):
        frac_i=float(table[i,1])
        val_i= float(table[i,indx])
        if(val_i==0.0):
            continue
        sumV = sumV + frac_i /val_i 
    return 1.0 / sumV
  
def Calculate_KsGs_Voigt(indx):
    sumV=0.0
    table=np.matrix(Input.HSRockFrameTable)
    colN=len(table[:,0])
    for i in range(0, colN):
        frac_i=float(table[i,1])
        val_i= float(table[i,indx])
        sumV = sumV + frac_i * val_i 
    return sumV    
#
def Calculate_KGFrame_KT():
    global f, aratio, theta_BSC, fn_BSC, f_frac, ks_BSC, gs_BSC

    Nval=2
    
    a1=Input.aratio1
    a2=Input.aratio2
    aratio=np.array([a1, a2])
    
    [theta_BSC, fn_BSC]=CalculateThetaFn(Nval,aratio)
     
    ki1= Input.K_inclusion1
    ki2= Input.K_inclusion2
    ki=np.array([ki1, ki2])
    
    gi1 =0.0
    gi2 =0.0
    gi=np.array([gi1, gi2]) 
    
    g0 = Input.shearmodulus
    k0 = Input.bulkmodulus
    
    f1=Input.volfrac1
    f2=Input.volfrac2 
    f_frac=np.array([f1, f2])
   
    
    a=gi/g0 -1.0 
    b=(1.0/3.0)*(ki/k0 - gi/g0)
    
    nusc=(3.0*k0-2.0*g0)/(2.0*(3.0*k0+g0)) 
    r=(1.0-2.0*nusc)/(2.0*(1.0-nusc))

    [p,q]= BerrymanSC(2,theta_BSC, fn_BSC, a,b,r)     
    
    ksum= (ki1-k0)*f1*p[0] + (ki2-k0)*f2*p[1]
    gsum= (gi1-g0)*f1*q[0] + (gi2-g0)*f2*q[1]

    Gterm = g0*4.0/3.0
    Zterm= g0*(9.0*k0 +8.0*g0)/(k0+2.0*g0)/6.0

    k= ((k0 +Gterm)*k0 +ksum*Gterm)/(k0 + Gterm - ksum)   
    g= ((g0 +Zterm)*g0 +gsum*Zterm)/(g0 + Zterm - gsum)    
    return k, g
#    
def Calculate_KGFrame_SelfConsistentforDry():
    global f, aratio, theta_BSC, fn_BSC, f_frac, ks_BSC, gs_BSC

    Nval=2 # this includes the rock mineral face
    
    a0=Input.aratio1
    a1=Input.aratio2
    
    aratio=np.array([a0,a1])
    
    [theta_BSC, fn_BSC]=CalculateThetaFn(Nval,aratio)
     
#    k0 = Input.bulkmodulus
    ki1= Input.K_inclusion1
    ki2= Input.K_inclusion2

#    g0 = Input.shearmodulus
    gi1= 0.0
    gi2= 0.0
     
    f0= Input.volfrac1
    f1= Input.volfrac2 
#    f0= 1.0 - f1 - f2
    f_frac=np.array([f0,f1])
   
    ks=np.array([ki1, ki2])
    gs=np.array([gi1, gi2]) 
    
    ksc=np.dot(f_frac,ks) 
    gsc=np.dot(f_frac,gs)    
    
    x0=np.array([ksc, gsc]) # voigt based Initial guess  
    res=scipy.optimize.root(func_BSC, x0, method ='krylov')
#    print(res.x[0], res.x[1])
    return res.x
#
def Calculate_KGFrame_SelfConsistent():
    global f, aratio, theta_BSC, fn_BSC, f_frac, ks_BSC, gs_BSC

    Nval=3 # this includes the rock mineral face
    
    a0= 1.0
    a1=Input.aratio1
    a2=Input.aratio2
    
    aratio=np.array([a0,a1, a2])
    
    [theta_BSC, fn_BSC]=CalculateThetaFn(Nval,aratio)
     
    k0 = Input.bulkmodulus
    ki1= Input.K_inclusion1
    ki2= Input.K_inclusion2

    g0 = Input.shearmodulus
    gi1= 0.0
    gi2= 0.0
     
    f1= Input.volfrac1
    f2= Input.volfrac2 
    f0= 1.0 - f1 - f2
    f_frac=np.array([f0,f1, f2])
   
    ks=np.array([k0, ki1, ki2])
    gs=np.array([g0, gi1, gi2]) 
    
    ksc=np.dot(f_frac,ks) 
    gsc=np.dot(f_frac,gs)    
    
    x0=np.array([ksc, gsc]) # voigt based Initial guess  
    res=scipy.optimize.root(func_BSC, x0, method ='krylov')
#    print(res.x[0], res.x[1])
    return res.x

def func_BSC(x):
    ksc, gsc = x
#    bulkmodulus= Calculated.rockframe_bulkmodulus
#    shearmodulus= Calculated.rockframe_shearmodulus
    
    bulkmodulus= Input.bulkmodulus
    shearmodulus= Input.shearmodulus
    ks=np.array([bulkmodulus, Input.K_inclusion1, Input.K_inclusion2])   
    gs=np.array([shearmodulus, 0.0, 0.0])   
    a=gs/gsc -1.0 
    b=(1.0/3.0)*(ks/ksc - gs/gsc) 
    nusc=(3.0*ksc-2.0*gsc)/(2.0*(3.0*ksc+gsc)) 
    r=(1.0-2.0*nusc)/(2.0*(1.0-nusc))
              
    [p,q]= BerrymanSC(3,theta_BSC, fn_BSC, a,b,r)    
    
    ksp=(ksc-ks)*p
    gsq=(gsc-gs)*q
 
    return np.inner(f_frac,ksp), np.inner(f_frac,gsq)

    
def BerrymanSC(Nval,theta, fn, a,b,r):
    f=np.zeros((9,Nval))
    p=np.zeros(Nval)
    q=np.zeros(Nval)
    for i in range(0, Nval):
        ae=a[i]
        be=b[i]
        fne=fn[i]
        thetae=theta[i]
#
        f[0,i]=1.0+ae*(1.5*(fne+thetae)-r*(1.5*fne+2.5*thetae-4.0/3.0))
        f[1,i]=1+ae*(1.0 + 1.5*(fne + thetae)-(r/2.0)*(3.0*fne+5.0*thetae))+be*(3.0-4.0*r)
        f[1,i]=f[1,i]+(ae/2)*(ae+3*be)*(3-4*r)*(fne+thetae-r*(fne-thetae+2*math.pow(thetae, 2)))    
        f[2,i]=1.0+ae*(1.0-(fne+1.5*thetae)+r*(fne+thetae))
        f[3,i]=1.0+(ae/4.0)*(fne+3.0*thetae-r*(fne-thetae))
        f[4,i]=ae*(-fne+r*(fne+thetae-(4.0/3.0))) + be*thetae*(3.0-4.0*r)
        f[5,i]=1.0+ae*(1.0+fne-r*(fne+thetae))+be*(1.0-thetae)*(3.0-4.0*r)
        f[6,i]=2.0+(ae/4.0)*(3.0*fne+9.0*thetae-r*(3.0*fne+5.0*thetae)) + be*thetae*(3.0-4.0*r)
        f[7,i]=ae*(1.0-2.0*r+(fne/2.0)*(r-1.0)+(thetae/2.0)*(5.0*r-3.0))+be*(1.0-thetae)*(3.0-4.0*r)
        f[8,i]=ae*((r-1.0)*fne-r*thetae) + be*thetae*(3.0-4.0*r)
#        
        pp=3.0*f[0,i]/f[1,i]
        qq=(2.0/f[2,i]) + (1.0/f[3,i]) +(np.dot(f[3,i],f[4,i]) + \
            np.dot(f[5,i],f[6,i]) - np.dot(f[7,i],f[8,i]))/(np.dot(f[1,i],f[3,i]))
        p[i]=pp/3.0
        q[i]=qq/5.0
    return p, q

def CalculateThetaFn(Nval,aratio):
    theta=np.zeros(Nval)
    fn=np.zeros(Nval)
    for i in range(0, Nval ):
        a=aratio[i]
        a2=a*a
        if (a<1 or a==1):
            a=a*0.99  # mutiplied by 0.99 to avoid division by zero
            a2=a*a
            th=(a/math.pow(1.0-a2,1.5))*(math.acos(a) - a*math.sqrt(1.0-a2))
        else:
            th=(a/math.pow(a2-1.0,1.5))*(a*math.sqrt(a2-1.0)-math.acosh(a))
        fnn=(a2/(a2-1.0))*(2.0-3.0*th)
        theta[i]=th
        fn[i]=fnn
    return theta, fn
################################################
def BerrymanSC0(theta, fn, a,b,r):
    f=np.zeros(9)
    ae=a
    be=b
    fne=fn
    thetae=theta
#
    f[0]=1.0+ae*(1.5*(fne+thetae)-r*(1.5*fne+2.5*thetae-4.0/3.0))
    f[1]=1.0+ae*(1.0 + 1.5*(fne + thetae)-(r/2.0)*(3.0*fne+5.0*thetae))+be*(3.0-4.0*r)
    f[1]=f[1]+(ae/2.0)*(ae+3.0*be)*(3.0-4.0*r)*(fne+thetae-r*(fne-thetae+2.0*math.pow(thetae, 2)))    
    f[2]=1.0+ae*(1.0-(fne+1.5*thetae)+r*(fne+thetae))
    f[3]=1.0+(ae/4.0)*(fne+3.0*thetae-r*(fne-thetae))
    f[4]=ae*(-fne+r*(fne+thetae-(4.0/3.0))) + be*thetae*(3.0-4.0*r)
    f[5]=1.0+ae*(1.0+fne-r*(fne+thetae))+be*(1.0-thetae)*(3.0-4.0*r)
    f[6]=2.0+(ae/4.0)*(3.0*fne+9.0*thetae-r*(3.0*fne+5.0*thetae)) + be*thetae*(3.0-4.0*r)
    f[7]=ae*(1.0-2.0*r+(fne/2.0)*(r-1.0)+(thetae/2.0)*(5.0*r-3.0))+be*(1.0-thetae)*(3.0-4.0*r)
    f[8]=ae*((r-1.0)*fne-r*thetae) + be*thetae*(3.0-4.0*r)
      
    pp=3.0*f[0]/f[1]
    qq=(2.0/f[2]) + (1.0/f[3]) +(np.dot(f[3],f[4]) + \
    np.dot(f[5],f[6]) - np.dot(f[7],f[8]))/(np.dot(f[1],f[3]))
    p=pp/3.0
    q=qq/5.0
    return p, q

def CalculateThetaFn0(aratio):
    a=aratio
    a2=a*a
    if (a<1 or a==1):
        a=a*0.99  # mutiplied by 0.99 to avoid division by zero
        a2=a*a
        th=(a/math.pow(1.0-a2,1.5))*(math.acos(a) - a*math.sqrt(1.0-a2))
    else:
        th=(a/math.pow(a2-1.0,1.5))*(a*math.sqrt(a2-1.0)-math.acosh(a))
    fnn=(a2/(a2-1.0))*(2.0-3.0*th)
    theta=th
    fn=fnn
    return theta, fn
  
################################################
def f(y, t, params):
    a0, Ki, Gi =   params  # unpack parameters
    K, G = y      # unpack current values of y
    [theta_BSC, fn_BSC]=CalculateThetaFn0(a0)
    a=Gi/G -1.0 
    b=(1.0/3.0)*(Ki/K - Gi/G) 
    nusc=(3.0*K-2.0*G)/(2.0*(3.0*K+G)) 
    r=(1.0-2.0*nusc)/(2.0*(1.0-nusc))
    
    [piK,qiG]= BerrymanSC0(theta_BSC, fn_BSC, a,b,r)

#   f = (Ki - Km) * P / (1.0 - pori), (G1-Gm) *Q /(1-por)
#  rhs of DEM equations
    yprime = [(1.0/(1.0-t))*(Ki-K)*piK,      
             (1.0/(1.0-t))*(Gi-G)*qiG]
    return yprime
    
###########################################################
# Main ODE solver
# uses scypy ODE
def Calculate_KGFrame_with_DEM():
    K0=Input.bulkmodulus
    G0=Input.shearmodulus
    
    inclusion_por1=Input.volfrac1
    inclusion_por2=Input.volfrac2

    if inclusion_por1>0.0:
        ai=Input.aratio1    
        Ki=Input.K_inclusion1
        G_inclusion1=0.0    
        Gi= G_inclusion1
        params = [ai, Ki, Gi]    # Bundle constant parameters for ODE solver        
        y0 = [K0, G0]    # Bundle initial conditions for ODE solver
        tStop=inclusion_por1 
        tInc = tStop/20.0
        t = np.arange(0., tStop + tInc, tInc)
# Call the ODE solver
        KG_soln1 = odeint(f, y0, t, args=(params,))    # f - is the function (yprime)
        Tlen=len(t)
        K0= KG_soln1[Tlen-1,0] 
        G0= KG_soln1[Tlen-1,1]

    if inclusion_por2>0.0:
        ai=Input.aratio2    
        Ki=Input.K_inclusion2

        G_inclusion2=0.0
    
        Gi= G_inclusion2
        params = [ai, Ki, Gi]    # Bundle constant parameters for ODE solver
        
        y0 = [K0, G0]    # Bundle initial conditions for ODE solver
        tStop=inclusion_por2 
        tInc = tStop/20.0
        t = np.arange(0., tStop + tInc, tInc)
# Call the ODE solver
        KG_soln2 = odeint(f, y0, t, args=(params,))    # f - is the function (yprime)
        Tlen=len(t)
        K0= KG_soln2[Tlen-1,0] 
        G0= KG_soln2[Tlen-1,1]
    return K0, G0
# End of rock frame bulk and shear moduli          
######################### Dry rock properties ######
def Calculate_DryRock_Density():        
    por = Calculate_Effective_Porosity()
    rock_density= Calculate_RockFrame_Density()
    IsCalculated.DryRock_Density=True
    RhoDry= (1.0-por)*rock_density
    return  RhoDry
 
def Calculate_Dry_Rock_Shearmodulus():
# Input: por, Ks[GPa], Kdry [GPa]
# Output: Kdry [MPa]
# Input: por, Ks[GPa]
# Output: Kdry [MPa]
    Calculated.rockframe_shearmodulus=Calculate_RockFrame_Shearmodulus()
    eff_press = Calculate_Effective_Pressure() 
        
    if(RockPhysicModels.ConfiningPModelName=="Linear"):
        if ( eff_press <= 0.0):
            if(not IsCalculated.Eff_PressureOnce):
                    IsCalculated.Eff_PressureOnce=True
                    print('*** Confining pressure effect is neglected.')
                    print('==> Effective pressure is not positive,', eff_press )
                    print('' )

            value=Function_Gdry(Calculated.rockframe_shearmodulus)
        else:            
            Gdry=Function_Gdry(Calculated.rockframe_shearmodulus) # not applied confining pressure yet
            value=Calculated_Kdry_Linear(Gdry)
    else:
        value=Function_Gdry(Calculated.rockframe_shearmodulus)
    Calculated.DryRock_Shearmodulus=1.0E3*value 
    IsCalculated.DryRock_Shearmodulus=True
    return Calculated.DryRock_Shearmodulus 

def Calculate_Dry_Rock_Bulkmodulus():
# Input: por, Ks[GPa]
# Input Kdry [GPa]
# Output: Kdry [MPa]
    Calculated.rockframe_bulkmodulus=Calculate_RockFrame_Bulkmodulus()    
#    eff_press = Calculate_Effective_Pressure()    
    value=Function_Kdry(Calculated.rockframe_bulkmodulus)
#
#        else:            
#            Kdry=Function_Kdry(Calculated.rockframe_bulkmodulus) # 
#            value=Calculated_Kdry_Linear(Kdry)
#    else:
#        value=Function_Kdry(Calculated.rockframe_bulkmodulus)  
        
    IsCalculated.DryRock_Bulkmodulus=True    
    Calculated.DryRock_Bulkmodulus=1.0E3*value 
    return Calculated.DryRock_Bulkmodulus

def Function_Kdry(Kframe):
    porosity = Calculate_Effective_Porosity()

    if(RockPhysicModels.DryRockModelName=="Forward carbonate advisor"):
        value=Calculate_Kdry_FCarbonateAdvisor()
    elif(RockPhysicModels.DryRockModelName=="Krief"):
        value=Calculate_KGDry_KriefwExp(Input.KriefExponent,porosity, Kframe) 
    elif(RockPhysicModels.DryRockModelName=="Krief with critical porosity"):
        value=Calculate_KGDry_CriticalPor(porosity, Input.critical_porosity,Kframe)    
    elif(RockPhysicModels.DryRockModelName=='Contact cement'):
        value= Calculate_Kdry_ContactCement()
    elif(RockPhysicModels.DryRockModelName=='Hertz-Mindlin'):
        value= Calculate_Kdry_with_Hertz_Mindlin()
    elif(RockPhysicModels.DryRockModelName=='Hertz-Mindlin with HS-'):
        value= Calculate_Gdry_with_Hertz_Mindlin_HSL()
    elif(RockPhysicModels.DryRockModelName=='User input'):
        value= Input.Kdry
    else:
        print('Issue with Kdry')
        value=0.0
    return value 

def Function_Gdry(Gframe):
    porosity = Calculate_Effective_Porosity()
    if(RockPhysicModels.DryRockModelName=="Forward carbonate advisor"):
        value=Calculate_Gdry_FCarbonateAdvisor()
    elif(RockPhysicModels.DryRockModelName=="Krief"):
        value=Calculate_KGDry_KriefwExp(Input.KriefExponent,porosity, Gframe) 
    elif(RockPhysicModels.DryRockModelName=="Krief with critical porosity"):
        value=Calculate_KGDry_CriticalPor(porosity, Input.critical_porosity,Gframe)    
    elif(RockPhysicModels.DryRockModelName=='Contact cement'):
        value= Calculate_Gdry_ContactCement()
    elif(RockPhysicModels.DryRockModelName=='Hertz-Mindlin'):
        value= Calculate_Gdry_with_Hertz_Mindlin()
    elif(RockPhysicModels.DryRockModelName=='Hertz-Mindlin with HS-'):
        value=Calculate_Gdry_with_Hertz_Mindlin_HSL()
    elif(RockPhysicModels.DryRockModelName=='User input'):
        value= Input.Gdry
    else:
        print('Issue with Gdry')
        value=0.0
    return value 

def Calculate_DryRockWithConfiningPressure_Shearmodulus():
# Input:  Gd[GPa]
# Output: Gd [GPa]
    pressure = Calculate_Effective_Pressure()

 # Pressure correction on Kdry
    if(RockPhysicModels.ConfiningPModelName=="Hertz-Mindlin"):
         value=Calculate_Gdry_with_Hertz_Mindlin(pressure)
    elif(RockPhysicModels.ConfiningPModelName=="Hertz-Mindlin with HS-"):
        value=Calculate_Gdry_with_Hertz_Mindlin_HSL()
    elif(RockPhysicModels.ConfiningPModelName=="MacBeth"):
        value=Calculated_Gdry_McBeth()
    else:
        value= Calculated.DryRock_Shearmodulus       
    Calculated.DryRock_Shearmodulus = value
    IsCalculated.DryRock_Shearmodulus = True
    return Calculated.DryRock_Shearmodulus

def Calculate_DryRockwithConfiningPressure_Bulkmodulus():
# Input:  Kd[GPa]
# Output: Kd [GPa] with confining pressure
    pressure = Calculate_Effective_Pressure()
    
 # Pressure correction on Kdry
    if(RockPhysicModels.ConfiningPModelName=="Hertz-Mindlin"):
        value=Calculate_Kdry_with_Hertz_Mindlin(pressure)
    elif(RockPhysicModels.ConfiningPModelName=="Hertz-Mindlin with HS-"):
        value=Calculate_Kdry_with_Hertz_Mindlin_HSL()
    elif(RockPhysicModels.ConfiningPModelName=="MacBeth"):
        value=Calculated_Kdry_McBeth()
    else:
        value= Calculated.DryRock_Bulkmodulus 
    Calculated.DryRock_Bulkmodulus = value
    IsCalculated.DryRock_Bulkmodulus = True
    return Calculated.DryRock_Bulkmodulus
        
def Calculate_KGDry_Krief(por, KmGm):  
#      por = Input.porosity*Input.net_to_gross
      if por>=1.0:
          return 0.0
      else:
          Exponent=3.0/(1.0-por)
          return KmGm*pow((1.0-por),Exponent)
 
def Calculate_KGDry_KriefwExp(expon,por, KmGm):  
#      por = Input.porosity*Input.net_to_gross
      if por>=1.0:
          return 0.0
      else:
          Exponent=expon/(1.0-por)
          return KmGm*pow((1.0-por),Exponent)     
      
def Calculate_KGDry_CriticalPor(por, cpor, KmOrGm):  
    if por>=1.0:
        return 0.0
    else:
        return KmOrGm*(1.0-por/cpor) 
###
def Calculate_Kdry_FCarbonateAdvisor():
    por=   Calculate_Effective_Porosity()
# volume fraction of vug in connected pores    
    fv=Input.vugfraction
    Ksolid = Calculated.rockframe_bulkmodulus
    Gsolid = Calculated.rockframe_shearmodulus
 
    fm = por - fv
    Gh =  Calculate_KGDry_Krief(por, Gsolid)
    porM = fm / (1.0 - fv) 
    KIntra = Ksolid
    Kh =  Calculate_KGDry_Krief(porM, KIntra)
    
    Kdry= 4.0 * Gh * Kh * (1 - fv) / (4.0 * Gh + 3.0 * Kh * fv)   
    return Kdry

def Calculate_Gdry_FCarbonateAdvisor():
      por=   Calculate_Effective_Porosity()
      fv=Input.vugfraction
      Ksolid = Calculated.rockframe_bulkmodulus
      Gsolid = Calculated.rockframe_shearmodulus
      fm = por - fv

      porM = fm / (1.0 - fv)
      GIntra = Gsolid;
      KIntra = Ksolid;
      Kh =  Calculate_KGDry_Krief(porM, KIntra)
      Gh =  Calculate_KGDry_Krief(porM, GIntra)

# Gdry is inverted from Eq 10-12 in SPe71704 by Ramakrishnan
# Gdry =  1/16 (8 Gh - 20 fv Gh - 9 Kh + 3 fv Kh + Sqrt[(-8 Gh + 20 fv Gh + 9 Kh - 3 fv Kh)^2 - 32 (-9 Gh Kh + 18 fv Gh Kh)])
      term1 = Gh * (8.0 - 20.0 * fv) + Kh * (-9.0 + 3.0 * fv)
      term2 = math.pow(-term1, 2.0) - 32.0 * Gh * Kh * (-9.0 + 18.0 * fv)
      Gdry = (term1 + math.sqrt(term2)) / 16.0
      return Gdry

    
def Calculate_VpDry():
    if(IsCalculated.DryRock_Bulkmodulus==False):
        Calculated.DryRock_Bulkmodulus=Calculate_Dry_Rock_Bulkmodulus()
    K_dry=Calculated.DryRock_Bulkmodulus
    if(IsCalculated.DryRock_Shearmodulus==False):
        Calculated.DryRock_Shearmodulus=Calculate_Dry_Rock_Shearmodulus()
    G_dry=Calculated.DryRock_Shearmodulus
   
    if(IsCalculated.DryRock_Density==False):
        Calculated.DryRock_Density=Calculate_DryRock_Density()
    rho_dry=Calculated.DryRock_Density
    IsCalculated.DryRock_vp=True
    Calculated.DryRock_vp = math.sqrt(K_dry/rho_dry + (4.0/3.0)*G_dry/rho_dry )
    return Calculated.DryRock_vp

def Calculate_VsDry():
    if(IsCalculated.DryRock_Shearmodulus==False):
        Calculated.DryRock_Shearmodulus=Calculate_Dry_Rock_Shearmodulus()
    G_dry=Calculated.DryRock_Shearmodulus
   
    if(IsCalculated.DryRock_Density==False):
        Calculated.DryRock_Density=Calculate_DryRock_Density()
    rho_dry=Calculated.DryRock_Density
    IsCalculated.DryRock_vs=True
    Calculated.DryRock_vs= math.sqrt(G_dry/rho_dry )
    return  Calculated.DryRock_vs

def Calculate_IpDry():
    if(IsCalculated.DryRock_Density==False):
        Calculated.DryRock_Density=Calculate_DryRock_Density()
    rho_dry=Calculated.DryRock_Density
    if(IsCalculated.DryRock_vp==False):
        Calculated.DryRock_vp=Calculate_VpDry()
    vp_dry=Calculated.DryRock_vp
    IsCalculated.DryRock_ip=True
    Calculated.DryRock_ip= vp_dry*rho_dry
    return Calculated.DryRock_ip

def Calculate_IsDry():
#    if(IsCalculated.DryRock_Density==False):
    Calculated.DryRock_Density=Calculate_DryRock_Density()
    rho_dry=Calculated.DryRock_Density
#    if(IsCalculated.DryRock_vs==False):
    Calculated.DryRock_vs=Calculate_VsDry()
    vs_dry=Calculated.DryRock_vs   
    Calculated.DryRock_is= vs_dry*rho_dry
#    IsCalculated.DryRock_is=True
    return Calculated.DryRock_is
######################
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 19:18:20 2016

@author: BAltundas
"""


#from MyGlobalClasses import  Input, IsCalculated,  Calculated, RockPhysicModels
#from GassmannAnisotropic import  AnisotropicModels
#import BulkFluidProperties
#import DryRockProperties
#import WaterProperties
#import OilProperties
#
def Calculate_Effective_Pressure():    
    if(IsCalculated.Eff_Pressure):
         eff_press = Calculated.Eff_Pressure
    else:
        porepres = Input.pressure
        PresConfin = Input.confining_pressure
        N= Input.effPresCoef
        eff_press  = PresConfin - N * porepres
#        eff_press  = Calculate_Effective_Pressure()
        Calculated.Eff_Pressure =  eff_press      
        IsCalculated.Eff_Pressure=True
    return eff_press

def Calculate_Effective_Porosity():
    IsCalculated.Eff_porosity=True
    Calculated.Eff_porosity= Input.porosity*Input.net_to_gross
    return  Calculated.Eff_porosity
    
def Calculate_Effective_Density():   
    por=Calculate_Effective_Porosity()
    rho_f=Calculate_Fluid_Bulkdensity()
    rho_dryrock=Calculate_DryRock_Density()
    Eff_Density = rho_f*por + rho_dryrock    
    Calculated.Eff_Density = Eff_Density
    IsCalculated.Eff_Density=True
    return  Eff_Density
    
    
def Calculate_Effective_Bulkmodulus():
    Calculated.fluid_bulkmodulus=Calculate_Fluid_Kf()
    K_f = Calculated.fluid_bulkmodulus

    if K_f <=0.0: # this might happen if por=1. We set it to be non zero value
        K_f=1.0        
    por= Calculate_Effective_Porosity()
    K_s= Calculate_RockFrame_Bulkmodulus()  # Input.bulkmodulus    
    Calculated.DryRock_Bulkmodulus=Calculate_Dry_Rock_Bulkmodulus()    
    K_d=Calculated.DryRock_Bulkmodulus 
    if(RockPhysicModels.FSMName==RockPhysicModels.FSM_GassmannModel):
        Calculated.Eff_Bulkmodulus=Calculate_Effective_Bulkmodulus_Gassmann(por,K_s, K_f, K_d)
    elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_PatcyModel):
        Calculated.Eff_Bulkmodulus=Calculate_Effective_Bulkmodulus_Patchy(por,K_s, K_d)
    IsCalculated.Eff_Bulkmodulus=True
    return  Calculated.Eff_Bulkmodulus

def Calculate_Effective_Pmodulus():
    if(RockPhysicModels.FSMName==RockPhysicModels.FSM_GassmannModel or RockPhysicModels.FSMName==RockPhysicModels.FSM_PatcyModel ):
        gdry=Calculate_Dry_Rock_Shearmodulus()
        bulkModulusSat=Calculate_Effective_Bulkmodulus()
        value= 4.0*gdry/3.0+ bulkModulusSat
    else:
        PModulus=AnisotropicModels()
        if(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC11_SshC44):#.'Gassmann [HTI(0):P-C11,Ssh-C44]'):
            value= PModulus.Calculate_HTI_C11sat()       
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC11_SsvC66):#'Gassmann [HTI(0):P-C11,Ssv-C66]'):
            value=  PModulus.Calculate_HTI_C11sat()
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC33_SC44):#'Gassmann [HTI(90):P-C33,S-C44]'):
            value= PModulus.Calculate_HTI_C33sat()
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_ORTH_PC33_SC44):
            value= PModulus.Calculate_ORTH_C33()
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_ORTH_PC33_SC55):
            value= PModulus.Calculate_ORTH_C33()
        else:
            value=0
    Calculated.Eff_PModulus=value
    IsCalculated.Eff_PModulus=True
#    print('Here',value)
    return  Calculated.Eff_PModulus

# # Gassmann model    
def Calculate_Effective_Bulkmodulus_Gassmann(por,Ks, Kf, Kd):
    KsMPa=Ks*1.0E3  # convert Ks to MPa
    deno=por/Kf + (1.0 - por)/KsMPa - Kd/(KsMPa*KsMPa)
    Kb=  Kd + math.pow((1.0 - Kd/KsMPa), 2)/deno
    return Kb
#
 # Patchy saturation model
def Calculate_Effective_Bulkmodulus_Patchy(por,Ks, Kd):
    Ko=Calculated.oil_bulkmodulus
    Ka=Calculated.brine_bulkmodulus
    Kg=Calculated.gas_bulkmodulus   
    Gb=Calculated.Eff_Shearmodulus   
    So=Input.soil
    Sg=Input.sgas   
    
    KoGassmann=Calculate_Effective_Bulkmodulus_Gassmann(por,Ks, Ko, Kd)
    KgGassmann=Calculate_Effective_Bulkmodulus_Gassmann(por,Ks, Kg, Kd)
    KaGassmann=Calculate_Effective_Bulkmodulus_Gassmann(por,Ks, Ka, Kd)   
    Calculated.Eff_Bulkmodulus=CalculateP(So, Sg, KoGassmann, KaGassmann, KgGassmann, Gb * 4.0 / 3.0)   
    return Calculated.Eff_Bulkmodulus
#   
def CalculateP(So, Sg, KoGassmann, KaGassmann, KgGassmann, ShearTerm):
    Sum=So / (KoGassmann + ShearTerm) + Sg / (KgGassmann + ShearTerm) + (1.0-Sg-So) / (KaGassmann + ShearTerm);
    return 1.0 / Sum -ShearTerm;
      
def Calculate_Effective_Shearmodulus():
# Input: Gd [MPa]
# output: Gb[Mpa] 
    if(RockPhysicModels.FSMName==RockPhysicModels.FSM_GassmannModel or RockPhysicModels.FSMName==RockPhysicModels.FSM_PatcyModel ):
        value=Calculate_Dry_Rock_Shearmodulus()
    else:
        GShear=AnisotropicModels()
        if(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC11_SshC44):#.'Gassmann [HTI(0):P-C11,Ssh-C44]'):
            value= GShear.Calculate_HTI_C44sat()       
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC11_SsvC66):#'Gassmann [HTI(0):P-C11,Ssv-C66]'):
            value=  GShear.Calculate_HTI_C66sat() 
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_HTI_0_PC33_SC44):#'Gassmann [HTI(90):P-C33,S-C44]'):
            value= GShear.Calculate_HTI_C44sat()  
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_ORTH_PC33_SC44):
            value= GShear.Calculate_ORTH_C44()
        elif(RockPhysicModels.FSMName==RockPhysicModels.FSM_ORTH_PC33_SC55):
            value= GShear.Calculate_ORTH_C55()
        else:
            value=0
    Calculated.Eff_Shearmodulus=value      
    IsCalculated.Eff_Shearmodulus=True
    return Calculated.Eff_Shearmodulus   
        
        
def Calculate_Effective_Vp():
# Input: Kb, Gb [MPa], rho[kg/m3]
# output: Vp[m/s] 
    PMod_eff=Calculate_Effective_Pmodulus()
    rho_eff =Calculate_Effective_Density()
    Calculated.Eff_vp = 1.0E3*math.sqrt(PMod_eff/rho_eff)
    IsCalculated.Eff_vp = True
    return Calculated.Eff_vp

def Calculate_Effective_Vs():
# Input: Kb, Gb [MPa], rho[kg/m3]
# output: Vs[m/s]    
    G_eff=Calculate_Effective_Shearmodulus()
    rho_eff =Calculate_Effective_Density()
    vs_eff = 1.0E3*math.sqrt(G_eff/rho_eff)
    return vs_eff
            
def Calculate_Effective_Ip():
# Input: Kb, Gb [MPa], rho[kg/m3]
# output: Vp[m/s]    
    vp_eff = Calculate_Effective_Vp()
    rho_eff= Calculate_Effective_Density()
    Calculated.Eff_ip=vp_eff*rho_eff/1.0E+3
    IsCalculated.Eff_vs=True
    return Calculated.Eff_ip

def Calculate_Effective_Is():
    Calculated.Eff_vs=Calculate_Effective_Vs()
    Vs_eff = Calculated.Eff_vs 
    Calculated.Eff_Density=Calculate_Effective_Density()
    rho_eff = Calculated.Eff_Density
    IsCalculated.Eff_is=True
    Calculated.Eff_is=Vs_eff*rho_eff/1.0E+3
    return Calculated.Eff_is

# Full Zoeppritz','Aki&Richards', 'normal incidence  
def Calculate_Effective_Rpp():    
    if RockPhysicModels.RefCoefName=='Full Zoeppritz':
        val=Calculate_Rpp_FullZoeppritz()
    elif RockPhysicModels.RefCoefName=='Aki&Richards':
        val=Calculate_Rpp_AkiRichards()
    else: # Normal incidence
        val=Calculate_Rpp_NormalIncidence()
    
    IsCalculated.Eff_Rpp=True
    Calculated.Eff_Rpp=val
    return Calculated.Eff_Rpp
    
def Calculate_Effective_Rps():
    if RockPhysicModels.RefCoefName=='Full Zoeppritz':
        val=Calculate_Rps_FullZoeppritz()
    elif RockPhysicModels.RefCoefName=='Aki&Richards':
        val=Calculate_Rps_AkiRichards()
    else: # Normal incidence
        val=Calculate_Rps_NormalIncidence()
        
    IsCalculated.Eff_Rps=True
    Calculated.Eff_Rps=val
    return Calculated.Eff_Rps
#normal incidence Rpp
def Calculate_Rpp_NormalIncidence():    
    vp1=Input.VpTop
    rho1=Input.RhoTop # kg/m3
    vp2=Calculate_Effective_Vp()
    rho2=Calculate_Effective_Density()
    
    ip2=vp2*rho2
    ip1=vp1*rho1

    Rpp= (ip2-ip1)/(ip2+ip1)
    Calculated.Rpp = Rpp
    return Rpp
#normal incidence
def Calculate_Rps_NormalIncidence():    
    vs1=Input.VsTop
    rho1=Input.RhoTop # kg/m3

    vs2=Calculate_Effective_Vs()
    rho2=Calculate_Effective_Density()
    
    is2=vs2*rho2
    is1=vs1*rho1

    Rps= (is2-is1)/(is2+is1)
    Calculated.Rps = Rps
    return Rps
# Aki-Richards Rpp
def Calculate_Rpp_AkiRichards():
    theta1=Calculated.theta1
    vp1=Input.VpTop
    vs1=Input.VsTop   # m/s
    rho1=Input.RhoTop # kg/m3
    vp2=Calculate_Effective_Vp()   
    vs2=Calculate_Effective_Vs()
    rho2=Calculate_Effective_Density()
    vp= (vp2+vp1)/2.0
    vs= (vs2+vs1)/2.0
    rho=(rho2+rho1)/2.0
    delvp_vp = (vp2-vp1)/vp
    delrho_rho=(rho2-rho1)/rho
    delz_z=delrho_rho +delvp_vp
    delmu_mu=delrho_rho+2.0*delvp_vp
    sin2thetai=math.pow(math.sin(theta1),2)
    tan2thetai=math.pow(math.tan(theta1),2)
    term1= 0.5*delz_z + (0.5*delvp_vp - 2.0* (vs*vs/(vp*vp))*delmu_mu)*sin2thetai
    term2= 0.5*delvp_vp*sin2thetai*tan2thetai
    Rpp= term1 + term2
    Calculated.Rpp = Rpp
    return Rpp
# Aki-Richards Rpp
def Calculate_Rps_AkiRichards():
    theta1=Calculated.theta1    
    vp1=Input.VpTop
    vs1=Input.VsTop   # m/s
    rho1=Input.RhoTop # kg/m3
    vp2=Calculate_Effective_Vp()   
    vs2=Calculate_Effective_Vs()
    rho2=Calculate_Effective_Density()
    vp= (vp2+vp1)/2.0
    vs= (vs2+vs1)/2.0
    rho=(rho2+rho1)/2.0
    delvp_vp = (vp2-vp1)/vp
    delrho_rho=(rho2-rho1)/rho
    delmu_mu=delrho_rho+2.0*delvp_vp
    sin2thetai=math.pow(math.sin(theta1),2)
    term1= 0.5*(delrho_rho + 2.0*vs*delmu_mu/vp)
    term2= 0.5*((vs*vs/(vp*vp))*(0.5*delrho_rho-(1.0+vp/vs)*delmu_mu)*sin2thetai)
    Rps= -math.sin(theta1)*(term1 +term2)
    Calculated.Rps = Rps
    return Rps
# Full Zoeppritz models
def Calculate_Rpp_FullZoeppritz():
    theta1=Calculated.theta1
    theta2=Calculated.theta2
    phi1=Calculated.phi1
    phi2=Calculated.phi2
    vp1=Input.VpTop
    vs1=Input.VsTop   # m/s
    rho1=Input.RhoTop # kg/m3
    vp2=Calculate_Effective_Vp()   
    vs2=Calculate_Effective_Vs()
    rho2=Calculate_Effective_Density()
    sinphi2=math.sin(phi2)
    sinphi1=math.sin(phi1)
    sinphi2sqr=sinphi2*sinphi2
    sinphi1sqr=sinphi1*sinphi1
    a=  rho2*(1.0-2.0*sinphi2sqr)-rho1*(1.0-2.0*sinphi1sqr)
    b= rho2*(1.0-2.0*sinphi2sqr)+2.0*rho1*sinphi1sqr
    c=rho1*(1.0-2.0*sinphi1sqr)+2.0*rho2*sinphi2sqr
    d= 2.0*(rho2*vs2*vs2 - rho1*vs1*vs1) 
    E= b*math.cos(theta1)/vp1 +c*math.cos(theta2)/vp2
    F=b*math.cos(phi1)/vs1+c*math.cos(phi2)/vs2
    G=a - d* math.cos(theta1)*math.cos(phi2)/vp1/vs2
    H=a - d* math.cos(theta2)*math.cos(phi1)/vp2/vs1
    p= Calculated.pratio    
    D= E*F + G*H*p*p 
    term1 = (b*math.cos(theta1)/vp1 - c*math.cos(theta2)/vp2)*F
    term2 = (a + d* math.cos(theta1)*math.cos(phi2)/vp1/vs2)*H*p*p
    Rpp = (term1-term2)/D
    Calculated.Rpp = Rpp
    return Rpp
    
def Calculate_Rps_FullZoeppritz():
    theta1=Calculated.theta1
    theta2=Calculated.theta2
    phi1=Calculated.phi1
    phi2=Calculated.phi2
    vp1=Input.VpTop
    vs1=Input.VsTop   # m/s
    rho1=Input.RhoTop # kg/m3
    vp2=Calculate_Effective_Vp()   
    vs2=Calculate_Effective_Vs()
    rho2=Calculate_Effective_Density()
    sinphi2=math.sin(phi2)
    sinphi1=math.sin(phi1)
    sinphi2sqr=sinphi2*sinphi2
    sinphi1sqr=sinphi1*sinphi1   
    a=  rho2*(1.0-2.0*sinphi2sqr)-rho1*(1.0-2.0*sinphi1sqr)
    b= rho2*(1.0-2.0*sinphi2sqr)+2.0*rho1*sinphi1sqr
    c=rho1*(1.0-2.0*sinphi1sqr)+2.0*rho2*sinphi2sqr
    d= 2.0*(rho2*vs2*vs2 - rho1*vs1*vs1)        
    E= b*math.cos(theta1)/vp1 +c*math.cos(theta2)/vp2
    F=b*math.cos(phi1)/vs1+c*math.cos(phi2)/vs2
    G=a - d* math.cos(theta1)*math.cos(phi2)/vp1/vs2
    H=a - d* math.cos(theta2)*math.cos(phi1)/vp2/vs1
    p= Calculated.pratio       
    D= E*F + G*H*p*p 
    term =a*b + c*d*math.cos(theta2)*math.cos(phi2)/vp2/vs2
    term2=-2.0*math.cos(theta1)*term*p
    Rps=term2/vs1/D
    Calculated.Rps = Rps
    return Rps
    
def Calculate_RPP_RPS_SetParameters():
    theta1=math.radians(Input.IncidentAngle)
    VpTop=Input.VpTop
    VsTop=Input.VsTop   # m/s   
    Calculated.Eff_vp = Calculate_Effective_Vp()
    Calculated.Eff_vs = Calculate_Effective_Vs()
    Calculated.Eff_Density= Calculate_Effective_Density()
    VpBottom=Calculated.Eff_vp
    VsBottom=Calculated.Eff_vs    
    sintheta1=math.sin(theta1)
    pratio=sintheta1/VpTop
    arg_theta2=pratio*VpBottom
    arg_phi1=pratio*VsTop
    arg_phi2=pratio*VsBottom
    Calculated.pratio=pratio
    Calculated.theta1=theta1
    Calculated.theta2=math.asin(arg_theta2)
    Calculated.phi1=math.asin(arg_phi1)
    Calculated.phi2=math.asin(arg_phi2)
#
# # EM properties
def Calculate_Effective_Conductivity():  
    por=Calculate_Effective_Porosity()
    n=Input.nExp
    m=Input.mExp
    Sw = 1.0- Input.soil - Input.sgas
    TCelcius=Input.temperature
    salinity=Input.salinity
    tortuosity=Input.tortuosity    
    Calculated.brine_conductivity=ComputeBrineConductivity(TCelcius, salinity)    
    CondW=Calculated.brine_conductivity  # S/m 
    if (RockPhysicModels.EMModelName=='Archie'):
        Eff_conductivity= math.pow(por, m) * math.pow(Sw, n) * CondW / tortuosity;
    elif (RockPhysicModels.EMModelName=='Waxman-Smits'):
        if(Sw==0.0):
            Eff_conductivity = 0.0
        else:
            QvCEC= Input.QvCEC
            b = 4.6 * (1 - math.exp(-0.77 * CondW)) # see Eq. 30 from Waxman and Smits, SPE-1863, 1968
            Eff_conductivity= math.pow(por, m) * math.pow(Sw, n) * (CondW + b * QvCEC / Sw) / tortuosity;
    else:
        return 0       
    IsCalculated.Eff_conductivity=True
    Calculated.Eff_conductivity=Eff_conductivity
    return Calculated.Eff_conductivity  

def Calculate_Effective_Resistivity():
    CondEff=Calculate_Effective_Conductivity()
    Calculated.Eff_conductivity=CondEff
    #IsCalculated.Eff_conductivity=True
    if Calculated.Eff_conductivity >0.0:
        Calculated.Eff_resistivity= 1.0/ Calculated.Eff_conductivity     
    else:
        0.0
    IsCalculated.Eff_resistivity=True
    return Calculated.Eff_resistivity
      
def Calculate_Effective_neutron_sigma():
    a = 0.0002725
    b = 0.32187
    c = 21.33
    
    DenO_min = 530.0 #kg/m3
    DenO_max = 830.0 #kg/m3
    SigmaO_min = 17.8 # c.u.
    SigmaO_max = 24.9 #c.u.
        
    por=Calculate_Effective_Porosity()
    sgas=Input.sgas
    soil=Input.soil
    salinity=Input.salinity
    DenOil=Calculated.oil_density    

    rockNeutronSigma= Input.rock_sigma_capture

#    SigmaW= Input.brine_sigma_capture
#    SigmaOil= Input.oil_sigma_capture   
#    SigmaG= Input.gas_sigma_capture
    
    pressureMPa=Input.pressure
    tempC=Input.temperature
    API=Input.api
    GOR=Input.gasoil_ratio
    SpecGrav=Input.gas_specific_gravity
    
    Calculated.oil_density= Calculate_Oil_Density(pressureMPa, tempC, API, GOR, SpecGrav)
    #compute _SigmaW(psi)
    psi = 1000.0 * salinity # convert to ppk
    SigmaW = a * psi * psi + b * psi + c
    # compute SigmaOil
    SigmaOil = SigmaO_min + (DenOil - DenO_min) / (DenO_max - DenO_min) * (SigmaO_max - SigmaO_min)
    SigmaG = 0.0 # by deafult, HC gas is CO2
    
    if (not Input.CO2Flag=="co2"):
        SigmaG = 9.0
    IsCalculated.Eff_neutron_sigma=True
    Eff_neutron_sigma= por * ((1.0-soil-sgas) * SigmaW + soil * SigmaOil + sgas * SigmaG) + (1 - por) * rockNeutronSigma
    Calculated.Eff_neutron_sigma=Eff_neutron_sigma    
    return Calculated.Eff_neutron_sigma
################################
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 23:39:55 2016

@author: BAltundas
"""

def Calculate_Oil_Density(pressureMPa, tempC, oilGravityAPI, gasOilRatio, gasGravitySpecific):

# Input: 
#   pressureMPA[MPa]
#   tempC[C]     
#Output:
#   RhoOil[kg/m3]
####################
     densityOilRefGcc = 141.5 / (131.5 + oilGravityAPI)
     densityGasApparentGcc = 0.61703*math.pow(10,-0.00326*oilGravityAPI)  + \
      (1.51775 - 0.54351 * math.log10(oilGravityAPI)) * math.log10(gasGravitySpecific)
     Fac1=1.223E-3 *gasOilRatio * gasGravitySpecific
     
     densityLiveOilGcc = (densityOilRefGcc +  Fac1) / (1.0 +  Fac1 / densityGasApparentGcc)
     Fac=densityLiveOilGcc / densityOilRefGcc
     m = -1.2818 + 4.8303 * (Fac) - 2.5485 * Fac*Fac
     n = 0.6827 - 1.3039 * (Fac) + 0.6212 * Fac*Fac
     
     densityLiveOilGcc = densityLiveOilGcc * (m + n * math.log(pressureMPa/tempC))
     
     a = 3.8794E-4 + 3.75885E-2 * math.pow(10.0, -2.653 * densityLiveOilGcc)
     b = 1.00763E-6 + 8.8631E-4 * math.pow(10,-3.7645 * densityLiveOilGcc)
     deltaRhoP = a * pressureMPa * math.exp(- b * pressureMPa / a)
     c = 1.69756E-4 + 9.33538E-4 * (tempC - 15.56) - 1.53832E-6 * math.pow(tempC - 15.56,2)
     d = 12.9686 + 4.01368E-3 * (tempC - 15.56) - 1.1863E-4 * math.pow(tempC - 15.56,2)
     deltaRhoT = c * math.exp(-d * deltaRhoP)

     densityLiveOilGcc = densityLiveOilGcc + deltaRhoP - deltaRhoT
     RhoOil = densityLiveOilGcc*1000.0
     return RhoOil
# Velocity
########################################
def Calculate_Velocity_Oil(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific):
# Input: 
#   pressureMPA[MPa]
#   tempC[C]     
#Output:
#   VelocityOil [m/s]   
   densityOilRefGcc = 141.5/(131.5 + oilGravityApi)
   term1=0.61703*math.pow(10.0, -0.00326*oilGravityApi)
   densityGasApparentGcc = term1 + (1.51775 - 0.54351*math.log10(oilGravityApi))*math.log10(gasGravitySpecific)
#   densityPV is what is called rho_PV in -1-, defined at equation (11)
   epsilon = 0.113
   densityPV = (densityOilRefGcc + epsilon*1.223E-3*gasOilRatio*\
      gasGravitySpecific)/(1.0 + 1.223E-3*gasOilRatio*gasGravitySpecific/densityGasApparentGcc)
   velocityP0 = 1900.3*math.pow(densityPV, 0.6477) - 256.2
   b = 3.044 + 0.012*(141.5/densityPV - 131.5)
   c = 3.0 + 3.1E-2*(141.5/densityPV - 131.5)
   d = 0.3356*math.exp(-4.036*densityPV)
   velocityOil= velocityP0 - b*TCelcius + c*pressureMPa + d*TCelcius*pressureMPa
   return velocityOil
# Bulkmodulus of oil
#######################################################   
def Calculate_Oil_Bulkmodulus(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific):
# Output:
#   Bulkmodulus of oil[MPa]
   velocity = Calculate_Velocity_Oil(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific)
   density  = Calculate_Oil_Density(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific)
   Koil=density*math.pow(velocity, 2)/1.0E6
#   print('Koil=',Koil)
   return Koil
# Bulkmodulus of oil
#######################################################   
def Calculate_Oil_BulkmodulusWDen(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific, density):
   velocity = Calculate_Velocity_Oil(pressureMPa, TCelcius, oilGravityApi, gasOilRatio, gasGravitySpecific)
#   print("KoilwBr", density*math.pow(velocity, 2))
   return density*math.pow(velocity, 2)
#################################
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 16:09:55 2016

@author: BAltundas
"""

#
#from MyGlobalClasses import Input, Calculated, IsCalculated, IsActiveF
#from WaterProperties import Calculate_Water_Density, Calculate_Brine_Bulkmodulus, Calculate_Brine_BulkmodulusWDen 
#from CO2Properties import Calculate_CO2_Density, Calculate_CO2_Bulkmodulus, Calculate_CO2_BulkmodulusWDen
#from HCGasProperties import Calculate_HCGas_Density, Calculate_HCGas_Bulkmodulus
#from OilProperties import Calculate_Oil_Density, Calculate_Oil_Bulkmodulus, Calculate_Oil_BulkmodulusWDen
################################### 
def Calculate_Fluid_Bulkdensity0(PMPa, TCelcius, so, sg, Salinity, oilGravityApi, gasOilRatio,SpecGasGravity):
    Calculated.brine_density=Calculate_Water_Density(PMPa, TCelcius, Salinity)
    Calculated.oil_density=Calculate_Oil_Density(PMPa, TCelcius, oilGravityApi, gasOilRatio,SpecGasGravity)

    if (Input.CO2Flag=="co2"):
        Calculated.gas_density=Calculate_CO2_Density(PMPa, TCelcius)
        if(IsActiveF.CO2Dissolution):
             tkMessageBox.showerror("Error:", "CO2 Dissolution to be implelemented")          
    else:
        Calculated.gas_density=Calculate_HCGas_Density(PMPa, TCelcius, SpecGasGravity)
    IsCalculated.Fld_density=True
    return (1.0-so-sg)*Calculated.brine_density+so* Calculated.oil_density+sg*Calculated.gas_density
###################################    
def Calculate_Fluid_Kb0(PMPa, TCelcius, so, sg, Salinity, oilGravityApi, gasOilRatio,SpecGasGravity):       
    Calculated.brine_bulkmodulus=Calculate_Brine_Bulkmodulus(PMPa, TCelcius, Salinity)  
    Calculated.oil_bulkmodulus=Calculate_Oil_Bulkmodulus(PMPa, TCelcius, oilGravityApi, gasOilRatio, SpecGasGravity)
    if (Input.CO2Flag):
        Calculated.gas_bulkmodulus= Calculate_CO2_Bulkmodulus(PMPa, TCelcius)
        if(IsActiveF.CO2Dissolution):
                tkMessageBox.showerror("Error:", "CO2 Dissolution to be implelemented")   
    else:
        Calculated.gas_bulkmodulus=Calculate_HCGas_Bulkmodulus(PMPa, TCelcius, SpecGasGravity)
    IsCalculated.Fld_bulkmod=True
    return (1.0-so-sg)*Calculated.brine_bulkmodulus+so*Calculated.oil_bulkmodulus + sg*Calculated.gas_bulkmodulus
###################################    
def Calculate_Fluid_KbWithDen0(PMPa, TCelcius, so, sg, Salinity, oilGravityApi, gasOilRatio,SpecGasGravity):
    Calculated.oil_bulkmodulus=Calculate_Oil_BulkmodulusWDen(PMPa, TCelcius, oilGravityApi, gasOilRatio, SpecGasGravity, Calculated.oil_density)
    Calculated.brine_bulkmodulus=Calculate_Brine_Bulkmodulus(PMPa, TCelcius, Salinity,  Calculated.brine_density)
    if (Input.CO2Flag):
        Calculated.gas_bulkmodulus= Calculate_CO2_BulkmodulusWDen(PMPa, TCelcius, Calculated.gas_density)
        if(IsActiveF.CO2Dissolution):
                tkMessageBox.showerror("Error:", "CO2 Dissolution to be implelemented")   
    else:
        Calculated.gas_bulkmodulus=Calculate_HCGas_Bulkmodulus(PMPa, TCelcius, SpecGasGravity)
    IsCalculated.Fld_bulkmod=True
    kf=Calculate_Fluid_Kf_Wood0( so, sg)
    return kf
###################################    
def Calculate_Fluid_Kf_Wood0(so, sg):
    IsCalculated.Fld_bulkmod=True
    term = (1.0-so-sg)/Calculated.brine_bulkmodulus+so/Calculated.oil_bulkmodulus + sg/Calculated.gas_bulkmodulus
    return math.pow(term,-1)
###################################    
def Calculate_Fluid_Vp0(fluid_density, fluid_bulkmodulus):
     IsCalculated.Fld_vp=True
     return math.sqrt(fluid_bulkmodulus/fluid_density)
###################################    
def Calculate_Fluid_Ip0(density, vp):#kPa.s
    IsCalculated.Fld_ip=True
    return density*vp/1.0E+6
############################
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:37:57 2018

@author: BAltundas
"""

#from MyGlobalClasses import Input
#import DryRockProperties
#import BulkFluidProperties
#import EffectiveProperties

#// Anisotropic Gassmann -
#// Saturated C11 by L. Huang, 2014, Fluid Substitution Effects on Seismic Anisotropy,  J. Geophysicsl Research: solidEarth,120, pp850-863 
class AnisotropicModels():
#    def __init__(self):        
    def Calculate_HTI_C11sat(self):
        self.deltaN = Input.DeltaN1
        deltaN=self.deltaN
        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        M = Lambda + 2.0 * self.Gdry

        if (self.Kf == 0):
                return M * (1.0 - deltaN);
        else:
                return M * (1.0 - deltaN) + math.pow(self.Km - self.Kdry * (1.0 - deltaN), 2.0) / ((self.Km / self.Kf) * self.Por * (self.Km - self.Kf) + (self.Km - self.Kdry + deltaN * self.Kdry * self.Kdry / M))
        
    def Calculate_HTI_C33sat(self):
        self.deltaN = Input.DeltaN1
        deltaN=self.deltaN
        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        M = Lambda + 2.0 * self.Gdry
        r = Lambda / (Lambda + 2.0 * self.Gdry)

        if (self.Kf == 0):
            return M * (1.0 - r*r*deltaN);
        else:
            return M * (1.0 - r * r * deltaN) + math.pow(self.Km - self.Kdry * (1.0 - r * deltaN), 2.0) / ((self.Km / self.Kf) * self.Por * (self.Km - self.Kf) + (self.Km - self.Kdry + deltaN * self.Kdry * self.Kdry / M))
####
    def Calculate_HTI_C44sat(self):
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        return self.Gdry

    def Calculate_HTI_C66sat(self):
        self.deltaN = Input.DeltaN1
        deltaN=self.deltaN
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        gamma = Lambda / (2.0 * (Lambda + self.Gdry))
        deltaT = (-2.0+gamma) + math.sqrt(4.0-4.0*gamma + 8.0*deltaN*gamma + gamma*gamma)
        deltaT = deltaT / (2.0 * gamma)
        return self.Gdry*(1-deltaT)

    def Calculate_ORTH_C33(self):
        self.deltaN1 = Input.DeltaN1
        deltaN1=self.deltaN1
        self.deltaN2 = Input.DeltaN2
        deltaN2=self.deltaN2

        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        M = Lambda + 2.0 * self.Gdry
        r = Lambda / (Lambda + 2.0 * self.Gdry)
        term1= M * (1.0 - r * r * (deltaN1 + deltaN2))
        term2= math.pow(self.Km - self.Kdry * (1.0 - r * (deltaN1 + deltaN2)), 2.0)
        term3= ((self.Km / self.Kf) * self.Por * (self.Km - self.Kf) + (self.Km - self.Kdry + (deltaN1 + deltaN2) * self.Kdry * self.Kdry / M))
        if (self.Kf == 0):
            return term1
        else:
            return term1 +term2 / term3

    def Calculate_ORTH_C11(self):
        self.deltaN1 = Input.DeltaN1
        deltaN1=self.deltaN1
        self.deltaN2 = Input.DeltaN2
        deltaN2=self.deltaN2

        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        M = Lambda + 2.0 * self.Gdry
        r = Lambda / (Lambda + 2.0 * self.Gdry)
        term1=M * (1.0 - deltaN1 - r*r*deltaN2)
        term2=math.pow(self.Km - self.Kdry * (1.0 - deltaN1 -  r * deltaN2), 2.0)
        term3=((self.Km / self.Kf) * self.Por * (self.Km - self.Kf)  + (self.Km - self.Kdry + (deltaN1+deltaN2) * self.Kdry * self.Kdry / M))
        if (self.Kf == 0):
            return term1
        else:
            return term1 + term2/term3
            
    def Calculate_ORTH_C22(self):
        self.deltaN1 = Input.DeltaN1
        deltaN1=self.deltaN1
        self.deltaN2 = Input.DeltaN2
        deltaN2=self.deltaN2

        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        M = Lambda + 2.0 * self.Gdry
        r = Lambda / (Lambda + 2.0 * self.Gdry)
        term1=M * (1.0 - r*r*deltaN1 - deltaN2)
        term2=math.pow(self.Km - self.Kdry * (1.0 - r * deltaN1 - deltaN2), 2.0)
        term3=((self.Km / self.Kf) * self.Por * (self.Km - self.Kf)  + (self.Km - self.Kdry + (deltaN1 + deltaN2) * self.Kdry * self.Kdry / M))
        if (self.Kf == 0):
            return term1
        else:
            return term1 + term2 / term3
            
    def Calculate_ORTH_C44(self):
        self.deltaN2 = Input.DeltaN2
        deltaN2=self.deltaN2

        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        gamma = Lambda / (2 * (Lambda + self.Gdry))
        deltaT2 = (-2.0 + gamma) + math.sqrt(4.0 - 4.0 * gamma + 8.0 * deltaN2 * gamma + gamma * gamma)
        deltaT2 = deltaT2 / (2.0 * gamma)
        return self.Gdry*(1.0-deltaT2)
        
    def Calculate_ORTH_C55(self):
        self.deltaN1 = Input.DeltaN1
        deltaN1=self.deltaN1
        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        gamma = Lambda / (2 * (Lambda + self.Gdry))

        deltaT1 = (-2.0 + gamma) + math.sqrt(4.0 - 4.0 * gamma + 8.0 * deltaN1 * gamma + gamma * gamma)
        deltaT1 = deltaT1 / (2.0 * gamma)
        return self.Gdry*(1.0-deltaT1)
        
    def Calculate_ORTH_C66(self):
        self.deltaN1 = Input.DeltaN1
        deltaN1=self.deltaN1
        self.deltaN2 = Input.DeltaN2
        deltaN2=self.deltaN2
        self.Por =  Calculate_Effective_Porosity()  
        self.Km = Calculate_RockFrame_Bulkmodulus()
        self.Kf=Calculate_Fluid_Kf()
        self.Gdry=Calculate_Dry_Rock_Shearmodulus()
        self.Kdry=Calculate_Dry_Rock_Bulkmodulus()
        Lambda = self.Kdry - 2.0 * self.Gdry / 3.0
        gamma = Lambda / (2 * (Lambda + self.Gdry))
        deltaT1 = (-2.0 + gamma) + math.sqrt(4.0 - 4.0 * gamma + 8.0 * deltaN1 * gamma + gamma * gamma)
        deltaT1 = deltaT1 / (2.0 * gamma)
        deltaT2 = (-2.0 + gamma) + math.sqrt(4.0 - 4.0 * gamma + 8.0 * deltaN2 * gamma + gamma * gamma)
        deltaT2 = deltaT2 / (2.0 * gamma);
        return self.Gdry*(1.0-deltaT1)*(1.0-deltaT2)/ (1.0 - deltaT1*deltaT2)
    
    def Calculate_Hudson_C33(self): # Not implemented
        """function [Vp0,Vs0,e,g,d,Ctih]=hudson1(ec,ar,Kfl,K,G,den,ax)
 hudson1 - calculate the anisotropic elastic parameters for cracked rock 
           using Hudson's first order weak inclusion theory valid for small
           crack density and aspect ratios. Assumes a 
           single crack set with all normals aligned along 1-axis.
           For dry cracks use fluid bulk modulus 0
 input and output parameters:
 Output: Vp0, Vs0 - P and S velocities of the cracked rock along the 1-axis
         e, g, d - epsilon,  gamma, delta, Thomsen's weakly anisotropic parameter
         Ctih - C6x6 matrix with symmetry axis along 1-axis 
         tih stands for transversely isotropic with a horizontal symmetry axis
 Input:
   ec - crack density
   ar - aspect ratio of cracks
   Kfl, K: bulk modulus of fluid in cracks, and bulk modulus of isotropic matrix
   G: shear modulus of isotropic matrix
   den: density of cracked rock

 optional input parameter: 
    ax - defines axis of symmetry; 
    ax =1, for crack normals aligned along 1-axis (default); 
    ax= 3, for crack normals along 3-axis.
"""
#% See also ECHENG
#
#% References:
#% Hudson (1980, 1981, 1990)
#% L. Thomsen, 1986, Weak elastic anisotropy, Geophysics Vol51 Oct 1986

#
        K = Calculate_RockFrame_Bulkmodulus()
        G = Calculate_RockFrame_Shearmodulus()
        Kfl=Calculate_Fluid_Kf()
        ar=Input.aratio1
        ax=1
        self.ax=ax
        ec=1.
        self.ec=ec

        lam=K-2.0/3.0*G
        
        mu=G
        kapa=Kfl*(lam+2.0*mu)/(math.pi*ar*mu*(lam+mu))
        
        u3=(4.0/3.0)*(lam+2.0*mu)/((lam+mu)*(1.0+kapa))
#        u1=16/3.0*(lam+2.0*mu)/(3.0*lam+4.0*mu)
#        c11=lam+2.0*mu-math.pow(lam, 2)*ec*u3/mu
#        c13=lam-lam*(lam+2.0*mu)*ec*u3/mu
        c33=lam+2.0*mu-math.pow(lam+2.0*mu, 2)*ec*u3/mu
#        c44=mu-mu*ec*u1
#        c66=mu
#        Vp0=math.sqrt(c33/den)
#        Vs0=math.sqrt(c44/den)
        return c33  # M-Modulus

    def Calculate_Hudson_C44(self):
        """function [Vp0,Vs0,e,g,d,Ctih]=hudson1(ec,ar,Kfl,K,G,den,ax)
 hudson1 - calculate the anisotropic elastic parameters for cracked rock 
           using Hudson's first order weak inclusion theory valid for small
           crack density and aspect ratios. Assumes a 
           single crack set with all normals aligned along 1-axis.
           For dry cracks use fluid bulk modulus 0
 input and output parameters:
 Output: Vp0, Vs0 - P and S velocities of the cracked rock along the 1-axis
         e, g, d - epsilon,  gamma, delta, Thomsen's weakly anisotropic parameter
         Ctih - C6x6 matrix with symmetry axis along 1-axis 
         tih stands for transversely isotropic with a horizontal symmetry axis
 Input:
   ec - crack density
   ar - aspect ratio of cracks
   Kfl, K: bulk modulus of fluid in cracks, and bulk modulus of isotropic matrix
   G: shear modulus of isotropic matrix
   den: density of cracked rock

 optional input parameter: 
    ax - defines axis of symmetry; 
    ax =1, for crack normals aligned along 1-axis (default); 
    ax= 3, for crack normals along 3-axis.
"""
#% See also ECHENG
#
#% References:
#% Hudson (1980, 1981, 1990)
#% L. Thomsen, 1986, Weak elastic anisotropy, Geophysics Vol51 Oct 1986

#
        K = Calculate_RockFrame_Bulkmodulus()
        G = Calculate_RockFrame_Shearmodulus()
#        Kfl=Calculate_Fluid_Kf()
#        ar=Input.aratio1

        ec=1.
        
        lam=K-2.0/3.0*G
        
        mu=G
#        kapa=Kfl*(lam+2.0*mu)/(math.pi*ar*mu*(lam+mu))
        
#        u3=(4.0/3.0)*(lam+2.0*mu)/((lam+mu)*(1.0+kapa))
        u1=16/3.0*(lam+2.0*mu)/(3.0*lam+4.0*mu)
#        c11=lam+2.0*mu-math.pow(lam, 2)*ec*u3/mu
#        c13=lam-lam*(lam+2.0*mu)*ec*u3/mu
#        c33=lam+2.0*mu-math.pow(lam+2.0*mu, 2)*ec*u3/mu
        c44=mu-mu*ec*u1
#        c66=mu
#        Vp0=math.sqrt(c33/den)
#        Vs0=math.sqrt(c44/den)
        return c44 
################################
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 23:57:26 2016

@author: BAltundas
"""

def Calculate_HCGas_Density(pressureMPa, TCelcius, gasGravitySpecific):
# The Gas specific gravity is the ratio of gas density to air density at T = 15.6 C (60 F) and P = 1 Atm
# These equations could be check with the numerical values from : http://www.crewes.org/ResearchLinks/ExplorerPrograms/FlProp/FluidProp.htm
  tempKelvin = TCelcius+273.15
# These values of the critical point are from Thomas and al. (1970)
#  gasCriticalPressure = (1.0e+6.0*(4.892 - 0.4048*gasGravitySpecific))/1.0e+6
  gasCriticalPressure = (4.892 - 0.4048*gasGravitySpecific)
  gasCriticalTemp = 94.72 + 170.75*gasGravitySpecific
  pressureR = pressureMPa/gasCriticalPressure
  tempR = tempKelvin/gasCriticalTemp
 # Equations 10a, 10b and 10c from the Batzle Wang paper
 # These guys seem to mix up 1 Atm and 10^5 Pa.
 # They also move from 15.5 C to 15.6 C
  r = 8.31441
  e = 0.109*math.pow(3.85 - tempR, 2)*math.exp(-(0.45 + (8.0*math.pow(0.56 - 1.0/tempR, 2)))*\
      (math.pow(pressureR, 1.2)/tempR))
  z = (0.03 + 0.00527*math.pow(3.5 - tempR, 3))*pressureR + (0.642*tempR - 0.007*math.pow(tempR, 4) - 0.52) + e
  rhoHCGas= 1.0E+3*28.8*gasGravitySpecific*pressureMPa/(z*r*tempKelvin)
  return rhoHCGas

#
# HCGas Bulk Modulus
def Calculate_HCGas_Bulkmodulus(pressureMPa, TCelcius, gasGravitySpecific):
 # The Gas specific gravity is the ratio of gas density to air density at T = 15.6 C (60 F) and P = 1 Atm
 # These equations could be check with the numerical values from : http://www.crewes.org/ResearchLinks/ExplorerPrograms/FlProp/FluidProp.htm
 tempKelvin = 273.15+TCelcius
 gasCriticalPressure =(4.892 - 0.4048*gasGravitySpecific);
 gasCriticalTemp = 94.72 + 170.75*gasGravitySpecific;
 pressureR = pressureMPa/gasCriticalPressure;
 tempR = tempKelvin/gasCriticalTemp;

 heatCapacityRatio = 0.85 + 5.6/(pressureR + 2.0) + \
    27.1/math.pow(pressureR + 3.5, 2) - 8.7*math.exp(-0.65*(pressureR + 1.0))
    
 z = (0.03 + 0.00527*math.pow(3.5 - tempR, 3))*pressureR +\
   (0.642*tempR - 0.007*math.pow(tempR, 4) - 0.52) + 0.109*math.pow(3.85 - tempR, 2)*math.exp(-((0.45 +\
   8*math.pow(0.56 - 1.0/tempR, 2))/tempR)*math.pow(pressureR, 1.2))
   
 zb2 = 0.109*math.pow(3.85 - tempR, 2)*math.exp(-((0.45 +\
     8*math.pow(0.56 - 1.0/tempR, 2))/tempR)*math.pow(pressureR, 1.2))
 
 dzDPr = (0.03 + 0.00527*math.pow(3.5 - tempR, 3)) - 1.2*math.pow(pressureR, 0.2)*\
                        ((0.45 + 8*math.pow(0.56 - 1.0/tempR, 2))/tempR)*zb2
 Kgas= pressureMPa*heatCapacityRatio/(1.0 - pressureR*dzDPr/z)
# print('kgas=',Kgas)
 return Kgas
#############################
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 15:00:15 2016

@author: BAltundas
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 17:13:21 2016

@author: BAltundas
"""
"""
##  
## 
##  Designed by Bilgin Altundas
"""
############################################################################
############################################################################
#IMPORTS>
############################################################################


#from Add_row_with_HS import CreateTable
#from Calculations import CalculateOutput
#from MyGlobalClasses import IsActiveF, Input, Calculated, RockPhysicModels,\
#     InputPropNames, PlotList,  PlotAux, InputVar, IsCalculated
#     
#from ValidateRefresh import Validate, ReinitializeIsCalculated
#from EffectiveProperties import Calculate_Effective_Vp, Calculate_Effective_Pmodulus,\
#     Calculate_Effective_Ip, Calculate_Effective_Bulkmodulus,  Calculate_Effective_Vs,\
#     Calculate_Effective_Density, Calculate_Effective_neutron_sigma,Calculate_Effective_Conductivity,\
#     Calculate_Effective_Resistivity, Calculate_Effective_Rpp, Calculate_Effective_Rps
#
#from PlotProps import Plot_Properties_Sw,Plot_Properties_SwTL, Plot_Properties_Pressure, Plot_Properties_PressureTL,\
#    Plot_Properties_Temperature,Plot_Properties_TemperatureTL, Scalar2ArrayWithRes,\
#    Plot_Properties_SwSg, Plot_Properties_SwSgTL, Plot_Properties_PT, Plot_Properties_PT_TL

def isActive():
    global entrySoil, slider, var
    slider.config(label=var.get())   # writes the label
    entrySoil.config(state='normal')
    slider.config(state='normal')
    
    if(IsActiveF.flgTLbaseline and (var.get()==InputPropNames.soil)):
        entrySoil.config(state='disable')
        slider.config(state='disable')
        print('You can not change Soil in 2D Sw-Sg plot. Uncheck baseline'  )
    else:
        value=GetVarValue(value=None)    # gets the value from the slider/scale
        slider.set(value=value)          # sets the sliderisActive

def isTobePlotted():
    global varPlot, chk_TLbaseline, chk_plot_hold
    PlotAux.varp=varPlot.get()
    ChangeHandler()
    if(PlotAux.varp=='Saturation'):
        chk_TLbaseline.deselect() 
        chk_plot_hold.deselect()
        Calculated.sw_array=Scalar2ArrayWithRes(0.0, Input.swat)
        IsActiveF.flgPlotHold=False
    elif(PlotAux.varp=='Pressure'):
        chk_TLbaseline.deselect() 
        chk_plot_hold.deselect()
        Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
        IsActiveF.flgPlotHold=False

    elif(PlotAux.varp=='Temperature'):
        chk_TLbaseline.deselect() 
        chk_plot_hold.deselect()
        Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
        IsActiveF.flgPlotHold=False

    else:
        print('Do nothing')
    return 1         

def isTobePlotted2D():
    global varPlot2D, chk_TLbaseline
    PlotAux.varp2D=varPlot2D.get()
    ChangeHandler()
    if(PlotAux.varp2D=='Sw-Sg'):
        Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
        Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
        IsActiveF.flgPlotHold=False
    elif(PlotAux.varp2D=='P-T'):
        Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
        Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
        IsActiveF.flgPlotHold=False
    else:
        print('Do nothing')
    return 1 

def isTLForward():
    global varTL_Fwd,chk_TLbaseline, chk_plot_hold
    PlotAux.varTL_Fwd=varTL_Fwd.get()
    chk_TLbaseline.config(state='normal')   
    chk_plot_hold.config(state='normal')   
    
    if(varTL_Fwd.get()=='Forward'):
        chk_TLbaseline.config(state='disabled')
    else:
        chk_TLbaseline.config(state='normal')
        if(PlotAux.var1D_2DPlot=='1D plot'):
            chk_plot_hold.config(state='disable')
        else:
            chk_plot_hold.config(state='normal')            
    return 1      
  
def onClickHold():
    global varTL_Fwd,chk_TLbaseline, chk_plot_hold
    PlotAux.varTL_Fwd=varTL_Fwd.get()
    chk_TLbaseline.config(state='normal')   
    chk_plot_hold.config(state='normal')   
    
    if(varTL_Fwd.get()=='Forward'):
        chk_TLbaseline.config(state='disabled')
    else:
        chk_TLbaseline.config(state='normal')
        if(PlotAux.var1D_2DPlot=='1D plot'):
            chk_plot_hold.config(state='disable')
        else:
            chk_plot_hold.config(state='normal')            
    return 1     
#**************************
##### Not used currently
def save_project27(fout):
# Fluid parameters
    print >> fout, Input.pressure
    print('Pressure',Input.pressure)
    print >> fout, Input.temperature
    print >> fout, Input.soil
    print >> fout, Input.sgas
    print >> fout, Input.swat
    print >> fout, Input.salinity
    print >> fout, Input.api
    print >> fout, Input.gas_specific_gravity
    print >> fout, Input.gasoil_ratio
    print >> fout, Input.net_to_gross
# Rock properties    
    print >> fout, Input.rockdensity
    print >> fout, Input.porosity
    print >> fout, Input.critical_porosity
    print >> fout, Input.bulkmodulus
    print >> fout, Input.shearmodulus   
    print >> fout, Input.CO2Flag
# EM
    print >> fout, Input.nExp
    print >> fout, Input.mExp
    print >> fout, Input.tortuosity
    print >> fout, Input.QvCEC   
# Nuclear
    print >> fout, Input.rock_sigma_capture
#    print >> fout,Input.oil_sigma_capture
#    print >> fout,Input.brine_sigma_capture
#    print >> fout,Input.gas_sigma_capture
    print >> fout,Input.vugfraction
    print >> fout,Input.KriefExponent
    print >> fout,Input.Kdry
    print >> fout,Input.Gdry

# rock matrix
    print >> fout,Input.aratio1
    print >> fout,Input.aratio2
# volume fractions used by DEm and KT
    print >> fout,Input.volfrac1
    print >> fout,Input.volfrac2 
    print >> fout,Input.K_inclusion1
    print >> fout,Input.K_inclusion2
# weights for the ave HS and voigt-Reuss
#    print >> fout,Input.HSRockFrameTable=[]
#    print >> fout,Input.Ave_weight_frac =0.5
# Pressure correction
    print >> fout,Input.confining_pressure
    print >> fout,Input.poisson_ratio 
    print >> fout,Input.coord_number
    print >> fout,Input.effPresCoef
    print >> fout,Input.Linear_CoefAK
    print >> fout,Input.Linear_CoefAG
# MacBeth
    print >> fout,Input.MacBeth_Pk
    print >> fout,Input.MacBeth_Ek  
    print >> fout,Input.MacBeth_Pg
    print >> fout,Input.MacBeth_Eg
# Rpp
    print >> fout,Input.RhoTop
    print >> fout,Input.VpTop    
    print >> fout,Input.VsTop    
    print >> fout,Input.IncidentAngle  
    fout.close() 
    
def save_project(fout):
    global propS
# Fluid parameters
    fout.writelines("%s\n" % propS.pressure.get())
    fout.writelines("%s\n" % propS.temperature.get()),
    fout.writelines("%s\n" % propS.soil.get()), 
    fout.writelines("%s\n" % propS.sgas.get()) 
    fout.writelines("%s\n" % propS.swat.get()) 
    fout.writelines("%s\n" % propS.salinity.get()) 
    fout.writelines("%s\n" % propS.api.get()) 
    fout.writelines("%s\n" % propS.gas_specific_gravity.get()) 
    fout.writelines("%s\n" % propS.gasoil_ratio.get()) 
    fout.writelines("%s\n" % propS.net_to_gross.get()) 
    fout.writelines("%s\n" % propS.rockdensity.get())
    fout.writelines("%s\n" % propS.porosity.get())
    fout.writelines("%s\n" % propS.critical_porosity.get())
    fout.writelines("%s\n" % propS.bulkmodulus.get())
    fout.writelines("%s\n" % propS.shearmodulus.get())
    fout.writelines("%s\n" % propS.CO2Flag.get())
    fout.writelines("%s\n" % propS.nExp.get())
    fout.writelines("%s\n" % propS.mExp.get())
    fout.writelines("%s\n" % propS.tortuosity.get())
    fout.writelines("%s\n" % propS.QvCEC.get())
    fout.writelines("%s\n" % propS.rock_sigma_capture.get())
#    fout.writelines("%s\n" % propS.oil_sigma_capture.get())
#    fout.writelines("%s\n" % propS.brine_sigma_capture.get())
#    fout.writelines("%s\n" % propS.gas_sigma_capture.get())
    fout.writelines("%s\n" % propS.vugfraction.get())
    fout.writelines("%s\n" % propS.KriefExponent.get())
    fout.writelines("%s\n" % propS.Kdry.get())
    fout.writelines("%s\n" % propS.Gdry.get())

    fout.writelines("%s\n" % propS.aratio1.get())
    fout.writelines("%s\n" % propS.aratio2.get())
    fout.writelines("%s\n" % propS.volfrac1.get())
    fout.writelines("%s\n" % propS.volfrac2.get()) 
    fout.writelines("%s\n" % propS.K_inclusion1.get())
    fout.writelines("%s\n" % propS.K_inclusion2.get())
    fout.writelines("%s\n" % propS.confining_pressure.get())
    fout.writelines("%s\n" % propS.poisson_ratio.get())
    fout.writelines("%s\n" % propS.coord_number.get())
    fout.writelines("%s\n" % propS.effPresCoef.get())
    fout.writelines("%s\n" % propS.Linear_CoefAK.get())
    fout.writelines("%s\n" % propS.Linear_CoefAG.get())
    fout.writelines("%s\n" % propS.MacBeth_Pk.get())
    fout.writelines("%s\n" % propS.MacBeth_Ek.get())
    fout.writelines("%s\n" % propS.MacBeth_Pg.get())
    fout.writelines("%s\n" % propS.MacBeth_Eg.get())
    fout.writelines("%s\n" % propS.RhoTop.get())
    fout.writelines("%s\n" % propS.VpTop.get())
    fout.writelines("%s\n" % propS.VsTop.get())
    fout.writelines("%s\n" % propS.IncidentAngle.get())
    fout.close() 
    
def Restart_project(fin): 
    global propS
    propS.pressure.set(value=fin.readline().rstrip())
# print('**',propS.pressure.get())
    propS.temperature.set(value=fin.readline().rstrip())
    propS.soil.set(value=fin.readline().rstrip()) 
    propS.sgas.set(value=fin.readline().rstrip()) 
    propS.swat.set(value=fin.readline().rstrip()) 
    propS.salinity.set(value=fin.readline().rstrip()) 
    propS.api.set(value=fin.readline().rstrip()) 
    propS.gas_specific_gravity.set(value=fin.readline().rstrip()) 
    propS.gasoil_ratio.set(value=fin.readline().rstrip()) 
    propS.net_to_gross.set(value=fin.readline().rstrip()) 
# Rock properties    
    propS.rockdensity.set(value=fin.readline().rstrip()) 
    propS.porosity.set(value=fin.readline().rstrip()) 
    propS.critical_porosity.set(value=fin.readline().rstrip()) 
    propS.bulkmodulus.set(value=fin.readline().rstrip()) 
    propS.shearmodulus.set(value=fin.readline().rstrip()) 
    propS.CO2Flag.set(value=fin.readline().rstrip()) 
# EM
    propS.nExp.set(value=fin.readline().rstrip()) 
    propS.mExp.set(value=fin.readline().rstrip()) 
    propS.tortuosity.set(value=fin.readline().rstrip()) 
    propS.QvCEC.set(value=fin.readline().rstrip()) 
# Nuclear
    propS.rock_sigma_capture.set(value=fin.readline().rstrip()) 
#    propS.oil_sigma_capture.set(value=fin.readline().rstrip()) 
#    propS.brine_sigma_capture.set(value=fin.readline().rstrip()) 
#    propS.gas_sigma_capture.set(value=fin.readline().rstrip()) 

    propS.vugfraction.set(value=fin.readline().rstrip()) 
    propS.KriefExponent.set(value=fin.readline().rstrip()) 
    propS.Kdry.set(value=fin.readline().rstrip()) 
    propS.Gdry.set(value=fin.readline().rstrip()) 
# rock matrix
    propS.aratio1.set(value=fin.readline().rstrip()) 
    propS.aratio2.set(value=fin.readline().rstrip()) 
# volume fractions used by DEm and KT
    propS.volfrac1.set(value=fin.readline().rstrip())     
    propS.volfrac2.set(value=fin.readline().rstrip())     
    propS.K_inclusion1.set(value=fin.readline().rstrip())     
    propS.K_inclusion2.set(value=fin.readline().rstrip()) 
# Pressure correction 
    propS.confining_pressure.set(value=fin.readline().rstrip())     
    propS.poisson_ratio.set(value=fin.readline().rstrip())     
    propS.coord_number.set(value=fin.readline().rstrip()) 
    propS.effPresCoef.set(value=fin.readline().rstrip())     
    propS.Linear_CoefAK.set(value=fin.readline().rstrip())     
    propS.Linear_CoefAG.set(value=fin.readline().rstrip()) 
# MacBeth
    propS.MacBeth_Pk.set(value=fin.readline().rstrip())     
    propS.MacBeth_Ek.set(value=fin.readline().rstrip())     
    propS.MacBeth_Pg.set(value=fin.readline().rstrip()) 
    propS.MacBeth_Eg.set(value=fin.readline().rstrip())     
    propS.RhoTop.set(value=fin.readline().rstrip())    
    propS.VpTop.set(value=fin.readline().rstrip())    
    propS.VsTop.set(value=fin.readline().rstrip())
    propS.IncidentAngle.set(value=fin.readline().rstrip())
    UpdateInput()
    fin.close()
    
def updateSliderValue(value=None):
    global propS, propval
    if(var.get()==InputPropNames.pressure): 
        val=slider.get()
        propS.pressure.set(value=val)
    elif(var.get()==InputPropNames.temperature): 
        val=slider.get()    
        propS.temperature.set(value=val)
    elif(var.get()==InputPropNames.soil): 
        val=slider.get()        
        swat=1.0 - float(val) - float(propS.sgas.get())
        propS.soil.set(value=val)
        if (swat<0):
            slider.set(value=val)
            er = "Water saturation is negative"
            tkMessageBox.showwarning("Error:",er)  
            return False    
        propS.swat.set(value=swat)
    elif(var.get()==InputPropNames.sgas): 
        val=slider.get()   
        swat=1.0 - float(val)-float(propS.soil.get())
        propS.sgas.set(value=val)
        if (swat<0):
            slider.set(value=val)
            er = "Water saturation is negative"
            tkMessageBox.showwarning("Error:",er) 
            return    
        propS.swat.set(value=swat)
    elif(var.get()==InputPropNames.swat): 
        val=slider.get()        
        sgas=1.0 - float(val)-float(propS.soil.get())
        propS.sgas.set(value=sgas)
        if (sgas<0):
            slider.set(value=val)
            er = "Gas saturation is negative"
            tkMessageBox.showwarning("Error:",er) 
            return   
        propS.swat.set(value=val)
    elif(var.get()==InputPropNames.salinity): 
        val=slider.get()        
        propS.salinity.set(value=val)
    elif(var.get()==InputPropNames.api): 
        val=slider.get()        
        propS.api.set(value=val)
    elif(var.get()==InputPropNames.gas_specific_gravity): 
        val=slider.get()     
        propS.gas_specific_gravity.set(value=val)
    elif(var.get()==InputPropNames.gasoil_ratio): 
        val=slider.get()        
        propS.gasoil_ratio.set(value=val)
    elif(var.get()==InputPropNames.net_to_gross):
        val=slider.get()   
        propS.net_to_gross.set(value=val)
    elif(var.get()==InputPropNames.rockdensity): 
        val=slider.get()
        propS.rockdensity.set(value=val)      
    elif(var.get()==InputPropNames.porosity): 
        val=slider.get()
        propS.porosity.set(value=val) 
    elif(var.get()==InputPropNames.critical_porosity): 
        val=slider.get()
        propS.critical_porosity.set(value=val) 
    elif(var.get()==InputPropNames.bulkmodulus): 
        val=slider.get()
        propS.bulkmodulus.set(value=val)  
    elif(var.get()==InputPropNames.shearmodulus): 
        val=slider.get()
        propS.shearmodulus.set(value=val) 
    else:
        print(var.get())
    propval.set(value=val)
    slider.set(value=val)
    return 0    

#   
def GetVarValue(value=None):
    global var
#    slider.config(state='normal')
    if(var.get()==InputPropNames.pressure):
        slider.config(from_=Input.pressureMin, to=Input.pressureMax, resolution=Input.pressureResolution, tickinterval=5)
        val=float(propS.pressure.get())
        Input.pressure=val
    if(var.get()==InputPropNames.temperature):
        slider.config(from_=Input.temperatureMin, to=Input.temperatureMax, resolution=Input.temperatureResolution, tickinterval=75)
        val=float(propS.temperature.get())
        Input.temperature=val
    if(var.get()==InputPropNames.soil):
        slider.config(from_=Input.soilMin, to=Input.soilMax, resolution=Input.soilResolution, tickinterval=1)
        val=float(propS.soil.get())
        Input.soil=val
    if(var.get()==InputPropNames.swat):
        slider.config(from_=Input.swatMin, to=Input.swatMax, resolution=Input.swatResolution, tickinterval=1)
        val=float(propS.swat.get())
        Input.swat=val
    if(var.get()==InputPropNames.sgas):
        slider.config(from_=Input.sgasMin, to=Input.sgasMax, resolution=Input.sgasResolution, tickinterval=1)
        val=float(propS.sgas.get())
        Input.sgas=val
    if(var.get()==InputPropNames.salinity):
        slider.config(from_=Input.salMin, to=Input.salMax, resolution=Input.salResolution, tickinterval=1)
        val=float(propS.salinity.get())
        Input.salinity=val
    if(var.get()==InputPropNames.api):
        slider.config(from_=Input.apiMin, to=Input.apiMax, resolution=Input.apiResolution, tickinterval=75)
        val=float(propS.api.get())
        Input.api=val
    if(var.get()==InputPropNames.gas_specific_gravity):
        slider.config(from_=Input.gas_specific_gravityMin, to=Input.gas_specific_gravityMax, \
                      resolution=Input.gas_specific_gravityResolution, tickinterval=1)
        val=float(propS.gas_specific_gravity.get())
        Input.gas_specific_gravity=val
    if(var.get()==InputPropNames.gasoil_ratio):  # 0 - 2000 scf/bl
        slider.config(from_=Input.gasoil_ratioMin, to=Input.gasoil_ratioMax, resolution=Input.gasoil_ratioResolution, tickinterval=75)
        val==float(propS.gasoil_ratio.get())
        Input.gasoil_ratio=val
    if(var.get()==InputPropNames.net_to_gross):
        slider.config(from_=Input.net_to_grossMin, to=Input.net_to_grossMax, resolution=Input.net_to_grossResolution, tickinterval=1)
        val=float(propS.net_to_gross.get())
        Input.net_to_gross=val
    if(var.get()==InputPropNames.rockdensity):
        slider.config(from_=Input.rockdensityMin, to=Input.rockdensityMax, resolution=Input.rockdensityResolution, tickinterval=1000)
        val=float(propS.rockdensity.get())
        Input.rockdensity=val
    if(var.get()==InputPropNames.porosity):
        slider.config(from_=Input.porosityMin, to=Input.porosityMax, resolution=Input.porosityResolution, tickinterval=1)
        val=float(propS.porosity.get())
        Input.porosity=val
    if(var.get()==InputPropNames.critical_porosity):
        slider.config(from_=Input.porosityMin, to=Input.porosityMax, resolution=Input.porosityResolution, tickinterval=1)
        val=float(propS.critical_porosity.get())
        Input.critical_porosity=val      
    if(var.get()==InputPropNames.bulkmodulus):
        slider.config(from_=Input.bulkmodulusMin, to=Input.bulkmodulusMax, resolution=Input.bulkmodulusResolution,tickinterval=25)
        val=float(propS.bulkmodulus.get())
        Input.bulkmodulus=val
    if(var.get()==InputPropNames.shearmodulus):
        slider.config(from_=Input.shearmodulusMin, to=Input.shearmodulusMax, resolution=Input.shearmodulusResolution, tickinterval=25)
        val=float(propS.shearmodulus.get())
        Input.shearmodulus=val
    slider.set(value=val)
    return float(val)

#############################################################################
def ChangeHandler():
  """To Pack the GUI inputs to the XML form"""
  global propS
#  global entrySoil  
# Update slider and input withentry upon clikcing Apply 
  val=GetVarValue()
  slider.set(value=val)    

# Fluid properties
  Input.pressure=float(propS.pressure.get())
  Input.temperature=float(propS.temperature.get())
    
  Input.sgas=float(propS.sgas.get())
  Input.swat =float(propS.swat.get())
  Input.soil=1.0 -  Input.swat-  Input.sgas#  float(propS.soil.get())
  
  Input.salinity=float(propS.salinity.get())
  Input.net_to_gross=float(propS.net_to_gross.get())
 
  Input.gasoil_ratio=float(propS.gasoil_ratio.get())
  Input.gas_specific_gravity=float(propS.gas_specific_gravity.get())
  Input.api=float(propS.api.get())
  IsActiveF.CO2Dissolution=propS.CO2Dissolution.get() 
  Input.CO2Flag=propS.CO2Flag.get()
# Rock Properties
  Input.rockdensity=float(propS.rockdensity.get())
  Input.porosity=float(propS.porosity.get())
  Input.critical_porosity=float(propS.critical_porosity.get())
  Input.vugfraction=float(propS.vugfraction.get())
  Input.KriefExponent=float(propS.KriefExponent.get())
  Input.Kdry=float(propS.Kdry.get())
  Input.Gdry=float(propS.Gdry.get())
 
# Calculated.Eff_porosity=Input.porosity*Input.net_to_gross
  Input.bulkmodulus=float(propS.bulkmodulus.get())
  Input.shearmodulus=float(propS.shearmodulus.get()) 
  
  Input.aratio1=float(propS.aratio1.get())
  Input.aratio2=float(propS.aratio2.get())
  
  Input.volfrac1=float(propS.volfrac1.get())
  Input.volfrac2=float(propS.volfrac2.get())
  
  Input.K_inclusion1=float(propS.K_inclusion1.get())
  Input.K_inclusion2=float(propS.K_inclusion2.get())
  
# Hs Bound Table
# Confining pressure params
  Input.confining_pressure =   float(propS.confining_pressure.get())
  Input.poisson_ratio = float(propS.poisson_ratio.get())
  Input.coord_number=float(propS.coord_number.get())
  Input.effPresCoef = float(propS.effPresCoef.get())
  Input.Linear_CoefAG= float(propS.Linear_CoefAG.get())
  Input.Linear_CoefAK= float(propS.Linear_CoefAK.get())
  Input.DeltaN1= float(propS.DeltaN1.get())
# Reflection coef
  Input.VpTop=float(propS.VpTop.get())
  Input.VsTop = float(propS.VsTop.get())
  Input.RhoTop= float(propS.RhoTop.get())
  Input.IncidentAngle= float(propS.IncidentAngle.get())
# Nuclear
  Input.rock_sigma_capture=float(propS.rock_sigma_capture.get())
#  Input.oil_sigma_capture=float(propS.oil_sigma_capture.get())
#  Input.brine_sigma_capture=float(propS.brine_sigma_capture.get())
#  Input.gas_sigma_capture=float(propS.gas_sigma_capture.get()) 
# Em 
  Input.nExp=float(propS.nExp.get())
  Input.mExp=float(propS.mExp.get())
  Input.tortuosity=float(propS.tortuosity.get())
  Input.QvCEC=float(propS.QvCEC.get())
#
  IsCalculated.Eff_Pressure = False
# Output 
# fluid
  IsActiveF.Fld_Rho=propS.flgRhoF.get()
  IsActiveF.Fld_Kb=propS.flgKbF.get()
  IsActiveF.Fld_Vp=propS.flgVpF.get()
  IsActiveF.Fld_Ip=propS.flgIpF.get()
# rock
  IsActiveF.Rock_Rho=propS.flgRhoR.get()
  IsActiveF.Rock_Kb=propS.flgKbR.get() 
  IsActiveF.Rock_Gb=propS.flgGbR.get() 
  IsActiveF.Rock_Vp=propS.flgVpR.get()  
  IsActiveF.Rock_Vs=propS.flgVsR.get()  
  IsActiveF.Rock_Ip=propS.flgIpR.get()    
  IsActiveF.Rock_Is=propS.flgIsR.get()  
# dry rock
  IsActiveF.Dry_Rho=propS.flgRhoD.get()
  IsActiveF.Dry_Kb=propS.flgKbD.get() 
  IsActiveF.Dry_Gb=propS.flgGbD.get() 
  IsActiveF.Dry_Vp=propS.flgVpD.get()  
  IsActiveF.Dry_Vs=propS.flgVsD.get()  
  IsActiveF.Dry_Ip=propS.flgIpD.get()    
  IsActiveF.Dry_Is=propS.flgIsD.get()    
# Effective
  IsActiveF.Eff_Rho=propS.flgRhoE.get()
  IsActiveF.Eff_Kb=propS.flgKbE.get()
  IsActiveF.Eff_Gb=propS.flgGbE.get()
  IsActiveF.Eff_PMod= propS.flgPMod.get()  

  IsActiveF.Eff_Vp=propS.flgVpE.get()
  IsActiveF.Eff_Vs=propS.flgVsE.get()
  IsActiveF.Eff_VpVs=propS.flgVpVsE.get()
  IsActiveF.Eff_Ip=propS.flgIpE.get()
  IsActiveF.Eff_Is=propS.flgIsE.get()
  
  IsActiveF.Eff_Rpp=propS.flgRppE.get()
  IsActiveF.Eff_Rps=propS.flgRpsE.get()
  IsCalculated.Eff_PressureOnce =  False
  
  if(RockPhysicModels.EMModelName=='none'):
      propS.flgCondE.set(False)
      propS.flgResE.set(False)
      
  IsActiveF.Eff_conductivity=propS.flgCondE.get()
  IsActiveF.Eff_resistivity=propS.flgResE.get()
  
  IsActiveF.Eff_neutron_sigma=propS.flgNeutron.get()  
   
  IsActiveF.flg2Dplot=(PlotAux.var1D_2DPlot=='2D plot') 
  IsActiveF.flgPlotHold=propS.flgPlotHold.get()

  IsActiveF.flgTLbaseline=propS.flgTLbaseline.get()

  PlotAux.varp2D=varPlot2D.get() 

#############################################################################
def Calculate(output_frame):
  """To Pack the GUI inputs to the XML form"""
  UpdateInput()
  CalculateOutput(output_frame)
#  
def UpdateInput():
  """To Pack the GUI inputs to the XML form"""
  ChangeHandler()
  Validate()
  ReinitializeIsCalculated()  
  
def Draw_Input_Pane(fr):
  """To Generate the Content for the Main Input Frame"""
  global var, varPlot,varPlot2D,propval,\
         slider, SlideLabel,  varLabel, varValue, sliderEntry, CeCVal,entrySoil, propS    

  styleB = ttk.Style()
  styleB.configure("Bold.TLabel", font=("TkDefaultFont", 9,"bold"), foreground="black")
  labelFluidProperties = ttk.Label(text="Fluid Properties", style="Bold.TLabel")

# Fluid Properties
  fluidprops = Labelframe(fr,labelwidget=labelFluidProperties,padding=2) 
#  fluidprops = Labelframe(fr,text="Fluid Properties",padding=2) 

  if sys.version_info < (3, 0):
      var=ttk.Tkinter.StringVar()
      SlideLabel=ttk.Tkinter.StringVar()
  else:
      SlideLabel=ttk.tkinter.StringVar()
      var=ttk.tkinter.StringVar()     
# Pressure 
  propS= InputVar()
  propS.pressure.set(value=str(Input.pressure))
  pressureRow=InputRow(fluidprops,InputPropNames.pressure,Input.pressure,'MPa',var,1,0)
  pressureRow.entry.config(textvar= propS.pressure)
##Temperature####
  propS.temperature.set(value=str(Input.temperature))
  temperatureRow=InputRow(fluidprops,InputPropNames.temperature,Input.temperature,u'\u2070C',var,2,0)
  temperatureRow.entry.config(textvar=propS.temperature)
#Soil###
  propS.soil.set(value=str(Input.soil))
  soilRow=InputRow(fluidprops,InputPropNames.soil,Input.soil,'',var,3,0)
  soilRow.entry.config(textvar=propS.soil)
  entrySoil= soilRow.entry
##SGAS##
  propS.sgas.set(value=str(Input.sgas))
  sgasRow=InputRow(fluidprops,InputPropNames.sgas,Input.sgas,'',var,4,0)
  sgasRow.button.select()
  sgasRow.entry.config(textvar=propS.sgas)
  
  propval=StringVar()
  propval.set(value=str(Input.sgas))
#Swat 
  propS.swat.set(value=str(Input.swat))
  swatRow=InputRow(fluidprops,InputPropNames.swat,Input.swat,'',var,5,0)
  swatRow.entry.config(textvar=propS.swat)  
# Salinity   
  propS.salinity.set(value=str(Input.salinity))
  salinityRow=InputRow(fluidprops,InputPropNames.salinity,Input.salinity,'wt%',var,6,0)
  salinityRow.entry.config(textvar=propS.salinity)
# API     
  propS.api.set(value=str(Input.api))
  apiRow=InputRow(fluidprops,InputPropNames.api,Input.api,'',var,7,0)
  apiRow.entry.config(textvar=propS.api)  
# Gas Specific Gravity
  propS.gas_specific_gravity.set(value=str(Input.gas_specific_gravity))
  gas_specific_gravityRow=InputRow(fluidprops,InputPropNames.gas_specific_gravity,Input.gas_specific_gravity,'',var,8,0)
  gas_specific_gravityRow.entry.config(textvar=propS.gas_specific_gravity)  
#GOR  

  propS.gasoil_ratio.set(value=str(Input.gasoil_ratio))
  gasoil_ratioRow=InputRow(fluidprops,InputPropNames.gasoil_ratio,Input.gasoil_ratio,'',var,9,0)
  gasoil_ratioRow.entry.config(textvar=propS.gasoil_ratio)      
#NTG     
  propS.net_to_gross.set(value=str(Input.net_to_gross))
  net_to_grossRow=InputRow(fluidprops,InputPropNames.net_to_gross,Input.net_to_gross,'',var,10,0)
  net_to_grossRow.entry.config(textvar=propS.net_to_gross)      

  fluidprops.grid(column=0,row=0,columnspan=3, rowspan=10,padx=2,pady=2,sticky='NWE')
# End of Defining Fluid Properties
#======================
# Rock Properties  
#======================
  labelrockprops = ttk.Label(text="Rock Grain Properties", style="Bold.TLabel")
  rockprops = Labelframe(fr,labelwidget=labelrockprops,padding=1) 

#  rockprops = Labelframe(fr,text="Rock Grain Properties",padding=2)
# Rock density 
  propS.rockdensity=StringVar(value=str(Input.rockdensity))   
  rockdensityRow=InputRow( rockprops,InputPropNames.rockdensity,Input.rockdensity,'kg/m3',var,0,2)  # rowindx, colindx_start
  rockdensityRow.entry.config(textvar=propS.rockdensity)       
#Porosity  
  propS.porosity=StringVar(value=str(Input.porosity))   
  porosityRow=InputRow( rockprops,InputPropNames.porosity,Input.porosity,'',var,1,2)  # rowindx, colindx_start
  porosityRow.entry.config(textvar=propS.porosity)      
#  critical_porosity  
  propS.critical_porosity=StringVar(value=str(Input.critical_porosity))   
  critical_porosityRow=InputRow( rockprops,InputPropNames.critical_porosity,Input.critical_porosity,'',var,2,2)  # rowindx, colindx_start
  critical_porosityRow.entry.config(textvar=propS.critical_porosity)       
# Bulk Modulus  
  propS.bulkmodulus=StringVar(value=str(Input.bulkmodulus))   
  bulkmodulusRow=InputRow( rockprops,InputPropNames.bulkmodulus,Input.bulkmodulus,'GPa',var,3,2)  # rowindx, colindx_start
  bulkmodulusRow.entry.config(textvar=propS.bulkmodulus)        
# shearmodulus 
  propS.shearmodulus=StringVar(value=str(Input.shearmodulus))   
  shearmodulusRow=InputRow( rockprops,InputPropNames.shearmodulus,Input.shearmodulus,'GPa',var,4,2)  # rowindx, colindx_start
  shearmodulusRow.entry.config(textvar=propS.shearmodulus) 
     
  rockprops.grid(column=4,row=0,rowspan=5, columnspan=4,padx=2,pady=2,sticky='NWE')
# End of Defining Rock Properties
#####################################################################
# Begin Gas Phase 
  labelHCorCO2 = ttk.Label(text="HC or "+ u'CO\u2082', style="Bold.TLabel")
#  HCorCO2 = Labelframe(fr,text="Gas Phase",padding=1) 
  HCorCO2 = Labelframe(fr,labelwidget=labelHCorCO2,padding=1) 
  propS.CO2Flag =StringVar(value="co2")
  Radiobutton(HCorCO2,text=u'CO\u2082',variable=propS.CO2Flag,value="co2"\
              ).grid(column=0,row=0,columnspan=2,sticky='NWS')
# CO2Dissolution   
  propS.CO2Dissolution = Tkinter.BooleanVar() 
  propS.CO2Dissolution=BooleanVar(value=IsActiveF.CO2Dissolution)
  chckCO2= Tkinter.Checkbutton(HCorCO2,text=u'with CO\u2082 dissolution in oil',variable=propS.CO2Dissolution)
  chckCO2.configure(state='disabled')
  chckCO2.grid(column=2,row=0,sticky='NWE')
 
  Radiobutton(HCorCO2,text="Hydrocarbon",variable=propS.CO2Flag,value="hcgas",\
             command=checkbutton_value).grid(column=0,row=1,columnspan=2,\
             padx=2,pady=2, sticky='NWS')
  
  IsActiveF.CO2Dissolution=propS.CO2Dissolution.get() 
  Input.CO2Flag=propS.CO2Flag.get()

  HCorCO2.grid(column=0,row=30,columnspan=3,padx=2,pady=2,sticky='NWE')   
#========================
# Slider Frame to update input values
#========================
  sliderFrame = ttk.Labelframe(fr,text="",padding=2)
  SlideLabel=StringVar()
  SlideLabel.set(value=var.get())

  slider = Scale(sliderFrame, label=SlideLabel.get(),from_=0, to=1, length=150,width=15,tickinterval=1,
               orient=HORIZONTAL, relief=SUNKEN, bd=1,
               sliderrelief=RAISED, resolution=0.5)
  slider.config(command =  updateSliderValue)  
  slider.grid(column=1,row=1,columnspan=1,rowspan=5, padx=2,pady=2,sticky='NWE')
  Entry(sliderFrame,textvar=propval,width=8, justify='center').\
  grid(row=3,column=5,padx=2,pady=2)
  sliderFrame.grid(column=3,row=5,columnspan=3,rowspan=3,padx=2,pady=2,sticky='NWE')
#        
def Draw_Output_Pane(fr):
  global propS,   chk_PMod,chk_KbE
# BeginOutput_Pane
#####################################################################
#  Label(fr,text="Seismic Properties",justify="left")\
#          .grid(column=0,row=0,columnspan=3,padx=2,pady=2,sticky='NEW')
############### Fluid properties          
  Output_fluid = Labelframe(fr,text="Fluid Properties",padding=2)  
# Rho 
  chk_RhoF=Checkbutton(Output_fluid,text="Density     ",variable=propS.flgRhoF,\
            onvalue=True)
  chk_RhoF.grid(column=1,row=0, sticky='NWE') 
  IsActiveF.Fld_Rho=propS.flgRhoF.get()
# Kb  
  chk_KbF=Checkbutton(Output_fluid,text="Bulk Modulus",variable=propS.flgKbF,\
            onvalue=True)
  chk_KbF.grid(column=2,row=0, sticky='NWE')
  IsActiveF.Fld_Kb=propS.flgKbF.get()
# Vp      
  chk_VpF=Checkbutton(Output_fluid,text="Vp           ",variable=propS.flgVpF,\
            onvalue=True)
  chk_VpF.grid(column=3,row=0, sticky='NWE')
  IsActiveF.Fld_Vp=propS.flgVpF.get()
# Ip   
  chk_IpF=Checkbutton(Output_fluid,text="Ip           ",variable=propS.flgIpF,\
            onvalue=True)
  chk_IpF.grid(column=4,row=0, sticky='NWE')
  IsActiveF.Fld_Ip=propS.flgIpF.get()
  Output_fluid.grid(column=0,row=1,columnspan=3,padx=2,pady=2,sticky='NWE')  
############### Rock fram propertyies properties          
  Output_rock = Labelframe(fr,text="Rockframe Properties",padding=2)  
# Rho 
  chk_RhoR=Checkbutton(Output_rock,text="Density     ",variable=propS.flgRhoR,\
            onvalue=True)
  chk_RhoR.grid(column=1,row=0, sticky='NWE') 
  IsActiveF.Rock_Rho=propS.flgRhoR.get()
# Km  
  chk_KbR=Checkbutton(Output_rock,text="Bulk Modulus",variable=propS.flgKbR,\
            onvalue=True)
  chk_KbR.grid(column=2,row=0, sticky='NWE')
  IsActiveF.Rock_Kb=propS.flgKbR.get()
# Gm  
  chk_GbR=Checkbutton(Output_rock,text="Shear Modulus",variable=propS.flgGbR,\
            onvalue=True)
  chk_GbR.grid(column=3,row=0, sticky='NWE')
  IsActiveF.Rock_Gb=propS.flgGbR.get()
# Vp      
  chk_VpR=Checkbutton(Output_rock,text="Vp           ",variable=propS.flgVpR,\
            onvalue=True)
  chk_VpR.grid(column=4,row=0, sticky='NWE')
  IsActiveF.Rock_Vp=propS.flgVpR.get()
# Vs      
  chk_VsR=Checkbutton(Output_rock,text="Vs           ",variable=propS.flgVsR,\
            onvalue=True)
  chk_VsR.grid(column=5,row=0, sticky='NWE')
  IsActiveF.Rock_Vs=propS.flgVsR.get()
# Ip   
  chk_IpR=Checkbutton(Output_rock,text="Ip           ",variable=propS.flgIpR,\
            onvalue=True)
  chk_IpR.grid(column=6,row=0, sticky='NWE')
  IsActiveF.Rock_Ip=propS.flgIpR.get()
  # Is   
  chk_IsR=Checkbutton(Output_rock,text="Is           ",variable=propS.flgIsR,\
            onvalue=True)
  chk_IsR.grid(column=7,row=0, sticky='NWE')
  IsActiveF.Rock_Is=propS.flgIpR.get()
  Output_rock.grid(column=0,row=2,columnspan=3,padx=2,pady=2,sticky='NWE')  
# Dry Properties
#####################################################################
  Output_Dry = Labelframe(fr,text="Dry Rock Properties",padding=2)
# Rho dry
  chk_RhoD=Checkbutton(Output_Dry,text="Density     ",variable=propS.flgRhoD,\
            onvalue=True)
  chk_RhoD.grid(column=1,row=0, sticky='NWE')
  IsActiveF.Dry_Rho=propS.flgRhoD.get()
# Kb Dry
  chk_KbD=Checkbutton(Output_Dry,text="Bulk Modulus",variable=propS.flgKbD,\
            onvalue=True)
  chk_KbD.grid(column=2,row=0, sticky='NWE')
  IsActiveF.Dry_Kb=propS.flgKbD.get()
# Gb Dry
  chk_GbD=Checkbutton(Output_Dry,text="Shear Modulus",variable=propS.flgGbD,\
            onvalue=True)
  chk_GbD.grid(column=3,row=0, sticky='NWE')
  IsActiveF.Dry_Gb=propS.flgGbD.get()
# Vp dry 
  chk_VpD=Checkbutton(Output_Dry,text="Vp           ",variable=propS.flgVpD,\
            onvalue=True)
  chk_VpD.grid(column=4,row=0, sticky='NWE') 
  IsActiveF.Dry_Vp=propS.flgVpD.get()
#  chk_VpD.select()
# Vs  
  chk_VsD=Checkbutton(Output_Dry,text="Vs          ",variable=propS.flgVsD,\
            onvalue=True)
  chk_VsD.grid(column=5,row=0, sticky='NWE')
  IsActiveF.Dry_Vs=propS.flgVsD.get()
# Ip      
  chk_IpD=Checkbutton(Output_Dry,text="Ip           ",variable=propS.flgIpD,\
            onvalue=True)
  chk_IpD.grid(column=6,row=0, sticky='NWE')
  IsActiveF.Dry_Ip= propS.flgIpD.get()
# Is 
  chk_IsD=Checkbutton(Output_Dry,text="Is          ",variable=propS.flgIsD,\
            onvalue=True)
  chk_IsD.grid(column=7,row=0, sticky='NWE')
  IsActiveF.Dry_Is = propS.flgIsD.get()
  Output_Dry.grid(column=0,row=3,columnspan=5,padx=2,pady=2,sticky='NW') 
# Effective Properties
#####################################################################
  Output_Effective = Labelframe(fr,text="Effective Rock Properties",padding=2)  
# Eff Rho 
  chk_RhoE=Checkbutton(Output_Effective,text="Density     ",\
                      variable=propS.flgRhoE, onvalue=True)
  chk_RhoE.grid(column=1,row=0, sticky='NWE')
  IsActiveF.Eff_Rho=propS.flgRhoE.get()
#  chk_RhoE.select()
# Eff Kb 
  chk_KbE=Checkbutton(Output_Effective,text="Bulk Modulus",\
                      variable=propS.flgKbE, onvalue=True)
#                      variable=flgKbE, onvalue=True, command=lambda: onClickKb())
  chk_KbE.grid(column=2,row=0, sticky='NWE')
  IsActiveF.Eff_Kb=propS.flgKbE.get()
# Eff Gb 
  chk_GbE=Checkbutton(Output_Effective,text="Shear Modulus",\
                      variable=propS.flgGbE, onvalue=True)
#                      variable=flgKbE, onvalue=True, command=lambda: onClickKb())
  chk_GbE.grid(column=3,row=0, sticky='NWE')
  IsActiveF.Eff_Gb=propS.flgGbE.get()
# Eff Vp 
  chk_VpE=Checkbutton(Output_Effective,text="Vp           ",\
  variable= propS.flgVpE, onvalue=True)
  chk_VpE.grid(column=4,row=0, sticky='NWE') 
  IsActiveF.Eff_Vp=propS.flgVpE.get()
  chk_VpE.select()
# Eff Vs   
  chk_VsE=Checkbutton(Output_Effective,text="Vs        ",\
      variable= propS.flgVsE,onvalue=True)    
  chk_VsE.grid(column=5,row=0, sticky='NWE')
  IsActiveF.Eff_Vs=propS.flgVsE.get()
# Eff VpVs   
  chk_VpVsE=Checkbutton(Output_Effective,text="Vp/Vs        ",\
      variable= propS.flgVpVsE,onvalue=True)    
  chk_VpVsE.grid(column=6,row=0, sticky='NWE')
  IsActiveF.Eff_VpVs=propS.flgVpVsE.get()
#  chk_VsE.select()
# Eff Ip  
  chk_IpE=Checkbutton(Output_Effective,text="Ip           ",\
  variable=propS.flgIpE, onvalue=True)
  chk_IpE.grid(column=7,row=0, sticky='NWE')
  IsActiveF.Eff_Ip=propS.flgIpE.get()
#  chk_IpE.select()
# Eff Is     
  chk_IsE=Checkbutton(Output_Effective,text="Is           ",\
  variable=propS.flgIsE, onvalue=True)
  chk_IsE.grid(column=8,row=0, sticky='NWE')
  IsActiveF.Eff_Is=propS.flgIsE.get()
# Eff PMod    
  chk_PMod=Checkbutton(Output_Effective,text="M-Modulus       ",\
  variable=propS.flgPMod, onvalue=True)
  chk_PMod.grid(column=9,row=0, sticky='NWE')
  IsActiveF.PMod=propS.flgPMod.get()
# Eff Rpp     
  Output_Effective.grid(column=0,row=4,columnspan=3,padx=2,pady=2,sticky='NWE') 
## Effective seismic properties  
#  Label(fr,text="Seismic Properties",justify="left")\
#    .grid(column=0,row=5,columnspan=3,padx=2,pady=2,sticky='NEW')  
  Output_seismic = Labelframe(fr,text="Effective Seismic Properties",padding=2)  
  chk_RppE=Checkbutton(Output_seismic,text="Rpp           ", variable=propS.flgRppE, onvalue=True)
  chk_RppE.grid(column=0,row=0, sticky='NWE')
  IsActiveF.Eff_Rpp=propS.flgRppE.get()
           
  chk_RpsE=Checkbutton(Output_seismic,text="Rps           ",variable=propS.flgRpsE, onvalue=True)
  chk_RpsE.grid(column=1,row=0, sticky='NWE')
  IsActiveF.Eff_Rps=propS.flgRpsE.get()
  Output_seismic.grid(column=0,row=5,columnspan=3,padx=2,pady=2,sticky='NWE')  
# Effective EM Properties
#  Label(fr,text="Effective EM Properties",justify="left")\
#    .grid(column=0,row=7,columnspan=3,padx=2,pady=2,sticky='NEW')
  Output_EM = Labelframe(fr,text="Effective EM Properties",padding=2)   

# Eff Cond
  chk_CondE=Checkbutton(Output_EM,text="Conductivity     ",variable=propS.flgCondE,\
            onvalue=True)
  chk_CondE.grid(column=1,row=0, sticky='NWE')
  IsActiveF.Eff_conductivity=propS.flgCondE.get()
  chk_ResE=Checkbutton(Output_EM,text="Resitivity",variable=propS.flgResE,\
            onvalue=True)
  chk_ResE.grid(column=2,row=0, sticky='NWE')
  IsActiveF.Eff_resistivity=propS.flgResE.get()
  Output_EM.grid(column=0,row=6,columnspan=3,padx=2,pady=2,sticky='NWE') 
###########################################
# Eff RST 
#  Label(fr,text="Nuclear Properties",justify="left")\
#    .grid(column=0,row=9,columnspan=3,padx=2,pady=2,sticky='NEW')  
  Output_RST = Labelframe(fr,text="Effective Nuclear Properties",padding=2)   
  chk_RST=Checkbutton(Output_RST,text="Cross Capture     ",\
          variable=propS.flgNeutron, onvalue=True)            
  chk_RST.grid(column=1,row=9, sticky='NWE')
  IsActiveF.Eff_RST=propS.flgNeutron.get()
  Output_RST.grid(column=0,row=7,columnspan=3,padx=2,pady=2,sticky='NWE')  
# End Draw_Output_Pane  
############################################################################    
def Draw_Rockphysics_Pane(fr):
  """To Generate the Content for the Main Input Frame"""
  global   Plot_frame, varPlot,varPlot2D, flg2Dplot, flgCheckUncertainty, Plot_Options_frame1D,Plot_Options_frame2D,\
  TLA_frame, vug_frame,ContactCement_frame, HertzMindlin_frame,Krief_frame, UInput_Dryframe, aratio_frame,earatio_frame,HS_frame,rock_matrix, tabl,\
  ConfP_frameHM, ConfP_frameLinear,ConfP_frameMacBeth, ConfP_frameContactCement, FSMGassmannHTI_frame,\
  varTL_Fwd,chk_TLbaseline, chk_plot_hold,var1D_2DPlot,Plot_list_frame
# ConPModCombo, 
  
  # reflection coefficient parameters
  
#  styleN = ttk.Style()
#  styleIT = ttk.Style()

#  style.configure("Bold.TLabel", font=("TkDefaultFont", 12, "bold"))
#  styleN.configure("Normal.TLabel", font=("TkDefaultFont", 10, "normal"), foreground="blue")
#  styleIT.configure("Italic.TLabel", font=("TkDefaultFont", 10, "italic"), foreground="blue")
  styleB = ttk.Style()
  styleB.configure("Bold.TLabel", font=("TkDefaultFont", 9,"bold"), foreground="blue")
  labelElasticpropsB = ttk.Label(text="Rock Physics and Seismic Response", style="Bold.TLabel")
#  labelElasticpropsI = ttk.Label(text="Rock Physics and Seismic Response", style="Italic.TLabel")
#  labelElasticpropsN = ttk.Label(text="Rock Physics and Seismic Response", style="Normal.TLabel")
#  elasticprops = Labelframe(multiphysics_frame,labelwidget=labelElasticpropsB) 

  
  multiphysics_frame = Labelframe(fr,text="",padding=0,  relief='raised')

  multrow=0
  ComboboxWidth=30
  Label(multiphysics_frame,text="",justify="left")\
    .grid(column=0,row=multrow,columnspan=3,rowspan=5,padx=1,pady=1,sticky='NE')
 # Elastic properties-
#  elasticprops = Labelframe(multiphysics_frame,text="Rock Physics and Seismic Response",padding=1) 
  labelElasticpropsB = ttk.Label(text="Rock Physics and Seismic Response", style="Bold.TLabel")
  elasticprops = Labelframe(multiphysics_frame,labelwidget=labelElasticpropsB) 
  rock_matrix = Labelframe(elasticprops,text="",padding=1)   
 
  aratio_frame=Labelframe(rock_matrix,text="Properties of inclusions",padding=1) # This will be active in certain dry rock options
  aratio_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')     
 
  label=Label(rock_matrix,text="Rock Frame Model",width=17)
  label.grid(column=0,row=0,columnspan=2,padx=2,sticky='NW')
  
  RockFrameModList=['User input','DEM','Self-consistent', 'Kuster-Toksoz', 'HS+', 'HS-', 'HSAve', 'Voigt', 'Reuss', 'Voigt-Reuss'];
  RockFrame=Combobox(rock_matrix,width=ComboboxWidth,state="readonly",\
          values=RockFrameModList,textvariable=propS.RockFrameMod)  
  RockFrame.current(0)
  
  propS.aratio1=StringVar(value=str(Input.aratio1))
  propS.aratio2=StringVar(value=str(Input.aratio2))
  
  propS.Ave_weight_frac = StringVar(value=str(Input.Ave_weight_frac))
  # fraction of the mineral phase within    rock frame before introducing
  # connected pores
  propS.volfrac1=StringVar(value=str(Input.volfrac1))
  propS.volfrac2=StringVar(value=str(Input.volfrac2))
  
  propS.K_inclusion1=StringVar(value=str(Input.K_inclusion1))
  propS.K_inclusion2=StringVar(value=str(Input.K_inclusion2))
  
# Frame for HS and Voigt-Reuss Bounds
  HS_frame=Labelframe(rock_matrix,text="",padding=1) # This will be active in certain dry rock options
  HS_frame.grid(column=0,row=2,padx=2,columnspan=4, pady=2,sticky='NE')    
    
  RockFrame.bind("<<ComboboxSelected>>",RockFrameModel)
  RockFrame.grid(column=2,row=0,columnspan=10,padx=2,pady=2,sticky='NW')
  RockPhysicModels.RockFrameModelName = propS.RockFrameMod.get()
  
  rock_matrix.grid(column=0,row=1,columnspan=10,padx=2,pady=1,sticky='NWE') 
 
# Dry ective properties Start 
  dry_rock = Labelframe(elasticprops,text="",padding=1)   
  dry_rock.grid(column=0,row=2,columnspan=10,padx=2,pady=1,sticky='W') 
   
  vug_frame=Labelframe(dry_rock,text="",padding=1) # This will be active in certain dry rock options
  Krief_frame=Labelframe(dry_rock,text="",padding=1) # This will be active in certain dry rock options
  ContactCement_frame=Labelframe(dry_rock,text="",padding=1) # This willdeactivate confining pressure frame
  HertzMindlin_frame=Labelframe(dry_rock,text="",padding=1) # This willdeactivate confining pressure frame

  UInput_Dryframe=Labelframe(dry_rock,text="",padding=1) # This will be active in certain dry rock options
  
  labelDRY=Label(dry_rock,text="Dry Rock Model", width=14,anchor=E)
  labelDRY.grid(column=0,row=0,columnspan=2,padx=4,sticky='NW')
          
#  DryMod=StringVar()
  DryModList=['Krief','Krief with critical porosity','User input', 'Contact cement','Forward carbonate advisor', 'Hertz-Mindlin','Hertz-Mindlin with HS-'];
  Dry=Combobox(dry_rock,width=ComboboxWidth,state="readonly",\
          values=DryModList,textvariable=propS.DryMod)  
  Dry.current(0)
  
  propS.vugfraction=StringVar(value=str(Input.vugfraction))
  propS.KriefExponent=StringVar(value=str(Input.KriefExponent))
  Dry.bind("<<ComboboxSelected>>",DryRockModel)
  
  Dry.grid(column=2,row=0,columnspan=5,padx=2,pady=2,sticky='NW')
  
  RockPhysicModels.DryRockModelName = propS.DryMod.get()
  
#  dry_rock.grid(column=0,row=3,columnspan=10,padx=2,pady=1,sticky='W') 
  
  Krief_label=Label(Krief_frame,text="Krief exponent ")
  Krief_entry= Entry(Krief_frame,textvar=propS.KriefExponent,width=8, justify='center')
  Krief_label.grid(column=0,row=0,padx=20,pady=2,sticky='E')
  Krief_entry.grid(column=1,row=0,padx=20,pady=2,columnspan=5,sticky='E')
  Krief_frame.grid(column=0,row=2,padx=2,pady=2,columnspan=8,sticky='W')
  
  # Confining Pressure effect-Start
#  conf_pressure = Labelframe(elasticprops,text="",padding=2)   
#  conf_pressure.grid(column=0,row=3,columnspan=3,padx=2,pady=1,sticky='NWE') 
#  
#  ConfP_frameHM=Labelframe(conf_pressure,text="",padding=1) # This will be active in certain dry rock options
#  ConfP_frameHM.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')   
#  
#  ConfP_frameLinear=Labelframe(conf_pressure,text="",padding=1) # This will be active in certain dry rock options
#  ConfP_frameMacBeth=Labelframe(conf_pressure,text="",padding=1) # This will be active in certain dry rock options
#  
#  ConfP_frameContactCement=Labelframe(conf_pressure,text="",padding=1) # This will be active in certain dry rock options
#  ConfP_frameContactCement.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')   
#
#  labelName=Label(conf_pressure,text="Confining Pressure Model", width=23,anchor=E)
#  labelName.grid(column=0,row=0,columnspan=2,padx=2, sticky='NW')
#
#  ConModList=['No pressure effect', 'Hertz-Mindlin','Hertz-Mindlin with HS-', 'Linear'];
#  ConPModCombo=Combobox( conf_pressure,width=ComboboxWidth,state="readonly",\
#          values=ConModList,textvariable=propS.ConfMod)  
#  ConPModCombo.current(0)
#
#  propS.confining_pressure= StringVar(value=str(Input.confining_pressure))
#  propS.effPresCoef= StringVar(value=str(Input.effPresCoef))
## HM
#  propS.coord_number= StringVar(value=str(Input.coord_number))
#  propS.poisson_ratio= StringVar(value=str(Input.poisson_ratio))
## Linear
#  propS.Linear_CoefAK= StringVar(value=str(Input.Linear_CoefAK))
#  propS.Linear_CoefAG= StringVar(value=str(Input.Linear_CoefAG))
## MacBeth
#  propS.MacBeth_Pk= StringVar(value=str(Input.MacBeth_Pk))
#  propS.MacBeth_Ek= StringVar(value=str(Input.MacBeth_Ek))
#  
#  propS.MacBeth_Pg= StringVar(value=str(Input.MacBeth_Pg))
#  propS.MacBeth_Eg= StringVar(value=str(Input.MacBeth_Eg))
#  
#  propS.KCement= StringVar(value=str(Input.KCement))
#  propS.GCement= StringVar(value=str(Input.GCement))
#  propS.KClay= StringVar(value=str(Input.KClay))
#  propS.GClay= StringVar(value=str(Input.GClay))
#  
#  propS.ClayPatchiness= StringVar(value=str(Input.ClayPatchiness))
#  propS.CementSat= StringVar(value=str(Input.CementSat))
#  
#  ConPModCombo.bind("<<ComboboxSelected>>",ConfPresModel)
#  ConPModCombo.grid(column=2,row=0,columnspan=2,padx=2,pady=2,sticky='NW')
#  RockPhysicModels.ConfiningPModelName =propS.ConfMod.get()
 # Confining Pressure effect-End
  
########################### # Dry ective properties END
  
# Fluid Susbtitution Models-2
  fluid_subs = Labelframe(elasticprops,text="",padding=2)   
  labelFSM=Label(fluid_subs,text="Fluid Substitution",width=17)
  labelFSM.grid(column=0,row=0,padx=1, sticky='NW',columnspan=2)
    
  FSModels=[RockPhysicModels.FSM_GassmannModel,RockPhysicModels.FSM_PatcyModel,RockPhysicModels.FSM_HTI_0_PC11_SshC44,\
          RockPhysicModels.FSM_HTI_0_PC11_SsvC66,RockPhysicModels.FSM_HTI_0_PC33_SC44,\
          RockPhysicModels.FSM_ORTH_PC33_SC44,RockPhysicModels.FSM_ORTH_PC33_SC55]
  
  FSM=Combobox(fluid_subs,width=ComboboxWidth,state="readonly",\
          values=FSModels,textvariable=propS.FSMMod)
  FSM.current(0)
  
  FSMGassmannHTI_frame= Labelframe(fluid_subs,text="",padding=1) 
  propS.deltaN1=StringVar(value=str(Input.DeltaN1))
  propS.deltaN2=StringVar(value=str(Input.DeltaN2))

  FSM.bind("<<ComboboxSelected>>",FSMName)
  FSM.grid(column=4,row=0,columnspan=5,padx=2,pady=2,sticky='NW') 
  RockPhysicModels.FSMName =propS.FSMMod.get()   
  fluid_subs.grid(column=0,row=4,columnspan=3,padx=2,pady=1,sticky='NWE')

# Reflection coefficients  
  Reflection_coef = Labelframe(elasticprops,text="",padding=2)   
  Label(Reflection_coef,text='Reflection Coefficients',width=35)\
          .grid(column=0,row=0,padx=2,pady=2,sticky='W',columnspan=6)
          
#  ReflectionCoefMod=StringVar()
  ReflectionCoef=Combobox(Reflection_coef,width=ComboboxWidth,state="readonly",\
          values=['Full Zoeppritz','Aki&Richards', 'Normal Incidence'],textvariable=propS.ReflectionCoefMod)
  ReflectionCoef.current(0)
  
  ReflectionCoef.bind("<<ComboboxSelected>>",RefCoefName)
  ReflectionCoef.grid(column=2,row=0,padx=4,pady=5,sticky='NW',columnspan=5) 
  
  RockPhysicModels.RefCoefName =propS.ReflectionCoefMod.get()   
  
  propS.VpTop=StringVar(value=str(Input.VpTop)) 
  Label(Reflection_coef,text=InputPropNames.VpTop)\
          .grid(column=0,row=1,padx=10,pady=2,sticky='NE')
  Entry(Reflection_coef,textvar=propS.VpTop,width=8, justify='center')\
          .grid(column=1,row=1,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Input.VpTop=float(propS.VpTop.get())
  
  Label(Reflection_coef,text=InputPropNames.VsTop)\
          .grid(column=3,row=1,padx=10,pady=2,sticky='NE')
  propS.VsTop=StringVar(value=str(Input.VsTop)) 
  Entry(Reflection_coef,textvar=propS.VsTop,width=8, justify='center')\
          .grid(column=4,row=1,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Input.VsTop=float(propS.VsTop.get())
  
  Label(Reflection_coef,text=InputPropNames.RhoTop)\
          .grid(column=0,row=2,padx=10,pady=2,sticky='NE')
  propS.RhoTop=StringVar(value=str(Input.VsTop)) 
  Entry(Reflection_coef,textvar=propS.RhoTop,width=8, justify='center')\
          .grid(column=1,row=2,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Input.RhoTop=float(propS.RhoTop.get())
        
  Label(Reflection_coef,text=InputPropNames.IncidentAngle)\
          .grid(column=3,row=2,padx=10,pady=2,sticky='NE')
  propS.IncidentAngle=StringVar(value=str(Input.IncidentAngle))
  Entry(Reflection_coef,textvar=propS.IncidentAngle,width=8, justify='center')\
          .grid(column=4,row=2,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Input.IncidentAngle=float(propS.IncidentAngle.get())   
  Reflection_coef.grid(column=0,row=5,columnspan=3,padx=2,pady=2,sticky='NWE')
      
  multrow=1
  elasticprops.grid(column=0,row=multrow,columnspan=20,padx=2,pady=5,sticky='NWE') 
  
#EM modeling
  multrow=2
#
  labelEM_model = ttk.Label(text="EM Response", style="Bold.TLabel")
  EM_model = Labelframe(multiphysics_frame,labelwidget=labelEM_model) 

#  EM_model = Labelframe(multiphysics_frame,text="EM Response",padding=2) 
  Label(EM_model,text="Conductivity models")\
          .grid(column=0,row=0,padx=20,pady=2,sticky='NE')
  
#  EMMod=StringVar()
  EMModList=['none','Archie','Waxman-Smits'];
  EM=Combobox(EM_model,width=ComboboxWidth,state="readonly",\
          values=EMModList,textvariable=propS.EMMod)  
  EM.current(0)
  
  EM_input_frame = Labelframe(EM_model,text="",width=40) 
#  EM_input_frame.grid(column=0,row=1,padx=20,pady=2,columnspan=10,sticky='W')
  
  
  propS.QvCEC= StringVar(value=str(Input.QvCEC))
  CecEntry=ttk.Entry(EM_input_frame,textvar=propS.QvCEC,width=8, justify='center')
  CecEntry.configure(state='disabled')
  EM.bind("<<ComboboxSelected>>",lambda event: EMModelName(EM_input_frame,CecEntry))
  EM.grid(column=1,row=0,columnspan=10,padx=8,pady=0,sticky='NWE')
  RockPhysicModels.EMModelName = propS.EMMod.get()
  Input.QvCEC=float(propS.QvCEC.get())
  
#n 
  propS.nExp=StringVar(value=str(Input.nExp))
  Label(EM_input_frame,text=InputPropNames.nExp)\
          .grid(column=0,row=1,padx=20,pady=2,sticky='NE')
  Entry(EM_input_frame,textvar=propS.nExp,width=10, justify='center')\
          .grid(column=1,row=1,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Label(EM_input_frame,text='', justify='left')\
          .grid(column=3,row=1,padx=2,pady=2,sticky='NE')
  Input.nExp=float(propS.nExp.get()) 
#m
  propS.mExp=StringVar(value=str(Input.mExp))
  Label(EM_input_frame,text=InputPropNames.mExp)\
          .grid(column=0,row=2,padx=20,pady=2,sticky='NE')
  Entry(EM_input_frame,textvar=propS.mExp,width=10, justify='center')\
          .grid(column=1,row=2,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Label(EM_input_frame,text='', justify='left')\
          .grid(column=3,row=2,padx=2,pady=2,sticky='NE')
  Input.mExp=float(propS.mExp.get()) 
  
# Tortuosity  
  propS.tortuosity=StringVar(value=str(Input.tortuosity))
  Label(EM_input_frame,text=InputPropNames.tortuosity)\
          .grid(column=0,row=3,padx=20,pady=2,sticky='NE')
  Entry(EM_input_frame,textvar=propS.tortuosity,width=10, justify='center')\
          .grid(column=1,row=3,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Label(EM_input_frame,text='', justify='left')\
          .grid(column=3,row=3,padx=2,pady=2,sticky='NE')
  Input.tortuosity=float(propS.tortuosity.get()) 
  
  Label(EM_input_frame,text='', justify='left')\
          .grid(column=3,row=4,padx=2,pady=2,sticky='NE')
   # Cec
  Label(EM_input_frame,text=InputPropNames.QvCEC)\
          .grid(column=0,row=4,padx=20,pady=2,sticky='NE')         
  CecEntry.grid(column=1,row=4,columnspan=2,padx=5,pady=2,sticky='NWE')   

# end Cec  
  
  multrow=3
  EM_model.grid(column=0,row=  multrow,columnspan=3,padx=2,pady=1,sticky='NWE')
#
  multrow=4  
  labelNeutron_model = ttk.Label(text="Nuclear Response", style="Bold.TLabel")
  Neutron_model = Labelframe(multiphysics_frame,labelwidget=labelNeutron_model) 

#  Neutron_model = Labelframe(multiphysics_frame,text="Nuclear Response",padding=2) 
  
  propS.rock_sigma_capture=StringVar(value=str(Input.rock_sigma_capture))
  Label(Neutron_model,text=InputPropNames.rock_sigma_capture)\
          .grid(column=0,row=2,padx=20,pady=2,sticky='NE')
  Entry(Neutron_model,textvar=propS.rock_sigma_capture,width=10, justify='center')\
          .grid(column=1,row=2,columnspan=2,padx=5,pady=2,sticky='NWE') 
  Label(Neutron_model,text='c.u', justify='left')\
          .grid(column=3,row=2,padx=2,pady=2,sticky='NE')          
  Input.rock_sigma_capture =float(propS.rock_sigma_capture.get()) 
  
#  propS.oil_sigma_capture=StringVar(value=str(Input.oil_sigma_capture))
#  Label(Neutron_model,text=InputPropNames.oil_sigma_capture)\
#          .grid(column=0,row=3,padx=20,pady=2,sticky='NE')
#  Entry(Neutron_model,textvar=propS.oil_sigma_capture,width=10, justify='center')\
#          .grid(column=1,row=3,columnspan=2,padx=5,pady=2,sticky='NWE') 
#  Label(Neutron_model,text='c.u', justify='left')\
#          .grid(column=3,row=3,padx=2,pady=2,sticky='NE')          
#  Input.oil_sigma_capture =float(propS.oil_sigma_capture.get()) 
#
#  propS.brine_sigma_capture=StringVar(value=str(Input.brine_sigma_capture))
#  Label(Neutron_model,text=InputPropNames.brine_sigma_capture)\
#          .grid(column=0,row=4,padx=20,pady=2,sticky='NE')
#  Entry(Neutron_model,textvar=propS.brine_sigma_capture,width=10, justify='center')\
#          .grid(column=1,row=4,columnspan=2,padx=5,pady=2,sticky='NWE') 
#  Label(Neutron_model,text='c.u', justify='left')\
#          .grid(column=3,row=4,padx=2,pady=2,sticky='NE')          
#  Input.brine_sigma_capture =float(propS.brine_sigma_capture.get()) 
#  
#  propS.gas_sigma_capture=StringVar(value=str(Input.gas_sigma_capture))
#  Label(Neutron_model,text=InputPropNames.gas_sigma_capture)\
#          .grid(column=0,row=5,padx=20,pady=2,sticky='NE')
#  Entry(Neutron_model,textvar=propS.gas_sigma_capture,width=10, justify='center')\
#          .grid(column=1,row=5,columnspan=2,padx=5,pady=2,sticky='NWE') 
#  Label(Neutron_model,text='c.u', justify='left')\
#          .grid(column=3,row=5,padx=2,pady=2,sticky='NE')          
#  Input.gas_sigma_capture =float(propS.gas_sigma_capture.get()) 
  
  multrow=5
  Neutron_model.grid(column=0,row=multrow,columnspan=3,padx=2,pady=2,sticky='NWE')
  multiphysics_frame.grid(column=0,row=0,rowspan=30,columnspan=3,padx=2,pady=4)
  #
  # Plotting frame
  #########################
  Plot_frame = Labelframe(fr,text="",padding=2,  relief='raised')
  Plot_Properties_Sw(Plot_frame, '',  'x-axis', 'y-axis','unit', Calculate_Effective_Ip,0)
  Plot_frame.grid(column=3,row=0,padx=2,pady=2,sticky='N',columnspan=10)  
            
# Plot list frame
  
#  Plot_list_frame = Labelframe(fr,text="Analysis",padding=1) 
  labelPlot_list_frame = ttk.Label(text="Analysis", style="Bold.TLabel")
  Plot_list_frame = Labelframe(fr,labelwidget=labelPlot_list_frame) 

  Plot_list_frame.grid(column=3,row=1,padx=2,pady=2,sticky='NW', columnspan=10)  

# Forward or TL analysis
  varTL_Fwd=StringVar()     
  chk_TLbaseline=Checkbutton(Plot_list_frame,text="Set the current as baseline",variable=propS.flgTLbaseline,\
            onvalue=True, command= lambda: onClickHold())
    
  RadioFwd=  Radiobutton(Plot_list_frame, variable=varTL_Fwd,value='Forward', command= isTLForward)
  PlotAux.varTL_Fwd=varTL_Fwd.get()
  Label_Fwd=Label(Plot_list_frame,text='Forward')
  RadioFwd.select()

  RadioTL=  Radiobutton(Plot_list_frame, variable=varTL_Fwd,value='R.Difference', command= isTLForward)
  PlotAux.varTL_Fwd=varTL_Fwd.get()
  Label_TL=Label(Plot_list_frame,text='R.Difference')
  
  chk_TLbaseline.config(state='disabled')
  IsActiveF.flgTLbaseline=propS.flgTLbaseline.get() 

  RadioFwd.grid(column=1,row=0,pady=4,sticky='E')   
  Label_Fwd.grid(column=2,row=0,pady=2,sticky='W') 
  RadioTL.grid(column=3,row=0,pady=4,sticky='E')   
  Label_TL.grid(column=4,row=0,pady=2,sticky='W') 
  chk_TLbaseline.grid(column=5,row=0, padx=4,pady=1, sticky='E', columnspan=4)
#update this part       
  PList=['Plot options','Compressional velocity','Shear velocity','Bulk modulus', 'M-Modulus', 'Density', \
  'Compressional impedance', 'Rpp', 'Rps','Conductivity','Resistivity', 'Nuclear'];
 
  plotting=Combobox( Plot_list_frame,width=1,state="readonly",\
          values=PList,textvariable=propS.PlotMod) 
  
  plotting.grid(column=1,row=1,padx=5,pady=8,sticky='NWE',columnspan=4) 
  plotting.current(0)  
  plotting.bind("<<ComboboxSelected>>",PlotName)
  PlotList.PlotName = propS.PlotMod.get()
    
  var1D_2DPlot=StringVar() 
  Radio1DPlot=  Radiobutton(Plot_list_frame, variable=var1D_2DPlot,value='1D plot', command= TwoDplotChanged)
  PlotAux.var1D_2DPlot=var1D_2DPlot.get()
  Label_1D=Label(Plot_list_frame,text='1D plot')

  Radio2DPlot=  Radiobutton(Plot_list_frame, variable=var1D_2DPlot,value='2D plot', command= TwoDplotChanged)
  Radio2DPlot.select()
  PlotAux.var1D_2DPlot=var1D_2DPlot.get()
  
  Label_2D=Label(Plot_list_frame,text='2D plot')
  Plot_Button=Button(Plot_list_frame,text='Plot',  font=("TkDefaultFont", 8,"bold"),width=4, command=PlotName2 )
  
  Plot_Button.grid(column=5,row=1,pady=2,padx=4,sticky='W') 
  Radio1DPlot.grid(column=6,row=1,pady=2,sticky='W')   
  Label_1D.grid(column=7,row=1,pady=2,sticky='W') 
  Radio2DPlot.grid(column=8,row=1,pady=2,sticky='W')   
  Label_2D.grid(column=9,row=1,pady=2,sticky='W') 
  
  Plot_Options_frame1D = Labelframe(Plot_list_frame,text="",padding=2, relief='raised')
  Plot_Options_frame2D = Labelframe(Plot_list_frame,text="",padding=2,  relief='raised')
  varPlot=StringVar()
  varPlot2D=StringVar() 
  chk_plot_hold=Checkbutton(Plot_Options_frame1D,text="Plot hold",variable=propS.flgPlotHold,onvalue=True)

  Label_2D_Plots=Label(Plot_Options_frame2D,text="X-Y Axis:   ")
  PlotRadioPT=  Radiobutton(Plot_Options_frame2D, variable=varPlot2D,value="P-T", command= isTobePlotted2D)
  Label_PT=Label(Plot_Options_frame2D,text="P-T")
  PlotRadioSwSg=  Radiobutton(Plot_Options_frame2D, variable=varPlot2D,value="Sw-Sg", command= isTobePlotted2D)
  Label_SwSg=Label(Plot_Options_frame2D,text="Sw-Sg")
  PlotRadioSwSg.select()
  Label_2D_Plots.grid(column=1,row=2,pady=2,sticky='W') 
  
  PlotRadioSwSg.grid(column=2,row=2,padx=2,pady=4,sticky='E')   
  Label_SwSg.grid(column=3,row=2,pady=2,sticky='E') 
  PlotRadioPT.grid(column=4,row=2,pady=4,sticky='E')   
  Label_PT.grid(column=5,row=2,pady=2,sticky='W')
  Plot_Options_frame2D.grid(column=0,row=3,columnspan=10,sticky='W')     
  
def TwoDplotChanged():
    global varPlot, varPlot2D,  chk_plot_hold,var1D_2DPlot,Plot_list_frame,\
    StringVar,Plot_Options_frame1D,Plot_Options_frame2D
        
    PlotAux.var1D_2DPlot=var1D_2DPlot.get()  
#1D
    Label_1D_Plots=Label(Plot_Options_frame1D,text="X-Axis:   ")     
    PlotRadioPressure=  Radiobutton(Plot_Options_frame1D, variable=varPlot,value="Pressure", command= isTobePlotted)
    Label_pres=Label(Plot_Options_frame1D,text="Pressure")
    PlotAux.varp=varPlot.get()   
    PlotRadioSaturation=  Radiobutton(Plot_Options_frame1D, variable=varPlot,value="Saturation", command= isTobePlotted)
    PlotRadioSaturation.select()
    Label_sat=Label(Plot_Options_frame1D,text="Saturation")
    PlotAux.varp=varPlot.get()    
    PlotRadioTemperature=  Radiobutton(Plot_Options_frame1D, variable=varPlot,value="Temperature", command= isTobePlotted)
    Label_temp=Label(Plot_Options_frame1D,text="Temperature")
    PlotAux.varp=varPlot.get()
    chk_plot_hold=Checkbutton(Plot_Options_frame1D,text="Plot hold",variable=propS.flgPlotHold,onvalue=True)
#2D    
    varPlot2D=StringVar() 
    Label_2D_Plots=Label(Plot_Options_frame2D,text="X-Y Axis:   ")
    PlotRadioPT=  Radiobutton(Plot_Options_frame2D, variable=varPlot2D,value="P-T", command= isTobePlotted)
    Label_PT=Label(Plot_Options_frame2D,text="P-T")
    PlotAux.varp2D=varPlot2D.get() 
    PlotRadioSwSg=  Radiobutton(Plot_Options_frame2D, variable=varPlot2D,value="Sw-Sg", command= isTobePlotted)
    Label_SwSg=Label(Plot_Options_frame2D,text="Sw-Sg")
    PlotRadioSwSg.select()
    PlotAux.varp2D=varPlot2D.get() 

    Label_2D_Plots.grid(column=1,row=2,pady=2,sticky='W')  
    PlotRadioSwSg.grid(column=2,row=2,padx=2,pady=4,sticky='E')   
    Label_SwSg.grid(column=3,row=2,pady=2,sticky='E') 
    PlotRadioPT.grid(column=4,row=2,pady=4,sticky='E')   
    Label_PT.grid(column=5,row=2,pady=2,sticky='W')
    Plot_Options_frame2D.grid(column=0,row=3,columnspan=10,sticky='W')      
   
    if(PlotAux.var1D_2DPlot=='2D plot'):
        Plot_Options_frame1D.grid_forget()      
        Label_2D_Plots.grid(column=1,row=2,pady=2,sticky='W')  
        PlotRadioSwSg.grid(column=2,row=2,padx=2,pady=4,sticky='E')   
        Label_SwSg.grid(column=3,row=2,pady=2,sticky='E') 
        PlotRadioPT.grid(column=4,row=2,pady=4,sticky='E')   
        Label_PT.grid(column=5,row=2,pady=2,sticky='W')
        Plot_Options_frame2D.grid(column=0,row=3,columnspan=10,sticky='W')      
        IsActiveF.flg2DPlot=propS.flgPlotHold.get()
        PlotAux.varp2D=varPlot2D.get() 

    else:
        isTLForward()
        Plot_Options_frame2D.grid_forget() 
        Label_1D_Plots.grid(column=1,row=1,pady=2,sticky='W')  
        PlotRadioSaturation.grid(column=2,row=1,padx=2,pady=4,sticky='E')   
        Label_sat.grid(column=3,row=1,pady=1,sticky='E')       
        PlotRadioTemperature.grid(column=4,row=1,pady=4,sticky='E')  
        Label_temp.grid(column=5,row=1,sticky='E')        
        PlotRadioPressure.grid(column=6,row=1,pady=4,sticky='E')
        Label_pres.grid(column=7,row=1,pady=2,sticky='W')    
        chk_plot_hold.grid(column=9,row=1, padx=4,pady=1, sticky='E')
        Plot_Options_frame1D.grid(column=0,row=3,columnspan=10, sticky='W')     
        
    propS.flgPlotHold.set(False)      
    IsActiveF.flgPlotHold=propS.flgPlotHold.get()   

def PlotName(event):    
     if (PlotAux.varTL_Fwd=='Forward'  ):
         PlotForward(event)
     else:
         PlotTL(event)
def PlotName2():    
     if (PlotAux.varTL_Fwd=='Forward'  ):
         PlotForward2()
     else:
         PlotTL2()
def PlotForward2():
     title=StringVar()
     ChangeHandler()
     title=''
     plt.close('all')
     indx=1 # might be used for options
     if(IsActiveF.flg2Dplot):
          [title, unit, funCalc]=Two_Dimnesional_plots() 
          if(PlotAux.varp2D=='Sw-Sg' ):
              xlabel= ''
              ylabel= ''
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Plot_Properties_SwSg(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
          else: #(PlotAux.varp2D=='P-T' ):
              xlabel= 'Pressure[MPa]'
              ylabel= 'Temperature[C]'
              Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
              Plot_Properties_PT(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     else:
         [title,unit,ylabel, funCalc]=One_Dimensional_plots()
         if PlotAux.varp=='Saturation':
             xlabel= '$\mathbf{S_{w}}$'
             Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
             Plot_Properties_Sw(Plot_frame, title, unit, xlabel, ylabel, funCalc,indx)
         elif PlotAux.varp=='Pressure':
             xlabel= 'Pressure[MPa]'
             Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
             Plot_Properties_Pressure(Plot_frame, title, unit, xlabel, ylabel,funCalc,indx)
         else: 
             Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
             xlabel= 'Temperature[C]'
             Plot_Properties_Temperature(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     RockPhysicModels.PlotName =propS.PlotMod.get()
    
def PlotForward(event):
     title=StringVar()
     ChangeHandler()
     title=''
     plt.close('all')
     indx=1 # might be used for options
     if(IsActiveF.flg2Dplot):
          [title, unit, funCalc]=Two_Dimnesional_plots() 
          if(PlotAux.varp2D=='Sw-Sg' ):
              xlabel= ''
              ylabel= ''
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Plot_Properties_SwSg(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
          else: #(PlotAux.varp2D=='P-T' ):
              xlabel= 'Pressure[MPa]'
              ylabel= 'Temperature[C]'
              Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
              Plot_Properties_PT(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     else:
         [title,unit,ylabel, funCalc]=One_Dimensional_plots()
         if PlotAux.varp=='Saturation':
             xlabel= '$\mathbf{S_{w}}$'
             Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
             Plot_Properties_Sw(Plot_frame, title, unit, xlabel, ylabel, funCalc,indx)
         elif PlotAux.varp=='Pressure':
             xlabel= 'Pressure[MPa]'
             Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
             Plot_Properties_Pressure(Plot_frame, title, unit, xlabel, ylabel,funCalc,indx)
         else: 
             Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
             xlabel= 'Temperature[C]'
             Plot_Properties_Temperature(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     RockPhysicModels.PlotName =propS.PlotMod.get()
     
def PlotTL2():
     title=StringVar()      
     ChangeHandler()     
     title=''
 
     indx=1 # might be used for options
     plt.close('all')
     if(IsActiveF.flg2Dplot):
         [title, unit, funCalc]=Two_Dimnesional_plots() 
         if(PlotAux.varp2D=='Sw-Sg' ):
              xlabel= '$\mathbf{S_{w}}$'
              ylabel= '$\mathbf{S_{o}}$'
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Plot_Properties_SwSgTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         else: #(PlotAux.varp2D=='P-T' ):
              xlabel= 'Pressure[MPa]'
              ylabel= 'Temperature[C]'
              Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
              Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
              Plot_Properties_PT_TL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     else:
         [title,unit, ylabel, funCalc]=One_Dimensional_plots()
         if PlotAux.varp=='Saturation':
             xlabel= '$\mathbf{S_{w}}$'
             Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
             Plot_Properties_SwTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         elif PlotAux.varp=='Pressure':
             xlabel= 'Pressure[MPa]'
             Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
             Plot_Properties_PressureTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         else: 
             xlabel= 'Temperature[C]'
             Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
             Plot_Properties_TemperatureTL(Plot_frame, title, unit, xlabel, ylabel, funCalc,indx)
     RockPhysicModels.PlotName =propS.PlotMod.get()     
def PlotTL(event):
     title=StringVar()      
     ChangeHandler()     
     title=''
 
     indx=1 # might be used for options
     plt.close('all')
     if(IsActiveF.flg2Dplot):
         [title, unit, funCalc]=Two_Dimnesional_plots() 
         if(PlotAux.varp2D=='Sw-Sg' ):
              xlabel= '$\mathbf{S_{w}}$'
              ylabel= '$\mathbf{S_{o}}$'
              Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Calculated.sg_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
              Plot_Properties_SwSgTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         else: #(PlotAux.varp2D=='P-T' ):
              xlabel= 'Pressure[MPa]'
              ylabel= 'Temperature[C]'
              Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
              Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
              Plot_Properties_PT_TL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
     else:
         [title,unit, ylabel, funCalc]=One_Dimensional_plots()
         if PlotAux.varp=='Saturation':
             xlabel= '$\mathbf{S_{w}}$'
             Calculated.sw_array=Scalar2ArrayWithRes(0.0, 1.0-Input.soil)
             Plot_Properties_SwTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         elif PlotAux.varp=='Pressure':
             xlabel= 'Pressure[MPa]'
             Calculated.pressure_array=Scalar2ArrayWithRes(Input.pressureMin, Input.pressureMax)
             Plot_Properties_PressureTL(Plot_frame, title, unit,xlabel, ylabel, funCalc,indx)
         else: 
             xlabel= 'Temperature[C]'
             Calculated.temperature_array=Scalar2ArrayWithRes(Input.temperatureMin, Input.temperatureMax)
             Plot_Properties_TemperatureTL(Plot_frame, title, unit, xlabel, ylabel, funCalc,indx)
     RockPhysicModels.PlotName =propS.PlotMod.get()
     
def One_Dimensional_plots():
    global  ylabel, funCalc, unit    
    ylabel= 'y-axis'    
    funCalc= Calculate_Effective_Density

    if propS.PlotMod.get()=="Compressional velocity":
        unit='[m/s]'
        ylabel= '$\mathbf{V_{p}}$ '
        funCalc = Calculate_Effective_Vp
    elif propS.PlotMod.get()=="Compressional impedance":
        unit='[kPa.s/m]'
        ylabel= '$\mathbf{I_{p}}$ '
        funCalc = Calculate_Effective_Ip
    elif propS.PlotMod.get()=="Bulk modulus":
        unit= '[MPa]'
        ylabel= 'Bulk modulus '
        funCalc= Calculate_Effective_Bulkmodulus
    elif propS.PlotMod.get()=="M-Modulus": 
        unit= '[MPa]'
        titleName = 'Compresional modulus'
        ylabel= 'M-Modulus'
        funCalc= Calculate_Effective_Pmodulus   
    elif propS.PlotMod.get()=="Shear velocity":
        unit='[m/s]'
        ylabel= '$\mathbf{V_{s}}$ '
        funCalc= Calculate_Effective_Vs     
    elif propS.PlotMod.get()=="Rpp":
        unit= ''
      #   text=u'kg/m\u00B3' 
      #   u'CO\u2082' subscript
      #   ylabel= r'$\rho$' +unit
        ylabel= 'Rpp ' 
        funCalc= Calculate_Effective_Rpp
    elif propS.PlotMod.get()=="Rps":
        unit= ''#u'[kg/m\u00B3]'
      #   text=u'kg/m\u00B3' 
      #   u'CO\u2082' subscript
      #   ylabel= r'$\rho$' +unit
        ylabel= 'Rps ' 
        funCalc= Calculate_Effective_Rps
    elif propS.PlotMod.get()=="Density":
        unit= u'[kg/m\u00B3]'
      #   text=u'kg/m\u00B3' 
      #   u'CO\u2082' subscript
      #   ylabel= r'$\rho$' +unit
        ylabel= 'Density ' 
        funCalc= Calculate_Effective_Density
        
    elif propS.PlotMod.get()=="Conductivity":
        unit= '[S/m]'
        ylabel= 'Conductivity '
        funCalc= Calculate_Effective_Conductivity    
    elif propS.PlotMod.get()=="Resistivity":
        # xlabel= '$\mathbf{S_{w}}$'
        unit= '[$\Omega$.m]'
        ylabel= 'Resistivity '
        funCalc= Calculate_Effective_Resistivity
    elif propS.PlotMod.get()=="Nuclear":
        unit= '[c.u]'
        ylabel= 'Neutron Capture '
        funCalc= Calculate_Effective_neutron_sigma
    else:
        unit= ''
        titleName = ''
 
    titleName=ylabel
    return titleName,unit,ylabel, funCalc
    
def Two_Dimnesional_plots(): 
    funCalc= Calculate_Effective_Density
    if propS.PlotMod.get()=="Compressional velocity":
        titleName = '$V_p$'
        unit='[m/s]'
        funCalc = Calculate_Effective_Vp
    elif propS.PlotMod.get()=="Compressional impedance": 
        titleName = '$I_p$'
        unit='[kPa.s/m]'
        funCalc = Calculate_Effective_Ip
    elif propS.PlotMod.get()=="Bulk modulus":
        titleName = 'Bulk modulus'
        unit= '[MPa]'
        funCalc= Calculate_Effective_Bulkmodulus
    elif propS.PlotMod.get()=="Shear velocity":
        titleName = '$V_s$'
        unit='[m/s]'
        funCalc= Calculate_Effective_Vs     
    elif propS.PlotMod.get()=="Density": 
        titleName = 'Density'
        unit= u'[kg/m\u00B3]'
      #   text=u'kg/m\u00B3' 
      #   u'CO\u2082' subscript
        funCalc= Calculate_Effective_Density
    elif propS.PlotMod.get()=="M-Modulus": 
        unit= '[MPa]'
        titleName = 'Compresional modulus'
        funCalc= Calculate_Effective_Pmodulus
    elif propS.PlotMod.get()=="Rpp": 
        titleName = 'Rpp'
        unit= ''
        funCalc= Calculate_Effective_Rpp  
    elif propS.PlotMod.get()=="Rps": 
        titleName = 'Rps'
        unit= ''
        funCalc= Calculate_Effective_Rps  
    elif propS.PlotMod.get()=="Conductivity":
        unit= '[S/m]'
        titleName = 'Conductivity'
        funCalc= Calculate_Effective_Conductivity
    elif propS.PlotMod.get()=="Resistivity":
        titleName = 'Resistivity'
        unit= '[$\Omega$.m]'
        funCalc= Calculate_Effective_Resistivity
    elif propS.PlotMod.get()=="Nuclear": 
        unit= '[c.u]'
        titleName = 'Neutron capture'
        funCalc= Calculate_Effective_neutron_sigma
    else:
         unit=''
         
    return titleName, unit, funCalc
         
def checkbutton_value():
#    global CO2Dissolution
    if(propS.CO2Flag.get()=="hcgas"):
       propS.CO2Dissolution.set(False)

def RockFrameModel(event):  

     cspan=1
     cspan2=5
# Inclusion frame 
     Aratio_label1=Label(aratio_frame,text="Inclusion 1: Aspect ratio ")
     Aratio_entry1= Entry(aratio_frame,textvar=propS.aratio1,width=6, justify='center')
     Aratio_label1.grid(column=0,row=0,columnspan=cspan,padx=4,pady=2,sticky='NE')
     Aratio_entry1.grid(column=1,row=0,columnspan=cspan ,padx=4,pady=2,sticky='NE')
     
     Aratio_label2=Label(aratio_frame,text="Inclusion 2: Aspect ratio ")
     Aratio_entry2= Entry(aratio_frame,textvar=propS.aratio2,width=6, justify='center')
     Aratio_label2.grid(column=0,row=1,columnspan=cspan,padx=4,pady=2,sticky='NE')
     Aratio_entry2.grid(column=1,row=1,columnspan=cspan,padx=4,pady=2,sticky='NE')
     
     volfrac1=  u'X\u2081'
     volfrac2=  u'X\u2082'
     
#     volfrac_label1 = ttk.Label(text="HC or "+ u'CO\u2082', style="Bold.TLabel")

     volfrac_label1=Label(aratio_frame,text=volfrac1)     
     volfrac_entry1= Entry(aratio_frame,textvar=propS.volfrac1,width=6, justify='center')
     volfrac_label1.grid(column=2,row=0,columnspan=cspan,padx=4,pady=2,sticky='NE')
     volfrac_entry1.grid(column=3,row=0,columnspan=cspan,padx=4,pady=2,sticky='NE')

     volfrac_label2=Label(aratio_frame,text=volfrac2)     
#     volfrac_label2=Label(aratio_frame,text="Vol fraction ")
     volfrac_entry2= Entry(aratio_frame,textvar=propS.volfrac2,width=6, justify='center')
     volfrac_label2.grid(column=2,row=1,columnspan=cspan,padx=4,pady=2,sticky='NE')
     volfrac_entry2.grid(column=3,row=1,columnspan=cspan,padx=4,pady=2,sticky='NE')
     
     K_inclusion_label1=Label(aratio_frame,text="Kinc [MPa]")
     K_inclusion_entry1= Entry(aratio_frame,textvar=propS.K_inclusion1,width=6, justify='center')
     K_inclusion_label1.grid(column=4,row=0,columnspan=cspan,padx=6,pady=2,sticky='NE')
     K_inclusion_entry1.grid(column=5,row=0,columnspan=cspan,padx=6,pady=2,sticky='NE')
     
     K_inclusion_label2=Label(aratio_frame,text="Kinc[MPa]")
     K_inclusion_entry2= Entry(aratio_frame,textvar=propS.K_inclusion2,width=6, justify='center')
     K_inclusion_label2.grid(column=4,row=1,columnspan=cspan,padx=6,pady=2,sticky='NE')
     K_inclusion_entry2.grid(column=5,row=1,columnspan=cspan,padx=6,pady=2,sticky='NE')
     
     aratio_frame.grid(column=0,row=2,padx=2,columnspan=cspan2, pady=2,sticky='NE')     
# HS frame for Hashin Shtrikman and Voight-Reuss bounds    
     HS_frame.grid(column=0,row=2,padx=2,columnspan=5, pady=2,sticky='NE')    
 
     """To Update Options when the Screen is Activated"""
     if propS.RockFrameMod.get() == 'User input':
         HS_frame.grid_forget()
         aratio_frame.grid_forget()
         print("Calculating Dry with no inclusion")         
     elif propS.RockFrameMod.get() == 'DEM':
         HS_frame.grid_forget()
         aratio_frame.grid(column=0,row=2,columnspan=cspan2,padx=2,pady=2,sticky='NE')
         print("Calculating Dry Properties using DEM")
     elif propS.RockFrameMod.get() == 'Self-consistent':
         HS_frame.grid_forget()
         aratio_frame.grid(column=0,row=2,columnspan=cspan2,padx=2,pady=2,sticky='NE')
         print("Calculating Dry Properties using self-consistent")    
     elif propS.RockFrameMod.get() == 'Kuster-Toksoz':
         HS_frame.grid_forget()
         aratio_frame.grid(column=0,row=2,columnspan=cspan2,padx=2,pady=2,sticky='NE')
         print("Calculating Dry Properties using Kuster-Toksoz")
     elif ((propS.RockFrameMod.get() == 'HS+') or (propS.RockFrameMod.get() == 'HS-') or   \
         propS.RockFrameMod.get() =='Voigt' or propS.RockFrameMod.get() == 'Reuss' or \
         propS.RockFrameMod.get() == 'HSAve' or propS.RockFrameMod.get() == 'Voigt-Reuss'):
         aratio_frame.grid_forget()
         weight_frac_entry= Entry(HS_frame,textvar=propS.Ave_weight_frac,width=5, justify='center')
         weight_frac_entry.grid(column=0,row=2,padx=2,columnspan=15, pady=2,sticky='W')   
         weight_frac_entry.configure(state='disabled') 
         Label_ave=Label(HS_frame,text="Av.Weight Fraction")
         Label_ave.grid(column=0,row=1,padx=2,columnspan=15, pady=2,sticky='W')
         
         if (not IsActiveF.Hs_pls):
             IsActiveF.Hs_pls= True
             matr=CreateTable(HS_frame)#.grid(column=0,row=2,columnspan=cspan2,padx=2,pady=2,sticky='NE')   
             matr.grid(column=0,row=0,padx=2,pady=2,sticky='NE')
             weight_frac_entry.configure(state='disabled') 
         if(propS.RockFrameMod.get() == 'HSAve' or propS.RockFrameMod.get() == 'Voigt-Reuss'):
             Label_ave.grid(column=0,row=1,padx=2,columnspan=15, pady=2,sticky='E')
             weight_frac_entry.configure(state='normal')      
       
        
         HS_frame.grid(column=0,row=2,padx=2,columnspan=5, pady=2,sticky='NE')    
         print("Calculating Dry Properties using", propS.RockFrameMod.get())
 
     RockPhysicModels.RockFrameModelName = propS.RockFrameMod.get() 
#######################
def DryRockModel(event):
     vugfrac_label=Label(vug_frame,text="Fraction of vug ")
     vugfrac_entry= Entry(vug_frame,textvar=propS.vugfraction,width=8, justify='center')
     vugfrac_label.grid(column=0,row=0,padx=20,pady=2,sticky='NE')
     vugfrac_entry.grid(column=1,row=0,padx=20,pady=2,sticky='NE')
     vug_frame.grid(column=0,row=2,padx=2,pady=2,sticky='W')
     
     Krief_label=Label(Krief_frame,text="Krief exponent ")
     Krief_entry= Entry(Krief_frame,textvar=propS.KriefExponent,width=8, justify='center')
     Krief_label.grid(column=0,row=0,padx=20,pady=2,sticky='E')
     Krief_entry.grid(column=1,row=0,padx=20,pady=2,sticky='E')
     Krief_frame.grid(column=0,row=2,padx=2,pady=2,sticky='W')

     UInput_Kdry_label=Label(UInput_Dryframe,text="Kdry[GPa] ")
     UInput_Kdry_entry= Entry(UInput_Dryframe,textvar=propS.Kdry,width=8, justify='center')
     UInput_Gdry_label=Label(UInput_Dryframe,text="Gdry[GPa] ")
     UInput_Gdry_entry= Entry(UInput_Dryframe,textvar=propS.Gdry,width=8, justify='center')
     UInput_Kdry_label.grid(column=0,row=0,padx=5,pady=2,sticky='NE')
     UInput_Kdry_entry.grid(column=1,row=0,padx=5,pady=2,sticky='NE')
     UInput_Gdry_label.grid(column=2,row=0,padx=5,pady=2,sticky='NE')
     UInput_Gdry_entry.grid(column=3,row=0,padx=5,pady=2,sticky='NE')
     UInput_Dryframe.grid(column=0,row=2,padx=2,pady=2,sticky='W')

     confP_label=Label(ContactCement_frame,text="Conf pressure[MPa] ")
     confP_entry= Entry(ContactCement_frame,textvar=propS.confining_pressure,width=8, justify='center')
     confP_label.grid(column=0,row=0,padx=10,pady=2,sticky='NE')
     confP_entry.grid(column=1,row=0,padx=10,pady=2,sticky='NE')
     effPresCoef_label=Label(ContactCement_frame,text="Biot coeff(N) ")
     effPresCoef_entry= Entry(ContactCement_frame,textvar=propS.poisson_ratio,width=8, justify='center')
     effPresCoef_label.grid(column=2,row=0,padx=10,pady=2,sticky='NE')
     effPresCoef_entry.grid(column=3,row=0,padx=10,pady=2,sticky='NE')      
     
     KCement_label=Label(ContactCement_frame,text="K cement[GPa] ")
     KCement_entry= Entry(ContactCement_frame,textvar=propS.KCement,width=8, justify='center')
     KCement_label.grid(column=0,row=1,padx=10,pady=2,sticky='NE')
     KCement_entry.grid(column=1,row=1,padx=10,pady=2,sticky='NE')      
     
     GCement_label=Label(ContactCement_frame,text="G cement[GPa ")
     GCement_entry= Entry(ContactCement_frame,textvar=propS.GCement,width=8, justify='center')
     GCement_label.grid(column=2,row=1,padx=10,pady=2,sticky='NE')
     GCement_entry.grid(column=3,row=1,padx=10,pady=2,sticky='NE')    
     
#     KClay_label=Label(ContactCement_frame,text="K Clay[GPa] ")
#     KClay_entry= Entry(ContactCement_frame,textvar=propS.KClay,width=8, justify='center')
#     KClay_label.grid(column=0,row=2,padx=10,pady=2,sticky='NE')
#     KClay_entry.grid(column=1,row=2,padx=10,pady=2,sticky='NE')      
#     GClay_label=Label(ContactCement_frame,text="G Clay[GPa] ")
#     GClay_entry= Entry(ContactCement_frame,textvar=propS.GClay,width=8, justify='center')
#     GClay_label.grid(column=2,row=2,padx=10,pady=2,sticky='NE')
#     GClay_entry.grid(column=3,row=2,padx=10,pady=2,sticky='NE')    
     
     Cement_Patchiness_label=Label(ContactCement_frame,text="Cement patchiness ")
     Cement_Patchiness_entry= Entry(ContactCement_frame,textvar=propS.CementPatchiness,width=8, justify='center')
     Cement_Patchiness_label.grid(column=0,row=3,padx=10,pady=2,sticky='NE')
     Cement_Patchiness_entry.grid(column=1,row=3,padx=10,pady=2,sticky='NE')  
     
     CementSat_label=Label(ContactCement_frame,text="Cement saturation ")
     CementSat_entry= Entry(ContactCement_frame,textvar=propS.CementSat,width=8, justify='center')
     CementSat_label.grid(column=2,row=3,padx=10,pady=2,sticky='NE')
     CementSat_entry.grid(column=3,row=3,padx=10,pady=2,sticky='NE')      
     
     coord_number_label=Label(ContactCement_frame,text="Coord # ")
     coord_number_entry= Entry(ContactCement_frame,textvar=propS.coord_number,width=8, justify='center')
     coord_number_label.grid(column=0,row=4,padx=10,pady=2,sticky='NE')
     coord_number_entry.grid(column=1,row=4,padx=10,pady=2,sticky='NE')      
     ContactCement_frame.grid(column=0,row=2,padx=2,pady=2,sticky='W')
     
#     HertzMindlin_frame
     confP_labelHM=Label(HertzMindlin_frame,text="Conf pressure[MPa] ")
     confP_entryHM= Entry(HertzMindlin_frame,textvar=propS.confining_pressure,width=8, justify='center')
     confP_labelHM.grid(column=0,row=0,padx=10,pady=2,sticky='NE')
     confP_entryHM.grid(column=1,row=0,padx=10,pady=2,sticky='NE')
     effPresCoef_labelHM=Label(HertzMindlin_frame,text="Biot coeff(N) ")
     effPresCoef_entryHM= Entry(HertzMindlin_frame,textvar=propS.poisson_ratio,width=8, justify='center')
     effPresCoef_labelHM.grid(column=2,row=0,padx=10,pady=2,sticky='NE')
     effPresCoef_entryHM.grid(column=3,row=0,padx=10,pady=2,sticky='NE')      
     coord_number_labelHM=Label(HertzMindlin_frame,text="Coord # ")
     coord_number_entryHM= Entry(HertzMindlin_frame,textvar=propS.coord_number,width=8, justify='center')
     coord_number_labelHM.grid(column=0,row=4,padx=10,pady=2,sticky='NE')
     coord_number_entryHM.grid(column=1,row=4,padx=10,pady=2,sticky='NE')      
     HertzMindlin_frame.grid(column=0,row=2,padx=2,pady=2,sticky='W')

     dryMod= propS.DryMod.get()
#     ConPModCombo.config(state='normal')
     if dryMod == 'Forward carbonate advisor':
         Krief_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         ContactCement_frame.grid_forget()
         HertzMindlin_frame.grid_forget()
         vug_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')
         print("Calculating Dry Properties using Forward carbonate advisor")
     elif (dryMod == 'Hertz-Mindlin'):
         vug_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         ContactCement_frame.grid_forget()
         Krief_frame.grid_forget()
         HertzMindlin_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')
         print("Calculating Dry Properties using Hertz-Mindlin")
     elif (dryMod == 'Hertz-Mindlin with HS-'):
         vug_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         ContactCement_frame.grid_forget()
         Krief_frame.grid_forget()
         HertzMindlin_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')
         print("Calculating Dry Properties using Hertz-Mindlin with HS-")
     elif (dryMod == 'Krief'):
         vug_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         ContactCement_frame.grid_forget()
         HertzMindlin_frame.grid_forget()
         Krief_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')
         print("Calculating Dry Properties using Krief")
     elif (dryMod == 'Contact cement'):
         vug_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         Krief_frame.grid_forget()
         HertzMindlin_frame.grid_forget()
#         if(propS.DryMod.get()=='Contact Cement'):
#             ConPModCombo.config(state='disable')             
         ContactCement_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NW') 
     elif (dryMod == 'User input'):
         ContactCement_frame.grid_forget()
         vug_frame.grid_forget()
         Krief_frame.grid_forget()
         HertzMindlin_frame.grid_forget()
         UInput_Dryframe.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NW')
         print("Enter Dry Properties")
     else:
         Krief_frame.grid_forget()
         vug_frame.grid_forget()
         UInput_Dryframe.grid_forget()
         ContactCement_frame.grid_forget()
         HertzMindlin_frame.grid_forget()
   
     RockPhysicModels.DryRockModelName = dryMod
#######################
def ConfPresModel(event):
#     global ConPModCombo
#     if(propS.DryMod.get()=='Contact cement'):
#         ConPModCombo.state('disable')
#         return
     if (propS.ConfMod.get()=="Hertz-Mindlin with HS-" or propS.ConfMod.get() == 'Hertz-Mindlin'):
         confP_label1=Label(ConfP_frameHM,text="Conf pressure[MPa] ")
         confP_entry1= Entry(ConfP_frameHM,textvar=propS.confining_pressure,width=8, justify='center')
         confP_label1.grid(column=0,row=0,padx=2,pady=2,sticky='NE')
         confP_entry1.grid(column=1,row=0,padx=2,pady=2,sticky='NE')
     
         coord_number_label=Label(ConfP_frameHM,text="Coord # ")
         coord_number_entry= Entry(ConfP_frameHM,textvar=propS.coord_number,width=8, justify='center')
         coord_number_label.grid(column=2,row=0,padx=2,pady=2,sticky='NE')
         coord_number_entry.grid(column=3,row=0,padx=2,pady=2,sticky='NE')
                  
         effPresCoef_label=Label(ConfP_frameHM,text="Biot coeff(N) ")
         effPresCoef_entry= Entry(ConfP_frameHM,textvar=propS.poisson_ratio,width=8, justify='center')
         effPresCoef_label.grid(column=0,row=1,padx=1,pady=1,sticky='NE')
         effPresCoef_entry.grid(column=1,row=1,padx=2,pady=2,sticky='NE')
         ConfP_frameHM.grid_forget()
         ConfP_frameLinear.grid_forget()
         ConfP_frameMacBeth.grid_forget()
         ConfP_frameContactCement.grid_forget()

         ConfP_frameHM.grid(column=0,row=1,padx=2,columnspan=7, pady=2,sticky='W')  
         
     elif(propS.ConfMod.get() == 'Linear'):
         ConfP_frameLinear.grid_forget()
         ConfP_frameHM.grid_forget()
         ConfP_frameMacBeth.grid_forget()
         ConfP_frameContactCement.grid_forget()

         
         confP_label1=Label(ConfP_frameLinear,text="Conf pressure[MPa] ")
         confP_entry1= Entry(ConfP_frameLinear,textvar=propS.confining_pressure,width=8, justify='center')
         confP_label1.grid(column=0,row=0,padx=10,pady=2,sticky='NE')
         confP_entry1.grid(column=1,row=0,padx=10,pady=2,sticky='NE')
         
         effPresCoef_label=Label(ConfP_frameLinear,text="Biot coeff(N) ")
         effPresCoef_entry= Entry(ConfP_frameLinear,textvar=propS.poisson_ratio,width=8, justify='center')
         effPresCoef_label.grid(column=2,row=0,padx=10,pady=2,sticky='NE')
         effPresCoef_entry.grid(column=3,row=0,padx=10,pady=2,sticky='NE')
     
         CoefAK_label=Label(ConfP_frameLinear,text="Coef Ak ")
         CoefAK_entry= Entry(ConfP_frameLinear,textvar=propS.Linear_CoefAK,width=8, justify='center')
         CoefAK_label.grid(column=2,row=1,padx=10,pady=2,sticky='NE')
         CoefAK_entry.grid(column=3,row=1,padx=10,pady=2,sticky='NE')
         
         CoefAG_label=Label(ConfP_frameLinear,text="Coef B  ")
         CoefAG_entry= Entry(ConfP_frameLinear,textvar=propS.Linear_CoefAG,width=8, justify='center')
         CoefAG_label.grid(column=0,row=1,padx=10,pady=2,sticky='NE')
         CoefAG_entry.grid(column=1,row=1,padx=10,pady=2,sticky='NE')
         
         ConfP_frameLinear.grid(column=0,row=2,padx=2,columnspan=5, pady=2,sticky='W')  
         
     elif propS.ConfMod.get() == 'MacBeth':
         ConfP_frameLinear.grid_forget()
         ConfP_frameHM.grid_forget()
         ConfP_frameContactCement.grid_forget()

              
         confP_label1=Label(ConfP_frameMacBeth,text="Conf pressure[MPa] ")
         confP_entry1= Entry(ConfP_frameMacBeth,textvar=propS.confining_pressure,width=8, justify='center')
         confP_label1.grid(column=0,row=0,padx=10,pady=2,sticky='NE')
         confP_entry1.grid(column=1,row=0,padx=10,pady=2,sticky='NE')
         
         effPresCoef_label=Label(ConfP_frameMacBeth,text="Biot coeff(N) ")
         effPresCoef_entry= Entry(ConfP_frameMacBeth,textvar=propS.poisson_ratio,width=8, justify='center')
         effPresCoef_label.grid(column=2,row=0,padx=10,pady=2,sticky='NE')
         effPresCoef_entry.grid(column=3,row=0,padx=10,pady=2,sticky='NE')
     
         CoefPK_label=Label(ConfP_frameMacBeth,text="Coef Pk ")
         CoefPK_entry= Entry(ConfP_frameMacBeth,textvar=propS.MacBeth_Pk,width=8, justify='center')
         CoefPK_label.grid(column=2,row=1,padx=10,pady=2,sticky='NE')
         CoefPK_entry.grid(column=3,row=1,padx=10,pady=2,sticky='NE')
         
         CoefEk_label=Label(ConfP_frameMacBeth,text="Coef Ek  ")
         CoefEk_entry= Entry(ConfP_frameMacBeth,textvar=propS.MacBeth_Ek,width=8, justify='center')
         CoefEk_label.grid(column=0,row=1,padx=10,pady=2,sticky='NE')
         CoefEk_entry.grid(column=1,row=1,padx=10,pady=2,sticky='NE')
         
         CoefPg_label=Label(ConfP_frameMacBeth,text="Coef Pg ")
         CoefPg_entry= Entry(ConfP_frameMacBeth,textvar=propS.MacBeth_Pg,width=8, justify='center')
         CoefPg_label.grid(column=2,row=2,padx=10,pady=2,sticky='NE')
         CoefPg_entry.grid(column=3,row=2,padx=10,pady=2,sticky='NE')
         
         CoefEg_label=Label(ConfP_frameMacBeth,text="Coef Eg  ")
         CoefEg_entry= Entry(ConfP_frameMacBeth,textvar=propS.MacBeth_Eg,width=8, justify='center')
         CoefEg_label.grid(column=0,row=2,padx=10,pady=2,sticky='NE')
         CoefEg_entry.grid(column=1,row=2,padx=10,pady=2,sticky='NE')
         
         
         ConfP_frameMacBeth.grid(column=0,row=2,padx=2,columnspan=5, pady=2,sticky='NW')  
         
     elif propS.ConfMod.get() == 'No pressure effect':
         ConfP_frameLinear.grid_forget()
         ConfP_frameHM.grid_forget()
         ConfP_frameMacBeth.grid_forget()
         ConfP_frameContactCement.grid_forget()

       
     RockPhysicModels.ConfiningPModelName =propS.ConfMod.get()

#######################
def ClickKbOff(flgForClick):
    if(flgForClick):
        chk_KbE.config(state='normal')
    else:
        propS.flgKbE.set(False)
        chk_KbE.config(state='disable')

def FSMName(event):     
    
     DeltaN1_label=Label(FSMGassmannHTI_frame,text="Delta N1 ")
     DeltaN1_entry= Entry(FSMGassmannHTI_frame,textvar=propS.deltaN1,width=8, justify='center')
     DeltaN1_label.grid(column=0,row=0,padx=20,pady=2,sticky='NE')
     DeltaN1_entry.grid(column=1,row=0,padx=20,pady=2,sticky='NE')

     DeltaN2_label=Label(FSMGassmannHTI_frame,text="Delta N2 ")
     DeltaN2_entry= Entry(FSMGassmannHTI_frame,textvar=propS.deltaN2,width=8, justify='center')
     DeltaN2_label.grid(column=2,row=0,padx=20,pady=2,sticky='NE')
     DeltaN2_entry.grid(column=3,row=0,padx=20,pady=2,sticky='NE')

     FSMGassmannHTI_frame.grid(column=0,row=2,padx=2,pady=2,sticky='W')
     
     flgClickKb=BooleanVar()
     flgClickKb.set(True)
     FSName =propS.FSMMod.get()
     """To Update Options when the Screen is Activated"""
     if FSName == RockPhysicModels.FSM_GassmannModel: #'Gassmann Model':
         FSMGassmannHTI_frame.grid_forget()
         print("Calculating Effective Props using Gassmann")
     elif FSName == RockPhysicModels.FSM_PatcyModel: #'Patchy Saturation Model':
         FSMGassmannHTI_frame.grid_forget()
         print("Calculating Effective Props using Patchy")
     else:
         flgClickKb.set(False)
         FSMGassmannHTI_frame.grid(column=0,row=1,padx=2,columnspan=5, pady=2,sticky='NE')        
         if (FSName == RockPhysicModels.FSM_HTI_0_PC11_SshC44 or FSName==RockPhysicModels.FSM_HTI_0_PC11_SsvC66 or FSName==RockPhysicModels.FSM_HTI_0_PC33_SC44 ):
             DeltaN2_entry.config(state='disable')
         else:
             DeltaN2_entry.config(state='normal')
             
     RockPhysicModels.FSMName =FSName
     ClickKbOff(flgClickKb.get())
     
     ####################### Full Zoeppritz','Aki&Richards', 'Shuey', 'Castagna'
def RefCoefName(event):
     """To Update Options when the Screen is Activated"""
     if propS.ReflectionCoefMod.get() == 'Full Zoeppritz':
         print("Calculating reflection ceefcients using Full Zoeppritz")
     elif propS.ReflectionCoefMod.get() == 'Aki&Richards':
         print("Calculating reflection coefcients using Aki&Richards")
     else: #normal incidence:
         print("Calculating reflection ocefcients using Normal incidence")
         
     RockPhysicModels.RefCoefName =propS.ReflectionCoefMod.get()
     
def EMModelName(EM_input_frame,entry):
    EM_input_frame.grid_forget()
    """To Update Options when the Screen is Activated"""
    if propS.EMMod.get() == 'Archie':
     entry.configure(state='disabled')
     EM_input_frame.grid(column=0,row=1,padx=1,pady=2,sticky='W',columnspan=20)
     print("Calculating conductivity using Archie")
    elif propS.EMMod.get() == 'Waxman-Smits':
     print("Calculating conductivity using WM")
     EM_input_frame.grid(column=0,row=1,padx=1,pady=2,sticky='W',columnspan=20)
     entry.configure(state='normal')
    elif propS.EMMod.get() == 'none':
     entry.configure(state='normal')
     EM_input_frame.grid_forget()
    RockPhysicModels.EMModelName = propS.EMMod.get() 
     
############################################################################
# Use for addign buttons on the input tab
def Draw_Command_Pane(rt,output_frame,fr):
  """To Generate the Content for the Command & Buttons Frame"""
  status = StringVar(value="""Designed by: Bilgin Altundas (baltundas@slb.com )
Schlumberger-Doll Research""")
  Label(fr,text="***",textvariable=status)\
        .grid(column=2,row=1,rowspan=8,padx=40,pady=2,sticky='NEWS')
  
  Button(fr,text='Apply',  font=("TkDefaultFont", 10,"bold"),width=10, command=UpdateInput )\
          .grid(column=20,row=0,padx=40,pady=0,sticky='NS')
  
  Button(fr,text="Calculate", font=("TkDefaultFont", 10,"bold"),width=10,command=lambda: Calculate(output_frame))\
                        .grid(column=30,row=0,padx=20,pady=2,)  
  Button(fr,text=" Close ",font=("TkDefaultFont", 10,"bold"),width=10,command=lambda:rt.destroy())\
                        .grid(column=40,row=0,padx=20,pady=2)
  
##########################################################################
class InputRow():
    def __init__(self, fr, inputname, inputval, unit,var, rowindx, colindx):
        """ Class used for geenrating input entri GUI"""
        self.entryval=StringVar(value=str(inputval))
        self.label=Label(fr,text=inputname, justify='right')
        self.entry= Entry(fr,textvar=self.entryval ,width=8, justify='center')
        self.unit=Label(fr,text=unit)
        self.button=  Radiobutton(fr, variable=var,value=inputname, command= isActive)
        self.label.grid(column=colindx,row=rowindx,padx=2,pady=2,sticky='NE')
        self.entry.grid(column=colindx+1,row=rowindx,columnspan=2,padx=2,pady=2,sticky='NWE')
        self.unit.grid(column=colindx+3,row=rowindx,padx=2,pady=2,sticky='NE')
        self.button.grid(column=colindx+4,row=rowindx,padx=2,pady=2,sticky='NE')   
        
    def getInputRowValue(self):
        return self.entryval
    def setInputRowValue(self, value):
        self.entryval=value
#### Not working
class MakeSlider():
    def __init__(self, sliderFrame, sliderlabel,var, propval):
        """ Class used for geenrating entri for slider GUI"""
        self.slider = Scale(sliderFrame, label=var,from_=0, to=1, length=150,width=15,tickinterval=1,
               orient=HORIZONTAL, relief=SUNKEN, bd=1,
               sliderrelief=RAISED, resolution=0.25)
        self.frame=sliderFrame
        self.slider.config(command =  self.updateSliderValue2())  
        self.entry=Entry(sliderFrame,textvar=propval,width=8, justify='center')
        self.slider.grid(column=7,row=3,columnspan=1,rowspan=5, padx=2,pady=2,sticky='NWE')
        self.entry.grid(row=3,column=8,padx=2,pady=2)
        
    def updateSliderValue2(self):
        print('slideru',self.slider.get())
        self.entry=Entry(self.frame,textvar=self.slider.get(),width=8, justify='center')
        print('slideru',self.slider.get())

################### Main ################
# -*- coding: utf-8 -*-
""" 
#Created on Thu Nov 10 15:00:15 2016
#@author: BAltundas
"""

def savefile():
    fout = asksaveasfile(mode='w', defaultextension=".txt")
    save_project(fout)
    print("Input parameters are saved")
    fout.close()
def exitfile():
    root.destroy()
def openproject():
    fin = askopenfile(mode='r')
    Restart_project(fin)   
def helpmenu():
    filename="Quick Look Screening User Guide.pdf"
    try:
        os.startfile(filename)
    except (OSError, IOError):
        tkMessageBox.showinfo("File not found", filename)    
def aboutmenu():
    txt=[ 'Grid-free quick look fluid monitoring screening tool for ranking',
     ' and decision making for selecting the most suitable fluid monitoring processes.',
          u'\u00A9'+' Schlumberger']
    tkMessageBox.showinfo('About QL', "\n".join(txt))

def contact():
#    r = Tkinter.Tk()
#    r.option_add('*font', 'Helvetica -12')
    tkMessageBox.showinfo('Contact','Bilgin Altundas (baltundas@slb.com), Schlumberger')
#    r.option_clear() 
def PythonOrg():
    webbrowser.open_new('https://www.python.org/')    

def pythonManual():
    webbrowser.open_new('https://docs.python.org/2/library/index.html')    
def TkinterManual():
    webbrowser.open_new('http://nullege.com/codes/search/Tkinter') 
############################################################################
#EXPORT>
############################################################################
__author__ = "Bilgin Altundas(baltundas@slb.com)"
__author_email__="baltundas@slb.com"
__version__ = "1.0"
############################################################################
_debug_message = 1
############################################################################
# Main FUNCTION>
############################################################################
#if __name__ == "__main__" :
if __name__.endswith('__main__'):
  global meta       
  meta = {}
  
  print(__doc__) 
  ## Create Main Window
  root=Tkinter.Tk()
      
  iconfilename= 'QL_icon.ico'
  try:
      root.wm_iconbitmap(iconfilename)
  except Tkinter.TclError:
      tkMessageBox.showinfo("File not found",iconfilename)
  blank_space =" "
  
  root.title(80*blank_space+"Quick-Look Fluid Monitoring Screening Tool v"+__version__+'     '+u'\u00A9'+" Schlumberger")  
  root.bind("<Escape>",lambda e:root.destroy())# hit escape to close the GUI
  root["padx"]=10
  root["pady"]=10 
  menU=Tkinter.Menu(root)
  root.config(menu=menU)
  subMenu=Tkinter.Menu(menU)
  menU.add_cascade(label="File", menu=subMenu)
  subMenu.add_command(label="Open project..", command=openproject)
  subMenu.add_command(label="Save project..", command=savefile)
  subMenu.add_separator()
  subMenu.add_command(label="Exit..", command=exitfile)
  aboutMenu=Tkinter.Menu(menU)
  menU.add_cascade(label="About", menu=aboutMenu)
  aboutMenu.add_command(label="About", command=aboutmenu)
  aboutMenu.add_command(label="User guide", command=helpmenu)
  aboutMenu.add_command(label="Contact", command=contact)

#  aboutMenu.add_command(label="Tkinter help", command=TkinterManual)
#  aboutMenu.add_command(label="Python help", command=PythonOrg)
#  { MAIN CONTENT BEGIN
  content = Tkinter.Frame(root,width=300,height=200,borderwidth=0.5,relief="groove")
  note = Notebook(content,padding=1)
# Draw_Input_Pane

  Input_Frame = Tkinter.Frame(note,width=200,height=200,borderwidth=3,\
                    relief="ridge",padx=5,pady=2)
  Draw_Input_Pane(Input_Frame)
  Input_Frame.grid(column=0,row=0,rowspan=2,padx=5,pady=5)
  note.add(Input_Frame,text="Input       ",padding=2)
  note.grid(column=0,row=0,rowspan=2,padx=5,pady=5)
#  Draw_Rockphysics_Pane
  Rockphysics_Frame = Tkinter.Frame(content,width=200,height=200,borderwidth=3,\
                    relief="ridge",padx=5,pady=1)
  Draw_Rockphysics_Pane(Rockphysics_Frame)
  Rockphysics_Frame.grid(column=1,row=0,padx=5,pady=5,sticky='NWES')
  note.add(Rockphysics_Frame,text="Rock Physics",padding=1) 
# Output_Frame
  Output_Frame = Tkinter.Frame(content,width=200,height=200,borderwidth=3,\
                    relief="ridge",padx=5,pady=2)
  Draw_Output_Pane(Output_Frame)
  Output_Frame.grid(column=1,row=1,padx=5,pady=5,sticky='NWES')
  note.add(Output_Frame,text="Output      ",padding=5) 
# Command_Frame
  Command_Frame = Tkinter.Frame(content,padx=2,pady=2)
  Draw_Command_Pane(root,Output_Frame,Command_Frame)
  Command_Frame.grid(column=0,row=2,columnspan=2,padx=5,pady=5,sticky='NWES')
  content.grid(column=0,row=0,sticky='NSEW')
  root.mainloop()