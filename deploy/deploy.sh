#!/bin/bash

# Set env vars
KATECHEO_KB=$(python deploy.py kb)
ARTICLE_ID=$(python deploy.py article_id)
ARTICLE_TITLE_KEY=$(python deploy.py article_title_key)
ARTICLE_BODY_KEY=$(python deploy.py article_body_key)
COSINE_SIMILARITY_THRESHOLD=$(python deploy.py similarity_threshold)
KATECHEO_COMP_MODEL=$(python deploy.py comprehension_model)

# Substitute the values in the deployment files
cp deployment.template.json deployment.json
sed -i '' -e 's/KBSUB/'"$KATECHEO_KB"'/g' deployment.json
sed -i '' -e 's/IDSUB/'"$ARTICLE_ID"'/g' deployment.json
sed -i '' -e 's/TITLESUB/'"$ARTICLE_TITLE_KEY"'/g' deployment.json
sed -i '' -e 's/BODYSUB/'"$ARTICLE_BODY_KEY"'/g' deployment.json
sed -i '' -e 's/THRESHOLDSUB/'"$COSINE_SIMILARITY_THRESHOLD"'/g' deployment.json
sed -i '' -e 's/MODELSUB/'"$KATECHEO_COMP_MODEL"'/g' deployment.json

# deploy model servers
kubectl apply -f deployment.json
