import java.awt.Color;
import java.awt.Graphics;
import java.awt.GridLayout;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

import java.util.ArrayList;

import javax.swing.JButton;
import javax.swing.JColorChooser;
import javax.swing.JFileChooser;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;

import java.awt.event.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
/*
TODO
keyboard shortcuts
font style/size
*/


public class PiKazSO extends javax.swing.JFrame implements Runnable
{
    //private boolean isSaved;
    private File elifAnt;
    private PaintPanel pp;    
    public PiKazSO()
    {
        //isSaved = true;
        elifAnt = null;
        pp = new PaintPanel();
        try
        {
            int tryThis;
        }
        catch(NullPointerException ex)
        {
            //quack
        }
    }

    public void updateTitleBar()
    {
        //If no file, set to untitled | untitled*

        // (test) ? whatToDoIfTheTestIsTrue : whatToDoIfTheTestIsFalse
        String title;
        if(elifAnt == null)
        {
            title = "Untitled";
        }
        else
        {
            title = elifAnt.getAbsolutePath();
        }
        //String asterisk = pp.isSaved() ? "" : " *";
        //setTitle(title + asterisk);
    }

    //return true if it is ok to continue the operation.
    //return false if the dangerous operation should be cancelled.
    private boolean preventDataLoss()
    {
        //if(pp.isSaved()) { return true; }
        //now we know that it hasn't been saved...  prompt the user 
        switch(JOptionPane.showConfirmDialog(this, "Do you want to save your changes?"))
        {
            case JOptionPane.CANCEL_OPTION:
                return false;
            case JOptionPane.NO_OPTION:
                return true;
            case JOptionPane.YES_OPTION:
                return dontDie(false);
        }
        return false;
    }

    //Save
    private boolean dontDie(boolean isSaveAs)
    {
        //This is the save as component...  we want to run this when?
        if(isSaveAs || elifAnt == null)
        {
            JFileChooser jfc = new JFileChooser();
            int response = jfc.showSaveDialog(this);
            if(response == JFileChooser.CANCEL_OPTION)
            {
                return false;
            }
            if(response == JFileChooser.ERROR_OPTION)
            {
                return false;
            }
            elifAnt = jfc.getSelectedFile();
            if(elifAnt.exists())
            {
                switch(JOptionPane.showConfirmDialog(this, elifAnt.getAbsolutePath() + " exists, are you sure you want to overwrite it?"))
                {
                    case JOptionPane.NO_OPTION:
                        return false;
                    case JOptionPane.CANCEL_OPTION:
                        return false;
                    case JOptionPane.YES_OPTION:
                        break;
                }
            }
        }

        //if(response == JFileChooser.CANCEL_OPTION)
        //once we get here, we know the user chose a file and clicked Save.
        try
        {
            ObjectOutputStream ooze = new ObjectOutputStream(new FileOutputStream(elifAnt));
            
            //ooze.writeObject(pp.getScurves());
            ooze.writeObject(pp.getBackgroundColor());
            ooze.writeObject(pp.getPenColor());
            //ooze.writeObject(pp.getPenTip());
            //ooze.writeInt(pp.getPenWidth());
            ooze.close();

            //pp.setIsSaved(true);
            updateTitleBar();
        }
        catch(IOException ex)
        {
            ex.printStackTrace();
            return false;
        }
            
        return true;
    }

    //This is the open a file method.
    private boolean itsAlive()
    {
        if(!preventDataLoss()) { return false; }

        //BufferedReader
        //File
        //Make sure it exists
        JFileChooser jfc = new JFileChooser();
        int response = jfc.showOpenDialog(this);
        if(response == JFileChooser.CANCEL_OPTION)
        {
            return false;
        }
        if(response == JFileChooser.ERROR_OPTION)
        {
            return false;
        }
        
        //now we know they really want to open this file.
        elifAnt = jfc.getSelectedFile();
        
        if(!elifAnt.exists()) { return false; }

        try
        {
            //TODO make this work for our picture.            
            //BufferedReader bringItOn = new BufferedReader(new FileReader(elifAnt));
            ObjectInputStream oui = new ObjectInputStream(new FileInputStream(elifAnt));
            //pp.setScurves((ArrayList<Curve>)oui.readObject());
            pp.setBackgroundColor((Color)oui.readObject());
            pp.setPenColor((Color)oui.readObject());
            //pp.setPenTip((Tip)oui.readObject());
            //pp.setPenWidth(oui.readInt());
            oui.close(); 
            pp.repaint();
        }
        catch(IOException ex)
        {
            ex.printStackTrace();
            return false;
        }
        catch(ClassNotFoundException ex)
        {
            ex.printStackTrace();
            return false;
        }
        
        return true;

    }

    private JMenu makeFileMenu()
    {
        JMenu fileMenu = new JMenu("File");

        JMenuItem newItem = new JMenuItem("New");
        JMenuItem openItem = new JMenuItem("Open...");
        JMenuItem saveItem = new JMenuItem("Save");
        JMenuItem saveAsItem = new JMenuItem("Save As...");
        JMenuItem quitItem = new JMenuItem("Quit");

        openItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                itsAlive();
            }
        });
        saveItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                dontDie(false);
            }
        });
        saveAsItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                dontDie(true);
            }
        });
        quitItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                if(preventDataLoss())
                {
                    System.exit(0);
                }
            }
        });
        
        fileMenu.add(openItem);
        fileMenu.add(saveItem);
        fileMenu.add(saveAsItem);
        fileMenu.add(quitItem);
        fileMenu.setDelay(40);
        return fileMenu;
    }

    private JMenu makeEditMenu()
    {
        JMenu editMenu = new JMenu("Edit");
        JMenuItem saItem = new JMenuItem("Select All");
        JMenuItem cutItem = new JMenuItem("Cut");
        JMenuItem copyItem = new JMenuItem("Copy");
        JMenuItem pasteItem = new JMenuItem("Paste");
        JMenuItem clearItem = new JMenuItem("Clear All");
        clearItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.clear();
            }
        });
        //saItem.addActionListener(e -> alfred.selectAll() );
        //cutItem.addActionListener(e -> alfred.cut() );
        //copyItem.addActionListener(e -> alfred.copy() );
        //pasteItem.addActionListener(e -> alfred.paste() );

        editMenu.add(saItem);
        editMenu.add(cutItem);
        editMenu.add(copyItem);
        editMenu.add(pasteItem);
        editMenu.add(clearItem);
        editMenu.setDelay(40);
        return editMenu;
    }

    private JMenu makeStampMenu()
    {
        JMenu stampMenu = new JMenu("Stamp");
        
        

        return stampMenu;
    }

    private JMenu makeToolsMenu()
    {
        JMenu jim = new JMenu("Tools");
        JMenu tipMenu = new JMenu("Tip");
        JMenuItem buttItem = new JMenuItem("Butt");
        JMenuItem roundItem = new JMenuItem("Round");
        JMenuItem squareItem = new JMenuItem("Square");

        buttItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.setPenTip(Tip.BUTT);
            }
        });
        roundItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.setPenTip(Tip.ROUND);
            }
        });
        squareItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.setPenTip(Tip.SQUARE);
            }
        });

        JMenu chooseMenu = new JMenu("Custom Width...");
        JTextField chooseItem = new JTextField(4);
        chooseItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                try
                {
                    //int newWidth = Integer.parseInt(chooseItem.getText());
                    //pp.setPenWidth(newWidth);
                }
                catch(NumberFormatException ex)
                {
                    //moo
                }
            }
        });
        chooseMenu.add(chooseItem);
        tipMenu.add(buttItem);
        tipMenu.add(roundItem);
        tipMenu.add(squareItem);
        jim.add(tipMenu);
        jim.add(chooseMenu);
        return jim;
        
    }

    private JMenu makeColorMenu()
    {
        JMenu jim = new JMenu("Color");
        JMenu penu = new JMenu("Pen");
        JMenu benu = new JMenu("Background");
        
        jim.add(penu); 
        jim.add(benu); 

        penu.add(new ColorSelectorMenuItem());
        final JMenuItem chooseItem = new JMenuItem("Choose Color...");
        
        chooseItem.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                Color newColor =  JColorChooser.showDialog(chooseItem, "Pick a color, any color (as long as it is one of the 16M colors available)", pp.getPenColor());
                pp.setPenColor(newColor);
            }
        });
        
        jim.add(chooseItem);
        return jim;
    }
    
    private void makeMenus()
    {
        JMenuBar jmb = new JMenuBar();
        jmb.add(makeFileMenu());
        jmb.add(makeEditMenu());
        jmb.add(makeToolsMenu());
        jmb.add(makeColorMenu());
        jmb.add(makeStampMenu());
        JMenuItem bob = new JMenuItem("ReColor");
        bob.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.reColor();
            }
        });
        jmb.add(bob);
        JMenuItem export = new JMenuItem("Export");
        export.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e)
            {
                //pp.export();
            }
        });
        jmb.add(export);
        setJMenuBar(jmb);
    }

    public void run()
    {
        setSize(800, 600);
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e){
                if(preventDataLoss())
                {
                    System.exit(0);
                }
            }
        });

        //getContentPane().add(new JScrollPane(pp));    
        getContentPane().add(pp);    
        updateTitleBar();
        makeMenus();
        
        setVisible(true);
    }

    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater( new PiKazSO() );
    }

    class ColorSelectorMenuItem extends JPanel
    {
        public ColorSelectorMenuItem()
        {
            setLayout(new GridLayout(2, 4));
            add(new ColorButton(Color.WHITE));
            add(new ColorButton(Color.RED));
            add(new ColorButton(Color.BLUE));
            add(new ColorButton(Color.GREEN));
            add(new ColorButton(Color.ORANGE));
            add(new ColorButton(Color.YELLOW));
            add(new ColorButton(Color.CYAN));
            add(new ColorButton(Color.MAGENTA));
        }

        
    }

    class ColorButton extends JPanel implements MouseListener
    {
        Color color;
        //Some kind of function for which color to set.
        public ColorButton(Color c)
        {
            color = c;
            addMouseListener(this);
//            addActionListener(e -> {
//                pp.setPenColor(color);
//                setBackground(color.darker());
//                ColorButton.this.repaint();
//            });
//            setBackground(color);
//            setOpaque(true);
//            setBorderPainted(false);
        }
        public void mouseEntered(MouseEvent e)  {} 
        public void mouseExited(MouseEvent e)   {} 
        public void mousePressed(MouseEvent e)  {} 
        public void mouseReleased(MouseEvent e) {} 
        public void mouseClicked(MouseEvent e)  
        {
            pp.setPenColor(color);
            
        }
        @Override
        public void paintComponent(Graphics g)
        {
            super.paintComponent(g);
            g.setColor( color );
            g.fillRect(0,0, getWidth(), getHeight());
        }
    }


}