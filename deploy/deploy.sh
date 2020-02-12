#!/bin/bash

# Set env vars
KATECHEO_KB=$(python deploy.py kb)
KATECHEO_ARTICLE_ID=$(python deploy.py article_id)
KATECHEO_ARTICLE_TITLE_KEY=$(python deploy.py article_title_key)
KATECHEO_ARTICLE_BODY_KEY=$(python deploy.py article_body_key)
KATECHEO_SIMILARITY_THRESHOLD=$(python deploy.py article_similarity_threshold)
KATECHEO_COMP_MODEL=$(python deploy.py comprehension_model)

# Substitute the values in the deployment files
cp deployment.template.json deployment.json
sed -i '' -e 's/KATECHEO_KB_SUB/'"$KATECHEO_KB"'/g' deployment.json
sed -i '' -e 's/KATECHEO_ARTICLE_ID_SUB/'"$KATECHEO_ARTICLE_ID"'/g' deployment.json
sed -i '' -e 's/KATECHEO_ARTICLE_TITLE_SUB/'"$KATECHEO_ARTICLE_TITLE_KEY"'/g' deployment.json
sed -i '' -e 's/KATECHEO_ARTICLE_BODY_SUB/'"$KATECHEO_ARTICLE_BODY_KEY"'/g' deployment.json
sed -i '' -e 's/KATECHEO_SIMILARITY_THRESHOLD_SUB/'"$KATECHEO_SIMILARITY_THRESHOLD"'/g' deployment.json
sed -i '' -e 's/KATECHEO_COMP_MODEL_SUB/'"$KATECHEO_COMP_MODEL"'/g' deployment.json

# deploy model servers
kubectl apply -f deployment.json
