import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class NimLearner extends JFrame
{
    private JButton oneButton;
    private JButton twoButton;
    private JButton threeButton;
    private int tokens;
    private int games;
    private JPanel tokensDisplay;
    private JPanel movesDisplay;
    private JLabel gamesLabel;
    private JLabel tokensLabel;
    int[][] ai;
    Random random;
    ArrayList<int[]> yourMoves;
    ArrayList<int[]> aiMoves;
    
    public static void main(String[] args)
    {
        new NimLearner();
    }
    
    public NimLearner()
    {
        setSize(900,500);
        setLayout(null);
        
        tokens = 7;
        games = 0;
        ai = new int[][] {{1024,0,0},{1024,1024,0},{1024,1024,1024},{1024,1024,1024},{1024,1024,1024},{1024,1024,1024},{1024,1024,1024}};
        random = new Random();
        yourMoves = new ArrayList<int[]>();
        aiMoves = new ArrayList<int[]>();
        
        tokensDisplay = new JPanel();
        tokensDisplay.setBounds(0,0,900,100);
        tokensDisplay.setLayout(new GridLayout(1, 2));
        
        gamesLabel = new JLabel("Games Played: " + Integer.toString(games));
        gamesLabel.setAlignmentX(CENTER_ALIGNMENT);
        tokensDisplay.add(gamesLabel);
        
        tokensLabel = new JLabel("Tokens Remaining: " + Integer.toString(tokens));
        tokensLabel.setAlignmentX(CENTER_ALIGNMENT);
        tokensDisplay.add(tokensLabel);
        
        add(tokensDisplay);
        
        oneButton = new JButton("1");
        oneButton.setBounds(0,100,300,100);
        add(oneButton);
        oneButton.addActionListener(new ActionListener()
                                        {
            public void actionPerformed(ActionEvent e)
            {
                takeTokens(1);
            }
        });
        
        twoButton = new JButton("2");
        twoButton.setBounds(300,100,300,100);
        add(twoButton);
        twoButton.addActionListener(new ActionListener()
                                        {
            public void actionPerformed(ActionEvent e)
            {
                takeTokens(2);
            }
        });
        
        threeButton = new JButton("3");
        threeButton.setBounds(600,100,300,100);
        add(threeButton);
        threeButton.addActionListener(new ActionListener()
                                          {
            public void actionPerformed(ActionEvent e)
            {
                takeTokens(3);
            }
        });
        
        movesDisplay = new JPanel();
        movesDisplay.setBounds(0,200,900,300);
        add(movesDisplay);
        movesDisplay.setLayout(new BoxLayout(movesDisplay,BoxLayout.Y_AXIS));
        movesDisplay.setBorder(BorderFactory.createLineBorder(new Color(0,0,0)));
        movesDisplay.setAlignmentX(CENTER_ALIGNMENT);
        
        setVisible(true);
        
        if(random.nextInt(2)==1)
        {
            aiMove();
        }
    }
    
    
    public void takeTokens(int x)
    {
        if(tokens == 0)
        {
            tokens = 7;
            games += 1;
            
            System.out.println("Game #" + Integer.toString(games));
                
            for(int i = 0; i<7; i++)
            {
                System.out.println(Integer.toString(i + 1) + " tokens: " + Arrays.toString(ai[i]));
            }
            
            tokensLabel.setText("Remaining Tokens: " + Integer.toString(tokens));
            gamesLabel.setText("Games Played: " + Integer.toString(games));
            
            movesDisplay.removeAll();
            yourMoves = new ArrayList<int[]>();
            aiMoves = new ArrayList<int[]>();
            
            revalidate();
            repaint();
            
            if(random.nextInt(2)==1)
            {
                aiMove();
            }
        }
        
        else if(x>tokens)
        {
            JLabel label = new JLabel("invalid move.");
            label.setAlignmentX(CENTER_ALIGNMENT);
            movesDisplay.add(label);
            
            revalidate();
            repaint();
        }
        
        else
        {
            yourMoves.add(new int[] {tokens,x});
            
            tokens -= x;
            
            JLabel label = new JLabel("you removed " + Integer.toString(x) + " tokens.");
            label.setAlignmentX(CENTER_ALIGNMENT);
            movesDisplay.add(label);
            
            if(tokens == 0)
            {
                JLabel outcomeLabel = new JLabel("you lose.");
                outcomeLabel.setAlignmentX(CENTER_ALIGNMENT);
                movesDisplay.add(outcomeLabel);
                
                System.out.println("Your moves:");
                for(int i = 0; i<yourMoves.size(); i++)
                {
                    int[] move = yourMoves.get(i);
                    System.out.println(Integer.toString(move[0]) + Integer.toString(move[1]));
                    ai[move[0] - 1][move[1] - 1] /= 2;
                    if(ai[move[0] - 1][move[1] - 1] == 0){ai[move[0] - 1][move[1] - 1] = 1;}
                }
                
                System.out.println("AI moves:");
                for(int i = 0; i<aiMoves.size(); i++)
                {
                    int[] move = aiMoves.get(i);
                    System.out.println(Integer.toString(move[0]) + Integer.toString(move[1]));
                    ai[move[0] - 1][move[1] - 1] *= 2;
                }
                
                tokensLabel.setText("Remaining Tokens: " + Integer.toString(tokens));
                
                revalidate();
                repaint();
            }
            
            else
            {
                aiMove();
            }
        }
    }
    
    public void aiMove()
    {
        int y;
        int[] choices = ai[tokens-1];
        int r = 0;
        if(choices[0] + choices[1] + choices[2] > 0)
        {
            try
            {
                r = random.nextInt(choices[0] + choices[1] + choices[2]);
            }
            catch(IllegalArgumentException e)
            {
                System.out.println(choices[0]);
                System.out.println(choices[1]);
                System.out.println(choices[2]);
            }
            if(r<choices[0]){y=1;}
            else if(r<choices[0] + choices[1]){y=2;}
            else{y=3;}
        }
        else{y=1;}
        
        aiMoves.add(new int[] {tokens,y});
        
        tokens -= y;
        
        JLabel labelToo = new JLabel("AI removed " + Integer.toString(y) + " tokens.");
        labelToo.setAlignmentX(CENTER_ALIGNMENT);
        movesDisplay.add(labelToo);
        
        if(tokens == 0)
        {
            
            JLabel outcomeLabel = new JLabel("you win.");
            outcomeLabel.setAlignmentX(CENTER_ALIGNMENT);
            movesDisplay.add(outcomeLabel);
            
            System.out.println("Your moves:");
            for(int i = 0; i<yourMoves.size(); i++)
            {
                int[] move = yourMoves.get(i);
                System.out.println(Integer.toString(move[0]) + Integer.toString(move[1]));
                ai[move[0] - 1][move[1] - 1] *= 2;
            }
            
            System.out.println("AI moves:");
            for(int i = 0; i<aiMoves.size(); i++)
            {
                int[] move = aiMoves.get(i);
                System.out.println(Integer.toString(move[0]) + Integer.toString(move[1]));
                ai[move[0] - 1][move[1] - 1] /= 2;
                if(ai[move[0] - 1][move[1] - 1] == 0){ai[move[0] - 1][move[1] - 1] = 1;}
            }
        }
        
        tokensLabel.setText("Remaining Tokens: " + Integer.toString(tokens));
        
        revalidate();
        repaint();
    }
}