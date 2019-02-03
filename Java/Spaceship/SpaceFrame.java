import javax.swing.*;
import javax.imageio.*;

import java.awt.*;
import java.awt.event.*;
import java.awt.image.*;

import java.util.*;
import java.util.logging.*;

import java.io.*;

import java.applet.*;

class SpaceFrame extends JFrame
{
    SpacePanel game = new SpacePanel();
    char dir;
    char[] dirs = new char[]{'W','S','A','D'};
    
    public SpaceFrame()
    {   
        this.add(game);
        
        for(int i = 0; i<5; i++)
        {
            (new Thread(new EnemySpaceship())).start();
        }
        
        (new Thread(new Counter())).start();
        
        this.addComponentListener(new ComponentAdapter()
                                      {
            public void componentResized(ComponentEvent e)
            {
                game.repaint();
            }
        });
        
        this.addKeyListener(new KeyListener()
                                {
            public void keyReleased(KeyEvent e)
            {
                dir = '-';
            }
            public void keyTyped(KeyEvent e){}
            
            public void keyPressed(KeyEvent e)
            {
                dir = (char)e.getKeyCode();
            }
        });
        
        (new Thread(new refreshTimer())).start();
    }
    
    public class refreshTimer implements Runnable
    {
        public void run()
        {
            int i = 0;
            while(1 == 1)
            {
                i++;
                if(i % (25 + (250/(game.kills + 10))) == 0)
                {
                    (new Thread(new EnemySpaceship())).start();
                }
                game.repaint();
                try
                {
                    Thread.sleep(50);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }
                if(dir == 'W')
                {
                    game.spaceship.dir = 'W';
                    game.spaceship.advance();
                }
                if(dir == 'S')
                {
                    game.spaceship.dir = 'S';
                    game.spaceship.advance();
                }
                if(dir == 'A')
                {
                    game.spaceship.dir = 'A';
                    game.spaceship.advance();
                }
                if(dir == 'D')
                {
                    game.spaceship.dir = 'D';
                    game.spaceship.advance();
                }
                if(dir == ' ')
                {
                    (new Thread(new Bullet(game.spaceship.getRelativeX() + 3, game.spaceship.getRelativeY() + 3, 4, 4, game.spaceship.dir, true, true))).start();
                }
            }
        }
    }
    
    public class EnemySpaceship implements Runnable
    {
        SpaceThing enemy;
        
        public EnemySpaceship()
        {
            enemy = new SpaceThing("enemySpaceshipU.png","enemySpaceshipD.png","enemySpaceshipL.png","enemySpaceshipR.png",(new Random()).nextInt(190),(new Random()).nextInt(90),10,10,dirs[(new Random()).nextInt(4)],true); 
        }
        
        public void run()
        {
            if(!(enemy.isCollidedX(game.spaceship)) && !(enemy.isCollidedY(game.spaceship)))
            {
                game.addThing(enemy);
                int i = 0;
                while(enemy.dir != 'Q')
                {
                    i++;
                    if(i % 15 == 0)
                    {
                        (new Thread(new Bullet(enemy.getRelativeX() + 3, enemy.getRelativeY() + 3, 4, 4, enemy.dir, false, false))).start();
                    }
                    
                    if((new Random()).nextInt(20) == 0)
                    {
                        enemy.dir = dirs[(new Random()).nextInt(4)];
                    }
                    
                    enemy.advance();
                    
                    try
                    {
                        Thread.sleep(70);
                    }
                    catch(InterruptedException e)
                    {
                        e.printStackTrace();
                    }
                    if(enemy.isCollidedX(game.spaceship) && enemy.isCollidedY(game.spaceship))
                    {
                        (new Thread(new Explode(enemy))).start();
                        (new Thread(new gameOver())).start();
                    }
                    if(enemy.isCollidedX(game.counter) && enemy.isCollidedY(game.counter))
                    {
                        (new Thread(new Explode(enemy))).start();
                    }
                }
            }
        }
    }
    
    public class Counter implements Runnable
    {
        public void run()
        {
            int i = 0;
            while(1==1)
            {
                i++;
                
                if(i % 30 == 0)
                {
                    (new Thread(new Bullet(game.counter.getRelativeX(), game.counter.getRelativeY(), 3, 3, dirs[(new Random()).nextInt(4)], true, false))).start();
                }
                
                if((new Random()).nextInt(20) == 0)
                {
                    game.counter.dir = dirs[(new Random()).nextInt(4)];
                }
                
                game.counter.advance();
                
                try
                {
                    Thread.sleep(50);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }
                if(game.counter.isCollidedX(game.spaceship) && game.counter.isCollidedY(game.spaceship))
                {
                    (new Thread(new gameOver())).start();
                }
            }
        }
        
    }
    
    public class Bullet implements Runnable
    {
        private SpaceThing bullet;
        private Boolean killsEnemy;
        private Boolean addsKill;
        
        public Bullet(int x, int y, int w, int h, char d, Boolean _killsEnemy, Boolean _addsKill)
        {
            bullet = new SpaceThing("bulletUD.png", "bulletUD.png", "bulletLR.png", "bulletLR.png", x, y, w, h, d, false);
            killsEnemy = _killsEnemy;
            addsKill = _addsKill;
        }
        
        public void run()
        {
            for(int i = 0; i<6; i++){bullet.advance();}
            game.addThing(bullet);
            while(bullet.dir != 'Q')
            {
                bullet.advance();
                try
                {
                    Thread.sleep(15);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }
                if(bullet.isCollidedX(game.spaceship) && bullet.isCollidedY(game.spaceship))
                {
                    game.deleteThing(bullet);
                    bullet.dir = 'Q';
                    (new Thread(new gameOver())).start();
                }
                if(killsEnemy){
                    for(int i = 0; i < game.things.size(); i++)
                    {
                        SpaceThing ruble = game.things.get(i);
                        
                        if(bullet.isCollidedX(ruble) && bullet.isCollidedY(ruble) && ruble.solid)
                        {
                            game.deleteThing(bullet);
                            (new Thread(new Explode(ruble))).start();
                            if((ruble.getFilenameU() == "enemySpaceshipU.png") && (ruble.dir != 'Q') && addsKill)
                            {
                                game.addKill();
                            }
                            ruble.dir = 'Q';
                            return;
                        }
                    }
                }
            }
            game.deleteThing(bullet);
        }
    }
    
    public class gameOver implements Runnable
    {
        public void run()
        {
            (new Thread(new Explode(game.spaceship))).start();
            game.addThing(new SpaceThing("youlose.png",0,0,200,100,false));
            try
            {
                Thread.sleep(4000);
            }
            catch(InterruptedException e)
            {
                e.printStackTrace();
            }
            SpaceFrame.this.dispose();
        }
    }
    
    public class Explode implements Runnable
    {
        SpaceThing fodder;
        
        public Explode(SpaceThing _fodder)
        {
            fodder = _fodder;
        }
        
        public void run()
        {
            for(int j=1; j<fodder.relativeWidth/2 + 3; j++)
            {
                SpaceThing explody = new SpaceThing("explosion.png", fodder.relativeX + fodder.relativeWidth/2 - j, fodder.relativeY + fodder.relativeHeight/2 - j, j*2, j*2, false);
                game.addThing(explody);
                try
                {
                    Thread.sleep(100);
                }
                catch(InterruptedException e)
                {
                    e.printStackTrace();
                }
                game.deleteThing(explody);
            }
            fodder.dir = 'Q';
            game.deleteThing(fodder);
        }
    }
    
    public static void main(String[] args)
    {
        SpaceFrame wilt = new SpaceFrame();
        wilt.setSize(1416,738);
        wilt.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        wilt.setVisible(true);
    }
}