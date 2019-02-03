import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

class SpacePanel extends JPanel
{
    public ArrayList<SpaceThing> things = new ArrayList<SpaceThing>();
    public SpaceThing spaceship;
    private SpaceThing spaceBlack;
    public SpaceThing counter;
    int kills = 0;
    
    public SpacePanel()
    {
        spaceBlack = new SpaceThing("spaceBlack.png",0,0,200,100,false);
        this.addThing(spaceBlack);
        
        spaceship = new SpaceThing("spaceshipU.png","spaceshipD.png","spaceshipL.png","spaceshipR.png",95,45,10,10,'W',true);
        this.addThing(spaceship);
        
        counter = new SpaceThing("counter.png","counter.png","counter.png","counter.png",0,0,10,10,'D',true);
        
        this.addMouseListener(new MouseListener()
                                  {
            public void mouseEntered(MouseEvent e){}
            public void mouseExited(MouseEvent e){}
            public void mousePressed(MouseEvent e){}
            public void mouseReleased(MouseEvent e){}
            public void mouseClicked(MouseEvent e){}
        });
    }
    
    @Override
    public void paintComponent(Graphics g)
    {
        super.paintComponent(g);
        synchronized(things){
            for(int i = 0; i<things.size(); i++)
            {
                SpaceThing worktable = things.get(i);
                int boardwidth = SpacePanel.this.getWidth();
                int boardheight = SpacePanel.this.getHeight();
                int realX = (int)((double)(boardwidth*worktable.getRelativeX()) * .005);
                int realY = (int)((double)(boardheight*worktable.getRelativeY()) * .01);
                int realWidth = (int)((double)(boardwidth*worktable.getRelativeWidth()) * .005);
                int realHeight = (int)((double)(boardheight*worktable.getRelativeHeight()) * .01);
                g.drawImage(things.get(i).getImage(),realX,realY,realWidth,realHeight,null);
            }
        }
        
        int boardwidth = SpacePanel.this.getWidth();
        int boardheight = SpacePanel.this.getHeight();
        int realX = (int)((double)(boardwidth*counter.getRelativeX()) * .005);
        int realY = (int)((double)(boardheight*counter.getRelativeY()) * .01);
        int realWidth = (int)((double)(boardwidth*10) * .005);
        int realHeight = (int)((double)(boardheight*10) * .01);
        g.drawImage(counter.getImage(),realX,realY,realWidth,realHeight,null);
        
        g.setFont(new Font("Impact", Font.PLAIN, SpacePanel.this.getHeight()/25));
        g.setColor(Color.YELLOW);
        g.drawString((""+kills*10),SpacePanel.this.getWidth()*(counter.getRelativeX() + 2)/200,SpacePanel.this.getHeight()*(counter.getRelativeY() + 6)/100);
    }
    
    public ArrayList<SpaceThing> getThings(){return things;}
    
    public void addThing(SpaceThing thing)
    {
        things.add(thing);
    }
    
    public void deleteThing(SpaceThing thing)
    {
        synchronized(things){
            things.remove(thing);
        }
    }
    
    public void addKill(){kills += 1;}
    
    public SpaceThing getSpaceship(){return this.spaceship;}
}