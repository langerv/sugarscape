sugarscape
==========

My implementation in Python of Epstein and Axtell's large scale agent-based computational model, the Sugarscape, to explore the role of social phenomenon such as seasonal migrations, pollution, sexual reproduction, combat, and transmission of disease and even culture.  
In other words: Cellular Automata + Agents = Sugarscape.

### Results

###### Evolution from random distribution under rules ({G1}, {M}):
![](results/sgEvolution0.png) ![](results/sgEvolution500.png)

###### Emergent diagonal waves of migration under rules ({G1}, {M}):
![](results/sgMigration0.png) ![](results/sgMigration6.png) ![](results/sgMigration20.png)

###### Seasonal migration and Hibernation resulting from rules ({S[1,8,50]}, {M}) and random distribution of agents:
![](results/sgSeasonal0.png) ![](results/sgSeasonal49.png) ![](results/sgSeasonal99.png)

###### Societal evolution through crossover of Genetic Attributes in Sexual Reproduction under rules ({G1}, {M, S}) coloring by agent vision:
![](results/sgSocietal0.png) ![](results/sgSocietal50.png) ![](results/sgSocietal500.png)

###### Cultural transmission by tag-flipping under rules ({G1}, {M, K}) coloring by tribes:
![](results/sgCultural0.png) ![](results/sgCultural132.png) ![](results/sgCultural694.png)

###### Combat between two tribbes under rules ({G1}, {Cinf}), with various outcomes: a) coexistence between Blue and Red b) Red dominance c) Blue dominance:
![](results/sgCombatCinfInitial.png) ![](results/sgCombatCinf10.png) ![](results/sgCombatCinf20.png)  
![](results/sgCombatCinfCoexistence.png) ![](results/sgCombatCinfRedDominance.png) ![](results/sgCombatCinfBlueDominance.png)

###### Trench war between two tribes under rules ({G1}, {C2, R[60, 100]}) coloring by tribes:
![](results/sgCombatC2Trench0.png) ![](results/sgCombatC2Trench100.png) ![](results/sgCombatC2Trench150.png)

### Instructions
Install Python 2.6 and above: https://www.python.org.  
Install Pygame 1.9 package: http://www.pygame.org.  
On command schell, execute: `python sugarscape.py`.  
Edit `sugarscape.py` and uncomment settings for the wanted simulation, run again.

##### Available controls during simulation:
- **[F1]**  : show current agents population.
- **[F2]**  : show current agents whealth histogram.
- **[F3]**  : show current agents metabolism and vision mean values.
- **[F12]** : start / pause / resume simulation.

### Reference
- Schelling, Thomas C. (1978). Micromotives and Macrobehavior, Norton.
- Epstein, Joshua M.; Axtell, Robert L. (1996). Growing Artificial Societies: Social Science From the Bottom Up, MIT/Brookings Institution.
