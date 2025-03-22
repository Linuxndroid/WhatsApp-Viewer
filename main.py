import configparser
import sqlite3
from sqlite3 import Connection
from typing import List, Optional, Dict
from pathlib import Path

import exporter
from models import Message, Chat

import os


def query_messages_from_table_messages(con: Connection, key_remote_jid: str, contacts: Dict[str, Optional[str]]) -> List[Message]:
    cur = con.cursor()
    query = """
            SELECT received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type 
            FROM messages 
            WHERE key_remote_jid =:key_remote_jid
            ORDER BY max(receipt_server_timestamp, received_timestamp)"""
    query = """
            SELECT * FROM (
                SELECT received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type 
                FROM messages 
                WHERE key_remote_jid =:key_remote_jid
                ORDER BY max(receipt_server_timestamp, received_timestamp)
            )
        UNION
            SELECT call_log.timestamp received_timestamp, jid.raw_string remote_resource, from_me key_from_me, NULL data, '' media_caption,
                CASE video_call
                    WHEN 0 THEN 255
                    WHEN 1 THEN 256
                END
                AS media_wa_type
            FROM call_log 
            INNER JOIN jid
                ON call_log.jid_row_id = jid._id
            WHERE raw_string =:key_remote_jid
        ORDER BY received_timestamp
    """
    messages = []
    for received_timestamp, remote_resource, key_from_me, data, media_caption, media_wa_type in cur.execute(query, {"key_remote_jid": key_remote_jid}):
        messages.append(
            Message(received_timestamp, remote_resource, key_from_me, data, media_caption, int(media_wa_type), contacts.get(remote_resource, None))
        )
    return messages


def query_messages_from_table_message(con: Connection, key_remote_jid: str, contacts: Dict[str, Optional[str]]) -> List[Message]:
    cur = con.cursor()
    query = """  
            SELECT
                m.timestamp,
                jid.raw_string,
                m.from_me,
                CASE
                    WHEN mr.revoked_key_id > 1 THEN '[Deleted]'
                    ELSE m.text_data
                END AS text,
                m.message_type
            FROM message AS m
            LEFT JOIN chat_view AS cv ON m.chat_row_id = cv._id
            LEFT JOIN jid ON m.sender_jid_row_id = jid._id
            LEFT JOIN message_revoked AS mr ON m._id = mr.message_row_id
            WHERE cv.raw_string_jid =:key_remote_jid
            ORDER BY max(receipt_server_timestamp, received_timestamp)
            """
    messages = []
    for timestamp, remote_jid, from_me, data, message_type in cur.execute(query, {"key_remote_jid": key_remote_jid}):
        messages.append(
            Message(timestamp, remote_jid, from_me, data, data, message_type, contacts.get(remote_jid, None))
        )
    return messages


def query_all_chats(db_path: str, contacts: Dict[str, Optional[str]]) -> List[Chat]:
    chats = []
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Check which table to use: Older databases use the table "messages", newer ones the table "message"
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    table_messages_exists = cur.fetchone() is not None
    print("[+] Using table 'messages'") if table_messages_exists else print("[+] Using table 'message'")

    query = "SELECT raw_string_jid as key_remote_jid, subject, sort_timestamp FROM chat_view WHERE sort_timestamp IS NOT NULL ORDER BY sort_timestamp DESC"
    for key_remote_jid, subject, sort_timestamp in cur.execute(query):
        if table_messages_exists:
            messages = query_messages_from_table_messages(con, key_remote_jid, contacts)
        else:
            messages = query_messages_from_table_message(con, key_remote_jid, contacts)

        chats.append(
            Chat(key_remote_jid, subject, sort_timestamp, contacts.get(key_remote_jid, None), messages)
        )
    con.close()
    return chats


def query_contacts(db_path: str) -> Dict[str, Optional[str]]:
    contacts = {}
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    for jid, wa_name, display_name in cur.execute("SELECT jid, wa_name, display_name from wa_contacts"):
        if display_name:
            contacts[jid] = display_name
        elif wa_name:
            contacts[jid] = wa_name
    con.close()
    return contacts

def check_paths(config: configparser.ConfigParser):
    if config["input"].getboolean("use_wa_db"):
        wa_path = Path(config["input"]['wa_path'].strip('"'))
        config["input"]['wa_path'] = str(wa_path)
        if not wa_path.exists():
            raise Exception(f'Config wa_path does not exist: {wa_path}')

    msgstore_path = Path(config["input"].get("msgstore_path").strip('"'))
    config["input"]['msgstore_path'] = str(msgstore_path)
    if not msgstore_path.exists():
        raise Exception(f'Config msgstore_path does not exist: {msgstore_path}')
    
    if config["output"].getboolean("export_html"):
        html_output_path = Path(config["output"].get("html_output_path").strip('"'))
        config["output"]['html_output_path'] = str(html_output_path)
        html_output_dir = Path(os.path.dirname(html_output_path))
        if not html_output_dir.exists():
            html_output_dir.mkdir()

    if config["output"].getboolean("export_txt"):
        txt_output_directory_path = Path(config["output"].get("txt_output_directory_path").strip('"'))
        config["output"]['txt_output_directory_path'] = str(txt_output_directory_path)
        if not txt_output_directory_path.exists():
            txt_output_directory_path.mkdir()

def main():
    print("### WhatsApp Database Exporter ###")

    config = configparser.ConfigParser()
    config.read("config.cfg")

    print("[+] Reading Config")
    check_paths(config)

    print("[+] Reading Database")
    if config["input"].getboolean("use_wa_db"):
        contacts = query_contacts(config["input"].get("wa_path"))
    else:
        contacts = {}
    chats = query_all_chats(config["input"].get("msgstore_path"), contacts)

    if config["output"].getboolean("export_html"):
        print("[+] Exporting to HTML")
        exporter.chats_to_html(chats, config["output"].get("html_output_path"))
    if config["output"].getboolean("export_txt"):
        print("[+] Exporting to txt files")
        exporter.chats_to_txt(chats, config["output"].get("txt_output_directory_path"))
    print("[+] Finished")


if __name__ == "__main__":
    main()
