import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

class SpaceThing
{
    private BufferedImage image;
    private String filenameU;
    private String filenameD;
    private String filenameL;
    private String filenameR;
    public int relativeX;
    public int relativeY;
    public int relativeWidth;
    public int relativeHeight;
    public Boolean solid;
    public char dir;
    
    public SpaceThing(String _filenameU, String _filenameD, String _filenameL, String _filenameR, int _x, int _y, int _width, int _height, char _dir, Boolean _solid)
    {
        this.filenameU = _filenameU;
        this.filenameD = _filenameD;
        this.filenameL = _filenameL;
        this.filenameR = _filenameR;
        this.relativeX = _x;
        this.relativeY = _y;
        this.relativeWidth = _width;
        this.relativeHeight = _height;
        this.solid = _solid;
        this.dir = _dir;
        this.advance();
    }
    
    public SpaceThing(String _filename, int _x, int _y, int _width, int _height, Boolean _solid)
    {
        this.filenameU = _filename;
        this.filenameD = _filename;
        this.filenameL = _filename;
        this.filenameR = _filename;
        this.relativeX = _x;
        this.relativeY = _y;
        this.relativeWidth = _width;
        this.relativeHeight = _height;
        this.solid = _solid;
        this.dir='W';
        this.setImage(filenameU);
    }
    
    public void advance()
    {
        if(dir == 'W')
        {
            relativeY--;
            setImage(filenameU);
        }
        if(dir == 'S')
        {
            relativeY++;
            setImage(filenameD);
        }
        if(dir == 'A')
        {
            relativeX--;
            setImage(filenameL);
        }
        if(dir == 'D')
        {
            relativeX++;
            setImage(filenameR);
        }
        if(solid)
        {
            if(relativeX < 0){relativeX++; dir = 'D';}
            if(relativeY < 0){relativeY++; dir = 'S';}
            if(relativeX + relativeWidth > 200){relativeX--;  dir = 'A';}
            if(relativeY + relativeHeight > 100){relativeY--; dir = 'W';}
        }
        else
        {
            if(relativeX + relativeWidth < 0){dir = 'Q';}
            if(relativeY + relativeHeight < 0){dir = 'Q';}
            if(relativeX > 200){dir = 'Q';}
            if(relativeY > 100){dir = 'Q';}
        }
    }
    
    public void setImage(String filename)
    {
        try
        {                
            image = ImageIO.read(new File(filename));
        }
        catch (IOException ex)
        {
            System.out.println("ur fukkd m8");
        }
    }
    
    public void setDir(char _dir)
    {
        dir = _dir;
    }
    
    public Boolean isCollidedX(SpaceThing that)
    {
        return ((this.relativeX + this.relativeWidth > that.relativeX) && (this.relativeX < that.relativeX + that.relativeWidth));
    }
    
    public Boolean isCollidedY(SpaceThing that)
    {
        return ((this.relativeY + this.relativeHeight > that.relativeY) && (this.relativeY < that.relativeY + that.relativeHeight));
    }
    
    public int getRelativeX(){return this.relativeX;}
    public int getRelativeY(){return this.relativeY;}
    public int getRelativeWidth(){return this.relativeWidth;}
    public int getRelativeHeight(){return this.relativeHeight;}
    public BufferedImage getImage(){return this.image;}
    public String getFilenameU(){return this.filenameU;}
}