import javax.swing.*;
import java.awt.*;
import java.util.*;

public class EvoSimulator extends JFrame
{
    private ArrayList<Plant> plants = new ArrayList<Plant>();
    
    public EvoSimulator()
    {
        setSize(1016,688);
        setTitle("Codu's Magical Plant Sim");
        setResizable(false);
        add(new Display());
        plants.add(new Plant());
        setVisible(true);
    }
    
    private class Display extends JPanel
    {
        @Override
        public void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            g.setColor(new Color(180,200,255));
            g.fillRect(0,0,1000,500);
            g.setColor(new Color(220,200,150));
            g.fillRect(0,500,1000,100);
        }
    }
    
    public static void main(String[] args)
    {
        new EvoSimulator();
    }
}