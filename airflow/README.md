# Apache Airflow Setup with Docker

This repository provides two scripts to automate the setup of Apache Airflow using Docker:
- `setup_airflow.bat`: For **Windows** users
- `setup_airflow.sh`: For **macOS/Linux** users

These scripts will:
- Prompt you for your desired Airflow admin credentials.
- Set up Apache Airflow with PostgreSQL and Redis as the backend.
- Create an admin user.
- Provide the Airflow UI URL for you to access after the setup is complete.

---

## Prerequisites

Before running the scripts, ensure you have the following installed on your machine:
- [Docker](https://www.docker.com/products/docker-desktop) (Docker Desktop for Windows/macOS)
- Docker Compose (included in Docker Desktop)
  
You can check if Docker is installed by running the following command:
```bash
docker --version
