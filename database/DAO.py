from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConstructors(minY, maxY):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT c.constructorId, c.constructorRef, c.name, c.nationality
                FROM races r
                JOIN results res ON r.raceId=res.raceId
                JOIN constructors c ON res.constructorId=c.constructorId
                WHERE r.year>=%s AND r.year<=%s AND res.`position` IS NOT NULL"""

        cursor.execute(query, (minY, maxY))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(minY, maxY, idMapConstructors):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT cd1.constructorId c1, cd2.constructorId c2, COUNT(DISTINCT cd1.driverId) as weight
                FROM (SELECT res.constructorId, res.driverId FROM races r JOIN results res ON r.raceId=res.raceId
                    WHERE r.year>=%s AND r.year<=%s AND res.`position` IS NOT NULL) cd1,
                    (SELECT res.constructorId, res.driverId FROM races r JOIN results res ON r.raceId=res.raceId
                    WHERE r.year>=%s AND r.year<=%s AND res.`position` IS NOT NULL) cd2 
                WHERE cd1.driverId = cd2.driverId AND cd1.constructorId < cd2.constructorId
                GROUP BY cd1.constructorId, cd2.constructorId"""

        cursor.execute(query, (minY, maxY, minY, maxY))

        for row in cursor:
            results.append((idMapConstructors[row["c1"]], idMapConstructors[row["c2"]], row["weight"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def setOldestDOB(minY, maxY, idMapConstructors):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """SELECT res.constructorId as cId, MIN(d.dob) as oldest_driver_dob
                FROM results res
                    JOIN drivers d ON res.driverId = d.driverId 
                    JOIN races r ON res.raceId = r.raceId 
                WHERE r.year>=%s AND r.year<=%s AND res.`position` IS NOT NULL 
                GROUP BY res.constructorId"""

        cursor.execute(query, (minY, maxY))

        for row in cursor:
            idMapConstructors[row["cId"]].oldest_driver_dob = row["oldest_driver_dob"]

        cursor.close()
        conn.close()
        return
