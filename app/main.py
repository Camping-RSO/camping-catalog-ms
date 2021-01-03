import graphene
from influxdb import InfluxDBClient
from flask import Flask
from flask_graphql import GraphQLView
import os


def get_influx_client():
    host = os.environ.get('INFLUX_HOST')
    port = os.environ.get('INFLUX_PORT')
    user = os.environ.get('INFLUX_USER')
    password = os.environ.get('INFLUX_PASSWORD')
    database = os.environ.get('INFLUX_DATABASE')
    return InfluxDBClient(host, port, user, password, database, True)


def influx_query():
    client = get_influx_client()
    results = client.query("SELECT * FROM logs")
    logs = []
    for measurement in results.get_points(measurement='logs'):
        microservice = measurement['microservice']
        message = measurement['message']
        logs.append(Log(microservice=microservice, message=message))
    client.close()
    return logs


def influx_write(microservice, message):
    client = get_influx_client()
    json_body = [
        {
            "measurement": "logs",
            "fields": {
                "microservice": "{}".format(microservice),
                "message": "{}".format(message),
            }
        }
    ]
    client.write_points(json_body)
    client.close()


class Log(graphene.ObjectType):
    microservice = graphene.String()
    message = graphene.String()


class CreateLog(graphene.Mutation):
    class Arguments:
        microservice = graphene.String()
        message = graphene.String()

    log = graphene.Field(lambda: Log)

    def mutate(root, info, microservice, message):
        log = Log(microservice=microservice, message=message)
        influx_write(microservice, message)
        return CreateLog(log=log)


class Mutation(graphene.ObjectType):
    create_log = CreateLog.Field()


# We must define a query for our schema
class Query(graphene.ObjectType):
    logs = graphene.List(Log)

    def resolve_logs(parent, info):
        return influx_query()


schema = graphene.Schema(query=Query, mutation=Mutation)

# query and mutation examples:
#
# query = """
#     query something{
#       logs {
#         microservice
#         message
#       }
#     }
# """
# mutation = """
#     mutation addLog{
#       createLog(microservice:"camping-test-ms", message:"test") {
#           log {
#             microservice
#             message
#           }
#       }
#     }
# """

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World from camping"


app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
