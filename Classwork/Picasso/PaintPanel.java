import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.ArrayList;
import javax.swing.JPanel;
public class PaintPanel extends JPanel implements MouseListener, MouseMotionListener
{
    private Color penColor;
    private Color backgroundColor;
    private ArrayList<Point> pointy;

    public PaintPanel(Color fgc, Color bgc)
    {
        pointy = new ArrayList<Point>();
        penColor = fgc;
        backgroundColor = bgc;
        addMouseListener(this);
        addMouseMotionListener(this);
    }

    public PaintPanel()
    {
        this( Color.BLACK, new Color(0xCD853F) );
    }
    
    public void draw(Graphics g)
    {
        Graphics2D g2d = (Graphics2D) g;
        g2d.setColor(penColor);
        for(int i = 0; i < pointy.size() - 1; i++)
        {
            
            g2d.drawLine(pointy.get( i ).x, pointy.get( i ).y,
                         pointy.get(i+1).x, pointy.get(i+1).y );
            
        }
    }    

    public void mouseDragged(MouseEvent e)
    { 
        pointy.add(e.getPoint()); 
        repaint();
    }
    public void mouseMoved(MouseEvent e)   { /* System.out.println( "moved: "   + e.getPoint());*/ }
    public void mouseClicked(MouseEvent e) { /* System.out.println( "clicked: " + e.getPoint());*/ } 
    public void mouseEntered(MouseEvent e) { /* System.out.println( "entered: " + e.getPoint());*/ }
    public void mouseExited(MouseEvent e)  { /* System.out.println( "exited: "  + e.getPoint());*/ } 
    public void mousePressed(MouseEvent e) 
    { 
        pointy.add(e.getPoint()); 
        repaint();
    }
    public void mouseReleased(MouseEvent e)
    { 
        pointy.add(e.getPoint()); 
        repaint();
    }

    public void setPenColor(Color c)
    {
        penColor = c;
    }
    public Color getPenColor()
    {
        return penColor;
    }
    public void setBackgroundColor(Color c)
    {
        backgroundColor = c;
    }
    public Color getBackgroundColor()
    {
        return backgroundColor;
    }


    @Override
    public void paintComponent(Graphics g)
    {
        //This should be the first line of every paint component method
        //that you override
        super.paintComponent(g);
        g.setColor( backgroundColor );
        g.fillRect(0,0, getWidth(), getHeight());
        draw(g);
    }
}