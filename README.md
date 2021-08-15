# Day Trading Journaling Platform for Developers

This is a Djano-based platform with a frontend based on the Open-source **[Django Template](https://www.creative-tim.com/templates/django)** crafted on top of **Argon Dashboard** and Bootstrap.

It exposes an API for users to submit their trades both historical and realtime and uses a MongoDB database to persist the data. Users can then analyze and monitor their strategies.

For realtime updates, the platform maintains a websocket connection with the frontend to update the plots automatically using Redis.
