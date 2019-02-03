import javax.swing.*;
import javax.swing.event.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

/* TO_DO:
 * add braces to conditions
 * add brackets
 * add help pane
 * add save function
 * add syllable boundary code
 */

public class WordGenerator extends JFrame
{
    private InputPanel soundTypesPanel;
    private InputPanel changeRulesPanel;
    private InputPanel syllableTypesPanel;
    private InputPanel wordRulesPanel;
    private InputPanel outputPanel;
    private InputPanel soundChangeInputPanel;
    private JButton runButton;
    private JButton helpButton;
    private JButton restoreDefaultsButton;
    private JButton showIPAButton;
    private JButton soundChangeButton;
    private SliderPanel syllableCountSliderPanel;
    private SliderPanel wordCountSliderPanel;
    private String currentUnderlyingOutput = "";
    private ArrayList<SoundList> soundTypes;
    private JMenuBar menuBar;
    private JMenu optionsMenu;
    private JCheckBoxMenuItem scaMenuItem;
    private JCheckBoxMenuItem pseudotextMenuItem;
    private JCheckBoxMenuItem showChangesMenuItem;
    private SyllableList syllableTypes;
    private IPAFrame ipa = new IPAFrame();
    private Color backgroundColor = new Color(40,0,140);
    private Color foregroundColor = new Color(255,255,180);
    private Font universalFont = new Font("Times New Roman",Font.BOLD,16);
    private Random randomizer = new Random();
    
    public WordGenerator()
    {
        setSize(1006,651);
        setResizable(false);
        setTitle("/u/qzorum's Mighty Conlang Word Generator and Sound Change Applier Twofer");
        setLayout(null);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        getContentPane().setBackground(backgroundColor);
        
        soundTypesPanel = new InputPanel("Sound Types", 0, 0, 200, 560);
        changeRulesPanel = new InputPanel("Sound Change Rules", 400, 0, 200, 560);
        syllableTypesPanel = new InputPanel("Syllable Types", 200, 0, 200, 260);
        wordRulesPanel = new InputPanel("Word Suprasegmentals", 200, 300, 200, 260);
        soundChangeInputPanel = new InputPanel("Sound Change Applier Input", 0, 0, 400, 560);
        outputPanel = new InputPanel("Output", 600, 0, 400, 510);
        
        add(soundTypesPanel);
        add(changeRulesPanel);
        add(syllableTypesPanel);
        add(wordRulesPanel);
        add(outputPanel);
        
        runButton = new JButton("Run!");
        runButton.setBounds(610,560,180,30);
        runButton.setBackground(foregroundColor);
        runButton.setFont(universalFont);
        runButton.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                WordGenerator.this.runGenerator();
            }
        });
        add(runButton);
        
        helpButton = new JButton("Help!");
        helpButton.setBounds(810,560,180,30);
        helpButton.setBackground(foregroundColor);
        helpButton.setFont(universalFont);
        add(helpButton);
        
        restoreDefaultsButton = new JButton("Restore Defaults");
        restoreDefaultsButton.setBounds(10,560,180,30);
        restoreDefaultsButton.setBackground(foregroundColor);
        restoreDefaultsButton.setFont(universalFont);
        restoreDefaultsButton.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                if(JOptionPane.showConfirmDialog(null, "Are you sure you want to erase your precious inputs??") == JOptionPane.YES_OPTION)
                {
                    WordGenerator.this.restoreDefaults();
                }
            }
        });
        add(restoreDefaultsButton);
        
        soundChangeButton = new JButton("Apply Sound Changes");
        soundChangeButton.setBounds(410,560,180,30);
        soundChangeButton.setBackground(foregroundColor);
        soundChangeButton.setFont(universalFont);
        soundChangeButton.addActionListener(new ActionListener()
                                                {
            public void actionPerformed(ActionEvent e)
            {
                soundTypes = new ArrayList<SoundList>();
                for(String line : soundTypesPanel.getText().split("\n"))
                {
                    soundTypes.add(new SoundList(line));
                }
                if(!currentUnderlyingOutput.equals("") || !soundChangeInputPanel.getText().equals(""))
                {
                    applySoundChanges();
                }
            }
        });
        add(soundChangeButton);
        
        showIPAButton = new JButton("Extended Characters");
        showIPAButton.setBounds(210,560,180,30);
        showIPAButton.setBackground(foregroundColor);
        showIPAButton.setFont(universalFont);
        showIPAButton.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                ipa.open();
            }
        });
        add(showIPAButton);
        
        syllableCountSliderPanel = new SliderPanel("Avg. Syllables Per Word", true);
        syllableCountSliderPanel.setBounds(200,260,200,40);
        add(syllableCountSliderPanel);
        
        wordCountSliderPanel = new SliderPanel("Words to Output", false);
        wordCountSliderPanel.setBounds(610,510,380,40);
        add(wordCountSliderPanel);
        
        menuBar = new JMenuBar();
        optionsMenu = new JMenu("Output Options");
        scaMenuItem = new JCheckBoxMenuItem("Sound Change Applier", false);
        scaMenuItem.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                if(scaMenuItem.getState())
                {
                    remove(soundTypesPanel);
                    remove(syllableTypesPanel);
                    remove(wordRulesPanel);
                    remove(syllableCountSliderPanel);
                    add(soundChangeInputPanel);
                    WordGenerator.this.revalidate();
                    repaint();
                }
                else
                {
                    soundChangeInputPanel.setText("");
                    remove(soundChangeInputPanel);
                    add(soundTypesPanel);
                    add(syllableTypesPanel);
                    add(wordRulesPanel);
                    add(syllableCountSliderPanel);
                    WordGenerator.this.revalidate();
                    repaint();
                }
            }
        });
        pseudotextMenuItem = new JCheckBoxMenuItem("Pseudotext", false);
        pseudotextMenuItem.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                if(pseudotextMenuItem.getState())
                {
                    showChangesMenuItem.setState(false);
                }
                if(!currentUnderlyingOutput.equals(""))
                {
                    applySoundChanges();
                }
            }
        });
        showChangesMenuItem = new JCheckBoxMenuItem("Show Changes", false);
        showChangesMenuItem.addActionListener(new ActionListener()
                                                    {
            public void actionPerformed(ActionEvent e)
            {
                if(showChangesMenuItem.getState())
                {
                    pseudotextMenuItem.setState(false);
                }
                if(!currentUnderlyingOutput.equals(""))
                {
                    applySoundChanges();
                }
            }
        });
        optionsMenu.add(scaMenuItem);
        optionsMenu.add(pseudotextMenuItem);
        optionsMenu.add(showChangesMenuItem);
        menuBar.add(optionsMenu);
        setJMenuBar(menuBar);
        
        restoreDefaults();
        
        setVisible(true);
        System.out.println(this.getContentPane().getSize());
    }
    
    private class IPAFrame extends JFrame
    {
        private JTextArea IPAtable;
        
        public IPAFrame()
        {
            setSize(530,340);
            setResizable(false);
            setTitle("IPA & Miscellaneous Symbols");
            setLocationRelativeTo(null);
            setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
        }
        
        public void open()
        {
            IPAtable = new JTextArea();
            IPAtable.setEditable(false);
            IPAtable.setLineWrap(true);
            IPAtable.setFont(universalFont);
            IPAtable.setBackground(foregroundColor);
            add(IPAtable);
            setVisible(true);
            String unicode = "";
            for(int i = 0x00C0; i < 0x02B0; i++)
            {
                unicode += (char)i + " ";
            }
            for(int i = 0x0390; i < 0x03CF; i++)
            {
                unicode += (char)i + " ";
            }
            for(int i = 0x0410; i < 0x0450; i++)
            {
                unicode += (char)i + " ";
            }
            IPAtable.setText(unicode);
        }
    }
    
    private class InputPanel extends JPanel
    {
        private JTextArea textarea;
        private JLabel label;
        private JPanel labelPanel;
        
        public InputPanel(String title, int x, int y, int width, int height)
        {
            setBounds(x, y, width, height);
            setLayout(null);
            setBackground(backgroundColor);
            
            label = new JLabel(title);
            labelPanel = new JPanel();
            labelPanel.setBounds(10, 5, width - 20, 30);
            label.setAlignmentX(Component.CENTER_ALIGNMENT);
            label.setForeground(foregroundColor);
            label.setFont(universalFont);
            labelPanel.setBackground(backgroundColor);
            labelPanel.add(label);
            add(labelPanel);
            
            textarea = new JTextArea();
            textarea.setBounds(10, 40, width - 20, height - 50);
            textarea.setLineWrap(true);
            textarea.setWrapStyleWord(true);
            textarea.setBackground(foregroundColor);
            textarea.setFont(universalFont);
            JScrollPane scroll = new JScrollPane(textarea);
            scroll.setVerticalScrollBarPolicy(ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS);
            scroll.setBounds(10, 40, width - 20, height - 50);
            add(scroll);
        }
        
        public String getText()
        {
            return textarea.getText();
        }
        
        public void setText(String text)
        {
            textarea.setText(text);
        }
        
        public boolean getFormat()
        {
            return(pseudotextMenuItem.getState());
        }
        
        public boolean getShowChanges()
        {
            return(showChangesMenuItem.getState());
        }
    }
    
    private class SliderPanel extends JPanel
    {
        private JSlider slide;
        private String title;
        private JLabel label;
        private boolean isSylls;
        
        public SliderPanel(String _title, boolean _isSylls)
        {
            setLayout(new GridLayout(2,2));
            setBackground(backgroundColor);
            isSylls = _isSylls;
            title = _title;
            
            if(isSylls)
            {
                slide = new JSlider(0,8);
                slide.setMajorTickSpacing(2);
                
                label = new JLabel(title + ": " + ((slide.getValue() / 2.0) + 1.0), JLabel.CENTER);
                
                slide.addChangeListener(new ChangeListener()
                                            {
                    public void stateChanged(ChangeEvent e)
                    {
                        label.setText(title + ": " + ((slide.getValue() / 2.0) + 1.0));
                    }
                });
            }
            else
            {
                slide = new JSlider(0,200);
                slide.setMajorTickSpacing(10);
                
                label = new JLabel(title + ": " + (int)(Math.pow(50,(slide.getValue()/100.0))), JLabel.CENTER);
                
                slide.addChangeListener(new ChangeListener()
                                            {
                    public void stateChanged(ChangeEvent e)
                    {
                        label.setText(title + ": " + (int)(Math.pow(50,(slide.getValue()/100.0))));
                    }
                });
            }
            
            slide.setPaintTicks(true);
            slide.setBackground(backgroundColor);
            add(slide);
            
            label.setForeground(foregroundColor);
            label.setFont(universalFont);
            add(label);
        }
        
        public void setValue(int val)
        {
            slide.setValue(val);
        }
        
        public int getValue()
        {
            if(isSylls)
            {
                return slide.getValue();
            }
            else
            {
                return (int)(Math.pow(50,(slide.getValue()/100.0)));
            }
        }
        
        public int getRandomValue()
        {
            int out = 1;
            for(int i = 0; i < getValue(); i++)
            {
                out += randomizer.nextInt(2);
            }
            return out;
        }
    }
    
    private class SoundList
    {
        private ArrayList<String> sounds;
        private String name;
        
        public SoundList(String input)
        {
            name = "";
            sounds = new ArrayList<String>();
            input = input.replaceAll(" ","");
            
            boolean writingName = true;
            boolean multiplying = false;
            String currentSound = "";
            String currentMultiplier = "";
            
            for(int i = 0; i < input.length(); i++)
            {
                if(input.charAt(i) == '=')
                {
                    writingName = false;
                }
                else if(writingName)
                {
                    name += input.charAt(i);
                }
                else if(input.charAt(i) == ',')
                {
                    if(currentMultiplier == "")
                    {
                        currentMultiplier = "1";
                    }
                    for(int j = 0; j < Integer.parseInt(currentMultiplier); j++)
                    {
                        sounds.add(currentSound);
                    }
                    currentSound = "";
                    currentMultiplier = "";
                    multiplying = false;
                }
                else if(input.charAt(i) == '*')
                {
                    multiplying = true;
                }
                else if(multiplying)
                {
                    currentMultiplier += input.charAt(i);
                }
                else
                {
                    currentSound += input.charAt(i);
                }
            }
            
            if(currentMultiplier == "")
            {
                currentMultiplier = "1";
            }
            for(int j = 0; j < Integer.parseInt(currentMultiplier); j++)
            {
                sounds.add(currentSound);
            }
        }
        
        public void printout()
        {
            System.out.println("Name: " + name);
            for(String sound : sounds)
            {
                System.out.print(sound + ", ");
            }
            System.out.println();
        }
        
        public String getName()
        {
            return name;
        }
        
        public ArrayList<String> getSounds()
        {
            return sounds;
        }
        
        public String getRandomSound()
        {
            return(sounds.get(randomizer.nextInt(sounds.size())));
        }
        
        public int indexOf(String x)
        {
            for(int i = x.length(); i > 0; i--)
            {
                if(sounds.contains(x.substring(0, i)))
                {
                    return sounds.indexOf(x.substring(0, i));
                }
            }
            return 0;
        }
        
        public String get(int index)
        {
            return(sounds.get(index));
        }
    }
    
    private class SyllableList
    {
        private ArrayList<String> syllableList;
        
        public SyllableList(String input)
        {
            syllableList = new ArrayList<String>();
            input = input.replaceAll(" ","");
            
            for(String line : input.split("\n"))
            {
                boolean multiplying = false;
                String currentSyllable = "";
                String currentMultiplier = "";
                for(int i = 0; i < line.length(); i++)
                {
                    if(line.charAt(i) == '*')
                    {
                        multiplying = true;
                        currentSyllable += line.charAt(i);
                    }
                    else if(line.charAt(i) == '}')
                    {
                        multiplying = false;
                        currentSyllable += currentMultiplier;
                        currentMultiplier = "";
                        currentSyllable += line.charAt(i);
                    }
                    else if(line.charAt(i) == '|')
                    {
                        multiplying = false;
                        currentSyllable += currentMultiplier;
                        currentMultiplier = "";
                        currentSyllable += line.charAt(i);
                    }
                    else if(multiplying)
                    {
                        currentMultiplier += line.charAt(i);
                    }
                    else
                    {
                        currentSyllable += line.charAt(i);
                    }
                }
                if(currentMultiplier == "")
                {
                    currentMultiplier = "1";
                }
                if(currentSyllable.charAt(currentSyllable.length() - 1) == '*')
                {
                    currentSyllable = currentSyllable.substring(0,currentSyllable.length() - 1);
                }
                for(int j = 0; j < Integer.parseInt(currentMultiplier); j++)
                {
                    syllableList.add(currentSyllable);
                }
            }
        }
    
        public void printout()
        {
            for(String syllableType : syllableList)
            {
                System.out.println(syllableType);
            }
        }
        
        public ArrayList<String> getSyllableTypes()
        {
            return syllableList;
        }
        
        public String getRandomType()
        {
            String out = "";
            String syllableType = syllableList.get(randomizer.nextInt(syllableList.size()));
            ArrayList<Integer> parens = new ArrayList<Integer>();
            parens.add(1);
            ArrayList<String> bracketed = new ArrayList<String>();
            String bracketItem = "";
            boolean multiplying = false;
            String currentMultiplyer = "";
            for(int i = 0; i < syllableType.length(); i++)
            {
                if(syllableType.charAt(i) == '(')
                {
                    parens.add(randomizer.nextInt(2));
                }
                else if(syllableType.charAt(i) == ')')
                {
                    parens.remove(parens.size() - 1);
                }
                else if(!parens.contains(0))
                {
                    if(syllableType.charAt(i) == '{')
                    {
                        bracketed.add("[");
                    }
                    else if(syllableType.charAt(i) == '}')
                    {
                        if(currentMultiplyer.equals(""))
                        {
                            currentMultiplyer = "1";
                        }
                        for(int j = 0; j < Integer.parseInt(currentMultiplyer); j++)
                        {
                            bracketed.add(bracketItem);
                        }
                        bracketItem = "";
                        currentMultiplyer = "";
                        multiplying = false;
                        out += bracketed.get(randomizer.nextInt(bracketed.size() - 1) + 1);
                        bracketed = new ArrayList<String>();
                    }
                    else if(syllableType.charAt(i) == '|')
                    {
                        if(currentMultiplyer.equals(""))
                        {
                            currentMultiplyer = "1";
                        }
                        for(int j = 0; j < Integer.parseInt(currentMultiplyer); j++)
                        {
                            bracketed.add(bracketItem);
                        }
                        bracketItem = "";
                        currentMultiplyer = "";
                        multiplying = false;
                    }
                    else if(syllableType.charAt(i) == '*')
                    {
                        multiplying = true;
                    }
                    else if(multiplying)
                    {
                        currentMultiplyer += syllableType.charAt(i);
                    }
                    else if(bracketed.size() == 0)
                    {
                        out += syllableType.charAt(i);
                    }
                    else
                    {
                        bracketItem += syllableType.charAt(i);
                    }
                }
            }
            return out;
        }
    }
    
    private class SuprasegmentAnalyst
    {
        private int sylls;
        private ArrayList<String> rules = new ArrayList<String>();
        private ArrayList<String> applications = new ArrayList<String>();
        private ArrayList<String> appcodes = new ArrayList<String>();
        
        public SuprasegmentAnalyst(String ruleInput, int _sylls)
        {
            sylls = _sylls;
            ruleInput = ruleInput.replace(" ","");
            for(int i = 0; i < sylls; i++)
            {
                applications.add("");
            }
            if(!ruleInput.replace("\n","").equals(""))
            {
                for(String line : ruleInput.split("\n"))
                {
                    appcodes.add(line.split(":")[0]);
                    if((line.split(":")[0]).equals("H"))
                    {
                        int harmonic = randomizer.nextInt((line.split(":")[1]).split(";").length);
                        rules.add((line.split(":")[1]).split(";")[harmonic]);
                    }
                    else
                    {
                        rules.add(line.split(":")[1]);
                    }
                }
                for(int code = 0; code < appcodes.size(); code++)
                {
                    if(appcodes.get(code).equals("H"))
                    {
                        for(int i = 0; i < sylls; i++)
                        {
                            applications.set(i, applications.get(i) + code);
                        }
                    }
                    else if(appcodes.get(code).equals("A"))
                    {
                        int i = randomizer.nextInt(sylls);
                        applications.set(i, applications.get(i) + code);
                    }
                }
            }
        }
        
        public String apply(int syllindex, String input)
        {
            String toApply = applications.get(syllindex);
            for(int i = 0; i < toApply.length(); i++)
            {
                for(String rule : rules.get(Integer.parseInt(Character.toString(toApply.charAt(i)))).split(","))
                {
                    if(rule.equals("~"))
                    {
                        rule = "#>#/_";
                    }
                    input = applyRule(rule, input);
                }
            }
            return input;
        }
    }
    
    private void restoreDefaults()
    {
        soundTypesPanel.setText("C = p, t, k, m, n, l\nU = a, i, u\nO = a, e, o\nN = n\nS = s\nM = m, p\nL = a, e, i, o, u\nH = á, é, í, ó, ú");
        changeRulesPanel.setText("n>m/_M\ns>sh/_i/a_");
        syllableTypesPanel.setText("{(S)C*5|S|*2}U(N)");
        wordRulesPanel.setText("H: U>O/_; ~\nA: L>H/_");
    }
    
    public void runGenerator()
    {
        outputPanel.setText("");
        currentUnderlyingOutput = "";
        
        soundTypes = new ArrayList<SoundList>();
        for(String line : soundTypesPanel.getText().split("\n"))
        {
            soundTypes.add(new SoundList(line));
        }
        
        syllableTypes = new SyllableList(syllableTypesPanel.getText());
        String currentWord;
        for(int word = 0; word < wordCountSliderPanel.getValue(); word++)
        {
            currentWord = "";
            int sylls = syllableCountSliderPanel.getRandomValue();
            SuprasegmentAnalyst seg = new SuprasegmentAnalyst(wordRulesPanel.getText(), sylls);
            for(int syllindex = 0; syllindex < sylls; syllindex++)
            {
                String currentSyllableType = syllableTypes.getRandomType();
                String currentSyllable = "";
                for(int i = 0; i < currentSyllableType.length(); i++)
                {
                    for(SoundList soundType : soundTypes)
                    {
                        if(currentSyllableType.substring(i, i+1).equals(soundType.getName()))
                        {
                            currentSyllable += soundType.getRandomSound();
                        }
                    }
                }
                currentSyllable = seg.apply(syllindex, currentSyllable);
                currentWord += currentSyllable;
            }
            currentUnderlyingOutput += (currentWord + "\n");
        }
        
        applySoundChanges();
    }
    
    public void applySoundChanges()
    {
        String out = "";
        if(outputPanel.getFormat())
        {
            out += "     ";
        }
        boolean isSentenceBound = true;
        String[] endpuncts = {".",".",".",".",".",".",".",".",".","!","?"};
        String[] interpuncts = {",",",",",",",",",",",",",",",",",",",",",",",",",",";"};
        boolean inQuotes = false;
        
        if(scaMenuItem.getState())
        {
            currentUnderlyingOutput = soundChangeInputPanel.getText();
        }
        
        for(String word : currentUnderlyingOutput.split("\n"))
        {
            String changedWord = word;
            if(!changeRulesPanel.getText().replace(" ","").replace("\n","").equals(""))
            {
                for(String rule : changeRulesPanel.getText().split("\n"))
                {
                    changedWord = applyRule(rule, changedWord);
                }
            }
            
            String spacer = "\n";
            if(outputPanel.getShowChanges())
            {
                out += (word + " > ");
            }
            else if(outputPanel.getFormat())
            {
                spacer = " ";
                if(isSentenceBound)
                {
                    if(!inQuotes && randomizer.nextInt(15) == 0)
                    {
                        out += "\"";
                        inQuotes = true;
                    }
                    changedWord = capitalize(changedWord);
                    isSentenceBound = false;
                }
                else if(randomizer.nextInt(8) == 0)
                {
                    changedWord += endpuncts[randomizer.nextInt(endpuncts.length)];
                    isSentenceBound = true;
                    if(!inQuotes && randomizer.nextInt(7) == 0)
                    {
                        changedWord += "\n     ";
                    }
                    if(inQuotes && randomizer.nextInt(2) == 0)
                    {
                        changedWord += "\"";
                        inQuotes = false;
                    }
                }
                else if(randomizer.nextInt(5) == 0)
                {
                    changedWord += interpuncts[randomizer.nextInt(interpuncts.length)];
                }
            }
            out += (changedWord + spacer);
        }
        
        out = out.substring(0, out.length() - 1);
        if(outputPanel.getFormat() && !isSentenceBound)
        {
            out += endpuncts[randomizer.nextInt(endpuncts.length)];
        }
        
        outputPanel.setText(out);
    }


    public String applyRule(String rule, String input)
    {
        String condition = (rule.split("/")[1]);
        String precondition = "";
        String postcondition = "";
        String preexception = "$";
        String postexception = "$";
        if(condition.charAt(0) != '_')
        {
            precondition = condition.split("_")[0];
        }
        if(condition.charAt(condition.length() - 1) != '_')
        {
            postcondition = condition.split("_")[1];
        }
        if(rule.split("/").length == 3)
        {
            String exception = (rule.split("/")[2]);
            if(exception.charAt(0) != '_')
            {
                preexception = exception.split("_")[0];
            }
            if(exception.charAt(exception.length() - 1) != '_')
            {
                postexception = exception.split("_")[1];
            }
        }
        String forms = (rule.split("/")[0]);
        String before = forms.split(">")[0];
        String after = "";
        if(forms.charAt(forms.length() - 1) != '>')
        {
            after = forms.split(">")[1];
        }
        
        input = ("##" + input + "##");
        String output = "";
        
        for(int i = 2; i < input.length() - 2;)
        {
            boolean isBefore = applies(before, input, i, 0, before.length());
            
            boolean preconditionApplies = false;
            if(isBefore)
            {
                preconditionApplies = applies(precondition, input, i, -1, before.length());
            }
            
            boolean postconditionApplies = false;
            if(preconditionApplies)
            {
                postconditionApplies = applies(postcondition, input, i, 1, before.length());
            }
            
            boolean preexceptionApplies = true;
            if(postconditionApplies)
            {
                preexceptionApplies = applies(preexception, input, i, -1, before.length());
            }
            
            boolean postexceptionApplies = true;
            if(postconditionApplies)
            {
                postexceptionApplies = applies(postexception, input, i, 1, before.length());
            }
                
            if(!preexceptionApplies && !postexceptionApplies)
            {
                String toAdd = "";
                int corr = 0;
                int len = before.length();
                for(int j = 0; j < before.length(); j++)
                {
                    if(isCaps(before.charAt(j)))
                    {
                        corr = soundTypeIndex(before.charAt(j)).indexOf(input.substring(i + j, input.length()));
                        len += soundTypeIndex(before.charAt(j)).get(corr).length() - 1;
                    }
                }
                for(int j = 0; j < after.length(); j++)
                {
                    if(isCaps(after.charAt(j)))
                    {
                        toAdd += soundTypeIndex(after.charAt(j)).get(corr);
                    }
                    else
                    {
                        toAdd += after.charAt(j);
                    }
                }
                output += toAdd;
                i += len;
            }
            else
            {
                output += input.charAt(i);
                i++;
            }
        }
        return(output.replace("#", ""));
    }
    
    public boolean applies(String crit, String input, int index, int position, int beforeLength)
    {
        boolean expanded = false;
        boolean applies = false;
        ArrayList<String> poss = new ArrayList<String>();
        poss.add(crit);
        while(!expanded)
        {
            expanded = true;
            ArrayList<String> expansion = new ArrayList<String>();
            for(String item : poss)
            {
                boolean containsCaps = false;
                for(int i = 0; i < item.length(); i++)
                {
                    if(isCaps(item.charAt(i)))
                    {
                        expanded = false;
                        containsCaps = true;
                        for(String sound : soundTypeIndex(item.charAt(i)).getSounds())
                        {
                            expansion.add(item.substring(0,i) + sound + item.substring(i+1));;
                        }
                    }
                }
                if(!containsCaps)
                {
                    expansion.add(item);
                }
            }
            poss = expansion;
        }
        for(String x : poss)
        {
            int start;
            int end;
            if(position == -1)
            {
                start = index - x.length();
                end = index;
            }
            else if(position == 1)
            {
                start = index + beforeLength;
                end = index + beforeLength + x.length();
            }
            else
            {
                start = index;
                end = index + x.length();
            }
            if(start >= 0 && end < input.length() && input.substring(start, end).equals(x))
            {
                applies = true;
            }
        }
        return applies;
    }
    
    private SoundList soundTypeIndex(char c)
    {
        for(SoundList soundType : soundTypes)
        {
            if(soundType.getName().equals("" + c))
            {
                return soundType;
            }
        }
        return null;
    }
    
    private boolean isCaps(char c)
    {
        return(c>='A'&&c<='Z');
    }
    
    private String capitalize(String line)
    {
        return(Character.toUpperCase(line.charAt(0)) + line.substring(1));
    }
    
    public static void main(String[] args)
    {
        new WordGenerator();
    }
}