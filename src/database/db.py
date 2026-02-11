import aiosqlite
from src.core.config import settings

async def init_db():
    async with aiosqlite.connect(settings.DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_message(user_id: int, role: str, content: str):
    async with aiosqlite.connect(settings.DB_NAME) as db:
        await db.execute(
            "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        await db.commit()

async def get_last_messages(user_id: int, limit: int = 10):
    async with aiosqlite.connect(settings.DB_NAME) as db:
        async with db.execute(
            """SELECT role, content FROM messages 
               WHERE user_id = ? 
               ORDER BY id DESC LIMIT ?""", 
            (user_id, limit)
        ) as cursor:
            rows = await cursor.fetchall()
            return [{"role": row[0], "content": row[1]} for row in rows][::-1]

async def clear_history(user_id: int):
    async with aiosqlite.connect(settings.DB_NAME) as db:
        await db.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        await db.commit()