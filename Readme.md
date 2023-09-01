## Getting Started
First prepare work env :

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


second, run the development server:

```bash
python app.py
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.

## Deployment
cf create-app product_life_backend --app-type docker        
cf create-app-manifest product_life_backend -p manifest.yaml
docker build . -t product_life_backend
docker tag product_life_backend khaledhadjali/product_life_backend:latest
docker push khaledhadjali/product_life_backend:latest
cf push product_life_backend -o khaledhadjali/product_life_backend:latest