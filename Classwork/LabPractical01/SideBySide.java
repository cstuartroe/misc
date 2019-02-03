import javax.swing.*;

import java.awt.*;

/**
  *
  * One: 1.5 points<br/>
  * Create a GUI using a JFrame.<br/>
  * Have a JTextArea and a JButton share space in a JFrame equally.<br/>
  * The button should say "Click Me".<br/>
  * The TextArea should say "immutable truth"<br/>
  * Do not allow the user to change the text.
  *
  */

public class SideBySide implements Runnable
{
    JFrame frame = new JFrame();
    
    /*
     * Sets necessary features of frame and adds the two items to it
     */
    public void run()
    {
        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(2,2));
        frame.add(new JButton("Click Me"));
        JTextArea texty = new JTextArea("immutable truth");
        texty.setEditable(false);
        frame.add(texty);
        
        frame.setVisible(true);
    }

    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new SideBySide());
    }
}