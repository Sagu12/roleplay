from fastapi import FastAPI
from src.prediction.api.v1 import misstm_chat, doctor_chat, fitnesscoach_chat, teacher_chat, bf_chat
from fastapi_health import health
from src.prediction.api.v1.health_check import healthy_condition, sick_condition
import newrelic.agent
import os,sentry_sdk
from dotenv import load_dotenv
from configparser import ConfigParser
app = FastAPI()

load_dotenv(r"src/prediction/env/.env")
environment = os.getenv("env")
url_sentry = os.getenv("sentry_url")
sentry_sdk.init(url_sentry, traces_sample_rate=1.0, environment=environment, debug=False)

config = ConfigParser()
config.read(r'src/prediction/newrelic.ini')
newrelic_app_name = config.get('newrelic', 'app_name')

app_name= os.getenv("app_name")
distributed_tracing_enabled= os.getenv("distributed_tracing.enabled")
transaction_tracer_record_sql= os.getenv("transaction_tracer.record_sql")
license_key= os.getenv('license_key')

newrelic_distributed_tracing_enabled = config.get('newrelic', 'distributed_tracing.enabled')
newrelic_transaction_tracer_record_sql = config.get('newrelic', 'transaction_tracer.record_sql')
newrelic_license_key = config.get('newrelic', 'license_key')

updated_newrelic_app_name = config.set('newrelic', 'app_name', app_name)
updated_newrelic_distributed_tracing_enabled = config.set('newrelic', 'distributed_tracing.enabled', distributed_tracing_enabled)
updated_newrelic_transaction_tracer_record_sql = config.set('newrelic', 'transaction_tracer.record_sql', transaction_tracer_record_sql)
updated_newrelic_license_key = config.set('newrelic', 'license_key', license_key)

with open(r'src/prediction/test_update.ini', 'w') as configfile:
    config.write(configfile)

newrelic.agent.initialize(r'src/prediction/test_update.ini')

app.include_router(misstm_chat.predict,tags=["gf_chat"])
app.include_router(bf_chat.predict,tags=["bf_chat"])
app.include_router(doctor_chat.predict,tags=["doctor_chat"])
app.include_router(teacher_chat.predict,tags=["teacher_chat"])
app.include_router(fitnesscoach_chat.predict,tags=["fitness_coach_chat"])
app.add_api_route("/health-check", health([healthy_condition, sick_condition]))