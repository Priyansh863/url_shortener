import hashlib
from datetime import datetime, timedelta
from app.database import get_db
from typing import Optional


class UrlShortenerRepository:

    def __init__(self):

        self.db = get_db().cursor()

    async def generate_short_url(self, original_url: str) -> str:
        hash_object = hashlib.sha256(original_url.encode())
        return hash_object.hexdigest()

    async def create_shortened_url(self, original_url: str, password: str, expiry_hours: int) -> str:
        try:
            short_url = await self.generate_short_url(str(original_url))
            creation_time = datetime.utcnow()
            expiration_time = creation_time + timedelta(hours=expiry_hours)

            result = self.db.execute(
                """
                SELECT short_url, original_url, creation_time, expiration_time FROM urls
                WHERE original_url = ?
            """,
                (str(original_url),),
            )
            existing_url = result.fetchone()
            if existing_url:
                return {
                    "message": "Updated Successfully",
                    "success": True,
                    "data": existing_url[0],
                }
            else:
                short_url = "https://short.ly/"+short_url
                result = self.db.execute(
                    """
                    INSERT INTO urls (short_url, original_url, password,creation_time, expiration_time)
                    VALUES (?, ?, ?, ?,?)
                """,
                    (
                        str(short_url),
                        str(original_url),
                        password,creation_time,
                        expiration_time,
                    ),
                )
                result.connection.commit()
                return {"message": "Updated Successfully", "success": True, "data": short_url}
        except Exception as e:
            return {"message": str(e), "success": False, "data": None}

    async def get_original_url(self, short_url: str, ip_address: str, password: str):
        try:
            self.db.execute(
                """
                SELECT short_url,original_url, creation_time, expiration_time,password FROM urls
                WHERE short_url = ?
            """,
                (short_url,),
            )

            existing_url = self.db.fetchone()

            print(existing_url, "existing_urlexisting_url")

            if existing_url and existing_url[4]:
                if(existing_url[4] != password):
                    return {
                        "message": "Invalid password",
                        "success": False,
                    }

            if existing_url:
                if datetime.utcnow() > datetime.fromisoformat(existing_url[3]):
                    return {
                        "message": "URL expired",
                        "success": True,
                        "data": existing_url,
                    }
                else:
                    await self.log_access(short_url, datetime.utcnow().isoformat(), ip_address)
                    return {
                        "message": "URL found",
                        "success": True,
                        "data": existing_url[1],
                    }
            else:
                return {
                    "message": "Short URL not found",
                    "success": False,
                }
        except Exception as e:
            return {"message": str(e), "success": False, "data": None}

    async def log_access(self, short_url: str, timestamp: str, ip_address: str):
        try:
            result=self.db.execute(
                """
            INSERT INTO access_logs (short_url, timestamp, ip_address)
            VALUES (?, ?, ?)
        """,
                (str(short_url), timestamp, ip_address),
            )
            result.connection.commit()
            return {"message": "Logged Successfully", "success": True}
        except Exception as e:
            return {"message": str(e), "success": False, "data": None}

    async def get_access_logs(self, short_url: str) -> Optional[list]:
        try:
            self.db.execute(
                """
            SELECT * FROM access_logs
            WHERE short_url = ?
        """,
                (short_url,),
            )
            data = self.db.fetchall()
            if(data):
                return {
                    "message": "Data found",
                    "success": True,
                    "data": {"log_count": len(data),"logs": data},
                }
            else:
                return {
                    "message": "Data not found",
                    "success": False,
                    "data": None
                }
        except Exception as e:
            return {"message": str(e), "success": False, "data": None}
