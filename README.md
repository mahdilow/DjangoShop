for local development:

  create 'backend.env' and set:
	
          ALGO_APPLICATION_ID=
          ALGOLIA_KEY=
          ALLOWED_HOSTS=
          DEBUG=
          LIARA_ACCESS_KEY=
          LIARA_BUCKET_NAME=
          LIARA_ENDPOINT=
          SECRET_KEY=
          
create 'postgres.env' and set :

                DB_URL=postgresql://user:password@postgres:5432/db_name
     if using docker:
                POSTGRES_USER=
                POSTGRES_PASSWORD=
                POSTGRES_DB=
