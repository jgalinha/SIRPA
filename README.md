
# Table of Contents

1.  [Introdução](#orgb3ee48d)
2.  [Frontend](#orgac91ed2)
3.  [Backend](#org103f9b7)
4.  [Docker Compose](#org7b82721)
5.  [Bakcups](#org10d306f)



<a id="orgb3ee48d"></a>

# Introdução

O **Sistema Integrado de Registo de Presenças em Aula (SIRPA)** é um sistema devolvido para a disciplina de Projeto Integrado da Licenciatura em Engenharia informátia da ESTIG.

O sistema tem como objectivo o registo de presença dos alunos via QRCode


<a id="orgac91ed2"></a>

# Frontend

Frontend [README.org](frontend/README.md)


<a id="org103f9b7"></a>

# Backend

Backend [README.org](backend/README.md)


<a id="org7b82721"></a>

# Docker Compose

    version: '3'
    
    services:
        web:
            container_name: sirpa-app
            # image: sirpa:0.0.1-dev
            build:
                context: './frontend/'
            ports:
                - "3000:3000"
            volumes:
                - './frontend/:/app'
            networks:
              - sirpa-network
            command: npm start
        api:
            container_name: sirpa-api
            # image: sirpa-api:0.0.1
            build:
                context: './backend/api'
                dockerfile: '../Dockerfile-fastapi'
            ports:
                - "8000:8000"
            volumes:
                - './backend/api/api:/api'
            networks:
                - sirpa-network
        postgres:
            container_name: sirpa-postgres
            image: postgres
            env_file:
                - backend/.env
            ports:
                - "5432:5432"
            volumes:
                - ~/sirpa_data/:/var/lib/postgresql/data
            networks:
                - sirpa-network
        pgadmin:
            container_name: sirpa-pgadmin
            image: dpage/pgadmin4
            ports:
                - "16543:80"
            volumes:
                - pgadmin-data:/var/lib/pgadmin
            env_file:
                - backend/.env
            depends_on:
                - postgres
            networks:
                - sirpa-network
    
    volumes:
        pgadmin-data:
    
    networks:
        sirpa-network:
            driver: bridge

-   Run cmd
    
        # -d is to run in detach mode (backgroud)
        docker-compose up -d

-   Stop cmd
    
        # -d is to run in detach mode (backgroud)
        docker-compose down


<a id="org10d306f"></a>

# Bakcups

pgbackrest

<https://www.enterprisedb.com/postgresql-database-backup-recovery-what-works-wal-pitr>
<https://access.crunchydata.com/documentation/crunchy-postgres-containers/4.2.2/examples/backup-restoration/pgbackrest/>
<https://pgbackrest.org/>
<https://severalnines.com/database-blog/validating-your-postgresql-backups-docker>
<https://www.reddit.com/r/PostgreSQL/comments/ms036b/backup_postgresql_docker/>
<https://deck-chores.readthedocs.io/en/stable/>

barman

<https://pgbarman.org/>
<https://github.com/EnterpriseDB/barman>
<https://hub.docker.com/r/ubcctlt/barman>

rsync

gpg

<https://app.qr-code-generator.com/>

