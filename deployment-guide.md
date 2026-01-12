1. Test django

```
python manage.py test
```

2. Build container

```
docker build -f Dockerfile \
  -t registry.digitalocean.com/django-crm/crm:latest 
  -t registry.digitalocean.com/django-crm/crm:v1 
```

3. Push Container with 2 tags: latest and random

```
docker push registry.digitalocean.com/django-crm/crm --all-tags
```

4. Update secrets (if needed)

```
kubectl delete secret django-crm-prod-env
kubectl create secret generic django-crm-prod-env --from-env-file=crm/.env.prod

```

5. Update Deployment `k8s/apps/crm.yaml`:

kubectl apply -f k8s/apps/crm.yaml

Add in a rollout strategy:
`imagePullPolicy: Always`


### Four ways (given above) to trigger a deployment rollout (aka update the running pods):
- Forced rollout
Given a `imagePullPolicy: Always`, on your containers you can:

```
kubectl rollout restart deployment/django-k8s-web-deployment
```

- Image update:
```
kubectl set image deployment/django-k8s-web-deployment django-k8s-web=registry.digitalocean.com/cfe-k8s/django-k8s-web:latest
```

- Update an Environment Variable (within Deployment yaml):

```
env:
  - name: Version
    value: "abc123"
  - name: PORT
    value: "8002"
```

- Deployment yaml file update:

Change 
```
image: registry.digitalocean.com/cfe-k8s/django-k8s-web:latest
```
to
```
image: registry.digitalocean.com/cfe-k8s/django-k8s-web:v1 
```
Keep in mind you'll need to change `latest` to any new tag(s) you might have (not just `v1`)
```
kubectl apply -f k8s/apps/django-k8s-web.yaml
```


6. Roll Update:
```
kubectl rollout status deployment/crm-deployment
```
7. Migrate database

Get a single pod (either method works)

```
export SINGLE_POD_NAME=$(kubectl get pod -l app=crm-deployment -o jsonpath="{.items[0].metadata.name}")
```
or 
```
export SINGLE_POD_NAME=$(kubectl get pod -l=app=crm-deployment -o NAME | tail -n 1)
```

Then run `migrate.sh` 

```
kubectl exec -it $SINGLE_POD_NAME -- bash /app/migrate.sh
```