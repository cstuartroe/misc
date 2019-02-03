import javax.swing.*;
import javax.swing.event.*;

import java.awt.*;
import java.awt.event.*;

/*
 * This class generates a frame with a color display, as well sliders and a hex input to edit rgb values. 
 */
public class PosterizedColorCalculator extends JFrame
{
    // Panels containing RGB value sliders
    private ColorSliderPanel redSliderPanel = new ColorSliderPanel("Red");
    private ColorSliderPanel grnSliderPanel = new ColorSliderPanel("Green");
    private ColorSliderPanel bluSliderPanel = new ColorSliderPanel("Blue");
    
    // Panel containing a text field in which to enter hex codes
    private JPanel byteEntry = new JPanel();
    private JTextField byteField = new JTextField(2);
    
    //Panel in which color is displayed
    private JPanel displayPanel = new JPanel();
    
    
    /*
     * This contructor sets important features of the generic ColorCalculator and adds relevant items to it.
     */
    public PosterizedColorCalculator()
    {
        setTitle("Conor's Color Calculator");
        setSize(600,600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);
        setVisible(true);
        
        // If the frame is resized this recalculates the position of frames
        this.addComponentListener(new ComponentAdapter()
                                      {
            public void componentResized(ComponentEvent e)
            {
                setComponentPositions();
            }
        });
        
        // If text is entered in the hex field this analyzes it and either sets RGB values or gives an error dialog.
        byteField.addActionListener(new ActionListener()
                                       {
            public void actionPerformed(ActionEvent e)
            {
                int temp = (redSliderPanel.getValue() * 0b10000) + (grnSliderPanel.getValue() * 0b100) + (bluSliderPanel.getValue());
                try
                {
                    temp = Integer.parseInt(byteField.getText(),16);
                }
                catch(NumberFormatException f)
                {
                    JOptionPane.showMessageDialog(PosterizedColorCalculator.this, "The text entered is not a valid byte code.");
                }
                redSliderPanel.setValue(temp / 0b10000);
                grnSliderPanel.setValue((temp / 0b100) % 0b100);
                bluSliderPanel.setValue(temp % 0b100);
                resetDisplay();
            }
        });
        
        byteEntry.add(byteField);
        
        getContentPane().add(redSliderPanel);
        getContentPane().add(grnSliderPanel);
        getContentPane().add(bluSliderPanel);
        getContentPane().add(byteEntry);
        getContentPane().add(displayPanel);
        setComponentPositions();
        resetDisplay();
    }
    
    /*
     * Computes and sets the bounds of all frames in the calculator based on control panel side and dimensions of frame.
     */
    public void setComponentPositions()
    {
        Container pane = getContentPane();
        
        redSliderPanel.setBounds(0,0,pane.getWidth()/4,pane.getHeight()/8);
        grnSliderPanel.setBounds(pane.getWidth()/4,0,pane.getWidth()/4,pane.getHeight()/8);
        bluSliderPanel.setBounds(pane.getWidth()/2,0,pane.getWidth()/4,pane.getHeight()/8);
        byteEntry.setBounds(pane.getWidth()*3/4,0,pane.getWidth()/4,pane.getHeight()/8);
        displayPanel.setBounds(0,pane.getHeight()/8,pane.getWidth(),pane.getHeight()*7/8);
        
        revalidate();
    }
    
    /*
     * Updates slider positions, hex field, and color display
     * Called every time a slider or the text field is manipulated
     */
    public void resetDisplay()
    {
        redSliderPanel.resetLabel();
        grnSliderPanel.resetLabel();
        bluSliderPanel.resetLabel();
        byteField.setText(toByte());
        displayPanel.setBackground(new PosterizedColor(redSliderPanel.getValue(),grnSliderPanel.getValue(),bluSliderPanel.getValue(),false).getColor());
        repaint();
    }
    
    /*
     * Returns a string representation of the current hex color code
     * Ensures that output is six characters long, adding zeroes to left
     */
    public String toByte()
    {
        return(String.format("%2s", (Integer.toString((bluSliderPanel.getValue() + grnSliderPanel.getValue()*0b100 + redSliderPanel.getValue()*0b10000)))).replace(' ', '0'));
    }
    
    // This class is simply a panel containing a slider
    private class ColorSliderPanel extends JPanel
    {
        private JSlider slide = new JSlider(0,3);
        private String title;
        private JLabel label;
        
        /*
         * This constructor creates a panel with a slider in the center and a label below showing color and current value, in decimal
         * @param _title the label underneath the slider, telling the user which color it controls
         */
        public ColorSliderPanel(String _title)
        {
            setLayout(new GridLayout(2,2));
            
            slide.setMajorTickSpacing(1);
            slide.setPaintTicks(true);
            add(slide);
            setValue(0);
            
            title = _title;
            label = new JLabel(title + ": " + getValue(), JLabel.CENTER);
            add(label);
            
            // Calls resetDisplay if the slider is changed, updating hex field and color display
            slide.addChangeListener(new ChangeListener()
                                        {
                public void stateChanged(ChangeEvent e)
                {
                    PosterizedColorCalculator.this.resetDisplay();
                }
            });
        }
        
        /*
         * Sets value of slider, as when a hex code is entered
         * @param val the value to set slider to
         */
        public void setValue(int val)
        {
            slide.setValue(val);
        }
        
        // Returns the current value of the slider
        public int getValue()
        {
            return slide.getValue();
        }
        
        // Updates the decimal representation of value in the label
        public void resetLabel()
        {
            label.setText(title + ": " + getValue());
        }
    }
    
    /*
     * The main function creates an instance of the class
     */
    public static void main(String[] args)
    {
        new PosterizedColorCalculator();
    }
}