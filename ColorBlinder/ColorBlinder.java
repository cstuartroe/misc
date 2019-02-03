import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

public class ColorBlinder extends JFrame
{
    JImagePanel panel;
    
    public ColorBlinder(String _filename)
    {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        getContentPane().setLayout(new GridLayout());
        setResizable(false);
        setTitle("Colorblindness Simulator");
        
        JMenuBar jmb = new JMenuBar();
        JMenu filters = new JMenu("Filters");
        JMenuItem normal = new JMenuItem("Normal Vision");
        normal.addActionListener(new ActionListener()
                                     {
            public void actionPerformed(ActionEvent e)
            {
                panel.reimage();
                repaint();
            }
        });
        filters.add(normal);
        filters.add(new FilterMenuItem("Negative","ng"));
        filters.add(new FilterMenuItem("Red-Green Colorblindness","rg"));
        filters.add(new FilterMenuItem("Red-Blue Colorblindness","rb"));
        filters.add(new FilterMenuItem("Green-Blue Colorblindness","gb"));
        filters.add(new FilterMenuItem("Monochrome Colorblindness","mn"));
        filters.add(new FilterMenuItem("Black & White","bw"));
        filters.add(new FilterMenuItem("Red Highlight","rh"));
        filters.add(new FilterMenuItem("Green Highlight","gh"));
        filters.add(new FilterMenuItem("Blue Highlight","bh"));
        filters.add(new FilterMenuItem("Posterize","pt"));
        filters.add(new FilterMenuItem("Primaries","pr"));
        filters.add(new FilterMenuItem("Left Hue Shift","ls"));
        filters.add(new FilterMenuItem("Right Hue Shift","rs"));
        filters.add(new FilterMenuItem("Intensifier","in"));
        filters.add(new FilterMenuItem("Normalize","nm"));
        JMenu images = new JMenu("Images");
        images.add(new ImageMenuItem("Test Strip", "teststrip3.png"));
        images.add(new ImageMenuItem("Colored Pencils", "coloredPencils.png"));
        images.add(new ImageMenuItem("Sesame Street", "c.png"));
        images.add(new ImageMenuItem("Waterfall", "lake.png"));
        images.add(new ImageMenuItem("Field and Mountains", "field.png"));
        images.add(new ImageMenuItem("Horses", "horses.png"));
        images.add(new ImageMenuItem("Snake", "snake.png"));
        jmb.add(filters);
        jmb.add(images);
        setJMenuBar(jmb);
        
        panel = new JImagePanel(_filename);
        getContentPane().add(panel);
        
        setVisible(true);
    }
    
    private class FilterMenuItem extends JMenuItem
    {
        public FilterMenuItem(String title, final String toFilter)
        {
            setText(title);
            addActionListener(new ActionListener()
                                  {
                public void actionPerformed(ActionEvent e)
                {
                    panel.refilter(toFilter);
                    ColorBlinder.this.repaint();
                }
            });
        }
    }
    
    private class ImageMenuItem extends JMenuItem
    {
        public ImageMenuItem(String title, final String filename)
        {
            setText(title);
            addActionListener(new ActionListener()
                                  {
                public void actionPerformed(ActionEvent e)
                {
                    panel.reimage(filename);
                    ColorBlinder.this.repaint();
                }
            });
        }
    }
    
    private class JImagePanel extends JPanel
    {
        String filename;
        BufferedImage image;
        
        public JImagePanel(String _filename)
        {
            filename = _filename;
            try
            {                
                image = ImageIO.read(new File(filename));
            }
            catch (IOException ex)
            {
                System.out.println("ur fukkd m8");
            }
            refilter("null");
        }
        
        public void reimage(String _filename)
        {
            filename = _filename;
            try
            {                
                image = ImageIO.read(new File(filename));
            }
            catch (IOException ex)
            {
                System.out.println("ur fukkd m8");
            }
            refilter("null");
        }
        
        public void reimage()
        {
            try
            {                
                image = ImageIO.read(new File(filename));
            }
            catch (IOException ex)
            {
                System.out.println("ur fukkd m8");
            }
            refilter("null");
        }
        
        public void refilter(String filterType)
        {
            ColorFilter.filter(image, filterType);
            ColorBlinder.this.setSize(image.getWidth() + 6,image.getHeight() + 51);
        }
        
        public void setFilename(String _filename)
        {
            filename = _filename;
            refilter("null");
        }
        
        @Override
        public void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            g.drawImage(image,0,0,getWidth(),getHeight(),null);
        }
    }
    
    public static void main(String args[])
    {
        new ColorBlinder("teststrip3.png");
    }
}