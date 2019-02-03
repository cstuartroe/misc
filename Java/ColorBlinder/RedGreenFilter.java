import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

public class RedGreenFilter
{
    public void filter(BufferedImage init)
    {
        WritableRaster newRaster = init.getRaster();
        for(int x = 0; x < newRaster.getWidth(); x++)
        {
            for(int y = 0; y < newRaster.getHeight(); y++)
            {
                int[] iArray = new int[4];
                int[] colorArray = newRaster.getPixel(x, y, iArray);
                newRaster.setPixel(x/2, y, colorArray);
            }
        }
    }
}