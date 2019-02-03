import java.awt.Color;
import java.awt.Graphics;
import javax.swing.JPanel;
import java.util.Random;
public class ColorPanel extends JPanel
{
    private Color currentColor;

    public ColorPanel(Color c)
    {
        currentColor = c;
    }

    public ColorPanel()
    {
        this( new Color(0xCD853F) );
    }

    public void setColor(Color c)
    {
        currentColor = c;
    }
    public Color getColor()
    {
        return currentColor;
    }

    @Override
    public void paintComponent(Graphics g)
    {
        //This should be the first line of every paint component method
        //that you override
        super.paintComponent(g);

        g.setColor( currentColor );
        g.fillRect(0,0, getWidth(), getHeight());
    }
}