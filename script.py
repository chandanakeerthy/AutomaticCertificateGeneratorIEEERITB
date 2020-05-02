# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:09:46 2020

@author: nshas
"""

import cv2
import os 
import xlrd 

''' attach path of excel sheet containing names, if not using excel. Comment below 3 lines'''

#loc = (r"")          #excel sheet path        
#wb = xlrd.open_workbook(loc)       
#sheet = wb.sheet_by_index(0)
#col=                               #column number containing names
 
font = cv2.FONT_HERSHEY_SIMPLEX     #Chnage font style,to any style supported by cv2
fontScale = 2                       #Scale the font as per requirement
color = (171, 122, 9)               #Font color in BGR
thickness = 5                       #Font Thickness
#for i in range(len(sheet.col(col))-1):   #use this for bulk certificate using excel
for i in range(1):                        #use for single certificate
    text=" ".upper()             #enter name in case of single certificate, else comment
    #text=sheet.cell_value(i+1,col)
    img=cv2.imread(r"C:\Users\nshas\Downloads\IEEE.jpeg") #attach path of cert-template
    
    '''underlying code, till org is applicable only if the name has to appear at mid of certificate, if name has to printed in some particular location.Calculate the org and assign accordingly. Org is the pixel value of bottom-left position of text on the image.Use the last 3 lines of code to adjust ORG'''
    
    cert_len=img.shape[1]
    cert_mid=cert_len//2
    txtsize=cv2.getTextSize(text, font,  fontScale, thickness)
    txt_len=txtsize[0][0]
    if(txt_len%2==0):
        mid=txt_len//2
    else:
        mid=(txt_len+1)//2
    
    
    
    org=(cert_mid-mid,450)
    img1 = cv2.putText(img, text, org, font,  fontScale, color, thickness, cv2.LINE_AA)
    path=r"C:\Users\nshas\Downloads\Certificates"        #path to save the certificates
    cv2.imwrite(os.path.join(path , text+".png"), img1 )
    
    
    '''Use the below code while testing the alignment of font, comment when generating mass certificates'''
    
    resize = cv2.resize(img1,(877,620))
    cv2.imshow('image',resize)
    cv2.waitKey(0)
