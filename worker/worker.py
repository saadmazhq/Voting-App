import os
import redis
import psycopg2

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", "6379"))

db_host = os.getenv("POSTGRES_HOST", "db")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_user = os.getenv("POSTGRES_USER", "postgres")
db_password = os.getenv("POSTGRES_PASSWORD", "postgres")
db_name = os.getenv("POSTGRES_DB", "votes")

r = redis.Redis(host=redis_host, port=redis_port, db=0)

def process_vote(choice):
    conn = psycopg2.connect(
        host=db_host, port=db_port,
        user=db_user, password=db_password,
        dbname=db_name
    )
    cur = conn.cursor()
    if choice == "YES":
        cur.execute("UPDATE vote_totals SET yes_count = yes_count + 1 WHERE id = TRUE;")
    elif choice == "NO":
        cur.execute("UPDATE vote_totals SET no_count = no_count + 1 WHERE id = TRUE;")
    conn.commit()
    conn.close()

def main():
    while True:
        _, vote = r.brpop("votes")
        process_vote(vote.decode("utf-8"))

if __name__ == "__main__":
    main()