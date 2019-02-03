import javax.swing.*;

import java.awt.*;
import java.awt.event.*;

/**
  *
  * Two: 1 point <br/>
  *
  * Create a GUI using a JFrame.<br/>
  * There should be 3 spaces:<br/>
  *      On the left:   a button that says Even.<br/>
  *      On the right:  a button that says Odd.<br/>
  *      In the middle: text starting at "0".<br/>
  *<br/>
  * When you click the Odd button, have the text increase to the next largest
  * odd number.<br/>
  * When you click the Even button, have the text increase to the next largest
  * even number.<br/>
  *
  */

public class EvenOdd implements Runnable
{
    int counter = 0;
    
    JFrame frame = new JFrame();
    JButton even = new JButton("Even");
    JButton odd = new JButton("Odd");
    JTextArea texty = new JTextArea(Integer.toString(counter));
    
    
    /*
     * Sets necessary features of frame and adds the three items to it
     */
    public void run()
    {
        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(1,3));
        
        
        //This ActionListener sets counter to the next-highest even number and sets texty's text to counter
        even.addActionListener(new ActionListener()
                                   {
            public void actionPerformed(ActionEvent e)
            {
                EvenOdd.this.counter += 2;
                EvenOdd.this.counter -= EvenOdd.this.counter % 2;
                EvenOdd.this.texty.setText(Integer.toString(EvenOdd.this.counter));
            }
        });
        frame.add(even);
        
        texty.setEditable(false);
        frame.add(texty);
        
        //This ActionListener sets counter to the next-highest odd number and sets texty's text to counter
        odd.addActionListener(new ActionListener()
                                   {
            public void actionPerformed(ActionEvent e)
            {
                EvenOdd.this.counter += 2;
                EvenOdd.this.counter -= (EvenOdd.this.counter + 1) % 2;
                EvenOdd.this.texty.setText(Integer.toString(EvenOdd.this.counter));
            }
        });
        frame.add(odd);
        
        frame.setVisible(true);
    }

    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new EvenOdd());
    }
}