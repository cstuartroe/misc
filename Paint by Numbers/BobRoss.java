import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JColorChooser;

import java.awt.Color;
import java.awt.Container;
import java.awt.GridLayout;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;


public class BobRoss extends JFrame implements Runnable
{
    private ColorPanel currentPanel;
    private ColorPanel one;
    private ColorPanel two;
    private ColorPanel three;
    
    public BobRoss(String title)
    {
        super(title);
        
        one = new ColorPanel(Color.RED);
        two = new ColorPanel();
        three = new ColorPanel(Color.BLUE);
        currentPanel = one;
    }
    
    public JMenuItem makePanelMenuItem(String name, ColorPanel whatToDo)
    {
        JMenuItem jimmy = new JMenuItem(name);
        jimmy.addActionListener( e -> currentPanel = whatToDo );
        return jimmy;
    }
    
    public void makeMenus()
    {
        JMenuBar jmb = new JMenuBar();
        
        JMenu fileMenu = new JMenu("File");
        JMenu panelMenu = new JMenu("Panel");
        JMenu colourMenu = new JMenu("Colour");
        
        JMenuItem quitItem = new JMenuItem("Quit");
        
        jmb.add(fileMenu);
        jmb.add(panelMenu);
        jmb.add(colourMenu);
        
        quitItem.addActionListener(e -> {
            System.exit(0);
        });
        
        fileMenu.add(quitItem);
        panelMenu.add(makePanelMenuItem("Left", one));
        panelMenu.add(makePanelMenuItem("Middle", two));
        panelMenu.add(makePanelMenuItem("Right", three));
        
        JMenuItem colorChooserItem = new JMenuItem("Color Chooser");
        
        colorChooserItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                currentPanel.setColor((new JColorChooser()).showDialog(colorChooserItem, "Colors!", currentPanel.getColor()));
                currentPanel.repaint();
            }
        });
        
        colourMenu.add(new ColorMenuItem("Red", Color.RED));
        colourMenu.add(new ColorMenuItem("Yellow", Color.YELLOW));
        colourMenu.add(new ColorMenuItem("Blue", Color.BLUE));
        colourMenu.add(new ColorMenuItem("Magenta", Color.MAGENTA));
        colourMenu.add(colorChooserItem);
        
        setJMenuBar(jmb);
        
    }
    
    public void run()
    {
        setSize(800,600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        makeMenus(); 
        
        Container cp = getContentPane();
        cp.setLayout(new GridLayout(1, 3));
        
        
        cp.add(one);
        cp.add(two);
        cp.add(three);
        
        setVisible(true);
    }
    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new BobRoss("Paint By Numbers"));
    }
    
    class ColorMenuItem extends JMenuItem
    {
        Color color;
        public ColorMenuItem(String label, Color c)
        {
            super(label);
            color = c;
            addActionListener(new ActionListener(){
                public void actionPerformed(ActionEvent e)
                {
                    currentPanel.setColor(c);
                    currentPanel.repaint();
                    //Go make sure we have the correct namespace to repaint the 
                    //whole frame.
                    //BobRoss.this.repaint();
                    
                }});
        }
    }
}