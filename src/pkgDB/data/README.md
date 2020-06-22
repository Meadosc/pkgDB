## Data directory

Contains raw and process meta data of all packages.

- `db` - Directory has a database with `packages.db` with 2 tables - sources and binaries, used to store metadata of all packages.
- `json` - post processed output with `package_name:license` information for easy consumption
- `raw_meta` - Raw text files with package meta information fetched from ubuntu.


Look at `pkgDB/scripts/` to find the scripts used to fetch raw data and also database schema.



