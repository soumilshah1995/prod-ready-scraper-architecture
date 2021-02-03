try:

    from datetime import timedelta
    from airflow import DAG

    # Operators
    from airflow.operators.python_operator import PythonOperator
    from airflow.operators.email_operator import EmailOperator

    from datetime import datetime

    # Setting up Triggers
    from airflow.utils.trigger_rule import TriggerRule

    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from time import sleep

    print("All Dag modules are ok ......")
except Exception as e:
    print("Error  {} ".format(e))


def connectSelenium(**context):
    URL = "http://hub:4444/wd/hub"
    options = webdriver.ChromeOptions()
    options.headless = True

    driver = webdriver.Remote(
        command_executor=URL,
        desired_capabilities=DesiredCapabilities.CHROME,
        options=options)
    print(driver)
    # start scraping


def on_failure_callback(context):
    print("Fail works  !  ")


with DAG(dag_id="invoices_dag",
         schedule_interval="@once",
         default_args={
             "owner": "airflow",
             "start_date": datetime(2020, 11, 1),
             "retries": 1,
             "retry_delay": timedelta(minutes=1),
             'on_failure_callback': on_failure_callback,
             'email': ['shahsoumil519@gmail.com'],
             'email_on_failure': False,
             'email_on_retry': False,

         },
         catchup=False) as dag:

    connectSelenium = PythonOperator(
        task_id="connectSelenium",
        python_callable=connectSelenium,
        provide_context=True
    )

    email = EmailOperator(
        task_id='send_email',
        to='shahsoumil519@gmail.com',
        subject='Airflow Alert',
        html_content=""" <h3>Email Test Airflow </h3> """,
    )

connectSelenium >> email




























# ====================================Notes====================================

# all_success           -> triggers when all tasks arecomplete
# one_success           -> trigger when one task is complete
# all_done              -> Trigger when all Tasks are Done
# all_failed            -> Trigger when all task Failed
# one_failed            -> one task is failed
# none_failed           -> No Task Failed

# for Getting Variables from airlfow
# from airflow.models import Variable
# dag_config = Variable.get("VAR1")
# print("VAR 1 is : {} ".format(dag_config))
#instance = context.get("ti").xcom_pull(key='mykey')

# context['ti'].xcom_push(key='mykey', value=df)
#         op_kwargs={'filename': "Soumil.csv"},

# ==============================================================================



# ============================== Executor====================================

# There are Three main  types of executor
# -> Sequential Executor  run single task in linear fashion wih no parllelism default Dev
# -> Local Exector  run each task in seperate process
# -> Celery Executor Run each worker node within multi node architecture Most scalable

# ===========================================================================