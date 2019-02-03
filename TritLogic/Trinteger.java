public class Trinteger
{
    private Tryte[] tryteList = new Tryte[3];
    
    public Trinteger(int x)
    {
        tryteList[0] = new Tryte(x / 729);
        tryteList[1] = new Tryte((x % 729) / 27);
        tryteList[2] = new Tryte(x % 27);
    }
    
    public Trinteger(String s)
    {
        tryteList[0] = new Tryte(s.charAt(0));
        tryteList[1] = new Tryte(s.charAt(1));
        tryteList[2] = new Tryte(s.charAt(2));
    }
    
    public static Trinteger add(Trinteger first, Trinteger second)
    {
        return(new Trinteger(0));
    }
    
    public int toInt()
    {
        return(tryteList[0].toInt() * 729 + tryteList[1].toInt() * 27 + tryteList[2].toInt());
    }
    
    public String toString()
    {
        String out = "";
        for(int i = 0; i < 3; i++)
        {
            out += tryteList[i].toChar();
        }
        return(out);
    }
}