import java.util.*;

class MatrixOperator
{
    private static double[][] matrix = {{2,1,-1,3},{-1,3,-1,-2},{-1,1,2,-5},{1,3,3,-2}};
    
    public static void main(String[] args)
    {
        System.out.println("Shit boo the determinant is " + Double.toString(determinant(matrix)));
    }
    
    public MatrixOperator(double[][] _matrix)
    {
        matrix = _matrix;
    }
    
    public static void readTerms(double[][] _matrix)
    {
        for(int row = 0; row < _matrix.length; row++)
        {
            for(int column = 0; column < _matrix[row].length; column++)
            {
                System.out.println(matrix[row][column]);
            }
        }
    }
    
    public static double determinant(double[][] _matrix)
    {
        return determinant(_matrix, true);
    }
    
    public static double determinant(double[][] _matrix, boolean parent) throws ArrayIndexOutOfBoundsException
    {
        int size = _matrix.length;
        
        if(size == 2)
        {
            if(parent && ((_matrix[0].length != size) || (_matrix[1].length != size)))
            {
                //System.out.println();
                throw new ArrayIndexOutOfBoundsException("Breh. A square matrix that ain't. It got 2 rows and more than 2 columns");
            }
            
            return _matrix[0][0]*_matrix[1][1] - _matrix[0][1]*_matrix[1][0];
        }
        else
        {
            double det = 0;
            for(int i = 0; i < size; i++)
            {
                if(parent && (_matrix[i].length != size))
                {
                    //System.out.println();
                    throw new ArrayIndexOutOfBoundsException("Breh. A square matrix that ain't. You got " + Integer.toString(size) + " rows but row " + Integer.toString(i) + " only got " + Integer.toString(_matrix[i].length) + " terms.");
                }
                
                double[][] submtx = new double[size-1][];
                
                for(int j = 0; j < size; j++)
                {
                    if(j != i)
                    {
                        submtx[(j>i) ? j-1 : j] = Arrays.copyOfRange(_matrix[j],1,size);
                    }
                }
                
                //System.out.println((Math.pow(-1,i))*(_matrix[i][0])*(determinant(submtx)));
                det += (Math.pow(-1,i))*(_matrix[i][0])*(determinant(submtx, false));
            }
            
            if(parent){System.out.println("That's a tasty-ass matrix");}
            return det;
        }
    }
}