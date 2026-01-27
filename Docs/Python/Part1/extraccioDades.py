from connMongo import get_db_connection

def main():
    db = get_db_connection()
    col = db["FEB3_players_statistics"]

    print(col.find_one())

if __name__ == "__main__":
    main()