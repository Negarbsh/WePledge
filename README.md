# WePledge
code for the webapp


## Django login

You can login at `http://localhost:8000/admin` using 

- user: *admin@admin.com* 
- password *adminpass*


## Rebuilding the backend containers

Before rebuilding all backend docker containers (wepledge_pgadmin_1, wepledge_backend_1 and db) do the following: 

1. Delete all files except for the *__init__.py* in the folder *./WePledge/backend/src/emissions/migrations*.
2. Delete all backend containers (wepledge_pgadmin_1, wepledge_backend_1 and db).
3. Run `docker volume prune` to delete the database. 
4. Run `docker compose up´.