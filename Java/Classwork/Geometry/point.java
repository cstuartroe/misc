public class point
{
    //New Keyword - state should always be private, gives better control over how objects are used
    
    //Defining the state of the object at the top
    private double x;
    private double y;
    
    public static enum NamedLine{OVER_X, OVER_Y, OVER_Y_EQ_X, OVER_Y_EQ_NEG_X}
    
    //Convention:
    //If you have state, you must write a constructor
    //At the end of your constructor, your state must be initialized.
    
    public point(double _x, double _y)
    {
        //"this" means current instance of class.
        this.x = _x;
        this.y = _y;
    }
    
    public point()
    {
        //this is the most basic constructor we can make
        //it takes no arguments, does nothing
        //This calls a sibling constructor
        //Overloaded the constructor for our point class - different function signature, so it's ok
        //Overloading - having two or more functions w/ the same name
        this(0,0);
    }
    
    //@Override is a keyword that tells compiler to check to see that
    //your function signature is correct when overriding a method
    //A function is identified by its name and the types of its parameter list - Function Signature
    //Functions with same name should have same return type
    @Override
    public String toString()
    {
        //if you concatenate a string with a non-string, the non-string automatically does toString
        return "(" + x + ", " + y + ")";
    }
    
    @Override
    //.equals must take object
    public boolean equals(Object other)
    {
        if(!(other instanceof point))
        {
            return false;
        }
        return (x == ((point)other).x && y == ((point)other).y);
    }
    
    public double distanceTo(point other)
    {
        return Math.hypot(this.x-other.x, this.y-other.y);
    }
    
    public point midpoint(point that)
    {
        return new point((this.x+that.x)/2,(this.y+that.y)/2);
    }
    
    public point reflectOverX()
    {
        return new point(this.x,-this.y);
    }
    
    public point reflectOverY()
    {
        return new point(-this.x,this.y);
    }
    
    public point reflectOverY_EQ_X()
    {
        return new point(this.y,this.x);
    }
    
    public point reflectOverY_EQ_NEG_X()
    {
        return new point(-this.y,-this.x);
    }
    
    public point reflect(point p, NamedLine overWhat)
    {
        point newPoint;
        switch( overWhat )
        {
            case OVER_X:
                newPoint = new point(p.x, -p.y);
                break;
            case OVER_Y:
                newPoint = new point(-p.x, p.y);
                break;
            case OVER_Y_EQ_X:
                newPoint = new point(p.y, p.x);
                break;
            case OVER_Y_EQ_NEG_X:
                newPoint = new point(-p.y, -p.x);
                break;
            default:
                newPoint = new point();
                break;
        }
        return newPoint;
    }
    
    public point reflectOverLine(double m, double i)
    {
        double reflectionX = ((this.x / m) + this.y - i) * (m / ((m * m) + 1));
        double reflectionY = (m * reflectionX) + i;
        return new point((2 * reflectionX) - this.x, (2 * reflectionY) - this.y);
    }
    
    //howFar is in radians.
    public point rotate(double howFar)
    {
        double newX = Math.cos(howFar)*this.x - Math.sin(howFar)*this.y;
        double newY = Math.sin(howFar)*this.x + Math.cos(howFar)*this.y;
        return new point(newX, newY);
    }
    
    @Override
    public point clone()
    {
        return new point(this.x, this.y);
    }
    
    public double getX()
    {
        return this.x;
    }
    
    public double getY()
    {
        return this.y;
    }
    
    public void setX(double newVal)
    {
        this.x = newVal;
    }
    
    public void setY(double newVal)
    {
        this.y = newVal;
    }
    
    public void move(double deltaX, double deltaY)
    {
        this.setX(this.x + deltaX);
        this.setY(this.y + deltaY);
    }
}