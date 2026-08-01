import subprocess
from dataclasses import dataclass

@dataclass
class TableNames:
    id: str
    table_name: str

class SqlMachine:
    def __init__(self):
        self.create_table_names_table()

    def create_table_names_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS public.\"TableNames\" (
            id TEXT PRIMARY KEY,
            table_name TEXT NOT NULL UNIQUE
        );
        """
        self.run(create_table_sql)
    
    def insert_table_name(self, table_name):
        insert_sql = f"""
        INSERT INTO public.\"TableNames\" (id, table_name)
        VALUES (gen_random_uuid()::text, '{table_name}')
        ON CONFLICT (table_name) DO NOTHING;
        """
        self.run(insert_sql)
    
    def select_table_names(self):
        select_sql = "SELECT * FROM public.\"TableNames\";"
        result = self.run(select_sql)
        parsed_result = []
        for line in result.splitlines():
            line = line.strip()
            row = line.split('|')
            if len(row) == 2 and row[0].strip() != 'id' and row[1].strip() != 'table_name':
                parsed_result.append(row[1].strip())
        return parsed_result

    def run(self, sql_command):
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
            print("Query executed successfully!")
            print("Output:", result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print("Error executing command:", e.stderr)
            return None