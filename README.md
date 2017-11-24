# Webhook to save messages and respond automatically

Docker compose create:
 * Flask app (on port 5000): Communicate with rapidpro like kannel channel and with the client gsm
 * Celery worker: Save messages to redis database
 * Flower interface:  Expose the queues and the workers
