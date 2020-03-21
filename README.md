# Tixte FOSS [![Build Status](https://dev.azure.com/michaelmcnulty37/Tixte%20FOSS/_apis/build/status/michaelfm1211.tixte-foss?branchName=master)](https://dev.azure.com/michaelmcnulty37/Tixte%20FOSS/_build/latest?definitionId=5&branchName=master)

Welcome to Tixte FOSS, the MIT licensed, free and open source open source, and customizable gaming platform.

## Contributing

Before contributing to Tixte FOSS set up a python virtual environment called venv (we ask you name the virtual environment venv for compatibility reasons) with this command

```bash
bash-3.2$ virtualenv venv
```

Before contributing we recommend installing python-dotenv and autoenv globally via PIP. If you choose not to do this you must remember to activate the virtual environment and set \$APP_SETTINGS. Next, you will need to install all the dependencies for Tixte FOSS with

```bash
bash-3.2$ pip install -r requirements.txt
```

Finally, please follow the following requirements(they may seem silly but they are necessary):

1. Use the Git VCS.
2. Use Python 3
3. Format all code with autopep8(unless it breaks the code, in that case append "# nopep8" to the end of the line)

## Building

## With gunicorn

To run Tixte FOSS with gunicorn please follow the instructions in the Contributing section first. You will then need to set the environment variables $DATABASE_URL which is a URL to a PostgreSQL server(using the format postgres://user:password@example.com:port/database), and \$PORT which is the port for the server to run on. You will then need to run the setup utility with

```bash
(venv) bash-3.2$ python setup.py
```

After that all you need to do is run this command:

```bash
(venv) bash-3.2$ gunicorn tixte_foss:app
```

### Docker

First you will need to create a PostgreSQL server. This guide will create a container using the offical PostgreSQL Docker image, but if you already have a PostgreSQL server you can skip this step. To create a PostgreSQL Docker container use these commands to pull the image and create a container using that image.

```bash
bash-3.2$ docker pull postgres
bash-3.2$ export POSTGRES_PORT=7000 # We will use port 7000 on the host machine, this port can be anything
bash-3.2$ docker run -p $POSTGRES_PORT:5432 -d postgres
```

The output of that last command should show you the ID of the Docker Postgres container. In our case the ID of the PostgreSQL container is a130f4bb222fa55e3bd1c231e215034dc5be3f53484b26b95897c2e1254245b3. Run the following command to run a bash shell in the PostgreSQL container and attach it to your terminal

```bash
bash-3.2$ docker exec -it a130f4bb222fa55e3bd1c231e215034dc5be3f53484b26b95897c2e1254245b3 bash
```

To create a PostgreSQL database you will need to first login as the user postgres then run the psql command.

```bash
root@a130f4bb222f:/$ su postgres
postgres@a130f4bb222f:/$ psql
```

Now all of the commands you enter will be interpreted as PostgreSQL commands. Use the CREATE DATABASE PostgreSQL command to create a tixte database

```sql
postgres=# CREATE DATABASE tixte;
CREATE DATABASE
```

The Postgres Docker container should now be set up. To get out of the container, type exit once to get out of the psql command, then type exit another time to get out of the postgres user, then type exit final time to exit the container.

Once PostgreSQL is set up, you need to build Tixte for docker deployment first build the Dockerfile with

```bash
bash-3.2$ docker build -t tixte-foss .
```

This will generate a Docker image ready for development. Now you have to specify the URL to your postgres server or container. In the folowing command replace &lt;POSTGRESQL URL&gt; with the URL of your PostgreSQL server following the scheme postgres://user:password@example.com:port/database If you followed this guide entirely so far than this should work for you: postgres://postgres@localhost:7000/tixte

```bash
bash-3.2$ export DATABASE_URL="<POSTGRESQL URL>"
```

Now you will need to create the Tixte FOSS container. You can create a simple one with

```bash
bash-3.2$ docker run -p 8080:80 -e DATABASE_URL=$DATABASE_URL -e APP_SETTINGS="config.ProductionConfig" tixte-foss
```

If all goes well the Tixte FOSS Setup Utility should start. The default administrator password is password. Once the setup utility has completed the server should start automatically. You should now be able to go to http://0.0.0.0:8080 and be greated by the Tixte FOSS home page. To change your password go to http://0.0.0.0:8080
