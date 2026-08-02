from app6_backend.database import SqlMachine
from app6_backend.langchain_generate import GenWorkflow
from app6_backend.prompts import (
    query_conversion_prompt, 
    table_entry_prompt,
    clean_query_prompt,
    chat_prompt
)

sql_machine = SqlMachine()
chat_agent = GenWorkflow(chat_prompt, clean_query_prompt)
table_entry_agent = GenWorkflow(table_entry_prompt, clean_query_prompt)
query_conversion_agent = GenWorkflow(query_conversion_prompt, clean_query_prompt)

def parse_sql(file_content):
    prefixes = ["CREATE TABLE"]
    sql_commands, table_names = [], []
    parse_start, sql_command = False, ''
    for line in file_content.splitlines():
        for prefix in prefixes:
            if line.strip().startswith(prefix):
                parse_start = True 
                table_names.append(line.split()[2].strip('"'))
            if parse_start:
                sql_command += line + '\n'
                if line.strip().endswith(';'):
                    sql_commands.append(sql_command)
                    sql_command = ''
                    parse_start = False
    return table_names, sql_commands

def llm_generate(prompt, file_name, file_content, temperature, max_tokens):
    """Dummy function to simulate generation call."""
    print(
        f"Prompt: {prompt}\n"
        f"File Name: {file_name}\n"
        f"Temperature: {temperature}\n"
        f"Max Tokens: {max_tokens}\n"
    )
    try:
        table_names, sql_commands = parse_sql(file_content)
        for table_name, sql_command in zip(table_names, sql_commands):
            sql_command = query_conversion_agent.workflow_response(sql_command)
            print(f"Executing SQL Command:\n{sql_command}")
            sql_machine.run(sql_command)
            user_prompt = f'[INSTRUCTIONS]\n{prompt}\n\n[SQL SCHEMA]\n{sql_command}'
            sql_machine.run(table_entry_agent.workflow_response(user_prompt))
            sql_machine.insert_table_name(table_name, sql_command)
        return True
    except Exception as e:
        print(f"Error during generation: {e}")
        return False


def llm_chat_with_data(user_prompt: str, table_name: str, history: list):
    """Function to handle chat with data."""
    try:
        if table_name not in sql_machine.select_table_names():
            return f"Table '{table_name}' does not exist."
        user_prompt = f'[INSTRUCTIONS]\n{user_prompt}\n\n[TABLE NAME]\n{table_name}' + \
                    f'[TABLE SCHEMA]\n{sql_machine.run(f"SELECT schema FROM public.\"TableNames\" WHERE table_name = \'{table_name}\';")}' + \
                    f'[TABLE DATA]\n{sql_machine.run(f"SELECT * FROM {table_name};")}'
        sql_command = chat_agent.workflow_response(user_prompt)
        print(f"Executing SQL Command:\n{sql_command}")
        sql_machine.run(sql_command)
        return True
    except Exception as e:
        print(f"Error during chat with data: {e}")
        return False


if __name__ == "__main__":
    prompt = 'Create tables defined in the ddl schema file.'
    with open('../examples/simple.ddl', 'r') as f:
        file_content = f.read()
    llm_generate(prompt, 'simple.ddl', file_content, temperature=0.7, max_tokens=512)