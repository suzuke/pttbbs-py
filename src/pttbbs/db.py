# -*- encoding: UTF-8 -*-

import os
import sqlite3

DB_PATH = 'users.db'

class DB:
    "Interface for database access"

    def __init__(self):
        self.exist = os.path.exists(DB_PATH)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def create(self):
        "Initialize database"

        users =      """CREATE TABLE Users
                        (
                            UId TEXT UNIQUE NOT NULL,
                            PW TEXT,
                            ACL INTEGER NOT NULL,
                            Avatar TEXT,
                            Motto TEXT,
                            Signature TEXT,
                            Mood TEXT,
                            Sex TEXT,
                            Birthday TEXT,
                            LastName TEXT,
                            FirstName TEXT,
                            HomePhone TEXT,
                            WorkPhone TEXT,
                            EMail TEXT UNIQUE,
                            Address TEXT,
                            City TEXT,
                            Country TEXT
                        )"""

        # essentially assignment means directories
        supers =     """CREATE TABLE SuperUsers
                        (
                            UId TEXT NOT NULL,
                            Assignment TEXT NOT NULL,
                            AssignerId TEXT
                        )"""

        sessions =   """CREATE TABLE Sessions
                        (
                            UId TEXT NOT NULL,
                            IP TEXT NOT NULL,
                            Port TEXT NOT NULL,
                            LoginTime DATE NOT NULL,
                            LogoffTime DATE NOT NULL,
                            Location TEXT
                        )"""

        relations =  """CREATE TABLE Relations
                        (
                            UId TEXT NOT NULL,
                            FId TEXT NOT NULL,
                            Status TEXT NOT NULL
                        )"""

        # e.g. Board Announcement on path /boards/Title/
        boards =     """CREATE TABLE Boards
                        (
                            Path TEXT NOT NULL,
                            Title NOT NULL,
                            CreatorId TEXT,
                            CreationDate DATE
                        )"""

        # Threads will always be under a path like /boards/Announcement/Title/
        threads =    """CREATE TABLE Threads
                        (
                            Path TEXT UNIQUE NOT NULL,
                            Title TEXT NOT NULL,
                            AuthorId TEXT,
                            Content TEXT,
                            Moderated TEXT,
                            CreationDate DATE,
                            LastModifiedDate DATE
                        )"""

        # Push path is the thread (or push) it resides in e.g. /path/to/thread/
        replies =    """CREATE TABLE Replies
                        (
                            PathToThread TEXT UNIQUE NOT NULL,
                            AuthorId TEXT,
                            Content TEXT,
                            Moderated TEXT,
                            CreationDate DATE,
                            LastModifiedDate DATE
                        )"""

        guest =      """INSERT INTO Users
                        (
                            UId,
                            ACL
                        )
                        VALUES
                        (
                            'guest',
                            0
                        )"""

        admin =      """INSERT INTO Users
                        (
                            UId,
                            PW,
                            ACL
                        )
                        VALUES
                        (
                            'admin',
                            'password',
                            100
                        );

                        INSERT INTO SuperUsers
                        (
                            UId,
                            Assignment
                        )
                        VALUES
                        (
                            'admin',
                            '/'
                        );"""

        self.cursor.execute(users)
        self.cursor.execute(supers)
        self.cursor.execute(sessions)
        self.cursor.execute(relations)
        self.cursor.execute(boards)
        self.cursor.execute(threads)
        self.cursor.execute(replies)
        self.cursor.execute(guest)
        self.cursor.executescript(admin)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()

instance = DB()
