import javax.swing.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.Color.*;

import java.util.*;

/**
  * Five: .5 point<br/>
  * Build a chessboard (8x8 grid of alternating black and white squares with
  * a white square in the upper left corner) and a key.<br/>
  * In your key have a button for each type of chess piece (King, Queen, Bishop, Knight, Rook, Pawn).<br/>
  * When a button is clicked, your mouse will be representing a piece of that type.<br/>
  * When the mouse moves into a square, turn all the possible places your 
  * chosen piece may legally move to green.  When the mouse moves out of that square
  * return those squares to their original color.<br/><br/>
  *
  * Make the title bar reflect the selected piece type.<br/><br/>
  *
  * Rooks can move up/down, left/right (N/S/E/W) all the way to the edge of the board<br/>
  * Bishops can move in diagonals (NE/NW/SE/SW) from their current position to the edge of the board<br/>
  * Queens have the abilities of both Rooks and Bishops<br/>
  * Kings can move one space in any direction (N/S/E/W/NE/NW/SE/SW)<br/>
  * Pawns: Assume that your direction is up (so there are no pawns allowed on the 1st (bottom) row)<br/>
  * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; From the 2nd row, pawns can move 1 or 2 spaces forward.<br/>
  * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; From the 3rd row to the 7th row they can move 1 space forward.<br/>
  * &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; From the 8th row they cannot move.<br/>
  * 
  */

public class ShowYourMoves implements Runnable
{
    JFrame frame = new JFrame("Rook");
    ArrayList<ChessSpace> spaces = new ArrayList<ChessSpace>();
    String piece = "Bishop";
    
    public void run()
    {
        frame.setSize(800,600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new GridLayout(8,8));
        
        JMenuBar jmb = new JMenuBar();
        JMenu pieceMenu = new JMenu("Piece");
        jmb.add(pieceMenu);
        frame.setJMenuBar(jmb);
        
        for(int i = 0; i < 64; i++)
        {
            ChessSpace space = new ChessSpace(i, spaces);
            frame.add(space);
            spaces.add(space);
        }
        
        frame.setVisible(true);
    }
    
    class pieceMenuItem extends JMenuItem
    {
        public pieceMenuItem(String title)
        {
            addActionListener(new ActionListener()
                                  {
                public void actionPerformed(ActionEvent e)
                {
                    ShowYourMoves.this.piece = title;
                }
            });
        }
    }
    
    public void checkSpaces(int x, int y, Boolean entering)
    {
        for(int i = 0; i < 64; i++)
        {
            ChessSpace other = spaces.get(i);
            Boolean toggled = false;
            
            switch(this.piece)
            {
                case "Rook":
                    if(Boolean.logicalXor(other.getSpaceX() == x, other.getSpaceY() == y))
                    {
                        toggled = true;
                    }
                case "Bishop":
                    if((other.getSpaceX() + other.getSpaceY()) == (x + y))
                    {
                        toggled = true;
                    }
            }
            
            if(toggled)
            {
                if(entering)
                {
                    other.setToGreen();
                }
                else
                {
                    other.setToInherent();
                }
            }
        }
    }
    
    private class ChessSpace extends JPanel
    {
        Color inherentColor;
        private int x;
        private int y;
            
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
                public void mouseEntered(MouseEvent e)
                {
                    ShowYourMoves.this.checkSpaces(x, y, true);
                }
                
                public void mouseExited(MouseEvent e)
                {
                    ShowYourMoves.this.checkSpaces(x, y, false);
                }
                
                public void mouseClicked(MouseEvent e)
                {}
                
                public void mousePressed(MouseEvent e)
                {}
                
                public void mouseReleased(MouseEvent e)
                {}
            });
        }
        
        public void setToGreen()
        {
            setBackground(Color.GREEN);
        }
        
        public void setToInherent()
        {
            setBackground(inherentColor);
        }
        
        public int getSpaceX()
        {
            return x;
        }
        
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