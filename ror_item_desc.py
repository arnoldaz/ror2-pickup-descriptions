import argparse
import fileinput
import re
from pathlib import Path

PICKUP_REGEX = r"\"(.*)_PICKUP\"\s*:\s*\"(.*)\""
DESCRIPTION_REGEX = r"\"(.*)_DESC\"\s*:\s*\"(.*)\""

DEFAULT_INSTALL_DIR = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Risk of Rain 2\\"
LANGUAGE_FOLDER = "Risk of Rain 2_Data\\StreamingAssets\\Language\\en\\"
ITEMS_FILE = "Items.json"
EQUIPMENT_FILE = "Equipment.json"

parser = argparse.ArgumentParser()
parser.add_argument("--installDir", type=Path, help="RoR2 install directory")

def isCorrectInstallDir(installDir: Path) -> bool:
    return installDir.is_dir() and (installDir / "Risk of Rain 2.exe").exists()

def modifyFilePickupText(filePath: Path) -> None:
    descriptionDictionary = {}

    with open(filePath, "r") as file:
        while line := file.readline():
            match = re.search(DESCRIPTION_REGEX, line)
            if match:
                descriptionDictionary[match.group(1)] = match.group(2)

    with fileinput.input(filePath, inplace=True) as file:
        while line := file.readline():
            match: re.Match = re.search(PICKUP_REGEX, line)
            if match and (key := match.group(1)) in descriptionDictionary:
                oldPickupText = match.group(2)
                newPickupText = descriptionDictionary[key]
                print(line.replace(oldPickupText, newPickupText), end="")
            else:
                print(line, end="")

def main(args: argparse.Namespace) -> None:
    installDir = Path(DEFAULT_INSTALL_DIR)
    if args.installDir is not None:
        installDir = Path(args.installDir)

    if not isCorrectInstallDir(installDir):
        print("RoR2 install directory is not found.")
        return

    itemsFilePath = installDir / LANGUAGE_FOLDER / ITEMS_FILE
    equipmentFilePath = installDir / LANGUAGE_FOLDER / EQUIPMENT_FILE

    modifyFilePickupText(itemsFilePath)
    modifyFilePickupText(equipmentFilePath)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
