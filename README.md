Required commands:

    docker run --name my-redis -p 6379:6379 -d redis

(for part 2:)

    docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management