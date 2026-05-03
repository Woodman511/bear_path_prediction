import pandas as pd
from datetime import datetime

from pandas.core.interchange import dataframe

"""
timePeriod returns:
[12:01 AM - 6:00 AM] -> 0
[6:01 AM - 12:00 PM] -> 1
[12:01 PM - 6:00 PM] -> 2
[6:01 PM - 12:00 AM] -> 3
"""
def timePeriod(row: pd.Series) -> int:
    rawTime = datetime.strptime(row["Time"], "%I:%M %p")

    militaryTime = int(rawTime.strftime("%H:%M".replace(":", "")))

    if 0 < militaryTime < 600:
        print(0)
        return 0
    elif 600 <= militaryTime < 1200:
        print(1)
        return 1
    elif 1200 <= militaryTime < 1800:
        print(2)
        return 2
    elif militaryTime >= 1800 or militaryTime == 0:
        print(3)
        return 3
    else:
        raise ValueError(f"Invalid time on \"line no\": {row["Line_No"]}. "
                         f"detected time as {militaryTime}")

# remember first tuple output will always be (None, None) ??
def calculateSpeed(row: pd.Series) -> tuple[int, float]:
    speedData: tuple[int, float] = -1, -1.0

    try:
        prevRow = row.shift(1)

        currentCoords: tuple[float, float] = (row["Latitude"], row["Longitude"])
        previousCoords: tuple[float, float] = (prevRow["Latitude"], prevRow["Longitude"])

        currentTime = datetime.strptime(row["Time"], "%I:%M %p").strftime("%H:%M".replace(":", ""))
        previousTime = datetime.strptime(prevRow["Time"], "%I:%M %p").strftime("%H:%M".replace(":", ""))

        if timePeriod(row) == timePeriod(prevRow):
            distance: float = 0
    except:
        return speedData



def main() -> None:
    blackData2012: pd.DataFrame = pd.read_csv("BlackBear2012_data.csv").drop("OBJECTID", axis="columns")
    blackData2013: pd.DataFrame = pd.read_csv("BlackBear2013_data.csv").drop("OBJECTID", axis="columns")

    blackBearData: pd.DataFrame = pd.concat([blackData2012, blackData2013], ignore_index=True)
    brownBearData: pd.DataFrame = pd.read_csv("BrownBear_data.csv").drop("OBJECTID", axis="columns")

    # successfully shifts series down by 1!
    # dataTest: pd.Series = blackBearData.loc[1]
    # print(dataTest.shift(1)["Line_No"])

    # blackBearData.apply(timePeriod, axis=1)
    # blackBearData.apply(calculateSpeed, axis=1)

if __name__ == "__main__":
    main()