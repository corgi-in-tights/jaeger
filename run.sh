docker build -t my-redis-image .
docker run -d --name my-redis-container -p 6379:6379 my-redis-image

pipenv run python3 src/manage.py