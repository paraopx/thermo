# Processing thermodynamic contributions

A brief description of what this project does and who it's for


## Features

- Light/dark mode toggle
- Live previews
- Fullscreen mode
- Cross platform


## Requirements
## Running code

To run tests, run the following command

```bash
  npm run test
```


## Example

```
Current file: bh3.out
Temperature used in calculation: 298.15
User-specified temperature and temperature used in calculation match!
Units of energy contributions are given as in Gaussian output file.
FileName: bh3.out
ZeroPointCorrection: 0.02609
ThermalCorrectionToEnergy: 0.02898
ThermalCorrectionToEnthalpy: 0.029924
ThermalCorrectionToGibbsFreeEnergy: 0.006815
SumOfElectronicAndZeroPointEnergies: -26.551331
SumOfElectronicAndThermalEnergies: -26.548441
SumOfElectronicAndThermalEnthalpies: -26.547496
SumOfElectronicAndThermalFreeEnergies: -26.570606
TotalE: 18.185
TotalS: 48.638
ElectronicE: 0.0
ElectronicS: 0.0
TranslationalE: 0.889
TranslationalS: 33.864
RotationalE: 0.889
RotationalS: 14.631
VibrationalE: 16.408
VibrationalS: 0.142
Electronic_Energy: -26.5774206974
Electronic_Energy_HighLevel: -26.6084393586
Solvation_Energy: -26.5770833369

Current file: nh3.out
Temperature used in calculation: 298.15
User-specified temperature and temperature used in calculation match!
Units of energy contributions are given as in Gaussian output file.
FileName: nh3.out
ZeroPointCorrection: 0.0345
ThermalCorrectionToEnergy: 0.037368
ThermalCorrectionToEnthalpy: 0.038312
ThermalCorrectionToGibbsFreeEnergy: 0.015418
SumOfElectronicAndZeroPointEnergies: -56.457386
SumOfElectronicAndThermalEnergies: -56.454518
SumOfElectronicAndThermalEnthalpies: -56.453574
SumOfElectronicAndThermalFreeEnergies: -56.476468
TotalE: 23.449
TotalS: 48.184
ElectronicE: 0.0
ElectronicS: 0.0
TranslationalE: 0.889
TranslationalS: 34.441
RotationalE: 0.889
RotationalS: 13.656
VibrationalE: 21.671
VibrationalS: 0.088
Electronic_Energy: -56.4918862626
Electronic_Energy_HighLevel: -56.5670951982
Solvation_Energy: -56.4932368734

Current file: nh3bh3.out
Temperature used in calculation: 298.15
User-specified temperature and temperature used in calculation match!
Units of energy contributions are given as in Gaussian output file.
FileName: nh3bh3.out
ZeroPointCorrection: 0.070054
ThermalCorrectionToEnergy: 0.073841
ThermalCorrectionToEnthalpy: 0.074785
ThermalCorrectionToGibbsFreeEnergy: 0.046609
SumOfElectronicAndZeroPointEnergies: -83.058878
SumOfElectronicAndThermalEnergies: -83.055091
SumOfElectronicAndThermalEnthalpies: -83.054147
SumOfElectronicAndThermalFreeEnergies: -83.082323
TotalE: 46.336
TotalS: 59.301
ElectronicE: 0.0
ElectronicS: 0.0
TranslationalE: 0.889
TranslationalS: 36.233
RotationalE: 0.889
RotationalS: 20.175
VibrationalE: 44.559
VibrationalS: 2.894
Electronic_Energy: -83.1289318756
Electronic_Energy_HighLevel: -83.2270962633
Solvation_Energy: -83.1401415587

deltaZeroPointCorrection: 5.9387 KCal/Mol
deltaElectronic_Energy (Δɛ): -37.4148 KCal/Mol
deltaElectronic_Energy_HighLevel (Δɛ'): -32.3551 KCal/Mol
deltaSolvation_Energy (ΔGsolv): -43.8131 KCal/Mol
deltaSolvation_Corr (Î”Gsolv-corr): -6.3983 KCal/Mol
deltaEtot: 4.7019 KCal/Mol
delta(Etot+Electronic_Energy): -32.713 KCal/Mol
deltaHcorr (ΔHcorr): 4.1095 KCal/Mol
delta(Hcorr+Electronic_Energy) (ΔH): -33.306 KCal/Mol
delta(Hcorr+High_Electronic_Energy) (ΔH'): -28.2456 KCal/Mol
deltaGcorr: 15.296 KCal/Mol
delta(Gcorr+Electronic_Energy) (ΔG): -22.1189 KCal/Mol
delta(Electronic_Energy_HighLevel+Gcorr+Solvation_Corr) (ΔG'): -23.4574 KCal/Mol
deltaStot: -0.0375 KCal/Mol-Kelvin
T*deltaStot: -11.1869 KCal/Mol
deltaStrans: -0.0321 KCal/Mol-Kelvin
T*deltaStrans: -9.5623 KCal/Mol
deltaSrot: -0.0081 KCal/Mol-Kelvin
T*deltaSrot: -2.4186 KCal/Mol
deltaSvib: 0.0027 KCal/Mol-Kelvin
T*deltaSvib: 0.7943 KCal/Mol
The absolute value of total entropy change: 42.848
deltaStrans%: 74.9%
deltaSrot%: 18.9%
deltaSvib%: 6.2%
```

![bh3nh3](https://github.com/paraopx/thermo/assets/117524398/8ee261e5-fc2d-4d47-866d-4f46ffbf00aa)


![nh3bh3_298](https://github.com/paraopx/thermo/assets/117524398/7a1eaa58-a0f4-4e92-a6bf-90fcfd509ed8)


