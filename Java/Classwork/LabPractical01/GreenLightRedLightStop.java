import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color.*;

/**
  * Three: 1 point<br/>
  * Make a JFrame.<br/>
  * Put a yellow JPanel in it.<br/>
  * When the mouse enters the panel have the panel turn Red.  When the mouse exits the panel, have the panel turn Green.<br/>
  *
  * When the panel is clicked, have it stop responding to mouse movements.<br/>
  * If the panel is clicked again, have it start responding again.
  */

public class GreenLightRedLightStop implements Runnable
{
    JFrame frame = new JFrame();
    JPanel panel = new JPanel();
    
    Boolean panelResponsive = true;
    
    /*
     * This sets the necessary features for frame, adds panel, and adds MouseListeners to panel
     */
    public void run()
    {
        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout());
        
        panel.setBackground(Color.YELLOW);
        panel.addMouseListener(new MouseListener()
                                   {
            //If mouse enters and panel is responsive, the panel becomes red
            public void mouseEntered(MouseEvent e)
            {
                if(GreenLightRedLightStop.this.panelResponsive)
                {
                    GreenLightRedLightStop.this.panel.setBackground(Color.RED);
                }
            }
            
            //If mouse exits and panel is responsive, the panel becomes green
            public void mouseExited(MouseEvent e)
            {
                if(GreenLightRedLightStop.this.panelResponsive)
                {
                    GreenLightRedLightStop.this.panel.setBackground(Color.GREEN);
                }
            }
            
            public void mouseClicked(MouseEvent e)
            {}
            
            
            //If mouse is pressed, this toggles whether the panel is responsive or not.
            public void mousePressed(MouseEvent e)
            {
                GreenLightRedLightStop.this.panelResponsive = Boolean.logicalXor(GreenLightRedLightStop.this.panelResponsive, true);
            }
            
            public void mouseReleased(MouseEvent e)
            {}
        });
        frame.add(panel);
        
        frame.setVisible(true);
    }

    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new GreenLightRedLightStop());
    }
}