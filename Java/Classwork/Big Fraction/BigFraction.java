import java.math.BigInteger;
//-----------------------------------------------
/**
 * This class represents a fraction that can handle large numerator and denominator
 * Immutable arbitrary-precision fraction, using BigInteger for numerator and denominator
 * This class tries to be smart about how the fraction is stored.
 * The fraction is born reduced and sign is determined by numerator.
 */
//---------------------------------------------------
public class BigFraction
{
    private BigInteger num;
    private BigInteger denom;
    //---------------------------------------------
    /**
     * This constructor accepts two BigIntegers and returns a fully reduced fraction.
     * @param _num BigInteger representing the numerator of this fraction
     * @param _denom BigInteger representing the denominator of this fraction
     */
    //-----------------------------------------------
    public BigFraction(BigInteger _num, BigInteger _denom) 
    {
      //if(_denom < 0)
        if(_denom.compareTo(BigInteger.ZERO) < 0)
        {
            _num = _num.negate();
            _denom = _denom.negate();
        }
        //--------------------------------------------
        BigInteger d = _num.gcd(_denom);
        _num = _num.divide(d);
        _denom = _denom.divide(d);
        //---------------------------------------------
        this.num = _num;
        this.denom = _denom;
    }
    //---------------------------------------------
    /**
     * This constructor accepts two longs and returns a fully reduced fraction.
     * @param _num long representing the numerator of this fraction
     * @param _denom long representing the denominator of this fraction
     */
    //-------------------------------------------------
    public BigFraction(long _num, long _denom)
    {
        this(BigInteger.valueOf(_num),BigInteger.valueOf(_denom));
    }
    //---------------------------------------------
    /**
     * This constructor accepts a single BigInteger and returns a fraction.
     * @param _num BigInteger representing the numerator of this fraction
     */
    //-----------------------------------------------
    public BigFraction(long _num)
    {
        this(BigInteger.valueOf(_num),BigInteger.ONE);
    }
    //-----------------------------------------------
    /**
     * Returns the fraction as a string num + "/" + denom.
     */
    //-----------------------------------------------
    @Override
    public String toString()
    {
        return "" + num + "/" + denom;
    }
    //------------------------------------------------
    /**
     * @param that run BigFraction
     */
    //--------------------------------------------
    //public BigFraction add(BigFraction that
    //---------------------------------------------
    public static void main(String[] args)
    {
        BigFraction f = new BigFraction(1,2);
        BigFraction g = new BigFraction(3);
        BigFraction h = new BigFraction(3,-6);
        BigFraction i = new BigFraction(-3,-6);
        System.out.println(f);
        System.out.println(g);
        System.out.println(h);
        System.out.println(i);
    }
}