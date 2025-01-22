# Pipeline ETL Oracle para PostgreSQL com Airflow

Este projeto implementa um pipeline de Extração, Transformação e Carga (ETL) que migra dados de um banco de dados Oracle para um banco de dados PostgreSQL, usando Apache Airflow para orquestração.

## Descrição

O pipeline lê dados de uma tabela chamada `SALES_TRANSACTIONS` no Oracle, aplica transformações específicas e carrega os dados transformados em uma tabela correspondente chamada `ANALYTICS_TRANSACTIONS` no PostgreSQL.

## Funcionalidades

*   Extração de dados do Oracle.
*   Transformações:
    *   Exclusão de registros com `AMOUNT <= 0`.
    *   Normalização da coluna `CUSTOMER_ID` para letras maiúsculas.
    *   Criação de uma nova coluna `CATEGORY` com base no valor de `AMOUNT` (LOW, MEDIUM, HIGH).
*   Carregamento de dados no PostgreSQL.
*   Orquestração com Apache Airflow.
*   Logs detalhados das etapas do pipeline.
*   Mecanismo de reexecução para casos de falha.

## Pré-requisitos

*   **Python 3.7+:** Certifique-se de ter o Python instalado.
*   **Apache Airflow:** Instale e configure o Airflow. Consulte a documentação oficial: [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
*   **cx_Oracle:** Instale o driver Oracle para Python: `pip install cx_Oracle`
    *   Você também precisará instalar o Instant Client da Oracle. Consulte a documentação do `cx_Oracle` para instruções detalhadas.
*   **psycopg2:** Instale o driver PostgreSQL para Python: `pip install psycopg2`
*   **Pandas:** Instale a biblioteca Pandas: `pip install pandas`
*   **Pendulum:** Instale a biblioteca pendulum para lidar com datas e horários: `pip install pendulum`
*   **Banco de dados Oracle:** Um banco de dados Oracle em execução com a tabela `SALES_TRANSACTIONS`.
*   **Banco de dados PostgreSQL:** Um banco de dados PostgreSQL em execução.
*   **Variáveis de Ambiente:** Configure as seguintes variáveis de ambiente:
    *   `ORACLE_CONN_STRING`: String de conexão para o Oracle (ex: `usuario/senha@host:porta/serviço`).
    *   `POSTGRES_CONN_STRING`: String de conexão para o PostgreSQL (ex: `dbname=nome_do_banco user=usuario password=senha host=host port=porta`).

## Configuração

1.  **Clone o repositório (se aplicável):**

    ```bash
    git clone <seu_repositorio>
    cd <nome_do_projeto>
    ```

2.  **Crie a tabela no PostgreSQL:**
    Execute o script SQL `create_table.sql` no seu banco de dados PostgreSQL:

    ```bash
    psql -d <nome_do_banco> -f create_table.sql
    ```

3.  **Copie os arquivos para o Airflow:**
    Copie os arquivos `etl_script.py` e `etl_dag.py` para o diretório `dags` do seu Airflow (geralmente `$AIRFLOW_HOME/dags`).

4.  **Instale as dependências Python:**
    Crie um arquivo `requirements.txt` na pasta `dags` com o conteúdo:

    ```
    apache-airflow
    cx-Oracle
    psycopg2
    pandas
    pendulum
    ```

    E execute:
    ```bash
    pip install -r $AIRFLOW_HOME/dags/requirements.txt
    ```

5.  **Variáveis de Ambiente no Airflow:**
    Na interface web do Airflow (Admin -> Variables), crie as variáveis `ORACLE_CONN_STRING` e `POSTGRES_CONN_STRING` com os valores das suas strings de conexão.

## Execução

1.  **Inicie o Airflow:**

    ```bash
    airflow webserver -p 8080 # Ou outra porta
    airflow scheduler
    ```

2.  **Acesse a interface web do Airflow:** Abra o navegador e acesse a interface web do Airflow (geralmente em `http://localhost:8080`).

3.  **Ative a DAG:** Encontre a DAG chamada `etl_oracle_postgres` na lista de DAGs e ative-a.

4.  **Execute a DAG:** Clique no botão "Trigger DAG" para executar a DAG manualmente. A DAG também será executada automaticamente de acordo com o agendamento definido (`@daily` neste exemplo).

5.  **Verifique os logs:** Monitore a execução da DAG na interface web do Airflow e verifique os logs das tarefas para identificar possíveis erros. Os logs também serão salvos no arquivo `etl.log` localmente.

6.  **Verifique os dados no PostgreSQL:** Consulte a tabela `ANALYTICS_TRANSACTIONS` no seu banco de dados PostgreSQL para verificar se os dados foram carregados corretamente.

## Arquivos

*   `create_table.sql`: Script SQL para criar a tabela `ANALYTICS_TRANSACTIONS` no PostgreSQL.
*   `etl_script.py`: Script Python com as funções de ETL (extração, transformação e carregamento).
*   `etl_dag.py`: DAG do Airflow que orquestra o pipeline.

## Estrutura do Projeto


├── dags/
│   ├── etl_dag.py        # DAG do Airflow
│   ├── etl_script.py     # Script Python com as funções de ETL
│   └── requirements.txt # Dependências do projeto
├── create_table.sql      # Script SQL para criar a tabela no PostgreSQL
└── README.md             # Este arquivo

## Observações

*   Certifique-se de que as strings de conexão dos bancos de dados estejam corretas e que os bancos estejam acessíveis.
*   Adapte o agendamento da DAG (`schedule`) conforme necessário.
*   Este exemplo usa Pandas para as transformações. Para volumes de dados extremamente grandes, considere usar o PySpark para melhor escalabilidade.
*   A configuração das variáveis de ambiente no Airflow (Admin -> Variables) é a forma mais segura e recomendada.

## Contribuições

Contribuições são bem-vindas!

## Licença

MIT