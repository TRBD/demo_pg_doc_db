# demo_pg_doc_db
Demo of Practical Document DB Inspired Usage for Structured Data Workflows


See companion writeup: https://medium.com/@trbd/practical-document-db-inspired-usage-for-structured-data-workflows-945ff5665e9a


Notes on running the example


The project is set to work on localhost, port 5432, database demo_doc_db. This can be changed in the config.py file.


Initializing the database is w/o issue from the command line

    # Windows: 
    > psql -U postgres -f <path_to_project>\demo_pg_doc_db\resources\pg_create_db.sql postgres
    # Linux: 
    $ psql -U postgres postgres -f <path_to_project>/demo_pg_doc_db/resources/pg_create_db.sql

Populating it with the sample data ought to be possible in Linux but Windows has trouble passing a dynamic filename to a psql .sql script, thus will need to copy-paste it to a psql terminal.

    # Windows:
    # Comment out line 42 of resources/pg_load_db.sql| uncomment line 41
    > psql
    # Copy/past pg_load_db.sql contents
    # Linux
    $ psql -U postgres postgres -v copy_file=”<path_to_project>/data/sample_data.txt” -f <path_to_project>/demo_pg_doc_db/resources/pg_load_db.sql

To run the exercise detailed in the accompanying post, navigate to the project directory and execute:

    $ python -m example.exercise
