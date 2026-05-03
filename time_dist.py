import pandas as pd
from datetime import datetime, date
import math
import freqency_grid as fg

BLACKDATA2012: pd.DataFrame = (pd.read_csv("BlackBear2012_data.csv")
                                   .drop("OBJECTID", axis="columns"))
BLACKDATA2013: pd.DataFrame = (pd.read_csv("BlackBear2013_data.csv")
                                   .drop("OBJECTID", axis="columns"))

BLACKBEARDATA: pd.DataFrame = pd.concat([BLACKDATA2012, BLACKDATA2013], ignore_index=True)
BROWNBEARDATA: pd.DataFrame = pd.read_csv("BrownBear_data.csv").drop("OBJECTID", axis="columns")

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
        return 0
    elif 600 <= militaryTime < 1200:
        return 1
    elif 1200 <= militaryTime < 1800:
        return 2
    elif militaryTime >= 1800 or militaryTime == 0:
        return 3
    else:
        raise ValueError(f"Invalid time on \"line no\": {row["Line_No"]}. "
                         f"detected time as {militaryTime}")

# returns time difference in minutes
def timeDifference(row1, row2) -> float:
    time1 = pd.to_datetime(row1["Time"]).time()
    time2 = pd.to_datetime(row2["Time"]).time()

    timeDiff = datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)
    return timeDiff.seconds / 60

# returns a tuple containing [time period int (see timePeriod returns), speed in meters/min]
def calculateSpeed(row: pd.Series) -> tuple[int, float]:
    speedData: tuple[int, float] = -1, -1.0

    idx = BLACKBEARDATA.index.get_loc(row.name)
    prevRow = BLACKBEARDATA.iloc[idx - 1]

    currentCoords: tuple[float, float] = (row["Latitude"], row["Longitude"])
    previousCoords: tuple[float, float] = (prevRow["Latitude"], prevRow["Longitude"])

    currentTime = (datetime.strptime(row["Time"], "%I:%M %p")
                   .strftime("%H:%M".replace(":", "")))
    previousTime = (datetime.strptime(prevRow["Time"], "%I:%M %p")
                    .strftime("%H:%M".replace(":", "")))

    if timePeriod(row) == timePeriod(prevRow):
        differencePoint: tuple[float, float] = (
            fg.lat_lon_to_meters(currentCoords[0], currentCoords[1],
                                 previousCoords[0], previousCoords[1])
        )

        distance: float = math.sqrt(abs((differencePoint[0] ** 2) + (differencePoint[1] ** 2)))
        minutes: float = abs(timeDifference(prevRow, row))

        if minutes > 0:
            speed: float = distance / minutes
        else:
            speed: float = -1

        speedData = timePeriod(row), speed

    return speedData

def cleanDistData(df: pd.DataFrame) -> pd.DataFrame:
    for x in df.index:
        if df[x][0] == -1 or df[x][1] == -1.0:
            df.drop(x, inplace=True)

    return df

def main() -> None:
    blackDistDataframe = BLACKBEARDATA.apply(calculateSpeed, axis=1)

    """
    if we can rewrite time-handling parts of calculateSpeed() and 
    timeDifference() to account for the different time format in the 
    brown bear data, brown bear data could theoretically be processed
    as below
    """
    # brownDistDataframe = BROWNBEARDATA.apply(calculateSpeed, axis=1)

    # AWESOME!!!!!
    print(cleanDistData(blackDistDataframe))

if __name__ == "__main__":
    main()