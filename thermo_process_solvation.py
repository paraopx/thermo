import os
import sys
from os.path import exists
import re
from matplotlib import pyplot as plt

def find_dictionary_by_filename(dictionary_list, filename):
    for dictionary in dictionary_list:
        if 'FileName' in dictionary and dictionary['FileName'] == filename:
            return dictionary
    return None


if len(sys.argv) < 2:
    print("Please provide the directory path as a command-line argument.")
    sys.exit(1)

if len(sys.argv) <= 6:
    raise Exception("Not enough files given")

current_dir = sys.argv[1]
outputPath = sys.argv[2]
temperature = float(sys.argv[3])
print("\n")
print(f"User-specified Temperature: {temperature}")
print("\n")
firstFile = sys.argv[4]
secondFile = sys.argv[5]
thirdFile = sys.argv[6]
fourthFile = ""
if len(sys.argv) == 8:
    fourthFile = sys.argv[7]


def create_file_list():
    if len(sys.argv) == 8:
        file_list = [firstFile, secondFile, thirdFile, fourthFile]
        return file_list
    if len(sys.argv) == 7:
        file_list = [firstFile, secondFile, thirdFile]
        return file_list

files = create_file_list()
print(f"Files given by user: {files}")

if not os.path.isdir(current_dir):
    print("The provided directory does not exist.")
    sys.exit(1)

for _file in files:
    if exists(current_dir + "/" + _file):
        continue
    print(_file + " is not found")
    exit(1)

dictionaries = []

writer = open(current_dir + "\\" + outputPath, "wt", encoding='utf-8')

file_names = os.listdir(current_dir)

paths = []
y = []

# Iterate over the file names and filter the ones with ".out"
for file_name in file_names:
    if ".out" in file_name and file_name in files:
        paths.append(file_name)

print("\n")

print("Files to process: ", paths)

print("\n")


for idx in range(len(paths)):
    print("Current file: ", paths[idx])
    print("Path of output: " + current_dir + "\\" + paths[idx])
    writer.write("Current file: " + paths[idx] + "\n")
    f = open(current_dir + "\\" + paths[idx], "rt", encoding="utf-8")
    lines = f.readlines()
    f.close()

    star_pattern = re.compile(r'Polarizable Continuum Model \(PCM\)')

    for idx_, line in enumerate(lines):
        if re.match(star_pattern, line.strip()):
            break
    print(idx_)

    output_first_part = lines[:idx_]
    output_second_part = lines[idx_:]

    # Check temperature
    for line in output_first_part:
        if "Temperature" in line and "Pressure" in line:
            line = line.strip()
            splitted_0 = line.split(' ')
            temperature_ = float(splitted_0[3])
            print(f"Temperature used in calculation: {temperature_}")
            writer.write("Temperature used in calculation: " + str(temperature_) + "\n")

    if temperature_ != temperature:
        writer.write("Temperature given as argument does not match the temperature applied in the calculation!")
        raise ValueError("Temperature given as argument does not match the temperature applied in the calculation!")

    else:
        print("User-specified temperature and temperature used in calculation match!")
        writer.write("User-specified temperature and temperature used in calculation match!" + "\n")

    data = {}
    data["FileName"] = paths[idx]
    for line in output_first_part:
        line = line.replace("\n", "")
        if "Zero-point correction=" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            splitted[1] = splitted[1].split('(')[0]
            data["ZeroPointCorrection"] = float(splitted[1])

        elif "Thermal correction to Energy=" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["ThermalCorrectionToEnergy"] = float(splitted[1])
        elif "Thermal correction to Enthalpy=" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["ThermalCorrectionToEnthalpy"] = float(splitted[1])
        elif "Thermal correction to Gibbs Free Energy=" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["ThermalCorrectionToGibbsFreeEnergy"] = float(splitted[1])

        elif "Sum of electronic and zero-point Energies=" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["SumOfElectronicAndZeroPointEnergies"] = float(splitted[1])
        elif "Sum of electronic and thermal Energies" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["SumOfElectronicAndThermalEnergies"] = float(splitted[1])
        elif "Sum of electronic and thermal Enthalpies" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["SumOfElectronicAndThermalEnthalpies"] = float(splitted[1])
        elif "Sum of electronic and thermal Free Energies" in line:
            line = line.strip()
            line = line.replace(" ", "")
            splitted = line.split('=')
            data["SumOfElectronicAndThermalFreeEnergies"] = float(splitted[1])

    firstTable = []

    i = 0
    for line in output_first_part:
        if "E (Thermal)" in line and "CV" in line and "S" in line:
            break
        i += 1

    j = 0


    i += 1
    i += 1
    while j < 5:
        firstTable.append(lines[i].replace("\n", ""))
        i += 1
        j += 1

    for row in firstTable:
        splitted = row.split(" ")
        rowData = []
        for x in splitted:
            if x != "":
                rowData.append(x)

        if "Total" in rowData:
            data["TotalE"] = float(rowData[1])
            data["TotalS"] = float(rowData[3])
        elif "Electronic" in rowData:
            data["ElectronicE"] = float(rowData[1])
            data["ElectronicS"] = float(rowData[3])
        elif "Translational" in rowData:
            data["TranslationalE"] = float(rowData[1])
            data["TranslationalS"] = float(rowData[3])
        elif "Rotational" in rowData:
            data["RotationalE"] = float(rowData[1])
            data["RotationalS"] = float(rowData[3])
        elif "Vibrational" in rowData:
            data["VibrationalE"] = float(rowData[1])
            data["VibrationalS"] = float(rowData[3])

    output_first_part.reverse()
    idx2 = 0
    while "SCF Done:" not in output_first_part[idx2]:
        idx2 += 1
    splitted2 = output_first_part[idx2].split(' ')
    data["Electronic_Energy"] = float(splitted2[7])


    output_second_part.reverse()
    idx3 = 0
    while "SCF Done:" not in output_second_part[idx3]:
        idx3 += 1
    splitted3 = output_second_part[idx3].split(' ')
    data["Electronic_Energy_HighLevel"] = float(splitted3[7])

    idx4 = idx3
    while "SMD-CDS (non-electrostatic)" not in output_second_part[idx4]:
        idx4 += 1
    idx4 += 3
    splitted4 = output_second_part[idx4].split()
    data["Solvation_Energy"] = float(splitted4[4])


    print("Units of energy contributions are given as in Gaussian output file.")
    writer.write("Units of energy contributions are given as in Gaussian output file.\n")
    for key, value in data.items():
        print(key + ":" + str(value))
        writer.write(key + ": " + str(value) + "\n")
    writer.write("\n")
    print()
    dictionaries.append(data)


firstDict = find_dictionary_by_filename(dictionaries, firstFile)
secondDict = find_dictionary_by_filename(dictionaries, secondFile)
thirdDict = find_dictionary_by_filename(dictionaries, thirdFile)

if len(dictionaries) == 3:

    deltaZeroCorr = thirdDict["ZeroPointCorrection"] - firstDict["ZeroPointCorrection"] - secondDict["ZeroPointCorrection"]
    print("deltaZeroPointCorrection:", round((deltaZeroCorr * 627.503), 4),"KCal/Mol", "\n")
    deltaElectronic_Energy = thirdDict["Electronic_Energy"] - firstDict["Electronic_Energy"] - secondDict["Electronic_Energy"]
    print("deltaElectronic_Energy (Δε):", round((deltaElectronic_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaElectronic_Energy_HighLevel = thirdDict["Electronic_Energy_HighLevel"] - firstDict["Electronic_Energy_HighLevel"] - secondDict["Electronic_Energy_HighLevel"]
    print("deltaElectronic_Energy_HighLevel (Δε'):", round((deltaElectronic_Energy_HighLevel * 627.503), 4), "KCal/Mol","\n")
    deltaSolvation_Energy = thirdDict["Solvation_Energy"] - firstDict["Solvation_Energy"] - secondDict["Solvation_Energy"]
    print("deltaSolvation_Energy (ΔGsolv):", round((deltaSolvation_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaSolvation_Corr = (thirdDict["Solvation_Energy"] - thirdDict["Electronic_Energy"]) - (firstDict["Solvation_Energy"] - firstDict["Electronic_Energy"]) - (secondDict["Solvation_Energy"] - secondDict["Electronic_Energy"])
    print("deltaSolvation_Corr (ΔGsolv-corr):", round((deltaSolvation_Corr * 627.503), 4), "KCal/Mol","\n")
    deltaEtot = thirdDict["ThermalCorrectionToEnergy"] - firstDict["ThermalCorrectionToEnergy"] - secondDict["ThermalCorrectionToEnergy"]
    print("deltaEtot:", round((deltaEtot * 627.503), 4), "KCal/Mol", "\n")
    delta_Etot_Electronic_Energy = thirdDict["SumOfElectronicAndThermalEnergies"] - firstDict["SumOfElectronicAndThermalEnergies"] - secondDict["SumOfElectronicAndThermalEnergies"]
    print("delta(Etot+Electronic_Energy):", round((delta_Etot_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaHcorr = thirdDict["ThermalCorrectionToEnthalpy"] - firstDict["ThermalCorrectionToEnthalpy"] - secondDict["ThermalCorrectionToEnthalpy"]
    print("deltaHcorr (ΔHcorr):", round((deltaHcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_Electronic_Energy = thirdDict["SumOfElectronicAndThermalEnthalpies"] - firstDict["SumOfElectronicAndThermalEnthalpies"] - secondDict["SumOfElectronicAndThermalEnthalpies"]
    print("delta(Hcorr+Electronic_Energy) (ΔH):", round((delta_Hcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_High_Electronic_Energy = deltaHcorr + deltaElectronic_Energy_HighLevel
    print("delta(Hcorr+High_Electronic_Energy) (ΔH'):", round((delta_Hcorr_High_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaGcorr = thirdDict["ThermalCorrectionToGibbsFreeEnergy"] - firstDict["ThermalCorrectionToGibbsFreeEnergy"] - secondDict["ThermalCorrectionToGibbsFreeEnergy"]
    print("deltaGcorr: (ΔHcorr)", round((deltaGcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Gcorr_Electronic_Energy = thirdDict["SumOfElectronicAndThermalFreeEnergies"] - firstDict["SumOfElectronicAndThermalFreeEnergies"] - secondDict["SumOfElectronicAndThermalFreeEnergies"]
    print("delta(Gcorr+Electronic_Energy): (ΔG)", round((delta_Gcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")

    delta_Electronic_Energy_Gcorr_SolvationCorr = (thirdDict["Electronic_Energy_HighLevel"] + thirdDict["ThermalCorrectionToGibbsFreeEnergy"] + (thirdDict["Solvation_Energy"] - thirdDict["Electronic_Energy"])) -\
                                    (firstDict["Electronic_Energy_HighLevel"] + firstDict["ThermalCorrectionToGibbsFreeEnergy"] + (firstDict["Solvation_Energy"] - firstDict["Electronic_Energy"])) - \
                                    (secondDict["Electronic_Energy_HighLevel"] + secondDict["ThermalCorrectionToGibbsFreeEnergy"] + (secondDict["Solvation_Energy"] - secondDict["Electronic_Energy"]))
    print("delta(Electronic_Energy_HighLevel+Gcorr+Solvation_Corr) (ΔG'):", round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4), "KCal/Mol", "\n")

    deltaStot = thirdDict["TotalS"] - firstDict["TotalS"] - secondDict["TotalS"]
    print("deltaStot:", round(deltaStot * 0.001, 4), "KCal/Mol-Kelvin" "\n")
    print("T*deltaStot:", round(deltaStot * 0.001 * temperature, 4), "KCal/Mol-Kelvin" "\n")
    deltaStrans = thirdDict["TranslationalS"] - firstDict["TranslationalS"] - secondDict["TranslationalS"]
    print("deltaStrans:", round(deltaStrans*0.001, 4), " KCal/Mol-Kelvin", "\n")
    print("T*deltaStrans:", round(temperature * deltaStrans * 0.001, 4), "KCal/Mol", "\n")
    deltaSrot = thirdDict["RotationalS"] - firstDict["RotationalS"] - secondDict["RotationalS"]
    print("deltaSrot:", round(deltaSrot*0.001, 4), "KCal/Mol-Kelvin", "\n")
    print("T*deltaStrans:", round(temperature * deltaSrot * 0.001, 4), "KCal/Mol", "\n")
    deltaSvib = thirdDict["VibrationalS"] - firstDict["VibrationalS"] - secondDict["VibrationalS"]
    print("deltaSvib:", round(deltaSvib*0.001, 4), "KCal/Mol-Kelvin", "\n")
    print("T*deltaStrans:", round(temperature * deltaSvib * 0.001, 4), "KCal/Mol", "\n")

    print()

    TotalSAbsoluteValue = abs(deltaStrans) + abs(deltaSrot) + + abs(deltaSvib)
    print("The absolute value of total entropy change:", round(TotalSAbsoluteValue*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaStransPercent = (abs(deltaStrans) / TotalSAbsoluteValue) * 100
    deltaSrotPercent = (abs(deltaSrot) / TotalSAbsoluteValue) * 100
    deltaSvibPercent = (abs(deltaSvib) / TotalSAbsoluteValue) * 100
    print("deltaStrans%:", round(deltaStransPercent, 1), "%", "\n")
    print("deltaSrot%:", round(deltaSrotPercent, 1), "%", "\n")
    print("deltaSvib%:", round(deltaSvibPercent,1), "%", "\n")


    writer.write("deltaZeroPointCorrection: " + str(round((deltaZeroCorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy' + Δε): " + str(round((deltaElectronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy_HighLevel (Δε'): " + str(round((deltaElectronic_Energy_HighLevel * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSolvation_Energy (ΔGsolv): " + str(round((deltaSolvation_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSolvation_Corr (ΔGsolv-corr): " + str(round((deltaSolvation_Corr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaEtot: " + str(round((deltaEtot * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Etot+Electronic_Energy): " + str(round((delta_Etot_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaHcorr (ΔHcorr): " + str(round((deltaHcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+Electronic_Energy) (ΔH): " + str(round((delta_Hcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+High_Electronic_Energy) (ΔH'): " + str(round((delta_Hcorr_High_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaGcorr: " + str(round((deltaGcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Gcorr+Electronic_Energy) (ΔG): " + str(round((delta_Gcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")

    writer.write("delta(Electronic_Energy_HighLevel+Gcorr+Solvation_Corr) (ΔG'): " + str(round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4)) + " KCal/Mol" + "\n")

    writer.write("deltaStot: " + str(round(deltaStot*0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaStot: " + str(round(deltaStot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaStrans: " + str(round(deltaStrans * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaStrans: " + str(round(deltaStrans * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSrot: " + str(round(deltaSrot * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaSrot: " + str(round(deltaSrot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSvib: " + str(round(deltaSvib * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaSvib: " + str(round(deltaSvib * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")

    writer.write("The absolute value of total entropy change: " + str(round(TotalSAbsoluteValue, 4)) + "\n")
    writer.write("deltaStrans%: " + str(round(deltaStransPercent, 1)) + "%" + "\n")
    writer.write("deltaSrot%: " + str(round(deltaSrotPercent, 1)) + "%" + "\n")
    writer.write("deltaSvib%: " + str(round(deltaSvibPercent, 1)) + "%" + "\n")

    y = [round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4), round((delta_Gcorr_Electronic_Energy * 627.503), 4), round((deltaGcorr * 627.503), 4), round((delta_Hcorr_High_Electronic_Energy * 627.503), 4), round((delta_Hcorr_Electronic_Energy * 627.503), 4), round((deltaHcorr * 627.503), 4), round((deltaElectronic_Energy_HighLevel * 627.503), 4), round((deltaElectronic_Energy * 627.503), 4), round((deltaSolvation_Energy * 627.503), 4), round((deltaSolvation_Corr * 627.503), 4), round((deltaStot * 0.001 * temperature), 4), round((deltaStrans * 0.001 * temperature), 4), round((deltaSrot * 0.001 * temperature), 4), round((deltaSvib * 0.001 * temperature), 4)]

elif len(dictionaries) == 4:

    fourthDict = find_dictionary_by_filename(dictionaries, fourthFile)

    deltaZeroCorr = fourthDict["ZeroPointCorrection"] - firstDict["ZeroPointCorrection"] - secondDict["ZeroPointCorrection"] - thirdDict["ZeroPointCorrection"]
    print("\n", "The result of deltaZeroPointCorrection: ", round((deltaZeroCorr * 627.503), 4), "KCal/Mol", "\n")
    deltaElectronic_Energy = fourthDict["Electronic_Energy"] - firstDict["Electronic_Energy"] - secondDict["Electronic_Energy"] - thirdDict["Electronic_Energy"]
    print("deltaElectronic_Energy (Δε): ", round((deltaElectronic_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaElectronic_Energy_HighLevel = fourthDict["Electronic_Energy_HighLevel"] - firstDict["Electronic_Energy_HighLevel"] - secondDict["Electronic_Energy_HighLevel"]- thirdDict["Electronic_Energy_HighLevel"]
    print("deltaElectronic_Energy_HighLevel (Δε'):", round((deltaElectronic_Energy_HighLevel * 627.503), 4), "KCal/Mol","\n")
    deltaSolvation_Energy = fourthDict["Solvation_Energy"] - firstDict["Solvation_Energy"] - secondDict["Solvation_Energy"]- thirdDict["Solvation_Energy"]
    print("deltaSolvation_Energy (ΔGsolv):", round((deltaSolvation_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaSolvation_Corr = (fourthDict["Solvation_Energy"] - fourthDict["Electronic_Energy"]) - (firstDict["Solvation_Energy"] - firstDict["Electronic_Energy"]) - (secondDict["Solvation_Energy"] - secondDict["Electronic_Energy"]) - (thirdDict["Solvation_Energy"] - thirdDict["Electronic_Energy"])
    print("deltaSolvation_Corr (ΔGsolv-corr):", round((deltaSolvation_Corr * 627.503), 4), "KCal/Mol","\n")
    deltaEtot = fourthDict["ThermalCorrectionToEnergy"] - firstDict["ThermalCorrectionToEnergy"] - secondDict["ThermalCorrectionToEnergy"] - thirdDict["ThermalCorrectionToEnergy"]
    print("deltaEtot:", round((deltaEtot * 627.503), 4), "KCal/Mol", "\n")
    delta_Etot_Electronic_Energy = fourthDict["SumOfElectronicAndThermalEnergies"] - firstDict["SumOfElectronicAndThermalEnergies"] - secondDict["SumOfElectronicAndThermalEnergies"] - thirdDict["SumOfElectronicAndThermalEnergies"]
    print("delta(Etot+Electronic_Energy):", round((delta_Etot_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaHcorr = fourthDict["ThermalCorrectionToEnthalpy"] - firstDict["ThermalCorrectionToEnthalpy"] - secondDict["ThermalCorrectionToEnthalpy"] - thirdDict["ThermalCorrectionToEnthalpy"]
    print("deltaHcorr: (ΔHcorr)", round((deltaHcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_Electronic_Energy = fourthDict["SumOfElectronicAndThermalEnthalpies"] - firstDict["SumOfElectronicAndThermalEnthalpies"] - secondDict["SumOfElectronicAndThermalEnthalpies"] - thirdDict["SumOfElectronicAndThermalEnthalpies"]
    print("delta(Hcorr+Electronic_Energy) (ΔH):", round((delta_Hcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_High_Electronic_Energy = deltaHcorr + deltaElectronic_Energy_HighLevel
    print("delta(Hcorr+High_Electronic_Energy) (ΔH'):", round((delta_Hcorr_High_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaGcorr = fourthDict["ThermalCorrectionToGibbsFreeEnergy"] - firstDict["ThermalCorrectionToGibbsFreeEnergy"] - secondDict["ThermalCorrectionToGibbsFreeEnergy"] - thirdDict["ThermalCorrectionToGibbsFreeEnergy"]
    print("deltaGcorr: (ΔGcorr)", round((deltaGcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Gcorr_Electronic_Energy = fourthDict["SumOfElectronicAndThermalFreeEnergies"] - firstDict["SumOfElectronicAndThermalFreeEnergies"] - secondDict["SumOfElectronicAndThermalFreeEnergies"] - thirdDict["SumOfElectronicAndThermalFreeEnergies"]
    print("delta(Gcorr+Electronic_Energy) (ΔG):", round((delta_Gcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")

    delta_Electronic_Energy_Gcorr_SolvationCorr = (fourthDict["Electronic_Energy_HighLevel"] + fourthDict["ThermalCorrectionToGibbsFreeEnergy"] + (fourthDict["Solvation_Energy"] - fourthDict["Electronic_Energy"])) -\
                                    (firstDict["Electronic_Energy_HighLevel"] + firstDict["ThermalCorrectionToGibbsFreeEnergy"] + (firstDict["Solvation_Energy"] - firstDict["Electronic_Energy"])) - \
                                    (secondDict["Electronic_Energy_HighLevel"] + secondDict["ThermalCorrectionToGibbsFreeEnergy"] + (secondDict["Solvation_Energy"] - secondDict["Electronic_Energy"])) - \
                                    (thirdDict["Electronic_Energy_HighLevel"] + thirdDict["ThermalCorrectionToGibbsFreeEnergy"] + (thirdDict["Solvation_Energy"] - thirdDict["Electronic_Energy"]))
    print("delta(Electronic_Energy_HighLevel+Gcorr+Solvation_Corr) (ΔG'):", round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4), "KCal/Mol", "\n")

    deltaStot = fourthDict["TotalS"] - firstDict["TotalS"] - secondDict["TotalS"] - thirdDict["TotalS"]
    print("deltaStot:", round(deltaStot*0.001, 4), "KCal/Mol-Kelvin" "\n")
    print("T*deltaStot:", round(deltaStot * 0.001 * temperature, 4), "KCal/Mol-Kelvin" "\n")
    deltaStrans = fourthDict["TranslationalS"] - firstDict["TranslationalS"] - secondDict["TranslationalS"] - thirdDict["TranslationalS"]
    print("deltaStrans:", round(deltaStrans*0.001, 4), "KCal/Mol-Kelvin", "\n")
    print("T*deltaStrans:", round(temperature * deltaStrans * 0.001, 4), "KCal/Mol", "\n")
    deltaSrot = fourthDict["RotationalS"] - firstDict["RotationalS"] - secondDict["RotationalS"] - thirdDict["RotationalS"]
    print("deltaSrot:", round(deltaSrot*0.001, 4), "KCal/Mol-Kelvin", "\n")
    print("T*deltaSrot:", round(temperature * deltaSrot*0.001, 4), "KCal/Mol", "\n")
    deltaSvib = fourthDict["VibrationalS"] - firstDict["VibrationalS"] - secondDict["VibrationalS"] - thirdDict["VibrationalS"]
    print("deltaSvib:", round(deltaSvib*0.001, 4), "KCal/Mol-Kelvin", "\n")
    print("T*deltaSvib:", round(temperature * deltaSvib*0.001, 4), "KCal/Mol-Kelvin", "\n")

    print()

    TotalSAbsoluteValue = abs(deltaStrans) + abs(deltaSrot) + + abs(deltaSvib)
    print("The absolute value of total entropy change:", round(TotalSAbsoluteValue*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaStransPercent = (abs(deltaStrans) / TotalSAbsoluteValue) * 100
    deltaSrotPercent = (abs(deltaSrot) / TotalSAbsoluteValue) * 100
    deltaSvibPercent = (abs(deltaSvib) / TotalSAbsoluteValue) * 100
    print("The deltaStrans%:", round(deltaStransPercent, 1), "%", "\n")
    print("The deltaSrot%:", round(deltaSrotPercent, 1), "%", "\n")
    print("The deltaSvib%:", round(deltaSvibPercent, 1), "%", "\n")


    writer.write("The result of ddeltaZeroPointCorrection:" + str(round((deltaZeroCorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy (Δε): " + str(round((deltaElectronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy_HighLevel (Δε'): " + str(round((deltaElectronic_Energy_HighLevel * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSolvation_Energy (ΔGsolv): " + str(round((deltaSolvation_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSolvation_Corr (ΔGsolv-corr): " + str(round((deltaSolvation_Corr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaEtot: " + str(round((deltaEtot * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Etot+Electronic_Energy): " + str(round((delta_Etot_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaHcorr (ΔHcorr): " + str(round((deltaHcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+Electronic_Energy) (ΔH): " + str(round((delta_Hcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+High_Electronic_Energy) (ΔH'): " + str(round((delta_Hcorr_High_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaGcorr (ΔGcorr): " + str(round((deltaGcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Gcorr+Electronic_Energy) (ΔG): " + str(round((delta_Gcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")

    writer.write("delta(Electronic_Energy_HighLevel+Gcorr+Solvation_Corr) (ΔG'): " + str(round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4)) + " KCal/Mol" + "\n")

    writer.write("deltaStot: " + str(round(deltaStot*0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaStot: " + str(round(deltaStot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaStrans: " + str(round(deltaStrans * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaStrans: " + str(round(deltaStrans * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSrot: " + str(round(deltaSrot * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaSrot: " + str(round(deltaSrot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSvib: " + str(round(deltaSvib * 0.001, 4)) + " KCal/Mol-Kelvin" + "\n")
    writer.write("T*deltaSvib: " + str(round(deltaSvib * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")

    writer.write("The absolute value of total entropy change: " + str(round(TotalSAbsoluteValue, 4)) + "\n")
    writer.write("deltaStrans%: " + str(round(deltaStransPercent, 1)) + "%" + "\n")
    writer.write("deltaSrot%: " + str(round(deltaSrotPercent, 1)) + "%" + "\n")
    writer.write("deltaSvib%: " + str(round(deltaSvibPercent, 1)) + "%" + "\n")

    y = [round((delta_Electronic_Energy_Gcorr_SolvationCorr * 627.503), 4), round((delta_Hcorr_High_Electronic_Energy * 627.503), 4),  round((deltaHcorr * 627.503), 4), round((deltaElectronic_Energy_HighLevel * 627.503), 4), round((deltaSolvation_Energy * 627.503), 4), round((deltaSolvation_Corr * 627.503), 4), round((deltaStot * 0.001 * temperature), 4), round((deltaStrans * 0.001 * temperature), 4), round((deltaSrot * 0.001 * temperature), 4), round((deltaSvib * 0.001 * temperature), 4)]

writer.close()

mylabels = [r'$\Delta$' + "G'", r'$\Delta$' + "G", r'$\Delta$' + "Gcorr", r'$\Delta$' + "H'", r'$\Delta$' + "H", r'$\Delta$' + "Hcorr", r'$\Delta$' + "ε'", r'$\Delta$' + "ε", r'$\Delta$' + "Gsolv", r'$\Delta$' + "Gsolv-corr", "T·" + r'$\Delta$' + "Stot", "T·" + r'$\Delta$' + "Strans", "T·" + r'$\Delta$' + "Srot", "T·" + r'$\Delta$' + "Svib"]

rounded_values = [round(val, 1) for val in y]

plt.ylabel('y', fontsize=16)
plt.bar(mylabels, y, color='#BED0E8')
plt.title('Energy Contributions at ' + str(temperature) + " K", fontweight='bold', fontsize=16, y=1.05)

for i in range(len(mylabels)):
        plt.annotate(str(rounded_values[i]), textcoords='offset points', xytext=(0, 3), xy=(mylabels[i], rounded_values[i]), ha='center', va='bottom', fontsize=10)

plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.axhline(0, color='black', linewidth=0.5)

plt.tick_params(axis='both', which='both', length=0)

plt.xticks(fontsize=10, rotation=40.0)
plt.ylabel("value in kcal/mol")
plt.tight_layout()
plt.savefig(current_dir + "\\" + "energy_contributions.png")
plt.show()
