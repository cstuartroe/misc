public class JasonStatham
{
    public static void main(String[] args)
    {
        // Most object creations must call new
        point p = new point();
        point q = new point(1,2);
        point r = new point(4,7);
        System.out.println(q.reflectOverLine(3,0));
        System.out.println(q);
    }
}