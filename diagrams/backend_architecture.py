from diagrams import Diagram
from diagrams.programming.framework import Spring
from diagrams.programming.framework import Angular

with Diagram("Utopia Airlines", show=False, direction='TB') as diag:
    eureka = Spring("Eureka Service Discovery Server")
    config = Spring("Spring Config Server")
    orchestrator = Spring("Orchestrator/Gateway")
    auth = Spring("Authentication Service")
    customers = Spring("Customers Service")
    tickets = Spring("Tickets/Booking Service")
    flights = Spring("Flights/Airplanes/Airports Service")
    user_portal = Angular("User Portal")

    for service in [config, auth, customers, tickets, flights, orchestrator]:
        service >> eureka

    for service in [auth, customers, tickets, flights, orchestrator]:
        service >> config

    customers >> auth
    tickets >> flights

    for service in [auth, customers, tickets, flights]:
        orchestrator >> service

    user_portal >> orchestrator
