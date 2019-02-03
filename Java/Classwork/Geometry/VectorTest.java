public class VectorTest
{
    public static void main(String[] args)
    {
        stuart_roe15cIntegerVector3D v = new stuart_roe15cIntegerVector3D(1,2,3);
        stuart_roe15cIntegerVector3D w = new stuart_roe15cIntegerVector3D(-1,1,0);
        stuart_roe15cIntegerVector3D x = v.crossProduct(w);
        System.out.println(v.dot(w));
        System.out.println(v.dot(x));
        System.out.println(w.dot(x));
    }
}