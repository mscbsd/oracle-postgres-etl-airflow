import os
import datetime
import logging

import pandas as pd
import cx_Oracle
import psycopg2

def extract_data_oracle(oracle_conn_string, table_name="SALES_TRANSACTIONS"):
    try:
        conn = cx_Oracle.connect(oracle_conn_string)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        conn.close()
        logging.info("Dados extraídos do Oracle com sucesso.")
        return df
    except cx_Oracle.Error as error:
        logging.error(f"Erro na extração do Oracle: {error}")
        return None

def transform_data(df):
    try:
        df = df[df['AMOUNT'] > 0].copy()
        df['CUSTOMER_ID'] = df['CUSTOMER_ID'].str.upper()
        df['CATEGORY'] = pd.cut(df['AMOUNT'], bins=[-float('inf'), 100, 500, float('inf')], labels=['LOW', 'MEDIUM', 'HIGH'], right=False)
        logging.info("Dados transformados com sucesso.")
        return df
    except Exception as error:
        logging.error(f"Erro na transformação dos dados: {error}")
        return None

def load_data_postgres(df, postgres_conn_string, table_name="ANALYTICS_TRANSACTIONS"):
    try:
        conn = psycopg2.connect(postgres_conn_string)
        cursor = conn.cursor()
        for index, row in df.iterrows():
            sql = f"""
                INSERT INTO {table_name} (TRANSACTION_ID, CUSTOMER_ID, AMOUNT, TRANSACTION_DATE, CATEGORY)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, tuple(row))
        conn.commit()
        conn.close()
        logging.info("Dados carregados no PostgreSQL com sucesso.")
        return True
    except psycopg2.Error as error:
        logging.error(f"Erro no carregamento para o PostgreSQL: {error}")
        return False

def setup_logging():
    logging.basicConfig(
        filename='etl.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

if __name__ == "__main__":
    setup_logging()
    oracle_conn_string = os.environ.get("ORACLE_CONN_STRING")
    postgres_conn_string = os.environ.get("POSTGRES_CONN_STRING")

    if not oracle_conn_string or not postgres_conn_string:
        logging.error("Variáveis de ambiente ORACLE_CONN_STRING e POSTGRES_CONN_STRING devem ser definidas.")
        exit(1)

    df = extract_data_oracle(oracle_conn_string)
    if df is not None:
      transformed_df = transform_data(df)
      if transformed_df is not None:
          load_data_postgres(transformed_df, postgres_conn_string)