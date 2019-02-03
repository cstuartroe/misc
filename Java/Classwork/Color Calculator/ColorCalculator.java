import javax.swing.*;
import javax.swing.event.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color.*;

/*
 * This class generates a frame with a color display, as well sliders and a hex input to edit rgb values. 
 */
public class ColorCalculator extends JFrame
{
    // Representes the side that the control panel is on = Left, Right, Top, or Bottom
    private char side = 'L';
    
    // The menu containing quit functions and the commands to change location of the control panel
    private JMenuBar menuBar = new ColorMenuBar();
    
    // Panels containing RGB value sliders
    private ColorSliderPanel redSliderPanel = new ColorSliderPanel("Red");
    private ColorSliderPanel grnSliderPanel = new ColorSliderPanel("Green");
    private ColorSliderPanel bluSliderPanel = new ColorSliderPanel("Blue");
    
    // Panel containing a text field in which to enter hex codes
    private JPanel hexEntry = new JPanel();
    private JTextField hexField = new JTextField(4);
    
    //Panel in which color is displayed
    private JPanel displayPanel = new JPanel();
    
    
    /*
     * This contructor sets important features of the generic ColorCalculator and adds relevant items to it.
     */
    public ColorCalculator()
    {
        setTitle("Conor's Color Calculator");
        setSize(800,600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);
        setJMenuBar(menuBar);
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
        hexField.addActionListener(new ActionListener()
                                       {
            public void actionPerformed(ActionEvent e)
            {
                int temp = (redSliderPanel.getValue() * 0x10000) + (grnSliderPanel.getValue() * 0x100) + (bluSliderPanel.getValue());
                try
                {
                    temp = Integer.parseInt(hexField.getText(),16);
                }
                catch(NumberFormatException f)
                {
                    JOptionPane.showMessageDialog(ColorCalculator.this, "The text entered is not a valid hex code.");
                }
                redSliderPanel.setValue(temp / 0x10000);
                grnSliderPanel.setValue((temp / 0x100) % 0x100);
                bluSliderPanel.setValue(temp % 0x100);
                resetDisplay();
            }
        });
        hexEntry.add(hexField);
        
        getContentPane().add(redSliderPanel);
        getContentPane().add(grnSliderPanel);
        getContentPane().add(bluSliderPanel);
        getContentPane().add(hexEntry);
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
        switch(side)
        {
            case 'L':
                redSliderPanel.setBounds(0,0,pane.getWidth()/3,pane.getHeight()/4);
                grnSliderPanel.setBounds(0,pane.getHeight()/4,pane.getWidth()/3,pane.getHeight()/4);
                bluSliderPanel.setBounds(0,pane.getHeight()/2,pane.getWidth()/3,pane.getHeight()/4);
                hexEntry.setBounds(0,pane.getHeight()*3/4,pane.getWidth()/3,pane.getHeight()/4);
                displayPanel.setBounds(pane.getWidth()/3,0,pane.getWidth()*2/3,pane.getHeight());
                break;
            case 'R':
                redSliderPanel.setBounds(pane.getWidth()*2/3,0,pane.getWidth()/3,pane.getHeight()/4);
                grnSliderPanel.setBounds(pane.getWidth()*2/3,pane.getHeight()/4,pane.getWidth()/3,pane.getHeight()/4);
                bluSliderPanel.setBounds(pane.getWidth()*2/3,pane.getHeight()/2,pane.getWidth()/3,pane.getHeight()/4);
                hexEntry.setBounds(pane.getWidth()*2/3,pane.getHeight()*3/4,pane.getWidth()/3,pane.getHeight()/4);
                displayPanel.setBounds(0,0,pane.getWidth()*2/3,pane.getHeight());
                break;
            case 'T':
                redSliderPanel.setBounds(0,0,pane.getWidth()/4,pane.getHeight()/3);
                grnSliderPanel.setBounds(pane.getWidth()/4,0,pane.getWidth()/4,pane.getHeight()/3);
                bluSliderPanel.setBounds(pane.getWidth()/2,0,pane.getWidth()/4,pane.getHeight()/3);
                hexEntry.setBounds(pane.getWidth()*3/4,0,pane.getWidth()/4,pane.getHeight()/3);
                displayPanel.setBounds(0,pane.getHeight()/3,pane.getWidth(),pane.getHeight()*2/3);
                break;
            case 'B':
                redSliderPanel.setBounds(0,pane.getHeight()*2/3,getWidth()/4,getHeight()/3);
                grnSliderPanel.setBounds(pane.getWidth()/4,pane.getHeight()*2/3,getWidth()/4,getHeight()/3);
                bluSliderPanel.setBounds(pane.getWidth()/2,pane.getHeight()*2/3,getWidth()/4,getHeight()/3);
                hexEntry.setBounds(pane.getWidth()*3/4,pane.getHeight()*2/3,getWidth()/4,getHeight()/3);
                displayPanel.setBounds(0,0,pane.getWidth(),pane.getHeight()*2/3);
                System.out.println(getWidth());
                break;
        }
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
        hexField.setText(toHex());
        displayPanel.setBackground(new Color(redSliderPanel.getValue(),grnSliderPanel.getValue(),bluSliderPanel.getValue()));
        repaint();
    }
    
    /*
     * Returns a string representation of the current hex color code
     * Ensures that output is six characters long, adding zeroes to left
     */
    public String toHex()
    {
        return(String.format("%6s", (Integer.toHexString((bluSliderPanel.getValue() + grnSliderPanel.getValue()*0x100 + redSliderPanel.getValue()*0x10000)))).replace(' ', '0'));
    }
    
    // This class is simply a panel containing a slider
    private class ColorSliderPanel extends JPanel
    {
        private JSlider slide = new JSlider(0,255);
        private String title;
        private JLabel label;
        
        /*
         * This constructor creates a panel with a slider in the center and a label below showing color and current value, in decimal
         * @param _title the label underneath the slider, telling the user which color it controls
         */
        public ColorSliderPanel(String _title)
        {
            setLayout(new GridLayout(2,2));
            
            slide.setMajorTickSpacing(64);
            slide.setPaintTicks(true);
            add(slide);
            setValue(127);
            
            title = _title;
            label = new JLabel(title + ": " + getValue(), JLabel.CENTER);
            add(label);
            
            // Calls resetDisplay if the slider is changed, updating hex field and color display
            slide.addChangeListener(new ChangeListener()
                                        {
                public void stateChanged(ChangeEvent e)
                {
                    ColorCalculator.this.resetDisplay();
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
     * This class is the menu bar in the color calculator
     * Contains file menu to quit and control position menu to change location of control panel
     */
    private class ColorMenuBar extends JMenuBar
    {
        private JMenu fileMenu = new JMenu("File");
        private JMenuItem quitItem = new JMenuItem("Quit");
        
        private JMenu controlPosition = new JMenu("Control Position");
        private JMenuItem leftSide = new JMenuItem("Left");
        private JMenuItem rightSide = new JMenuItem("Right");
        private JMenuItem topSide = new JMenuItem("Top");
        private JMenuItem bottomSide = new JMenuItem("Bottom");
        
        /*
         * This contructor creates the generic ColorMenuBar
         */
        public ColorMenuBar()
        {
            /*
             * If quit is clicked, program terminates.
             */
            quitItem.addActionListener(new ActionListener()
                                           {
                public void actionPerformed(ActionEvent e)
                {
                    System.exit(0);
                }
            });
            
            // Adding SideListeners to control position menu items, listeners that change value of ColorCalculator's char side
            leftSide.addActionListener(new SideListener('L'));
            
            rightSide.addActionListener(new SideListener('R'));
            
            topSide.addActionListener(new SideListener('T'));
            
            bottomSide.addActionListener(new SideListener('B'));
            
            fileMenu.add(quitItem);
            add(fileMenu);
            
            controlPosition.add(leftSide);
            controlPosition.add(rightSide);
            controlPosition.add(topSide);
            controlPosition.add(bottomSide);
            add(controlPosition);
        }
    }
    
    
    // This class is a listener that sets char side, added to control position items
    private class SideListener implements ActionListener
    {
        // char to set ColorCalculator's side to when listener is activated
        private char sideTo;
        
        /*
         * This contructor sets the value of the character to which side is set
         * @param _side A char L, R, T, or B corresponding to which side the button using the listener sets side to
         */
        public SideListener(char _side)
        {
            sideTo = _side;
        }
        
        /*
         * Sets ColorCalculator's side and recalculated positions based on that change
         */
        public void actionPerformed(ActionEvent e)
        {
            ColorCalculator.this.side = sideTo;
            ColorCalculator.this.setComponentPositions();
        }
    }
    
    /*
     * The main function creates an instance of the class
     */
    public static void main(String[] args)
    {
        new ColorCalculator();
    }
}