from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAllAlbums():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select a.*, sum(t.Milliseconds)/1000/60 as dTot
from album a, track t
where a.AlbumId = t.AlbumId
group by a.AlbumId
    """
        cursor.execute(query)

        for row in cursor:
            result.append(Album(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di nazioni

    @staticmethod
    def getNodes(dMin):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            select a.*, sum(t.Milliseconds)/1000/60 as dTot
from album a, track t
where a.AlbumId = t.AlbumId
group by a.AlbumId
having dTot > %s
    """
        cursor.execute(query,(dMin,))

        for row in cursor:
            result.append(Album(**row))
            # equivalente a fare (ArtObject(object_id= row["object_id"])
        cursor.close()
        conn.close()
        return result  # lista di nazioni

    @staticmethod
    def getAllEdges(nodi):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select DISTINCTROW t1.AlbumId as a1,t2.AlbumId as a2
from track t1, track t2, playlisttrack p1,playlisttrack p2
where t2.TrackId =p2.TrackId
and t1.TrackId =p1.TrackId
and p2.PlaylistId =p1.PlaylistId
and t1.AlbumId <t2.AlbumId

        """
        cursor.execute(query)

        for row in cursor:
            if row["a1"] in nodi and row["a2"] in nodi:
                result.append((nodi[row["a1"]], nodi[row["a2"]]))

        cursor.close()
        conn.close()
        return result  # lista di nazioni
