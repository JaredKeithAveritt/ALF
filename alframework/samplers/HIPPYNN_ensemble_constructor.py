import numpy as np
import sys

from hippynn.interfaces.ase_interface import HippynnCalculator
import hippynn.graphs

from alframework.samplers.ASE_ensemble_constructor import Well_Potential

from ase.calculators.calculator import Calculator as ASE_Calculator
from ase.calculators.calculator import all_changes
from ase.calculators.mixing import Mixer

class HIPYNN_MLMD_calculator(HippynnCalculator,Well_Potential):
 
    def __init__(self,models,well_params=None,debug_print=False):
        HippynnCalculator.__init__(self)
        Well_Potential.__init__(self, well_params))
        self.debug_print = debug_print
        ensemble_graph, _ = hippynn.graphs.make_ensemble(models)
        self.ensemble_energy = ensemble_graph.node_from_name("ensemble_energy")
        self.energy_node = self.ensemble_energy.mean
        self.extra_properties = {
            "ens_predictions": self.ensemble_energy.all,
            "ens_std": self.ensemble_energy.std,
        }
        self.calc = hippynn.interfaces.ase_interface.HippynnCalculator(
            energy=self.energy_node, extra_properties=self.extra_properties
        )
        self.implemented_properties = [
            "energy", "forces", "energy_stdev", "forces_stdev_mean", "forces_stdev_max"
        ]
    
    def calculate(self, atoms=None, properties=["energy"], system_changes=[]):
        super().calculate(atoms, properties, system_changes)
        self.calc.calculate(atoms, properties)
        self.results = self.calc.results


 
    def __init__(self, models, well_params=None, debug_print=False):
        # Initialize both parents explicitly
        HippynnCalculator.__init__(self)
        Well_Potential.__init__(self, well_params)
        self.debug_print = debug_print
        
        # Build an ensemble with the provided models
        ensemble_graph, _ = hippynn.graphs.make_ensemble(models)
        self.ensemble_energy = ensemble_graph.node_from_name("ensemble_energy")
        self.energy_node = self.ensemble_energy.mean
        
        # Prepare extra properties for the calculator
        self.extra_properties = {
            "ens_predictions": self.ensemble_energy.all,
            "ens_std": self.ensemble_energy.std,
        }
        
        # Wrap ensemble energy with an ASE compatible calculator
        self.calc = hippynn.interfaces.ase_interface.HippynnCalculator(
            energy=self.energy_node, extra_properties=self.extra_properties
        )
        
        # Optionally deduplicate implemented properties
        self.implemented_properties = list(set([
            "energy", "forces", "energy_stdev", "forces_stdev_mean", "forces_stdev_max"
        ]))
    
    def calculate(self, atoms=None, properties=None, system_changes=None):
        if properties is None:
            properties = ["energy"]
        if system_changes is None:
            system_changes = []
        
        super().calculate(atoms, properties, system_changes)
        self.calc.calculate(atoms, properties)
        self.results = self.calc.results

