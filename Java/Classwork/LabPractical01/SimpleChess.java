import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color.*;

import java.util.*;

/**
  * Four: 1 point<br/>
  * Build a chessboard. (8x8 grid of alternating black and white squares with
  * a white square in the upper left corner)<br/>
  * You may choose to represent a Rook, a Bishop, or a Queen (you only need to chose one).<br/>
  *
  * When the mouse moves into a square, turn all the legal places your 
  * chosen piece may move to green.  When the mouse moves out of that square
  * return those squares to their original color.<br/><br/>
  *
  * Note your chosen piece type in the title bar.<br/><br/>
  *
  * Rooks can move N/S or E/W all the way to the edge of the board<br/>
  * Bishops can move in diagonals from their current position as far as they want<br/>
  * Queens have the abilities of both Rooks and Bishops<br/>
  *
  */

public class SimpleChess implements Runnable
{
    JFrame frame = new JFrame("Rook");
    ArrayList<ChessSpace> spaces = new ArrayList<ChessSpace>();
    
    /*
     * This sets the proper GridLayout for frame and adds 64 spaces, setting their inherent colors and space coordinates in the process.
     */
    public void run()
    {
        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(8,8));
        
        for(int i = 0; i < 64; i++)
        {
            ChessSpace space = new ChessSpace(i, spaces);
            frame.add(space);
            spaces.add(space);
        }
        
        frame.setVisible(true);
    }
    
    /*
     * This class is a panel representing a chess space that knows its coordinates and inherent color
     */
    private class ChessSpace extends JPanel
    {
        Color inherentColor;
        private int x;
        private int y;
        
        /*
         * This contructor creates a space with specific coordinates and color
         * @param num The number of the chess piece, from which it extrapolates color and coordinates
         * @param spaces The list of other spaces which the space checks for ability to move to
         */
        public ChessSpace(int num, ArrayList<ChessSpace> spaces)
        {
            x = num % 8;
            y = num / 8;
            
            if(((((num / 8) % 2) + (num % 2)) % 2) == 0)
            {
                inherentColor = Color.WHITE;
            }
            else
            {
                inherentColor = Color.BLACK;
            }
            
            setBackground(inherentColor);
            
            
            addMouseListener(new MouseListener()
                                 {
                //If mouse is entered, spaces in same row Xor column turn green
                public void mouseEntered(MouseEvent e)
                {
                    for(int i = 0; i < 64; i++)
                    {
                        ChessSpace other = spaces.get(i);
                        if(Boolean.logicalXor(other.getSpaceX() == x, other.getSpaceY() == y))
                        {
                            other.setToGreen();
                        }
                    }
                }
                
                
                //If mouse exits, those spaces become inherent color again
                public void mouseExited(MouseEvent e)
                {
                    for(int i = 0; i < 64; i++)
                    {
                        ChessSpace other = spaces.get(i);
                        if(Boolean.logicalXor(other.getSpaceX() == x, other.getSpaceY() == y))
                        {
                            other.setToInherent();
                        }
                    }
                }
                
                public void mouseClicked(MouseEvent e)
                {}
                
                public void mousePressed(MouseEvent e)
                {}
                
                public void mouseReleased(MouseEvent e)
                {}
            });
        }
        
        
        //Sets color to green
        public void setToGreen()
        {
            setBackground(Color.GREEN);
        }
        
        //Sets color to inherent
        public void setToInherent()
        {
            setBackground(inherentColor);
        }
        
        
        //Returns x coordinate
        public int getSpaceX()
        {
            return x;
        }
        
        //Returns y coordinate
        public int getSpaceY()
        {
            return y;
        }
    }
    
    public static void main(String[] args)
    {
        javax.swing.SwingUtilities.invokeLater(new SimpleChess());
    }
}