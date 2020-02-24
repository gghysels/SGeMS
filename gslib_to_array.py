# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:28:00 2020

@author: gghysels

version 0.1.0
"""

import numpy as np
import matplotlib.pyplot as plt 

def gslib_to_array(filename, savetxt=False, fmt='%.2f', plot=False):
    
    """Convert 3D properties exported from SGeMS in .gslib format to arrays.

    Parameters
    ----------
    filename : str
        File path of the .gslib file
    savetxt : boolean, optional
        Flag to save arrays in a .txt file (seperate file for each layer). The default is False.
    fmt : str, optional
        Format for the values in the arrays. The default is '%.2f'.
    plot : boolean, optional
        Flag to plot the arrays. The default is False.

    Returns
    -------
    array : numpy.ndarray
        Array (4D) containing the layers times rows times cols array for each property.
        
    """
    
    with open(filename) as f:
        grid = f.readline() #read in name and dimensions of the grid
        grid_dim = grid.split(' ')[1][1:-2] #extract the amount of rows, columns and layers
        rows, cols, layers = [int(dim) for dim in grid_dim.split('x')]
        
        n = int(f.readline()) #read in the amount of properties in the gslib file
        
        properties = [] #list in which the names of all properties in the gslib file will be stored
        for p in range(n): #read next n lines and store n property names in a list
            properties.append(f.readline()[:-1])
            
        data = [[] for x in range(n)] #list for each property
        for line in f: #fill in list with data for each property
            l = line.split(' ')[:-1]
            for r in range(0,len(l)):
                data[r].append(l[r])
    
    array = np.zeros((n, layers, rows, cols)) #create empty array
    for p in range(n):
        for l in range(layers):
            l_data = data[p][l*rows*cols:(l+1)*rows*cols] #select data for specific layer
            for i in range(rows): #fill in array with value from data list
                for j in range(cols):
                    array[p][l][i][j] = l_data[(rows*cols)-cols*(i+1)+j]
            
    #save array to textfile
    if savetxt == True:
        for p in range(n):
            for l in range(layers):
                np.savetxt(properties[p]+'_l'+str(l+1)+'.txt', array[p][l], fmt=fmt)
    
    #plot array
    if plot == True:
        for p in range(n):
            for l in range(layers):
                fig, ax = plt.subplots()
                img = ax.imshow(array[p][l])
                plt.colorbar(img)  
                ax.set_title(properties[p]+'_l'+str(l+1))
        
    return array 