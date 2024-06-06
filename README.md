# Library booking system
Project for Big Data and Distributed Systems in PUT Poznań University of Technology. \
The project is a distributed system for a **library**, where you can reserve **books**.

## Author
**Adam Korba** (index 151962)

# Report
Report for this project [is availible here](report.md)

# How to run
1. Fetch the data
```
mkdir data
python3 fetch_data
```
2. Start the cassandra cluster
```
docker compose up -d
```
3. Seed the database
```
python3 seed.py
```
4. (Optional) Start stress tests
```
python3 stress_tests.py
```
5. Run the application
```
python3 main.py
```

