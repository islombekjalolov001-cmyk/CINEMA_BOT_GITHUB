"""Async SQLite database layer built on aiosqlite.

All database access in the project goes through the `Database` class below.
Every method is a coroutine so the bot never blocks the event loop on I/O.
"""
from __future__ import annotations

import time
from typing import Any, Optional

import aiosqlite


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    language TEXT DEFAULT 'uz',
    is_blocked INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS movies (
    code INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genre TEXT NOT NULL,
    country TEXT NOT NULL,
    year INTEGER,
    rating REAL,
    description TEXT,
    file_id TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS genres (
    key TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS countries (
    key TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS likes (
    user_id INTEGER NOT NULL,
    movie_code INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (user_id, movie_code)
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_name TEXT NOT NULL,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL UNIQUE,
    title TEXT,
    is_mandatory INTEGER DEFAULT 1,
    created_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS admins (
    user_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
);
"""


class Database:
    """Thin async wrapper around an SQLite database file."""

    def __init__(self, path: str) -> None:
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None

    async def connect(self) -> None:
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute("PRAGMA foreign_keys = ON")
        await self._conn.executescript(SCHEMA)
        await self._conn.commit()

    async def close(self) -> None:
        if self._conn is not None:
            await self._conn.close()

    @property
    def conn(self) -> aiosqlite.Connection:
        if self._conn is None:
            raise RuntimeError("Database ulanmagan. connect() chaqirilmagan.")
        return self._conn

    # ------------------------------------------------------------------ #
    # USERS
    # ------------------------------------------------------------------ #
    async def add_user(self, user_id: int, username: str | None, full_name: str) -> bool:
        """Insert user if not exists. Returns True if a new row was created."""
        cur = await self.conn.execute(
            "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
        )
        row = await cur.fetchone()
        if row:
            await self.conn.execute(
                "UPDATE users SET username = ?, full_name = ? WHERE user_id = ?",
                (username, full_name, user_id),
            )
            await self.conn.commit()
            return False

        await self.conn.execute(
            "INSERT INTO users (user_id, username, full_name, created_at) VALUES (?, ?, ?, ?)",
            (user_id, username, full_name, int(time.time())),
        )
        await self.conn.commit()
        return True

    async def get_user(self, user_id: int) -> aiosqlite.Row | None:
        cur = await self.conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return await cur.fetchone()

    async def find_user_by_identifier(self, identifier: str) -> aiosqlite.Row | None:
        normalized = identifier.strip().lstrip("@")
        if not normalized:
            return None
        if normalized.isdigit():
            return await self.get_user(int(normalized))

        cur = await self.conn.execute(
            "SELECT * FROM users WHERE LOWER(username) = ? LIMIT 1",
            (normalized.lower(),),
        )
        return await cur.fetchone()

    async def get_users_by_status(self, blocked: bool) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            "SELECT * FROM users WHERE is_blocked = ? ORDER BY created_at DESC",
            (int(blocked),),
        )
        return await cur.fetchall()

    async def set_language(self, user_id: int, language: str) -> None:
        await self.conn.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (language, user_id)
        )
        await self.conn.commit()

    async def get_language(self, user_id: int) -> str:
        row = await self.get_user(user_id)
        return row["language"] if row else "uz"

    async def all_user_ids(self) -> list[int]:
        cur = await self.conn.execute("SELECT user_id FROM users WHERE is_blocked = 0")
        rows = await cur.fetchall()
        return [r["user_id"] for r in rows]

    async def set_blocked(self, user_id: int, blocked: bool) -> None:
        await self.conn.execute(
            "UPDATE users SET is_blocked = ? WHERE user_id = ?", (int(blocked), user_id)
        )
        await self.conn.commit()

    async def users_dataframe_rows(self) -> list[aiosqlite.Row]:
        cur = await self.conn.execute("SELECT * FROM users ORDER BY created_at DESC")
        return await cur.fetchall()

    async def count_users_total(self) -> int:
        cur = await self.conn.execute("SELECT COUNT(*) AS c FROM users")
        return (await cur.fetchone())["c"]

    async def count_users_since(self, ts_from: int) -> int:
        cur = await self.conn.execute(
            "SELECT COUNT(*) AS c FROM users WHERE created_at >= ?", (ts_from,)
        )
        return (await cur.fetchone())["c"]

    # ------------------------------------------------------------------ #
    # MOVIES
    # ------------------------------------------------------------------ #
    async def add_movie(
        self,
        code: int,
        title: str,
        genre: str,
        country: str,
        year: int,
        rating: float,
        description: str,
        file_id: str,
    ) -> None:
        await self.conn.execute(
            """INSERT INTO movies (code, title, genre, country, year, rating, description, file_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (code, title, genre, country, year, rating, description, file_id, int(time.time())),
        )
        await self.conn.commit()

    async def get_movie(self, code: int) -> aiosqlite.Row | None:
        cur = await self.conn.execute("SELECT * FROM movies WHERE code = ?", (code,))
        return await cur.fetchone()

    async def movie_exists(self, code: int) -> bool:
        return await self.get_movie(code) is not None

    async def update_movie_field(self, code: int, field: str, value: Any) -> None:
        allowed = {"title", "genre", "country", "year", "rating", "description", "file_id"}
        if field not in allowed:
            raise ValueError(f"Ruxsat etilmagan maydon: {field}")
        await self.conn.execute(f"UPDATE movies SET {field} = ? WHERE code = ?", (value, code))
        await self.conn.commit()

    async def delete_movie(self, code: int) -> None:
        await self.conn.execute("DELETE FROM movies WHERE code = ?", (code,))
        await self.conn.execute("DELETE FROM likes WHERE movie_code = ?", (code,))
        await self.conn.commit()

    async def search_movies_by_name(self, query: str, limit: int = 20) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            "SELECT * FROM movies WHERE title LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit),
        )
        return await cur.fetchall()

    async def movies_by_genre(self, genre: str, offset: int, limit: int) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            "SELECT * FROM movies WHERE genre = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (genre, limit, offset),
        )
        return await cur.fetchall()

    async def count_movies_by_genre(self, genre: str) -> int:
        cur = await self.conn.execute("SELECT COUNT(*) AS c FROM movies WHERE genre = ?", (genre,))
        return (await cur.fetchone())["c"]

    async def movies_by_country(self, country: str, offset: int, limit: int) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            "SELECT * FROM movies WHERE country = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (country, limit, offset),
        )
        return await cur.fetchall()

    async def count_movies_by_country(self, country: str) -> int:
        cur = await self.conn.execute("SELECT COUNT(*) AS c FROM movies WHERE country = ?", (country,))
        return (await cur.fetchone())["c"]

    async def all_movies_paginated(self, offset: int, limit: int) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            "SELECT code, title FROM movies ORDER BY code ASC LIMIT ? OFFSET ?", (limit, offset)
        )
        return await cur.fetchall()

    async def count_movies_total(self) -> int:
        cur = await self.conn.execute("SELECT COUNT(*) AS c FROM movies")
        return (await cur.fetchone())["c"]

    # ------------------------------------------------------------------ #
    # LIKES
    # ------------------------------------------------------------------ #
    async def has_liked(self, user_id: int, movie_code: int) -> bool:
        cur = await self.conn.execute(
            "SELECT 1 FROM likes WHERE user_id = ? AND movie_code = ?", (user_id, movie_code)
        )
        return await cur.fetchone() is not None

    async def add_like(self, user_id: int, movie_code: int) -> bool:
        if await self.has_liked(user_id, movie_code):
            return False
        await self.conn.execute(
            "INSERT INTO likes (user_id, movie_code, created_at) VALUES (?, ?, ?)",
            (user_id, movie_code, int(time.time())),
        )
        await self.conn.commit()
        return True

    async def remove_like(self, user_id: int, movie_code: int) -> None:
        await self.conn.execute(
            "DELETE FROM likes WHERE user_id = ? AND movie_code = ?", (user_id, movie_code)
        )
        await self.conn.commit()

    async def count_likes(self, movie_code: int) -> int:
        cur = await self.conn.execute(
            "SELECT COUNT(*) AS c FROM likes WHERE movie_code = ?", (movie_code,)
        )
        return (await cur.fetchone())["c"]

    async def user_favorites(self, user_id: int, offset: int, limit: int) -> list[aiosqlite.Row]:
        cur = await self.conn.execute(
            """SELECT m.* FROM movies m
               JOIN likes l ON l.movie_code = m.code
               WHERE l.user_id = ?
               ORDER BY l.created_at DESC LIMIT ? OFFSET ?""",
            (user_id, limit, offset),
        )
        return await cur.fetchall()

    async def count_user_favorites(self, user_id: int) -> int:
        cur = await self.conn.execute(
            "SELECT COUNT(*) AS c FROM likes WHERE user_id = ?", (user_id,)
        )
        return (await cur.fetchone())["c"]

    # ------------------------------------------------------------------ #
    # REQUESTS
    # ------------------------------------------------------------------ #
    async def add_request(self, user_id: int, movie_name: str) -> None:
        await self.conn.execute(
            "INSERT INTO requests (user_id, movie_name, created_at) VALUES (?, ?, ?)",
            (user_id, movie_name, int(time.time())),
        )
        await self.conn.commit()

    # ------------------------------------------------------------------ #
    # CHANNELS
    # ------------------------------------------------------------------ #
    async def add_channel(self, chat_id: str, title: str, mandatory: bool) -> None:
        await self.conn.execute(
            """INSERT INTO channels (chat_id, title, is_mandatory, created_at)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(chat_id) DO UPDATE SET title = excluded.title,
                    is_mandatory = excluded.is_mandatory""",
            (chat_id, title, int(mandatory), int(time.time())),
        )
        await self.conn.commit()

    async def remove_channel(self, chat_id: str) -> None:
        await self.conn.execute("DELETE FROM channels WHERE chat_id = ?", (chat_id,))
        await self.conn.commit()

    async def mandatory_channels(self) -> list[aiosqlite.Row]:
        cur = await self.conn.execute("SELECT * FROM channels WHERE is_mandatory = 1")
        return await cur.fetchall()

    async def optional_channels(self) -> list[aiosqlite.Row]:
        cur = await self.conn.execute("SELECT * FROM channels WHERE is_mandatory = 0")
        return await cur.fetchall()

    async def all_channels(self) -> list[aiosqlite.Row]:
        cur = await self.conn.execute("SELECT * FROM channels")
        return await cur.fetchall()

    # ------------------------------------------------------------------ #
    # ADMINS
    # ------------------------------------------------------------------ #
    async def is_admin(self, user_id: int, static_admin_ids: list[int]) -> bool:
        if user_id in static_admin_ids:
            return True
        cur = await self.conn.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
        return await cur.fetchone() is not None


db: Database | None = None


def get_db() -> Database:
    """Return the global Database singleton (set up in loader.py)."""
    if db is None:
        raise RuntimeError("Database hali ishga tushirilmagan.")
    return db


def set_db(instance: Database) -> None:
    global db
    db = instance
