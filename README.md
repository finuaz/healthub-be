# HealtHub

HealtHub : Where Heathy and Tasty Meet

> This is the document for Back End repository of HealtHub

## Table of Contents

1. [Prequisites](#prequisites-)
2. [How to run the Backend](#how-to-run-the-backend-)
3. [API Documentation](#api-documentation)

---

### Prequisites :

- [Poetry](https://python-poetry.org/docs/#installation)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/installation/)
- [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/)

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
