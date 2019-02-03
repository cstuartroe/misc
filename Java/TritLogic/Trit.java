public class Trit
{
    private int state;
    private static char[] charvals = {'-','0','+'};
    
    public Trit(int x)
    {
        if(x < 0)
        {
            state = -1;
        }
        else if(x > 0)
        {
            state = 1;
        }
        else
        {
            state = 0;
        }
    }
    
    public Trit(char c)
    {
        if(c == '-')
        {
            state = -1;
        }
        else if(c == '+')
        {
            state = 1;
        }
        else
        {
            state = 0;
        }
    }
    
    public static Trit add(Trit first, Trit second)
    {
       if(first.toInt() == second.toInt())
       {
           return(new Trit(first.toInt() * -1));
       }
       else
       {
           return(new Trit(first.toInt() + second.toInt()));
       }
    }
    
    public static Trit add(Trit[] trits)
    {
        Trit out = new Trit(0);
        for(Trit t : trits)
        {
            out = Trit.add(out, t);
        }
        return out;
    }
    
    public static Trit mlt(Trit first, Trit second)
    {
        if(first.toInt() == 1)
        {
            return(new Trit(second.toInt()));
        }
        else if(first.toInt() == -1)
        {
            return(new Trit(second.toInt() * -1));
        }
        else
        {
            return(new Trit(0));
        }
    }
    
    public static Trit mlt(Trit[] trits)
    {
        Trit out = new Trit(0);
        for(Trit t : trits)
        {
            out = Trit.mlt(out, t);
        }
        return out;
    }
    
    public static Trit carry(Trit first, Trit second)
    {
        return(Trit.mlt(Trit.mlt(first, second), Trit.mlt(new Trit(-1), Trit.add(first, second))));
    }
    
    public static Trit carry(Trit first, Trit second, Trit third)
    {
        return(Trit.add(Trit.carry(first, second), Trit.carry(Trit.add(first, second), third)));
    }
    
    public char toChar()
    {
        return(charvals[state + 1]);
    }
    
    public int toInt()
    {
        return state;
    }
}