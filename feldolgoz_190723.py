import os
#os.system("cls")
import sys
from os.path import exists

import numpy as np
from matplotlib import pyplot as plt

def find_dictionary_by_filename(dictionary_list, filename):
    for dictionary in dictionary_list:
        if 'FileName' in dictionary and dictionary['FileName'] == filename:
            return dictionary
    return None


# Check if the directory argument is provided
if len(sys.argv) < 2:
    print("Please provide the directory path as a command-line argument.")
    sys.exit(1)

if len(sys.argv) <= 6:
    raise Exception("Not enough files given")

# Get the directory path from command-line argument
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
        #print("len is 8")
        return file_list
    if len(sys.argv) == 7:
        file_list = [firstFile, secondFile, thirdFile]
        #print("len is 7")
        return file_list

files = create_file_list()
print(f"Files given by user: {files}")

# Check if the provided directory exists
if not os.path.isdir(current_dir):
    print("The provided directory does not exist.")
    sys.exit(1)

for _file in files:
    if exists(current_dir + "/" + _file):
        continue
    print(_file + " is not found")
    exit(1)

dictionaries = []

# The type of "writer" is file handling object. The name of the actual txt. file will be the name we assign to outputPath.
writer = open(outputPath, "wt")


# Enumerate files in the directory and place files into a list.
file_names = os.listdir(current_dir)


# Create a new list to store file names with ".out"
paths = []
y = []

# Iterate over the file names and filter the ones with ".out"
for file_name in file_names:
    if ".out" in file_name and file_name in files:
        paths.append(file_name)


# for file_in_path in files:
#     if file_in_path not in files:
#         print(f"{file_name} is not found")

print("\n")

# Print the output file names
print("Files to process: ", paths)

print("\n")

for idx in range(len(paths)):  # irhatnam for idx in paths:??????????
    print("Current file: ", paths[idx])
    writer.write("Current file: " + paths[idx] + "\n")
    f = open(paths[idx], "rt", encoding="utf-8")
    lines = f.readlines()
    f.close()

    # Check temperature
    for line in lines:
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
        print("Temperature check is OK!")
        writer.write("Temperature check is OK" + "\n")

    data = {}
    data["FileName"] = paths[idx]
    # Create a dictionary key called "Filename" and the respective value is the gaussianoutputfilename.out
    for line in lines:
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

        #data["Gcorr"] = data[""]

    firstTable = []

    # Megkeressük az első olyan sor indexét, amit fel szeretnénk dolgozni
    i = 0
    for line in lines:
        if "E (Thermal)" in line and "CV" in line and "S" in line:
            break
        i += 1

    # Ezzel számoljuk, hágy még hány sort kell feldolgozni
    j = 0

    # Ezzel indexeljük a sorokat
    i += 1
    i += 1
    while j < 5:
        firstTable.append(lines[i].replace("\n", ""))
        i += 1
        j += 1

    for row in firstTable:
        splitted = row.split(" ")
        rowData = []
        for x in splitted:  # Removing space character from the list "splitted". The splitted = splitted.replace(" ", "") cannot work because of the absence of necessary delimiter.
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

    lines.reverse()
    idx2 = 0
    while "SCF Done:" not in lines[idx2]:
        idx2 += 1
    splitted2 = lines[idx2].split(' ')
    data["Electronic_Energy"] = float(splitted2[7])

    print("Units of energy contributions are given as in Gaussian output file.")
    writer.write("Units of energy contributions are given as in Gaussian output file.\n")
    for key, value in data.items():
        print(key + ":" + str(value))
        writer.write(key + ": " + str(value) + "\n")
    writer.write("\n")
    print()
    dictionaries.append(data)  # "data" dedicated to a .out file is a dictionary where all energy components are stored. "dictionaries" is just a list where each "data" dictionaries are kept.

firstDict = find_dictionary_by_filename(dictionaries, firstFile)  # firstDict contains all the energy components of the .out file given first.
secondDict = find_dictionary_by_filename(dictionaries, secondFile)
thirdDict = find_dictionary_by_filename(dictionaries, thirdFile)

if len(dictionaries) == 3:

    deltaZeroCorr = thirdDict["ZeroPointCorrection"] - firstDict["ZeroPointCorrection"] - secondDict["ZeroPointCorrection"]
    print("deltaZeroPointCorrection:", round((deltaZeroCorr * 627.503), 4),"KCal/Mol", "\n")
    deltaElectronic_Energy = thirdDict["Electronic_Energy"] - firstDict["Electronic_Energy"] - secondDict["Electronic_Energy"]
    print("deltaElectronic_Energy:", round((deltaElectronic_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaEtot = thirdDict["ThermalCorrectionToEnergy"] - firstDict["ThermalCorrectionToEnergy"] - secondDict["ThermalCorrectionToEnergy"]
    print("deltaEtot:", round((deltaEtot * 627.503), 4), "KCal/Mol", "\n")
    delta_Etot_Electronic_Energy = thirdDict["SumOfElectronicAndThermalEnergies"] - firstDict["SumOfElectronicAndThermalEnergies"] - secondDict["SumOfElectronicAndThermalEnergies"]
    print("delta(Etot+Electronic_Energy):", round((delta_Etot_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaHcorr = thirdDict["ThermalCorrectionToEnthalpy"] - firstDict["ThermalCorrectionToEnthalpy"] - secondDict["ThermalCorrectionToEnthalpy"]
    print("deltaHcorr:", round((deltaHcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_Electronic_Energy = thirdDict["SumOfElectronicAndThermalEnthalpies"] - firstDict["SumOfElectronicAndThermalEnthalpies"] - secondDict["SumOfElectronicAndThermalEnthalpies"]
    print("delta(Hcorr+Electronic_Energy):", round((delta_Hcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaGcorr = thirdDict["ThermalCorrectionToGibbsFreeEnergy"] - firstDict["ThermalCorrectionToGibbsFreeEnergy"] - secondDict["ThermalCorrectionToGibbsFreeEnergy"]
    print("deltaGcorr:", round((deltaGcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Gcorr_Electronic_Energy = thirdDict["SumOfElectronicAndThermalFreeEnergies"] - firstDict["SumOfElectronicAndThermalFreeEnergies"] - secondDict["SumOfElectronicAndThermalFreeEnergies"]
    print("delta(Gcorr+Electronic_Energy):", round((delta_Gcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaStot = thirdDict["TotalS"] - firstDict["TotalS"] - secondDict["TotalS"]
    print("deltaStot:", round(deltaStot*0.001, 4), "KCal/Mol-Kelvin" "\n")
    print("T*deltaStot:", round(deltaStot * 0.001 * temperature, 4), "KCal/Mol-Kelvin" "\n")
    deltaStrans = thirdDict["TranslationalS"] - firstDict["TranslationalS"] - secondDict["TranslationalS"]
    print("deltaStrans:", round(deltaStrans*0.001, 4), " KCal/Mol-Kelvin", "\n")
    deltaSrot = thirdDict["RotationalS"] - firstDict["RotationalS"] - secondDict["RotationalS"]
    print("deltaSrot:", round(deltaSrot*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaSvib = thirdDict["VibrationalS"] - firstDict["VibrationalS"] - secondDict["VibrationalS"]
    print("deltaSvib:", round(deltaSvib*0.001, 4), "KCal/Mol-Kelvin", "\n")

    TotalSAbsoluteValue = abs(deltaStrans) + abs(deltaSrot) + + abs(deltaSvib)
    print("The absolute value of total entropy change:", round(TotalSAbsoluteValue*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaStransPercent = (abs(deltaStrans) / TotalSAbsoluteValue) * 100
    deltaSrotPercent = (abs(deltaSrot) / TotalSAbsoluteValue) * 100
    deltaSvibPercent = (abs(deltaSvib) / TotalSAbsoluteValue) * 100
    print("deltaStrans%:", round(deltaStransPercent, 1), "%", "\n")
    print("deltaSrot%:", round(deltaSrotPercent, 1), "%", "\n")
    print("deltaSvib%:", round(deltaSvibPercent,1), "%", "\n")

    writer.write("deltaZeroPointCorrection: " + str(round((deltaZeroCorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy: " + str(round((deltaElectronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaEtot: " + str(round((deltaEtot * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Etot+Electronic_Energy): " + str(round((delta_Etot_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaHcorr: " + str(round((deltaHcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+Electronic_Energy): " + str(round((delta_Hcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaGcorr: " + str(round((deltaGcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Gcorr+Electronic_Energy): " + str(round((delta_Gcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaStot: " + str(round(deltaStot, 4)) + " KCal/Mol" + "\n")
    writer.write("T*deltaStot: " + str(round(deltaStot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaStrans: " + str(round(deltaStrans, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSrot: " + str(round(deltaSrot, 4)) + " KCal/Mol" + "\n")
    writer.write("deltaSvib: " + str(round(deltaSvib, 4)) + " KCal/Mol" + "\n")

    writer.write("The absolute value of total entropy change: " + str(round(TotalSAbsoluteValue, 4)) + "\n")
    writer.write("deltaStrans%: " + str(round(deltaStransPercent, 1)) + "%" + "\n")
    writer.write("deltaSrot%: " + str(round(deltaSrotPercent, 1)) + "%" + "\n")
    writer.write("deltaSvib%: " + str(round(deltaSvibPercent, 1)) + "%" + "\n")

elif len(dictionaries) == 4:

    fourthDict = find_dictionary_by_filename(dictionaries, fourthFile)

    deltaZeroCorr = fourthDict["ZeroPointCorrection"] - firstDict["ZeroPointCorrection"] - secondDict["ZeroPointCorrection"] - thirdDict["ZeroPointCorrection"]
    print("\n", "The result of deltaZeroPointCorrection: ", round((deltaZeroCorr * 627.503), 4), "KCal/Mol", "\n")
    deltaElectronic_Energy = fourthDict["Electronic_Energy"] - firstDict["Electronic_Energy"] - secondDict["Electronic_Energy"] - thirdDict["Electronic_Energy"]
    print("The result of deltaElectronic_Energy: ", round((deltaElectronic_Energy * 627.503), 4), "KCal/Mol","\n")
    deltaEtot = fourthDict["ThermalCorrectionToEnergy"] - firstDict["ThermalCorrectionToEnergy"] - secondDict["ThermalCorrectionToEnergy"] - thirdDict["ThermalCorrectionToEnergy"]
    print("deltaEtot:", round((deltaEtot * 627.503), 4), "KCal/Mol", "\n")
    delta_Etot_Electronic_Energy = fourthDict["SumOfElectronicAndThermalEnergies"] - firstDict["SumOfElectronicAndThermalEnergies"] - secondDict["SumOfElectronicAndThermalEnergies"] - thirdDict["SumOfElectronicAndThermalEnergies"]
    print("delta(Etot+Electronic_Energy):", round((delta_Etot_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaHcorr = fourthDict["ThermalCorrectionToEnthalpy"] - firstDict["ThermalCorrectionToEnthalpy"] - secondDict["ThermalCorrectionToEnthalpy"] - thirdDict["ThermalCorrectionToEnthalpy"]
    print("deltaHcorr:", round((deltaHcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Hcorr_Electronic_Energy = fourthDict["SumOfElectronicAndThermalEnthalpies"] - firstDict["SumOfElectronicAndThermalEnthalpies"] - secondDict["SumOfElectronicAndThermalEnthalpies"] - thirdDict["SumOfElectronicAndThermalEnthalpies"]
    print("delta(Hcorr+Electronic_Energy):", round((delta_Hcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaGcorr = fourthDict["ThermalCorrectionToGibbsFreeEnergy"] - firstDict["ThermalCorrectionToGibbsFreeEnergy"] - secondDict["ThermalCorrectionToGibbsFreeEnergy"] - thirdDict["ThermalCorrectionToGibbsFreeEnergy"]
    print("deltaGcorr:", round((deltaGcorr * 627.503), 4), "KCal/Mol", "\n")
    delta_Gcorr_Electronic_Energy = fourthDict["SumOfElectronicAndThermalFreeEnergies"] - firstDict["SumOfElectronicAndThermalFreeEnergies"] - secondDict["SumOfElectronicAndThermalFreeEnergies"] - thirdDict["SumOfElectronicAndThermalFreeEnergies"]
    print("delta(Gcorr+Electronic_Energy):", round((delta_Gcorr_Electronic_Energy * 627.503), 4), "KCal/Mol", "\n")
    deltaStot = fourthDict["TotalS"] - firstDict["TotalS"] - secondDict["TotalS"] - thirdDict["TotalS"]
    print("The result of deltaStot:", round(deltaStot*0.001, 4), "KCal/Mol-Kelvin" "\n")
    print("T*deltaStot:", round(deltaStot * 0.001 * temperature, 4), "KCal/Mol-Kelvin" "\n")
    deltaStrans = fourthDict["TranslationalS"] - firstDict["TranslationalS"] - secondDict["TranslationalS"] - thirdDict["TranslationalS"]
    print("The result of deltaStrans:", round(deltaStrans*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaSrot = fourthDict["RotationalS"] - firstDict["RotationalS"] - secondDict["RotationalS"] - thirdDict["RotationalS"]
    print("The result of deltaSrot:", round(deltaSrot*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaSvib = fourthDict["VibrationalS"] - firstDict["VibrationalS"] - secondDict["VibrationalS"] - thirdDict["VibrationalS"]
    print("The result of deltaSvib:", round(deltaSvib*0.001, 4), "KCal/Mol-Kelvin", "\n")

    TotalSAbsoluteValue = abs(deltaStrans) + abs(deltaSrot) + + abs(deltaSvib)
    print("The absolute value of total entropy change:", round(TotalSAbsoluteValue*0.001, 4), "KCal/Mol-Kelvin", "\n")
    deltaStransPercent = (abs(deltaStrans) / TotalSAbsoluteValue) * 100
    deltaSrotPercent = (abs(deltaSrot) / TotalSAbsoluteValue) * 100
    deltaSvibPercent = (abs(deltaSvib) / TotalSAbsoluteValue) * 100
    print("The deltaStrans%:", round(deltaStransPercent, 1), "%", "\n")
    print("The deltaSrot%:", round(deltaSrotPercent, 1), "%", "\n")
    print("The deltaSvib%:", round(deltaSvibPercent, 1), "%", "\n")

    writer.write("The result of ddeltaZeroPointCorrection:" + str(round((deltaZeroCorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaElectronic_Energy: " + str(round((deltaElectronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaEtot: " + str(round((deltaEtot * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Etot+Electronic_Energy): " + str(round((delta_Etot_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaHcorr: " + str(round((deltaHcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Hcorr+Electronic_Energy): " + str(round((delta_Hcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("deltaGcorr: " + str(round((deltaGcorr * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("delta(Gcorr+Electronic_Energy): " + str(round((delta_Gcorr_Electronic_Energy * 627.503), 4)) + " KCal/Mol" + "\n")
    writer.write("The result of deltaStot: " + str(round(deltaStot, 4)) + " KCal/Mol" + "\n")
    writer.write("T*deltaStot: " + str(round(deltaStot * 0.001 * temperature, 4)) + " KCal/Mol" + "\n")
    writer.write("The result of deltaStrans: " + str(round(deltaStrans, 4)) + " KCal/Mol" + "\n")
    writer.write("The result of deltaSrot: " + str(round(deltaSrot, 4)) + " KCal/Mol" + "\n")
    writer.write("The result of deltaSvib: " + str(round(deltaSvib, 4)) + " KCal/Mol" + "\n")

    writer.write("The absolute value of total entropy change: " + str(round(TotalSAbsoluteValue, 4)) + "\n")
    writer.write("The deltaStrans%: " + str(round(deltaStransPercent, 1)) + "%" + "\n")
    writer.write("The deltaSrot%: " + str(round(deltaSrotPercent, 1)) + "%" + "\n")
    writer.write("The deltaSvib%: " + str(round(deltaSvibPercent, 1)) + "%" + "\n")

writer.close()
#
# mylabels = paths
# y = np.array(y)
# plt.pie(y, labels=mylabels)
# plt.title('Pie Chart for Energy Contributions')
# plt.savefig(current_dir + "\\" + "diagram.png")
# plt.show()

# git test 2
# test
# test2