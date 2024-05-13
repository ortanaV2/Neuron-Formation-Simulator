# Neuron Formation Simulator
![](https://github.com/ortanaV2/Neuron-Formation-Simulator/blob/main/PreviewPicture.png?raw=true)

Video about the Project: https://youtu.be/JZToyWf-heQ 
## Settings and Thresholds
- Mutation_threshold = (d)10 *"Controlls the randomness of the nucleus for a mutation in the sector"*
- Calculation_speed = (d)250 *"Time sleep for the iteration interval (in ms)"*
- Dendrite_formation_speed = (d)2 *"Controlls the growth chance of the dendrite picking a free coordinate"*
- Dendrite_formation_threshold = (d)0.97 *"Controlls the energy loss percentage per dendrite grown"*
- Nucleus_expansion = (d)True *"Decides if simulation is allowed to expand exponentially"*
- Branching = (d)False *"Decides if the dendrites are branching"*
  
## Tempset
With defining a cell in the tempset, you are able to create starting cells.

`[(x, y), structure_type, tribe, origin, energy]`

`[(int, int), char, str, int, double]`

### Structure types

> _Defines the part of the cell_

N = Nucleus (Core)

D = Dendrite (Receiver)

T = Terminal (ConnectionPoint)

S = Soma (Cell-Body)

### Tribe

> _Differentiates the branch of a dendrite_

Tribe codex example: "FQ3C"

### Origin

> _Distinguishes the individual neurons_

### Energy

> _Controlls the structure expansion_
