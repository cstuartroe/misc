import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color;

import java.util.*;

public class deStijl implements Runnable
{
    
    ArrayList<Kameleon> panels = new ArrayList<Kameleon>();
    int width = 6;
    int height = 6;
    
    public void run()
    {
        JFrame flag = new JFrame("De Stijl");
        flag.setSize(700,700);
        flag.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        flag.setVisible(true);
        flag.setLayout(new GridLayout(width, height));
        
        for(int i = 0; i<width*height; i++){
            Kameleon chammy = new Kameleon();
            flag.add(chammy);
            panels.add(chammy);
        }
        
    }
    
    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new deStijl());
    } 
    
    class Kameleon extends JPanel
    {
        int[] colors = {16777215,15597568,119,0,16776960};
        private int on = 200;
        
        public Kameleon(){
            this.setBackground(new Color(colors[on % colors.length]));
            this.addMouseListener(new MouseListener() {
                public void mouseClicked(MouseEvent e){}
                public void mouseReleased(MouseEvent e){}
                public void mouseEntered(MouseEvent e){}
                public void mouseExited(MouseEvent e){}
                
                public void mousePressed(MouseEvent e){
                    if(SwingUtilities.isLeftMouseButton(e))
                    {
                        iteratePattern(Kameleon.this,1);
                    }
                    if(SwingUtilities.isRightMouseButton(e))
                    {
                        iteratePattern(Kameleon.this,-1);
                    }
                }
            });
        }
        
        public void iterateColor(int dir)
        {
            on += dir;
            Kameleon.this.setBackground(new Color(colors[on % colors.length]));
        }
        
        public void resetColor()
        {
            on = 200;
            Kameleon.this.setBackground(new Color(colors[on % colors.length]));
        }
    }
    
    public void iteratePattern(JPanel p, int dir)
    {
        int x = panels.indexOf(p);
        
        int[][] indexSet = new int[][]{{0,2,5,19,21,22,28,29,31},{3,23,24,32,35},{0,1,3,4,6,7,9,10,13,20,33},{1,6,9,10,13,15,19,20,22},{2,4,5,23,28,31,32,34,35},{3,6,9,23,24,26,27,32,34,35},{3,8,18,25,26,30},{11,12,14,15,16,31,32,33},{2,3,5,6,7,8,9,12,14,17,18,23,25,30,33}};
        
        int[] panelsToChange = new int[1];
        
        for(int i = 0; i<indexSet.length; i++)
        {
            for(int j = 0; j<indexSet[i].length; j++)
            {
                if(x == indexSet[i][j])
                {
                    panelsToChange = indexSet[i];
                }
            }
        }
        
        for(int k = 0; k<panelsToChange.length; k++)
        {
            panels.get(panelsToChange[k]).iterateColor(dir);
        }
    }
}