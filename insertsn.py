from config import load_config
import psycopg2

def insert_data(username, userlevel, userscore):
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # 1. Проверяем, есть ли юзер
                cur.execute("SELECT user_id FROM users WHERE user_name = %s", (username,))
                result = cur.fetchone()

                if result:
                    user_id = result[0]
                else:
                    cur.execute("INSERT INTO users (user_name) VALUES (%s) RETURNING user_id", (username,))
                    user_id = cur.fetchone()[0]

                # 2. Вставляем score
                cur.execute(
                    "INSERT INTO users_score (user_id, score, level) VALUES (%s, %s, %s)",
                    (user_id, userscore, userlevel)
                )

                conn.commit()
                print("\n✅ Данные успешно добавлены\n")

    except Exception as error:
        print("❌ Ошибка при добавлении данных:", error)
