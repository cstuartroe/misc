import java.util.*;
import javax.swing.*;
import java.awt.*;

public class TrinaryLogicComponent
{
    private Tryte[] hardDrive = new Tryte[27];
    private Tryte cursor = new Tryte(0);
    private String output;
    private TryteDisplay displayFrame;
    
    public TrinaryLogicComponent()
    {
        for(int i = 0; i < 27; i++)
        {
            hardDrive[i] = new Tryte(0);
        }
        displayFrame = new TryteDisplay();
    }
    
    public void analyze(String inputLine)
    {
        output = "";
        ArrayList<Tryte> commandSet = new ArrayList<Tryte>();
        for(int i = 0; i < inputLine.length(); i++)
        {
            commandSet.add(new Tryte(inputLine.charAt(i)));
        }
        Tryte commandCursor = new Tryte(0);
        while(commandCursor.toInt() < commandSet.size())
        {
            read(commandSet.get(commandCursor.toInt()));
            commandCursor = Tryte.add(commandCursor, new Tryte(1));
            displayFrame.refreshText();
        }
        output += "\n";
    }
    
    public void read(Tryte t)
    {
        boolean reading = true;
        
        while(reading)
        {
            setTryte(Tryte.add(getTryte(), new Tryte(t.getTrit(-1).toInt())));
            setCursor(Tryte.add(getCursor(), new Tryte(t.getTrit(0).toInt())));
            switch(t.getTrit(1).toChar())
            {
                case '-':
                    output += getTryte().toChar();
                    reading = false;
                    break;
                case '0':
                    reading = false;
                    break;
                case '+':
                    t = getTryte();
                    break;
            }
        }
    }
    
    private class TryteDisplay extends JFrame
    {
        JTextArea display;
        
        public TryteDisplay()
        {
            setSize(115,650);
            //setTitle("Hard Drive");
            setResizable(false);
            
            display = new JTextArea();
            display.setEditable(false);
            display.setFont(new Font("Courier New",Font.BOLD,20));
            
            refreshText();
            add(display);
            setVisible(true);
        }
        
        public void refreshText()
        {
            display.setText("");
            for(int i = -13; i <= 13; i++)
            {
                char cursorHere;
                if(TrinaryLogicComponent.this.cursor.toInt() == i)
                {
                    cursorHere = '<';
                }
                else
                {
                    cursorHere = ' ';
                }
                display.append(new Tryte(i).toString() + new Tryte(i).toChar() + " " + TrinaryLogicComponent.this.hardDrive[i + 13].toString() + TrinaryLogicComponent.this.hardDrive[i + 13].toChar() + cursorHere + "\n");
                repaint();
            }
        }
    }
    
    public Tryte getTryte()
    {
        return hardDrive[cursor.toInt() + 13];
    }
    
    public void setTryte(Tryte value)
    {
        hardDrive[cursor.toInt() + 13] = value;
    }
    
    public Tryte getCursor()
    {
        return cursor;
    }
    
    public void setCursor(Tryte value)
    {
        cursor = value;
    }
    
    public String getOutput()
    {
        return output;
    }
    
    public void setOutput(String value)
    {
        output = value;
    }
}