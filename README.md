### headphones-project-api-v2  
git clone https://github.com/sonya-sh/headphones-project-api-2.git
cd headphones-project-api-v2
docker-compose up --build
docker-compose exec backend python3 manage.py migrate --noinput
docker-compose exec backend python3 manage.py createsuperuser  

документация: /api/schema/swagger-ui/