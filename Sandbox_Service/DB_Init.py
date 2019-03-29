#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sqlite3

def main():

    conn=sqlite3.connect('webshell.db')
    c=conn.cursor()

    c.execute('''CREATE TABLE webshells (
            ID          INTEGER PRIMARY KEY, 
            hash        TEXT NOT NULL, 
            status      INTERGER NOT NULL, 
            uploadDate  TEXT, 
            processDate TEXT, 
            finishDate  TEXT, 
            message     TEXT, 
            stdout      TEXT)''')
    
    conn.commit()
    conn.close()


if __name__=='__main__':
    main()


