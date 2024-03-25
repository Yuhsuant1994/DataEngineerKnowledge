refering to Krish Naik example training video

https://www.youtube.com/watch?v=i_FtfdOKa2M&ab_channel=KrishNaik

# run locally 

`bentoml serve service.py:svc --reload`

# dockerize
$bentoml build
$bentoml list


Successfully built Bento(tag="iris_classifier:zmqsxlhgs2k3duud").

Next steps:

* Deploy to BentoCloud:
    $ bentoml deploy iris_classifier:zmqsxlhgs2k3duud -n ${DEPLOYMENT_NAME}

* Update an existing deployment on BentoCloud:
    $ bentoml deployment update --bento iris_classifier:zmqsxlhgs2k3duud ${DEPLOYMENT_NAME}

* Containerize your Bento with `bentoml containerize`:
    $ bentoml containerize iris_classifier:zmqsxlhgs2k3duud [or bentoml build --containerize]


# run docker locally

```
docker run -d \
  --network=bridge \
  --name bento-demo \
  -p 8080:3000 \
  -v
  iris_classifier:zmqsxlhgs2k3duud
```

## how to run on GCP cloud run

* `docker tag iris_classifier:zmqsxlhgs2k3duud gcr.io/[PROJECT-ID]/iris_classifier:zmqsxlhgs2k3duud` tag the image locally
* `docker push gcr.io/YOUR_PROJECT_ID/iris_classifier:zmqsxlhgs2k3duud` saved image to GCP: Google Container Registry (GCR)
* deploy on cloud run
    ```
    gcloud run deploy bento-demo \
    --image gcr.io/[PROJECT-ID]/iris_classifier:zmqsxlhgs2k3duud \
    --platform managed \
    --region [REGION] \
    --port 3000 \
    --allow-unauthenticated
    ``` 

# find blocking port  lsof -i :3000
