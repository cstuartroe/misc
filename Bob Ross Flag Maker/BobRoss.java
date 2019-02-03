import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color;

import java.util.*;

public class BobRoss implements Runnable
{
    /*String fuck = "fuck you fuck you fuck you fuck you fuck you fuck you fuck you duck you fuck you fuck you fuck you fuck you fuck you fuck you";
    int q = 0;*/
    
    ArrayList<Chameleon> panels = new ArrayList<Chameleon>();
    int currentPattern = 0;
    int width = 6;
    int height = 6;
    
    /*public JMenuBar makeMenus()
    {
        JMenuBar jmb = new JMenuBar();
        JMenu file = new JMenu("File");
        JMenu panel = new JMenu("Panel");
        JMenu color = new JMenu("Color");
        JMenuItem jmi = new JMenuItem("Quit");
        jmi.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                System.exit(0);
            }
        });
        file.add(jmi);
        jmb.add(file);
        jmb.add(panel);
        jmb.add(color);
        return jmb;
    }*/
    
    public void run()
    {
        /*JFrame jeff = new JFrame("Hello Sunshine");
        jeff.setSize(800,600);
        jeff.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        jeff.setVisible(false);
        
        JButton butt = new JButton();
        butt.setBackground(Color.RED);
        butt.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e){
                q += 1;
                butt.setText(fuck.substring(0,q));
                Random r = new Random();
                int x = r.nextInt(256);
                int y = r.nextInt(256);
                int z = r.nextInt(256);
                Color c = new Color(x,y,z);
                butt.setBackground(c);
            }
        });
        jeff.add(butt);*/
        
        JFrame flag = new JFrame("Make your own flag!");
        flag.setSize(1200,700);
        flag.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        flag.setVisible(true);
        flag.setLayout(new GridLayout(width, height));
        
        JMenuBar jmb = new JMenuBar();
        flag.setJMenuBar(jmb);
        JMenu pattern = new JMenu("Pattern");
        jmb.add(pattern);
        
        JMenuItem freeform = new JMenuItem("Freeform");
        freeform.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 0;
            }
        });
        pattern.add(freeform);
        
        JMenuItem twoHorizontal = new JMenuItem("Two Horizontal Stripes");
        twoHorizontal.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 1;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(twoHorizontal);
        
        JMenuItem threeHorizontal = new JMenuItem("Three Horizontal Stripes");
        threeHorizontal.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 2;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(threeHorizontal);
        
        JMenuItem twoVertical = new JMenuItem("Two Vertical Stripes");
        twoVertical.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 3;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(twoVertical);
        
        JMenuItem threeVertical = new JMenuItem("Three Vertical Stripes");
        threeVertical.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 4;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(threeVertical);
        
        JMenuItem cross = new JMenuItem("Cross");
        cross.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 5;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(cross);
        
        JMenuItem scandinavianCross = new JMenuItem("Scandinavian Cross");
        scandinavianCross.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                currentPattern = 6;
                for(int i = 0; i<width*height; i++)
                {
                    panels.get(i).resetColor();
                }
            }
        });
        pattern.add(scandinavianCross);
        
        for(int i = 0; i<width*height; i++){
            Chameleon chammy = new Chameleon();
            flag.add(chammy);
            panels.add(chammy);
        }
        
    }
    
    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new BobRoss());
        
        /*Thread myThread = new Thread(new Runnable(){
            public void run(){
                try{
                    Thread.sleep(2000);
                    System.out.println("This is in a thread");
                }
                catch(InterruptedException ex){}
            }
        });*/
                              
        //myThread.start();
        
    } 
    
    class Chameleon extends JPanel
    {
        int[] colors = {16777215,15597568,119,0,39168,16776960,16746496,11167266,10035746,8965375};
        private int on = 200;
        
        public Chameleon(){
            this.setBackground(new Color(colors[on % colors.length]));
            this.addMouseListener(new MouseListener() {
                public void mouseClicked(MouseEvent e){}
                public void mouseReleased(MouseEvent e){}
                public void mouseEntered(MouseEvent e){}
                public void mouseExited(MouseEvent e){}
                
                public void mousePressed(MouseEvent e){
                    if(SwingUtilities.isLeftMouseButton(e))
                    {
                        iteratePattern(Chameleon.this,1);
                    }
                    if(SwingUtilities.isRightMouseButton(e))
                    {
                        iteratePattern(Chameleon.this,-1);
                    }
                }
            });
        }
        
        public void iterateColor(int dir)
        {
            on += dir;
            Chameleon.this.setBackground(new Color(colors[on % colors.length]));
        }
        
        public void resetColor()
        {
            on = 200;
            Chameleon.this.setBackground(new Color(colors[on % colors.length]));
        }
    }
    
    public void iteratePattern(JPanel p, int dir)
    {
        int x = panels.indexOf(p);
        
        int[][] indexSet = new int[1][1];
        
        if(currentPattern == 0){indexSet = new int[][]{{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},{23},{24},{25},{26},{27},{28},{29},{30},{31},{32},{33},{34},{35}};}
        if(currentPattern == 1){indexSet = new int[][]{{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17},{18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35}};}
        if(currentPattern == 2){indexSet = new int[][]{{0,1,2,3,4,5,6,7,8,9,10,11},{12,13,14,15,16,17,18,19,20,21,22,23},{24,25,26,27,28,29,30,31,32,33,34,35}};}
        if(currentPattern == 3){indexSet = new int[][]{{0,1,2,6,7,8,12,13,14,18,19,20,24,25,26,30,31,32},{3,4,5,9,10,11,15,16,17,21,22,23,27,28,29,33,34,35}};}
        if(currentPattern == 4){indexSet = new int[][]{{0,1,6,7,12,13,18,19,24,25,30,31},{2,3,8,9,14,15,20,21,26,27,32,33},{4,5,10,11,16,17,22,23,28,29,34,35}};}
        if(currentPattern == 5){indexSet = new int[][]{{0,1,4,5,6,7,10,11,24,25,28,29,30,31,34,35},{2,3,8,9,12,13,14,15,16,17,18,19,20,21,22,23,26,27,32,33}};}
        if(currentPattern == 6){indexSet = new int[][]{{0,2,3,4,5,6,8,9,10,11,24,26,27,28,29,30,32,33,34,35},{1,7,12,13,14,15,16,17,18,19,20,21,22,23,25,31}};}
        
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