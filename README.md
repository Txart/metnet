# MetNet
Peatland METhane pore NETwork Mdodeling

## ToDo

  - Diffuse O2 from top to bottom
  - 

## Installation
--- Tested on Ubuntu 18.04 LTS---
New conda environment within Conda with minimal packages:

```
conda create -n [name of environment] -c python=3.7 numpy scipy matplotlib
```

Pip-install openpnm:

```
pip install openpnm
```

When running the Fickian diffusion, there is a mistake in the openpnm library.
TransientReactiveTransport should be changed in line 190: "newshape(self.Np, )" should be removed.

## How to use?
