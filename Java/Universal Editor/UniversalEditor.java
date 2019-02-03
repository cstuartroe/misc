import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import javax.swing.JFileChooser;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;

/*
TODO
cut, copy, paste
select all
keyboard shortcuts
font style/size
title bar
***
prevent data loss
***



*/


public class UniversalEditor extends javax.swing.JFrame implements Runnable
{
    JTextArea alfred;
    public UniversalEditor()
    {
        alfred = new JTextArea();
    }

    private boolean dontDie()
    {
        //what file
        //what to write.
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
        //if(response == JFileChooser.CANCEL_OPTION)
        //once we get here, we know the user chose a file and clicked Save.
        try
        {
            File myFile = jfc.getSelectedFile();
            BufferedWriter buffy = new BufferedWriter(new FileWriter(myFile));
            buffy.write(alfred.getText());
            buffy.close();
        }
        catch(IOException ex)
        {
            ex.printStackTrace();
            return false;
        }
            
        return true;
    }

    private boolean itsAlive()
    {
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
        File myFile = jfc.getSelectedFile();
        
        if(!myFile.exists()) { return false; }
        //now we know the file exists.

        try
        {
            BufferedReader bringItOn = new BufferedReader(new FileReader(myFile));
            StringBuffer sb = new StringBuffer();
            int something = bringItOn.read();
            while(something != -1)
            {
                sb.append((char)something);
                something = bringItOn.read();
            }
            alfred.setText(sb.toString());

        }
        catch(IOException ex)
        {
            ex.printStackTrace();
            return false;
        }
        
        return true;

    }

    private JMenu makeFileMenu()
    {
        JMenu fileMenu = new JMenu("File");

        JMenuItem openItem = new JMenuItem("Open...");
        JMenuItem saveItem = new JMenuItem("Save");
        JMenuItem quitItem = new JMenuItem("Quit");

        openItem.addActionListener(e -> itsAlive());
        saveItem.addActionListener(e -> dontDie());
        quitItem.addActionListener(e -> System.exit(0));
        
        fileMenu.add(openItem);
        fileMenu.add(saveItem);
        fileMenu.add(quitItem);

        return fileMenu;
    }

    private JMenu makeEditMenu()
    {
        JMenu editMenu = new JMenu("Edit");

        return editMenu;
    }

    private void makeMenus()
    {
        JMenuBar jmb = new JMenuBar();
        jmb.add(makeFileMenu());
        jmb.add(makeEditMenu());
        setJMenuBar(jmb);
    }

    public void run()
    {
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setTitle("depends on mm");
        makeMenus();
        
        //allow alfred to wrap batman
        //around lines
        alfred.setLineWrap(true);
        getContentPane().add( new JScrollPane(alfred) );

        setVisible(true);
    }

    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater( new UniversalEditor() );
    }
}