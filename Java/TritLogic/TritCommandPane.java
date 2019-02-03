import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class TritCommandPane extends JFrame
{
    private JTextArea displayField;
    private JTextField entryField;
    private TrinaryLogicComponent tlc;
    
    public TritCommandPane()
    {
        setSize(500,300);
        setResizable(false);
        setLayout(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setTitle("Trit Programming Terminal");
        
        displayField = new JTextArea();
        displayField.setFont(new Font("Courier New",Font.BOLD,20));
        displayField.setAlignmentY(Component.BOTTOM_ALIGNMENT);
        displayField.setEditable(false);
        displayField.setLineWrap(true);
        displayField.setBackground(new Color(205,205,255));
        JScrollPane scroll = new JScrollPane(displayField);
        scroll.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
        scroll.setBounds(0,0,494,212);
        add(scroll);
        
        entryField = new JTextField();
        entryField.setFont(new Font("Courier New",Font.BOLD,20));
        entryField.setBounds(0,212,494,60);
        entryField.setText(">>>");
        entryField.addActionListener(new ActionListener()
                                         {
            public void actionPerformed(ActionEvent e)
            {
                String inputLine = Tryte.toAlphaspace(entryField.getText());
                if(!inputLine.isEmpty())
                {
                    displayField.append(">>>" + inputLine);
                    tlc.analyze(inputLine);
                    displayField.append(tlc.getOutput());
                }
                entryField.setText(">>>");
            }
        });
        add(entryField);
        
        tlc = new TrinaryLogicComponent();
        
        setVisible(true);
        System.out.println(getContentPane().getSize());
    }
    
    public static void main(String[] args)
    {
        new TritCommandPane();
    }
}