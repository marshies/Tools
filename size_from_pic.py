# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 13:10:39 2017

@author: mbremer
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import os,re
from PyQt4 import QtCore, QtGui
import argparse



class ImageDimensioner(object):


    def __init__( self, img, scale_length = 12, name = 'image' ):
        """
        """
        #img = img[1000:2000,1000:2000,:]
#        img = cv2.resize(img,(1728,1152))

        self.img0 = img
        fx = 1#1000/img.shape[1]
        self.img = cv2.resize(img,(0,0),fx = fx,fy = fx)
        self.img_copy = img.copy()
        self.img_annotated = img.copy()
        self.name = name
        self.scale_length = scale_length
        self.point1 = None
        self.point2 = None
        self.mm_per_pixel = None


    def menu( self, ):
        """
        """
        self.img_copy = self.img.copy()
        cv2.putText( self.img_copy,
                     r"'s' for scale, 'z' to zoom, 'd' for distance, 'a' for angle, 'q' when done" ,
                     (160,120), cv2.FONT_HERSHEY_SIMPLEX, .8, (250,250,0) )
        cv2.imshow( self.name, self.img_copy )
        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            self.get_scale()

        if key == ord("d"):
            self.get_distance()

        if key == ord("a"):
            self.get_angle()

        if key == ord("z"):
            self.zoom_image()

        if key == ord("q"):
            self.get_annotated_figure()



    def zoom_image( self ):
        """
        """
        cv2.namedWindow( self.name )
        cv2.setMouseCallback( self.name, self.click_distance )
        self.img_copy = self.img.copy()
        cv2.putText( self.img_copy,
             r"click 2 opposite corners of the zoom rectangle, press 'r' when done" ,
             (160,120), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,250,250) )

        cv2.imshow( self.name, self.img_copy )
        key = cv2.waitKey(0) & 0xFF

        if key == ord("\r"):
            self.img = self.img[ self.point1[1]:self.point2[1],
                                 self.point1[0]:self.point2[0] ]

        self.menu()

    def get_scale( self ):
        """
        """
        cv2.namedWindow( self.name )
        cv2.setMouseCallback( self.name, self.click_distance )
        self.img_copy = self.img.copy()
        cv2.putText( self.img_copy,
             r"click 2 points the scale length apart, press 'r' when done" ,
             (160,120), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,250,250) )

        cv2.imshow( self.name, self.img_copy )
        key = cv2.waitKey(0) & 0xFF

        if key == ord("\r"):
            self.mm_per_pixel =   self.scale_length\
                                / np.dot( (self.point2 - self.point1),
                                        (self.point2 - self.point1) )**.5


        print('{} mm_per_pixel'.format(self.mm_per_pixel))
        self.menu()


    def get_distance( self ):
        """
        """
        cv2.namedWindow( self.name )
        cv2.setMouseCallback( self.name, self.click_distance )
        self.img_copy = self.img.copy()
        cv2.putText( self.img_copy, r"click 2 points, press 'r' when done or 'q' to quit",
                     (160,120), cv2.FONT_HERSHEY_SIMPLEX, .8, 250 )

        cv2.imshow( self.name, self.img_copy )
        key = cv2.waitKey(0) & 0xFF

        if key == ord("\r"):
            self.distance =   self.mm_per_pixel * np.dot( (self.point2 - self.point1),
                                        (self.point2 - self.point1) )**.5

            print('{} mm'.format(self.distance))
            cv2.line( self.img_annotated, tuple(self.point1), tuple(self.point2),(0,0,250))
            cv2.putText( self.img_annotated, '{} mm'.format(self.distance),
                         tuple(self.point1), cv2.FONT_HERSHEY_SIMPLEX, .8, (0,0,250) )
            cv2.imshow('annotated', self.img_annotated)
            self.get_distance()

        elif key == ord("q"):
            self.menu()



    def click_distance( self, event, x, y, flags, param ):
        """ if the left mouse button was clicked, record the center
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.point1 is None or self.point2 is not None:
                self.point1 = np.array([x, y])
                self.point2 = None
                self.img_copy = self.img.copy()
                cv2.circle( self.img_copy, tuple(self.point1), 5, 150)
                cv2.imshow(self.name, self.img_copy)

            elif self.point1 is not None:
                self.point2 = np.array([x, y])
                self.img_copy = self.img.copy()
                cv2.line( self.img_copy, tuple(self.point1), tuple(self.point2),(250,0,0))
                cv2.putText( self.img_copy,
                             r"press 'r' if satisfied" ,
                             (160,120), cv2.FONT_HERSHEY_SIMPLEX, .8, 250 )
                cv2.imshow(self.name, self.img_copy)


    def get_annotated_figure( self ):
        """
        """
        cv2.destroyAllWindows()
        return self.img_annotated




