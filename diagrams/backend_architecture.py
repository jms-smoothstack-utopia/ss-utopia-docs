from diagrams import Diagram
from diagrams import Cluster
from diagrams.aws.database import RDSMysqlInstance
from diagrams.programming.framework import Spring
from diagrams.programming.framework import Angular
from diagrams.onprem.vcs import Github

direction = "LR"

with Diagram("Utopia Airlines", direction=direction) as diag:
    with Cluster("Private Network"):
        eureka = Spring("Eureka")
        config = Spring("Config")


        with Cluster("Authentication"):
            auth = Spring()
            auth - RDSMysqlInstance()

        with Cluster("Customers"):
            customers = Spring()
            customers - RDSMysqlInstance()
            customers >> auth

        with Cluster("Flights/Airplanes/Airports"):
            flights = Spring()
            flights - RDSMysqlInstance()

        with Cluster("Tickets"):
            tickets = Spring()
            tickets - RDSMysqlInstance()
            tickets >> flights

    with Cluster("Public Network"):
        orchestrator = Spring("Gateway")
        user_portal = Angular("User Portal")
        user_portal >> orchestrator

    config >> Github("Config Files")

    eureka - [auth, customers, tickets, flights, config]
    config - [auth, customers, tickets, flights]
    orchestrator >> eureka
