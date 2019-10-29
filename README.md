# TP project

Social network prototype based on [Django](https://docs.djangoproject.com/) class based views. Realized: custom user model with "friends" features, extendable blog system with "bookmarks" features. "Messages" features based on [Django Channels](https://channels.readthedocs.io/en/latest/) and easy extendable to multi-users chats.


# How to run with Docker

1. Clone the repository

```bash
git clone https://github.com/olegush/37_transcendence_1.git
cd 37_transcendence_1
```

2. Rename .env.dev to .env

3. Build image and run containers, attached to services.
```bash
docker-compose up -d --build
```

4. Go to http://127.0.0.1:8000/ with superuser access superuser@superuser.com/pwd12345
