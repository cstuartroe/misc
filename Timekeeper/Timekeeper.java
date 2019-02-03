import java.util.*;
import javax.swing.*;
import java.awt.*;

public class Timekeeper implements Runnable
{
    private Calendar current;
    private long beginInMillis;
    private long millisSinceBegin;
    private int daysSinceBegin;
    private int metricSecondsSinceMidnight;
    private ArrayList<String> newCalendar;
    private JFrame frame;
    private JPanel panel;
    private JLabel label;
    private JLabel normalDate;
    private ArrayList<Color> seasonTheme;
    
    public static void main(String[] args)
    {
        (new Thread(new Timekeeper())).start();
    }
    
    public Timekeeper()
    {
        //current = Calendar.getInstance(TimeZone.getTimeZone("GMT"));
        //current.add(Calendar.MILLISECOND, TimeZone.getDefault().getOffset(current.getTimeInMillis()));
        current = Calendar.getInstance();
        
        Calendar begin = Calendar.getInstance();
        int beginYear = current.get(1);
        beginYear -= beginYear % 4;
        begin.set(beginYear,2,21,0,0,0);
        beginInMillis = begin.getTimeInMillis();
        
        newCalendar = new ArrayList<String>(1440);
        seasonTheme = new ArrayList<Color>(1440);
        String[] seasons = {"Early Spring","Late Spring","Early Summer","Late Summer","Early Autumn","Late Autumn","Early Winter", "Late Winter"};
        String[] weeks = {"First", "Second", "Third", "Fourth", "Fifth"};
        String[] weekdays = {"Sunday", "Moonday", "Mercuryday", "Venusday", "Earthday", "Marsday", "Jupiterday", "Saturnday", "Starday"};
        String[] seasonHeaders = {"Spring Equinox","Summer Solstice","Autumn Equinox","Winter Solstice"};
        Color[] seasonColors = {new Color(34,255,153), new Color(255,255,255), new Color(187,85,51), new Color(0,0,0)};
        
        for(int i = 0; i<1440; i++)
        {
            newCalendar.add(weeks[(i/9)%5] + " " + weekdays[i%9] + " of " + seasons[(i/45)%8]);
            seasonTheme.add(seasonColors[(i/90)%4]);
        }
        
        for(int i = 0; i<16; i++)
        {
            newCalendar.add(i*91, seasonHeaders[i%4]);
            seasonTheme.add(i*91, seasonColors[i%4]);
        }
        
        for(int i = 0; i<4; i++)
        {
            newCalendar.add(i*365, "New Years Day");
            seasonTheme.add(i*365, seasonColors[0]);
        }
        
        for(int i = 0; i<1460; i++)
        {
            newCalendar.set(i, newCalendar.get(i) + " in the Year " + Integer.toString(beginYear + 3346 + i/365));
        }
        
        newCalendar.add(913, "Leap Day in the Year " + Integer.toString(beginYear + 3348));
        seasonTheme.add(913, seasonColors[2]);
        
        frame = new JFrame();
        frame.setSize(800,100);
        frame.setVisible(true);
        frame.setResizable(false);
        
        panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        frame.add(panel);
        
        label = new JLabel();
        label.setAlignmentX(Component.CENTER_ALIGNMENT);
        label.setForeground(new Color(255,255,102));
        label.setFont(new Font("Arabic Typesetting", Font.BOLD, 30));
        panel.add(label);
        
        normalDate = new JLabel();
        normalDate.setAlignmentX(Component.CENTER_ALIGNMENT);
        normalDate.setForeground(new Color(255,255,102));
        normalDate.setFont(new Font("Arabic Typesetting", Font.BOLD, 25));
        panel.add(normalDate);
    }
    
    public void run()
    {
        while(1==1)
        {
            //current = Calendar.getInstance(TimeZone.getTimeZone("GMT"));
            current = Calendar.getInstance();
            
            //current.add(Calendar.MILLISECOND, TimeZone.getDefault().getOffset(current.getTimeInMillis()));
        
            millisSinceBegin = current.getTimeInMillis() - beginInMillis;
            daysSinceBegin = (int)(millisSinceBegin/86400000l);
            metricSecondsSinceMidnight = (int)((millisSinceBegin%86400000l)/864l);
            
            String calendarDay = newCalendar.get(daysSinceBegin);
            String metricTime = Integer.toString(metricSecondsSinceMidnight);
            metricTime = "00000".substring(metricTime.length()) + metricTime;
            metricTime = metricTime.substring(0,1) + ":" + metricTime.substring(1,3) + ":" + metricTime.substring(3);
            
            panel.setBackground(seasonTheme.get(daysSinceBegin));
            if(seasonTheme.get(daysSinceBegin).equals(new Color(255,255,255)))
            {
                label.setForeground(new Color(238,238,85));
                normalDate.setForeground(new Color(238,238,85));
            }
            label.setText(metricTime + " " + calendarDay);
            normalDate.setText(current.getTime().toString());
            
            panel.revalidate();
            panel.repaint();
            
            try
            {
                Thread.sleep(20);
            }
            catch(InterruptedException e){}
        }
    }
}