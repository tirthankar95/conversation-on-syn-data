'''
docker build -t my-postgres .

docker run -d \
  --name postgres-container \
  -p 5432:5432 \
  my-postgres

docker start postgres-container
docker exec -it postgres-container psql -U myuser -d mydb
'''
import subprocess

sql_command = """
CREATE TABLE IF NOT EXISTS user_tm (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# sql_command = """
# SELECT * FROM user_tm;
# """

command = [
    "docker", "exec", "-i", "postgres-container",
    "psql", "-U", "myuser", "-d", "mydb"
]

try:
    result = subprocess.run(
        command,
        input=sql_command,
        text=True,
        capture_output=True,
        check=True
    )
    print("Table created successfully!")
    print("Output:\n", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error executing command:", e.stderr)