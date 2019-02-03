public class Tryte
{
    private static char[] alphaspace = {':','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};
    private Trit[] tritList = new Trit[3];
    
    public Tryte(Trit x, Trit y, Trit z)
    {
        tritList[0] = x;
        tritList[1] = y;
        tritList[2] = z;
    }
    
    public Tryte(String s)
    {
        tritList[0] = new Trit(s.charAt(0));
        tritList[1] = new Trit(s.charAt(1));
        tritList[2] = new Trit(s.charAt(2));
    }
    
    public Tryte(char c)
    {
        for(int i = -13; i < 14; i++)
        {
            if(alphaspace[i + 13] == c)
            {
                tritList[0] = new Trit(((i + 13) / 9) - 1);
                tritList[1] = new Trit((((i + 13) % 9) / 3) - 1);
                tritList[2] = new Trit(((i + 13) % 3) - 1);
            }
        }
    }
    
    public Tryte(int x)
    {
        tritList[0] = new Trit(((x + 13) / 9) - 1);
        tritList[1] = new Trit((((x + 13) % 9) / 3) - 1);
        tritList[2] = new Trit(((x + 13) % 3) - 1);
    }
    
    public static Boolean isAlphaspace(char c)
    {
        for(char x : alphaspace)
        {
            if(x == c)
            {
                return true;
            }
        }
        return false;
    }
    
    public static String toAlphaspace(String in)
    {
        in = in.toUpperCase();
        String out = new String();
        for(int i = 0; i < in.length(); i++)
        {
            if(isAlphaspace(in.charAt(i)))
            {
                out += in.substring(i, i+1);
            }
            else if(in.charAt(i) == ' ')
            {
                out += ':';
            }
        }
        return out;
    }
    
    public static Tryte add(Tryte first, Tryte second)
    {
        Trit z = Trit.add(first.getTrit(1), second.getTrit(1));
        Trit y = Trit.add(new Trit[]{first.getTrit(0), second.getTrit(0), Trit.carry(first.getTrit(1), second.getTrit(1))});
        Trit x = Trit.add(new Trit[]{first.getTrit(-1), second.getTrit(-1), Trit.carry(first.getTrit(0), second.getTrit(0), Trit.carry(first.getTrit(1), second.getTrit(1)))});
        return(new Tryte(x, y, z));
    }
    
    public int toInt()
    {
        return(tritList[0].toInt() * 9 + tritList[1].toInt() * 3 + tritList[2].toInt());
    }
    
    public char toChar()
    {
        for(int i = -13; i < 14; i++)
        {
            if(i == toInt())
            {
                return alphaspace[i + 13];
            }
        }
        return('!');
    }
    
    public String toString()
    {
        String out = "";
        for(int i = 0; i < 3; i++)
        {
            out += tritList[i].toChar();
        }
        return(out);
    }
    
    public Trit getTrit(int index)
    {
        return tritList[index + 1];
    }
    
    public void setTrit(int index, Trit value)
    {
        tritList[index + 1] = value;
    }
}