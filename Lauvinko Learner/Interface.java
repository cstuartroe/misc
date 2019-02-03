import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class Interface
{
    JFrame frame;
    
    JPanel startMenuPanel;
    JPanel startButtonLearn;
    
    JPanel lessonsPanel;
    JPanel lessonOnePanel;
    
    public static void main(String[] args)
    {
        new Interface();
    }
    
    public Interface()
    {
        frame = new JFrame("Learn Lauvinko!");
        frame.setSize(new Dimension(1018,647));
        frame.setVisible(true);
        frame.setLayout(null);
        System.out.println(frame.getContentPane().getSize());
        
        startMenuPanel = new JPanel();
        startMenuPanel.setLayout(null);
        startButtonLearn = new JPanel();
        startButtonLearn.add(new JLabel("Learn!"));
        startButtonLearn.setBackground(Color.WHITE);
        startButtonLearn.addMouseListener(new MouseAdapter(){
            public void mousePressed(MouseEvent e)
            {
                frame.remove(startMenuPanel);
                startMenuPanel.setVisible(false);
                openLessons();
            }
        });
        startMenuPanel.add(startButtonLearn);
        
        lessonsPanel = new JPanel();
        lessonsPanel.setLayout(new GridLayout(6,6));
        lessonsPanel.setVisible(false);
        lessonOnePanel = new JPanel();
        lessonOnePanel.add(new JLabel("1 Basics"));
        lessonOnePanel.setBackground(Color.WHITE);
        lessonOnePanel.addMouseListener(new MouseAdapter(){
            public void mousePressed(MouseEvent e)
            {
                System.out.println("ey");
            }
        });
        lessonsPanel.add(lessonOnePanel);
        
        openStartMenu();
        
        frame.addComponentListener(new ComponentAdapter(){
            public void componentResized(ComponentEvent e)
            {
                Dimension contentPaneSize = frame.getContentPane().getSize();
                
                if(startMenuPanel.isVisible())
                {
                    startMenuPanel.setBounds(0,0,(int) contentPaneSize.getWidth(),(int) contentPaneSize.getHeight());
                    startButtonLearn.setBounds((int) contentPaneSize.getWidth()/4,(int) contentPaneSize.getHeight()*4/10,(int) contentPaneSize.getWidth()/2,(int) contentPaneSize.getHeight()/10);
                }
                
                if(lessonsPanel.isVisible())
                {
                    lessonsPanel.setBounds(0,0,(int) contentPaneSize.getWidth(),(int) contentPaneSize.getHeight());
                }
                
                
                frame.revalidate();
                frame.repaint();
            }
        });
        
        Dimension contentPaneSize = frame.getContentPane().getSize();
        startMenuPanel.setBounds(0,0,(int) contentPaneSize.getWidth(),(int) contentPaneSize.getHeight());
        startButtonLearn.setBounds((int) contentPaneSize.getWidth()/4,(int) contentPaneSize.getHeight()*4/10,(int) contentPaneSize.getWidth()/2,(int) contentPaneSize.getHeight()/10);
    }
    
    public void openStartMenu()
    {
        frame.add(startMenuPanel);
        Dimension contentPaneSize = frame.getContentPane().getSize();
        startMenuPanel.setBounds(0,0,(int) contentPaneSize.getWidth(),(int) contentPaneSize.getHeight());
        startMenuPanel.setVisible(true);
        //startButtonLearn.setVisible(true);
        
        frame.revalidate();
        frame.repaint();
    }
    
    public void openLessons()
    {
        frame.add(lessonsPanel);
        Dimension contentPaneSize = frame.getContentPane().getSize();
        lessonsPanel.setBounds(0,0,(int) contentPaneSize.getWidth(),(int) contentPaneSize.getHeight());
        lessonsPanel.setVisible(true);
        //lessonOnePanel.setVisible(true);
        
        
        frame.revalidate();
        frame.repaint();
    }
}