from haversine import haversine
from datetime import date

RESCENT = 1
NOTRESC = 2


def distance_calculator(myloc, patientloc):
    dist = haversine(myloc, patientloc, unit='km')
    return round(dist, 3)


def str_to_date(str):
    return date.fromisoformat(str)


def date_to_str(day):
    return day.isoformat()


def term_calculator(quarantine):
    today = date.today()
    quarantine = str_to_date(quarantine)
    term = today - quarantine

    if term.days <= 7:
        return 1

    elif term.days <= 14:
        return 2


def adjacent_list(userLoc, placeList):
    resAdjList = list()
    notAdjList = list()

    for i in placeList:
        placeLoc = (float(i[3]), float(i[4]))
        distance = distance_calculator(userLoc, placeLoc)

        if distance < 0.5 and term_calculator(i[6]) == 1:
            resAdjList.append(i)

        elif distance < 0.5 and term_calculator(i[6]) == 2:
            notAdjList.append(i)

    if not resAdjList:
        print("yellow")
        print(notAdjList)
        notAdjList.insert(0, NOTRESC)
        return notAdjList

    else:
        print("red")
        print(resAdjList)
        resAdjList.insert(0, RESCENT)
        return resAdjList


if __name__ == '__main__':
    loc1 = (35.88867, 128.61211)
    loc2 = (35.88823, 128.61135)
    #distance_calculator(loc1, loc2)
    term_calculator('2020-11-29')