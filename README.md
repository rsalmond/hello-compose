# Hello Compose

A very elaborate hello world app embedded in a robust docker development environment.

# Setup

`make fromscratch`

This will build the hello world app container, create a docker network, initialize the databases (master and replica), run the initial migrations, then launch the app.

# Use

`make build`

Rebuild the app container.

---

`make up`

Stand everything up and show logs (docker-compose up).

---

`make test`

Run the functional tests against the most recent build of the app container.

---

`make testdata`

Submit a canned API request to the app for testing.

---

`cp docker-compose.override.dev.yml docker-compose.override.yml`

_stop and start docker-compose_

`make dev`

Reconfigure docker compose to bring up the app container without starting the app, then drop into a shell in the container for testing / hacking.

---

`make nuke`

Scrap everything.
