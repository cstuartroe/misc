import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

public class ColorFilter
{
    public static void filter(BufferedImage init, String filterType)
    {
        WritableRaster newRaster = init.getRaster();
        for(int x = 0; x < newRaster.getWidth(); x++)
        {
            for(int y = 0; y < newRaster.getHeight(); y++)
            {
                int[] colorArray = newRaster.getPixel(x, y, new int[4]);
                int red = colorArray[0];
                int grn = colorArray[1];
                int blu = colorArray[2];
                int white = (red + grn + blu)/3;
                
                switch(filterType)
                {
                    case "ng":
                        red = 255 - red;
                        grn = 255 - grn;
                        blu = 255 - blu;
                        break;
                    case "rg":
                        int yellow = (red + grn)/2;
                        red = yellow;
                        grn = yellow;
                        break;
                    case "rb":
                        int magenta = (red + blu)/2;
                        red = magenta;
                        blu = magenta;
                        break;
                    case "gb":
                        int cyan = (grn + blu)/2;
                        grn = cyan;
                        blu = cyan;
                        break;
                    case "mn":
                        red = white;
                        grn = white;
                        blu = white;
                        break;
                    case "bw":
                        if(white>127)
                        {
                            red = 255;
                            grn = 255;
                            blu = 255;
                        }
                        else
                        {
                            red = 0;
                            grn = 0;
                            blu = 0;
                        }
                        break;
                    case "rh":
                        if(red < white)
                        {
                            red = white;
                        }
                        grn = 2 * white - red;
                        blu = 2 * white - red;
                        if(grn < 0)
                        {
                            grn = 0;
                            blu = 0;
                        }
                        break;
                    case "gh":
                        if(grn < white)
                        {
                            grn = white;
                        }
                        red = 2 * white - grn;
                        blu = 2 * white - grn;
                        if(red < 0)
                        {
                            red = 0;
                            blu = 0;
                        }
                        break;
                    case "bh":
                        if(blu < white)
                        {
                            blu = white;
                        }
                        red = 2 * white - blu;
                        grn = 2 * white - blu;
                        if(red < 0)
                        {
                            red = 0;
                            grn = 0;
                        }
                        break;
                    case "pt":
                        PosterizedColor pt = new PosterizedColor(red, grn, blu, true);
                        red = pt.getRed();
                        grn = pt.getGreen();
                        blu = pt.getBlue();
                        break;
                    case "pr":
                        if(white > 165)
                        {
                            red = 255;
                            grn = 255;
                            blu = 255;
                        }
                        else if(white < 90)
                        {
                            red = 0;
                            grn = 0;
                            blu = 0;
                        }
                        /*else if((grn > red) && (((grn + red) / 2) > blu))
                        {
                            grn = 255;
                            red = 255;
                            blu = 0;
                        }*/
                        else if(red > blu)
                        {
                            red = 255;
                            grn = 0;
                            blu = 0;
                        }
                        else
                        {
                            red = 0;
                            grn = 0;
                            blu = 255;
                        }
                        break;
                    case "ls":
                        int temp1 = red;
                        red = blu;
                        blu = grn;
                        grn = temp1;
                        break;
                    case "rs":
                        int temp2 = red;
                        red = grn;
                        grn = blu;
                        blu = temp2;
                        break;
                    case "in":
                        if(red<white)
                        {
                            red = white - (int)Math.sqrt((white * white) - (red * red));
                        }
                        else
                        {
                            red = white + (int)Math.sqrt(((255 - white) * (255 - white)) - ((255 - red) * (255 - red)));
                        }
                        if(grn<white)
                        {
                            grn = white - (int)Math.sqrt((white * white) - (grn * grn));
                        }
                        else
                        {
                            grn = white + (int)Math.sqrt(((255 - white) * (255 - white)) - ((255 - grn) * (255 - grn)));
                        }
                        if(blu<white)
                        {
                            blu = white - (int)Math.sqrt((white * white) - (blu * blu));
                        }
                        else
                        {
                            blu = white + (int)Math.sqrt(((255 - white) * (255 - white)) - ((255 - blu) * (255 - blu)));
                        }
                        break;
                    case "nm":
                        double scalar = 127.0 / white;
                        red = (int)(((scalar + .5) * red)/1.5);
                        grn = (int)(((scalar + .5) * grn)/1.5);
                        blu = (int)(((scalar + .5) * blu)/1.5);
                }
                
                newRaster.setPixel(x, y, new int[]{red,grn,blu,255});
            }
        }
    }
}