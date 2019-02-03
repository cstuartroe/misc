import javax.swing.*;
import javax.imageio.*;
import javax.swing.filechooser.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

import com.github.sarxos.webcam.Webcam;
import com.github.sarxos.webcam.WebcamPanel;
import com.github.sarxos.webcam.WebcamResolution;


public class WebcamViewer extends JFrame implements Runnable
{
    static Webcam webcam;
    
    BufferedImage view;
    
    VideoPanel vidPanel;
    JPanel filterPanel;
    
    boolean running = true;
    
    ArrayList<String> filters;
    
    public static void main(String[] args) throws InterruptedException
    {
        (new Thread(new WebcamViewer())).start();
    }
    
    public WebcamViewer()
    {
        filters = new ArrayList<String>();
        
        setSize(1350,710);
        setLayout(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setTitle("Go do yourself in the butt w/ a cactus.");
        
        webcam = Webcam.getDefault();
        webcam.setViewSize(WebcamResolution.VGA.getSize());
        System.out.println("Webcam Initializing...");
        webcam.open();
        System.out.println(WebcamResolution.VGA.getSize());
        
        vidPanel = new VideoPanel();
        add(vidPanel);
        vidPanel.setBounds(0,0,910,682);
        vidPanel.setLayout(null);
        
        JButton captureButton = new JButton("Take Photo");
        vidPanel.add(captureButton);
        captureButton.setBounds(405,630,100,20);
        captureButton.addActionListener(new ActionListener()
                                            {
            public void actionPerformed(ActionEvent e)
            {
                running = false;
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setFileFilter(new FileNameExtensionFilter("PNG Image File", "png"));
                int returnVal = fileChooser.showDialog(WebcamViewer.this, "Save as...");
                if(returnVal == JFileChooser.APPROVE_OPTION)
                {
                    File outputfile = fileChooser.getSelectedFile();
                    if(outputfile.exists())
                    {
                        if(JOptionPane.showConfirmDialog(WebcamViewer.this, outputfile.getAbsolutePath() + " already exists. Do you want to overwrite it?") != JOptionPane.YES_OPTION)
                        {
                            return;
                        }
                    }
                    
                    
                    try
                    {
                        ImageIO.write(view, "png", outputfile);
                    }
                    catch(java.io.IOException f)
                    {
                        f.printStackTrace();
                    }
                }
                
                
                running = true;
            }
        });
        
        filterPanel = new JPanel();
        filterPanel.setLayout(new GridLayout(5,3));
        JButton normal = new JButton("Normal Vision");
        normal.addActionListener(new ActionListener()
                                     {
            public void actionPerformed(ActionEvent e)
            {
                filters = new ArrayList<String>();
            }
        });
        normal.setBackground(Color.WHITE);
        filterPanel.add(normal);
        filterPanel.add(new FilterButton("Negative","ng",Color.BLACK));
        filterPanel.add(new FilterButton("Normalize","nm",new Color(127,127,127)));
        filterPanel.add(new FilterButton("Green-Blue Merge","gb",new Color(127,255,255)));
        filterPanel.add(new FilterButton("Red-Blue Merge","rb",new Color(255,127,255)));
        filterPanel.add(new FilterButton("Red-Green Merge","rg",new Color(255,255,127)));
        filterPanel.add(new FilterButton("Monochrome","mn",new Color(170,170,170)));
        filterPanel.add(new FilterButton("Black & White","bw",new Color(170,170,170)));
        filterPanel.add(new FilterButton("Primaries","pr",new Color(170,170,170)));
        filterPanel.add(new FilterButton("Red Highlight","rh",new Color(255,127,127)));
        filterPanel.add(new FilterButton("Green Highlight","gh",new Color(127,255,127)));
        filterPanel.add(new FilterButton("Blue Highlight","bh",new Color(127,127,255)));
        filterPanel.add(new FilterButton("Posterize","pt",new Color(170,170,170)));
        filterPanel.add(new FilterButton("Hue Shift","ls",new Color(170,170,170)));
        //filterPanel.add(new FilterButton("Right Hue Shift","rs"));
        filterPanel.add(new FilterButton("Intensifier","in",new Color(170,170,170)));
        add(filterPanel);
        filterPanel.setBounds(910,0,434,682);
        
        setResizable(false);
        setVisible(true);
    }
    
    public void run()
    {
        while(1==1)
        {
            if(running)
            {
                view = WebcamViewer.webcam.getImage();
                try
                {
                    Thread.sleep(50);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }
                for(int i = 0; i < filters.size(); i++)
                {
                    ColorFilter.filter(view, filters.get(i));
                }
                vidPanel.repaint();
            }
        }
    }
    
    private class VideoPanel extends JPanel
    {
        @Override
        public void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            g.drawImage(view,0,0,getWidth(),getHeight(),null);
        }
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
                    filters.add(toFilter);
                }
            });
        }
    }
    
    private class FilterButton extends JButton
    {
        public FilterButton(String title, final String toFilter, Color c)
        {
            setText(title);
            setBackground(c);
            addActionListener(new ActionListener()
                                  {
                public void actionPerformed(ActionEvent e)
                {
                    filters.add(toFilter);
                }
            });
        }
    }
}