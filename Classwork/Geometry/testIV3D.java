public class testIV3D
{
    public static void main(String[] args)
    {
        stuart_roe15cIntegerVector3D one = new stuart_roe15cIntegerVector3D(4,0,7);
        stuart_roe15cIntegerVector3D two = new stuart_roe15cIntegerVector3D(-2,-3,-5);
        stuart_roe15cIntegerVector3D thr = new stuart_roe15cIntegerVector3D(-2,1,3);
        System.out.println(one.angleBetween(thr));
    }
}