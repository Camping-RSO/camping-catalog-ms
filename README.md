# camping catalog ms

A microservice for storing camping actions.

Table of Contents
=================
- [Purpose](#purpose)
- [Environment variables](#environment-variables)
- [Examples](#examples)


## Purpose

The repository implements the recording of camping actions. The microservice is API done using [GraphQL](https://graphql.org/), which connects on [InfluxDB](https://www.influxdata.com/) 
time series base.


## Environment variables

This microservice camping API requires microservices endpoint. For that you can set:
- `INFLUX_HOST`,
- `INFLUX_PORT`,
- `INFLUX_USER`,
- `INFLUX_PASSWORD` and
- `INFLUX_DATABASE`

environment variables when running with Docker.


## Examples

Camping catalog microservice query and mutation examples:

```
query = 
     query something{
       logs {
         "camping-test-ms"
         "Post method was executed."
       }
     }

 mutation = 
     mutation addLog{
       createLog(microservice:"camping-test-ms", message:"test") {
           log {
             "camping-test-ms"
             "Post method was executed."
           }
       }
     } 
```
