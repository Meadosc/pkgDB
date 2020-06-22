# Structure

- `parse_insert_db.py` - Used to extract the metadata information from `./data/raw_meta/*.txt` and insert the information
to the `./data/db/packages.db` sqlite db.
- `extract_license.py` - Used to query for licenses with third-party sources (repos of Apline Linux, Arch etc) to fetch licenses 
of packages for which license information is not found anywhere else, the output is in `./data/json/*.json`
- `license_insert_db.py` - As the name suggests, script used to insert the licenses extracted from third party sources to
the `./data/db/packages.db`
- `restapi.py` - A REST interface for the packages database, a sample database is already part of the repo, and this API interface
could be a goodl place to start to see the structure of the db.
