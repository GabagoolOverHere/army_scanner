import mysql.connector
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database'),
    port=os.getenv('port')
)


class DB:

    def prepare_datas_for_database(self, message_author: str, commander_name: str, message_content: int):
        if self.find_player_by_name(message_author) is None:
            self.create_player(message_author, commander_name, message_content)
        else:
            player_id = self.find_player_by_name(message_author)
            self.update_player(commander_name, message_content,
                               player_id[0])
            self.delete_troops(player_id[0])

    def create_player(self, discord_name: str, commander_name: str, max_troop_size: int,
                      now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        conn.reconnect()
        c = conn.cursor()
        d = (discord_name, commander_name, max_troop_size, now)
        c.execute(
            """INSERT INTO players(discord_name, commander_name, max_troop_size, submission_date)
            VALUES (%s, %s, %s, %s)""", d)
        conn.commit()
        conn.close()

    def find_player_by_name(self, discord_name: str):
        conn.reconnect()
        c = conn.cursor()
        d = (discord_name,)
        c.execute(
            """SELECT id FROM players WHERE discord_name=%s""", d)
        datas = c.fetchone()
        conn.close()

        return datas

    def find_troop_by_name(self, troop_name: str):
        conn.reconnect()
        c = conn.cursor()
        t = (troop_name,)
        c.execute("""SELECT id FROM troops WHERE name=%s""", t)
        datas = c.fetchone()
        conn.close()

        return datas

    def update_player(self, commander_name: str, max_troop_size: int, id: int,
                      now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        conn.reconnect()
        c = conn.cursor()
        d = (commander_name, max_troop_size, now, id)
        c.execute(
            """UPDATE players SET commander_name=%s, max_troop_size=%s, submission_date=%s WHERE id=%s""", d)
        conn.commit()
        conn.close()

    def fill_troops(self, sorted_datas: list, discord_name: str):
        record_to_insert = []
        player_id = self.find_player_by_name(discord_name)
        for data in sorted_datas:
            troop_id = self.find_troop_by_name(data[0])
            record_to_insert.append((int(data[1]), troop_id[0], player_id[0]))
        conn.reconnect()
        c = conn.cursor()
        c.executemany(
            """INSERT INTO quantities(quantity, troop_id, player_id)
            VALUES (%s, %s, %s)""", record_to_insert)
        conn.commit()
        conn.close()

    def delete_troops(self, player_id: int):
        d = (player_id,)
        conn.reconnect()
        c = conn.cursor()
        c.execute(
            """DELETE from quantities WHERE player_id=%s""", d)
        conn.commit()
        conn.close()

    def leaderboard(self):
        conn.reconnect()
        c = conn.cursor()
        c.execute("""select commander_name, sum(tier*quantity) as points from troops t 
        join quantities q on q.troop_id = t.id 
        join players p on q.player_id = p.id 
        GROUP by commander_name
        order by points desc
        limit 20""")
        datas = c.fetchall()
        conn.close()

        return datas


if __name__ == '__main__':
    db = DB()
    datas = db.leaderboard()
    print(datas)
