import redis

# Connect to Redis running inside Docker
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)
