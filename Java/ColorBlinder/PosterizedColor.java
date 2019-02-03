import java.awt.*;

public class PosterizedColor
{
    int red;
    int grn;
    int blu;
    
    public PosterizedColor(int _r, int _g, int _b, boolean isntPosterized)
    {
        if(isntPosterized)
        {
            red = _r + 43;
            red /= 85;
            grn = _g + 43;
            grn /= 85;
            blu = _b + 43;
            blu /= 85;
        }
        else
        {
            red = _r;
            grn = _g;
            blu = _b;
        }
    }
    
    public PosterizedColor(Color c)
    {
        this(c.getRed(), c.getGreen(), c.getBlue(), true);
    }
    
    public PosterizedColor(int val)
    {
        red = val / 16;
        val %= 16;
        grn = val / 4;
        val %= 4;
        blu = val;
    }
    
    public Color getColor()
    {
        return new Color(red * 85, grn * 85, blu * 85);
    }
    
    public int getRed()
    {
        return (red * 85);
    }
    
    public int getGreen()
    {
        return (grn * 85);
    }
    
    public int getBlue()
    {
        return (blu * 85);
    }
    
    public Byte getByte()
    {
        return (byte)(red * 0b10000 + grn * 0b100 + blu);
    }
}