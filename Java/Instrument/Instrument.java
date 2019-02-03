import javax.sound.midi.*;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

class Instrument
{
    private JFrame frame;
    private JPanel winder;
    private KeyAdapter keyboi;
    private Synthesizer synth;
    private Receiver synthRcvr;
    
    private String[] keys = {"C","C#","D","D#","E","F","F#","G","G#","A","A#","B"};
    private String instrumentName = "Piano";
    
    private int key = 60;
    private int instrument = 0;
    private boolean low = false;
    private boolean minor = false;
    private boolean pianoRoll = false;
    
    private int tonic;
    private int third;
    
    private boolean qPressed = false;
    private boolean wPressed = false;
    private boolean ePressed = false;
    private boolean rPressed = false;
    
    private boolean uPressed = false;
    private boolean iPressed = false;
    private boolean oPressed = false;
    private boolean pPressed = false;
    private boolean semiPressed = false;
    private boolean bracketPressed = false;
    
    private boolean aPressed = false;
    private boolean sPressed = false;
    private boolean dPressed = false;
    private boolean fPressed = false;
    private boolean gPressed = false;
    private boolean hPressed = false;
    private boolean jPressed = false;
    private boolean kPressed = false;
    private boolean lPressed = false;
    private boolean aposPressed = false;
    private boolean yPressed = false;
    
    public static void main(String[] args)
    {
        new Instrument();
    }
    
    public Instrument()
    {
        try
        {
            synth = MidiSystem.getSynthesizer();
            synthRcvr = synth.getReceiver();
            synth.open();
        }
        catch(MidiUnavailableException e){System.out.println("midi unavailable bruh");}
        
        frame = new JFrame("Music Box");
        frame.setSize(new Dimension(600,50));
        frame.setVisible(true);
        frame.setLayout(null);
        winder = new JPanel()
        {
            public void addNotify() {
                super.addNotify();
                requestFocus();
            }
        };
        
        changeInstrument(instrument);
        reassessNotes();
        
        keyboi = new KeyAdapter(){
            public void keyPressed(KeyEvent e)
            {
                //dual-functional note keys
                if(e.getKeyChar()=='u' && !uPressed)
                {
                    uPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic + 8);
                    }
                    else
                    {
                        playNote(tonic);
                    }
                }
                if(e.getKeyChar()=='i' && !iPressed)
                {
                    iPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+10);
                    }
                    else
                    {
                        playNote(third);
                    }
                }
                if(e.getKeyChar()=='o' && !oPressed)
                {
                    oPressed = true;
                    
                    if(pianoRoll)
                    {
                        
                    }
                    else
                    {
                        playNote(tonic+7);
                    }
                }
                if(e.getKeyChar()=='p' && !pPressed)
                {
                    pPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+13);
                    }
                    else
                    {
                        playNote(tonic+11);
                    }
                }
                if(e.getKeyChar()==';' && !semiPressed)
                {
                    semiPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+14);
                    }
                    else
                    {
                        playNote(tonic+10);
                    }
                }
                if(e.getKeyChar()=='[' && !bracketPressed)
                {
                    bracketPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+15);
                    }
                    else
                    {
                        playNote(tonic+12);
                    }
                }
                
                //dual-functional modular keys
                if(e.getKeyChar()=='q' && !qPressed)
                {
                    qPressed = true;
                    reassessNotes();
                    
                    if(pianoRoll)
                    {
                        playNote(tonic-2);
                    }
                }
                if(e.getKeyChar()=='w' && !wPressed)
                {
                    wPressed = true;
                    reassessNotes();
                }
                if(e.getKeyChar()=='e' && !ePressed)
                {
                    ePressed = true;
                    reassessNotes();
                    if(pianoRoll)
                    {
                        playNote(tonic+1);
                    }
                }
                if(e.getKeyChar()=='r' && !rPressed)
                {
                    rPressed = true;
                    reassessNotes();
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+3);
                    }
                }
                
                //exclusively piano roll keys
                if(e.getKeyChar()=='a' && !aPressed)
                {
                    aPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic-1);
                    }
                }
                if(e.getKeyChar()=='s' && !sPressed)
                {
                    sPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic);
                    }
                }
                if(e.getKeyChar()=='d' && !dPressed)
                {
                    dPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+2);
                    }
                }
                if(e.getKeyChar()=='f' && !fPressed)
                {
                    fPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+4);
                    }
                }
                if(e.getKeyChar()=='g' && !gPressed)
                {
                    gPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+5);
                    }
                }
                if(e.getKeyChar()=='h' && !hPressed)
                {
                    hPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+7);
                    }
                }
                if(e.getKeyChar()=='j' && !jPressed)
                {
                    jPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+9);
                    }
                }
                if(e.getKeyChar()=='k' && !kPressed)
                {
                    kPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+11);
                    }
                }
                if(e.getKeyChar()=='l' && !lPressed)
                {
                    lPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+12);
                    }
                }
                if(e.getKeyChar()=='\'' && !aposPressed)
                {
                    aposPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+16);
                    }
                }
                if(e.getKeyChar()=='y' && !yPressed)
                {
                    yPressed = true;
                    
                    if(pianoRoll)
                    {
                        playNote(tonic+6);
                    }
                }
                
                //function keys
                if(e.getKeyChar()=='c')
                {
                    low = !low;
                    reassessNotes();
                }
                if(e.getKeyChar()=='m')
                {
                    pianoRoll = !pianoRoll;
                }
                if(e.getKeyChar()==' ' && !minor)
                {
                    minor = true;
                    reassessNotes();
                }
                if(e.getKeyChar()=='-')
                {
                    key--;
                    reassessNotes();
                    frame.setTitle("Music Box - Key of " + keys[key%12] + " on " + instrumentName);
                }
                if(e.getKeyChar()=='=')
                {
                    key++;
                    reassessNotes();
                    frame.setTitle("Music Box - Key of " + keys[key%12] + " on " + instrumentName);
                }
                
                //instrument selection keys
                if(e.getKeyChar()=='1')
                {
                    instrument = 0;
                    instrumentName = "Piano";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='2')
                {
                    instrument = 11;
                    instrumentName = "Vibraphone";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='3')
                {
                    instrument = 19;
                    instrumentName = "Organ";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='4')
                {
                    instrument = 24;
                    instrumentName = "Nylon-String Guitar";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='5')
                {
                    instrument = 30;
                    instrumentName = "Distorted Guitar";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='6')
                {
                    instrument = 45;
                    instrumentName = "Pizzicato Strings";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='7')
                {
                    instrument = 41;
                    instrumentName = "Viola";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='8')
                {
                    instrument = 80;
                    instrumentName = "Square Wave Synthesizer";
                    changeInstrument(instrument);
                }
                if(e.getKeyChar()=='9')
                {
                    instrument = 114;
                    instrumentName = "Steel Drums";
                    changeInstrument(instrument);
                }
            }
            
            public void keyReleased(KeyEvent e)
            {
                //dual functional note keys
                if(e.getKeyChar()=='u')
                {
                    uPressed = false;
                    if(pianoRoll)
                    {
                        endNote(tonic+8);
                    }
                    else
                    {
                        endNote(tonic);
                    }
                }
                if(e.getKeyChar()=='i')
                {
                    iPressed = false;
                    if(pianoRoll)
                    {
                        endNote(tonic+10);
                    }
                    else
                    {
                        endNote(third);
                    }
                }
                if(e.getKeyChar()=='o')
                {
                    oPressed = false;
                    if(pianoRoll)
                    {
                    }
                    else
                    {
                        endNote(tonic+7);
                    }
                }
                if(e.getKeyChar()=='p')
                {
                    pPressed = false;
                    if(pianoRoll)
                    {
                        endNote(tonic+13);
                    }
                    else
                    {
                        endNote(tonic+11);
                    }
                }
                if(e.getKeyChar()==';')
                {
                    semiPressed = false;
                    if(pianoRoll)
                    {
                        endNote(tonic+14);
                    }
                    else
                    {
                        endNote(tonic+10);
                    }
                }
                if(e.getKeyChar()=='[')
                {
                    bracketPressed = false;
                    if(pianoRoll)
                    {
                        endNote(tonic+15);
                    }
                    else
                    {
                        endNote(tonic+12);
                    }
                }
                
                //dual functional modular keys
                if(e.getKeyChar()=='q')
                {
                    qPressed = false;
                    reassessNotes();
                    if(pianoRoll)
                    {
                        endNote(tonic-2);
                    }
                }
                if(e.getKeyChar()=='w')
                {
                    wPressed = false;
                    reassessNotes();
                    if(pianoRoll)
                    {
                        
                    }
                }
                if(e.getKeyChar()=='e')
                {
                    ePressed = false;
                    reassessNotes();
                    if(pianoRoll)
                    {
                        endNote(tonic+1);
                    }
                }
                if(e.getKeyChar()=='r')
                {
                    rPressed = false;
                    reassessNotes();
                    if(pianoRoll)
                    {
                        endNote(tonic+3);
                    }
                }
                
                //exclusively piano roll keys
                if(e.getKeyChar()=='a')
                {
                    aPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic-1);
                    }
                }
                if(e.getKeyChar()=='s')
                {
                    sPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic);
                    }
                }
                if(e.getKeyChar()=='d')
                {
                    dPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+2);
                    }
                }
                if(e.getKeyChar()=='f')
                {
                    fPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+4);
                    }
                }
                if(e.getKeyChar()=='g')
                {
                    gPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+5);
                    }
                }
                if(e.getKeyChar()=='h')
                {
                    hPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+7);
                    }
                }
                if(e.getKeyChar()=='j')
                {
                    jPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+9);
                    }
                }
                if(e.getKeyChar()=='k')
                {
                    kPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+11);
                    }
                }
                if(e.getKeyChar()=='l')
                {
                    lPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+12);
                    }
                }
                if(e.getKeyChar()=='\'')
                {
                    aposPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+16);
                    }
                }
                if(e.getKeyChar()=='y')
                {
                    yPressed = false;
                    
                    if(pianoRoll)
                    {
                        endNote(tonic+6);
                    }
                }
                
                //function keys
                if(e.getKeyChar()==' ')
                {
                    minor = false;
                    reassessNotes();
                }
            }
        };
        
        winder.addKeyListener(keyboi);
        
        
        frame.getContentPane().add(winder);
        winder.setBounds(0,0,(int)frame.getContentPane().getSize().getWidth(),(int)frame.getContentPane().getSize().getHeight());
        //winder.setBackground(Color.RED);
        winder.setVisible(true);
    }
    
    public void reassessNotes()
    {
        endNote(tonic);
        endNote(third);
        endNote(tonic+7);
        endNote(tonic+10);
        endNote(tonic+11);
        endNote(tonic+12);
        
        tonic = key;
        
        if(low)
        {
            tonic -= 12;
        }
        
        if(!pianoRoll)
        {
            if(wPressed)
            {
                if(ePressed)
                {
                    if(rPressed)
                    {
                        tonic += 12;
                    }
                    else
                    {
                        tonic += 2;
                    }
                }
                else
                {
                    if(rPressed)
                    {
                        tonic += 11;
                    }
                    else
                    {
                        tonic += 5;
                    }
                }
            }
            else
            {
                if(ePressed)
                {
                    if(rPressed)
                    {
                        tonic += 4;
                    }
                    else
                    {
                        tonic += 7;
                    }
                }
                else
                {
                    if(rPressed)
                    {
                        tonic += 9;
                    }
                }
            }
            
            if(qPressed)
            {
                tonic += 1;
            }
            
            if(minor)
            {
                third = tonic+3;
            }
            else
            {
                third = tonic+4;
            }
            
            if(uPressed)
            {
                playNote(tonic);
            }
            if(iPressed)
            {
                playNote(third);
            }
            if(oPressed)
            {
                playNote(tonic+7);
            }
            if(pPressed)
            {
                playNote(tonic+11);
            }
            if(semiPressed)
            {
                playNote(tonic+10);
            }
            if(bracketPressed)
            {
                playNote(tonic+12);
            }
        }
    }
    
    public void playNote(int toneNum)
    {
        ShortMessage myMsg = new ShortMessage();
        // Play the note moderately loud
        // (velocity = 93)on channel 4 (zero-based).
        try{
            myMsg.setMessage(ShortMessage.NOTE_ON, 4, toneNum, 93); 
            synthRcvr.send(myMsg, -1); // -1 means no time stamp
        }
        catch(InvalidMidiDataException e){System.out.println("invalid midi data bruh");}
        
    }
    
    public void endNote(int toneNum)
    {
        ShortMessage myMsg = new ShortMessage();
        // Play the note moderately loud
        // (velocity = 93)on channel 4 (zero-based).
        try{
            myMsg.setMessage(ShortMessage.NOTE_OFF, 4, toneNum, 93); 
            synthRcvr.send(myMsg, -1); // -1 means no time stamp
        }
        catch(InvalidMidiDataException e){System.out.println("invalid midi data bruh");}
        
    }
    
    public void changeInstrument(int instr)
    {
        try
        {
            ShortMessage instrumentChange = new ShortMessage();
            instrumentChange.setMessage(ShortMessage.PROGRAM_CHANGE, 4, instr,0);
            synthRcvr.send(instrumentChange, -1);
            frame.setTitle("Music Box - Key of " + keys[key%12] + " on " + instrumentName);
        }
        catch(InvalidMidiDataException e){System.out.println("invalid midi data bruh");}
    }
}