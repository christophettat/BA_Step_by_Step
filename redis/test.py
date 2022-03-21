import redis

redis = redis.Redis(
    host= 'localhost',
    port= '6379')

redis.set('mykey', 'Hello from Python!')
value = redis.get('mykey') 
print(value)

redis.zadd('vehicles', {'bike1' : 1})
redis.zadd('vehicles', {'bike2' : 3})
redis.zadd('vehicles', {'bike3' : 7})
redis.zadd('vehicles', {'bike4' : 5})
redis.zadd('vehicles', {'bike6' : 5})
print(redis.zrange('vehicles', 2, 4))
print(redis.zrange('vehicles', 0, -1))
print(redis.zcount('vehicles', 2, 4))
print(redis.zrangebyscore('vehicles', 2, 5))
redis.zrem('vehicles', redis.zrangebyscore('vehicles', 2, 5))
print(redis.zrangebyscore('vehicles', 2, 5))

