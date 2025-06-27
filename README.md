# Neural Development Simulation

The Neuron Growing Simulator is a graphical simulation tool that models the development and connection of neural cells at a cellular level. It uses basic biological principles such as soma, dendrites, axons, and nucleus formation to visualize a growing neural network in real-time.

![image](https://github.com/user-attachments/assets/eb2aed58-8f43-4832-8338-d15045e0c36c)

___

## Features

- Simulation of neural structures including nucleus, soma, dendrites, axons, and synaptic terminals
- Energy distribution and threshold-based growth control
- Self-organizing network expansion through terminal connections
- Random mutation-based nucleus creation
- Real-time visualization and signal tracking
- Optional experimental branching behavior

## Simulation Elements

### Nucleus (N)
The nucleus is the central structure of every neuron. It can expand and generate a surrounding soma shell. With enough energy, it spreads radially into neighboring cells.

### Soma (S)
The soma forms the outer shell around the nucleus. It acts as a starting point for dendrite formation and may develop into a new nucleus under certain conditions.

### Dendrites (D)
Dendrites emerge from the soma and extend into adjacent free areas. They serve as the receiving arms for neural signals. Under certain conditions, dendrites may also branch.

### Axons (A)
Axons grow from the soma and seek connections with dendrites to form terminals. They transfer energy in the form of signals and initiate neural communication.

### Terminals (T)
Terminals connect dendrites from different origins. When a terminal is created, a link between the associated origins is stored, and an interaction signal is generated.

## Parameters

- Mutation Threshold: Controls the probability of mutations during nucleus creation
- Formation Distance: Minimum distance to other nuclei required to form a new one
- Dendrite Energy Loss Threshold: Controls how much energy is lost during dendrite formation
- Connection Tightness: Controls the density of axon-dendrite connection points
- Network Expansion: Enables creation of new nuclei once sufficient synaptic connections exist
- Branching: Enables experimental dendrite branching with additional control parameters

## Defining Initial Neurons

To create initial seed cells in the simulation, you can define them manually in the `tempset`. These cells act as the starting point for neural growth.

Each entry in the `tempset` list follows this structure:

`[(x, y), structure_type, tribe, origin, energy]`

Where:
- `(x, y)` are the grid coordinates of the cell (integers)
- `structure_type` defines the function of the cell (single character)
- `tribe` is a string identifier for dendritic branches
- `origin` is an integer ID representing the unique neuron identity
- `energy` is a floating-point number controlling the growth potential

### Structure Types

Defines the role of the cell in the neural structure:

- `N` = **Nucleus** – The central core of a neuron, capable of generating a soma shell
- `S` = **Soma** – The body around the nucleus; serves as a base for dendrites and axons
- `D` = **Dendrite** – A branching receiver that connects to axons from other neurons
- `A` = **Axon** – A growing structure that seeks dendrites to form terminals
- `T` = **Terminal** – A connection point where dendrites and axons meet, forming communication pathways

### Tribe

A four-character alphanumeric code (e.g., `FQ3C`) that identifies a dendritic or axonal sub-network within a neuron. Tribes help track which branches belong to which neuron and determine interaction compatibility.

### Origin

A unique integer used to distinguish one neuron from another. All parts (soma, dendrites, axons, terminals) that belong to the same neuron share the same `origin` value.

### Energy

A floating-point value that influences how far and fast a structure can grow. Typical values range between `0.0` and `1.0`. For example:
- `1.0` in a nucleus enables it to expand
- Lower energy values in axons or dendrites determine how growth is distributed

### Example

A single starting nucleus cell at position (100, 100) with full energy might look like this:

```python
tempset = [[(100, 100), "N", "AB12", 0, 1.0]]
```

## Visualization

The simulation uses a color-coded 2D grid display:

- Nucleus: #333333
- Soma: #4a4a4a
- Dendrites: #616161
- Axons: #4f4f4f
- Terminals: #8a8888

Cells are drawn onto a canvas and automatically updated. A text display in the top-left shows simulation parameters; signal tracking data is shown at the bottom center.

## Interaction Data

All terminal-based connections between origins are tracked. These connections are exported to a JSON file that logs the temporal progression and signal distribution.

## Requirements

- Python 3
- Tkinter for GUI rendering
- No external libraries required

## Use Cases

- Educational visualization of neural growth processes
- Experimental testing of neural system rules

## Notes

- The branching feature is experimental and may produce unpredictable results
- The simulation is stochastic: each run yields a unique output
- Cell size and loop interval can be adjusted to improve performance
