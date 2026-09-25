# HealtHub

HealtHub : Where Heathy and Tasty Meet

> This is the document for Back End repository of HealtHub

## Table of Contents

1. [Prequisites](#prequisites-)
2. [Database](#database)
3. [How to run the Backend](#how-to-run-the-backend-)
4. [API Documentation](#api-documentation)

---

### Prequisites :

- [Poetry](https://python-poetry.org/docs/#installation)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/)
- [Supabase CLI](https://supabase.com/docs/guides/cli) (only for applying migrations to the hosted project)

### Database

The API talks to the **hosted** Supabase Postgres project only. Copy `.env.example` to `.env` and fill in
the hosted pooler connection string:

```
DATABASE_URI=postgresql://postgres.<project-ref>:<url-encoded-password>@aws-0-<region>.pooler.supabase.com:5432/postgres
```

The app refuses to start when `DATABASE_URI` is missing and rejects any host that is not a hosted
Supabase domain, so `localhost` / `127.0.0.1` (local Supabase stack) and local SQLite files are never
used for the API.

Apply schema changes and seed data to the hosted project with the CLI in linked mode:

```
supabase link --project-ref <project-ref>
supabase db push --linked
```

Do not run `supabase start`; the local stack is not part of this workflow.

### How to run the Backend :

1. Setup Redis

   ```
   sudo service redis-server start
   redis-cli
   ```

   And this is to test if the redis already run

   ```
   ping
   > PONG
   ```

2. Setup Poetry

   ```
   poetry shell
   ```

3. Run the Flask App
   ```
   run flask
   ```
   If you wish to use debug version you can use this script instead
   ```
   run flask --debug
   ```

### API Documentation

To get API documentation you can use our Postman documentation

[HealtHub API docs](https://documenter.getpostman.com/view/10125656/2sA3JM82Tt)

Or you can use swagger for more flexibility. Copy this URL into your browser once the Flask App already run

    http://localhost:5000/swagger

.
