#!/bin/bash

# Set env vars
KATECHEO_KB=$(python deploy.py kb)
ARTICLE_ID=
ARTICLE_TITLE_KEY=
ARTICLE_BODY_KEY=
COSINE_SIMILARITY_THRESHOLD=

# Substitute the values in the deployment files
cp deployment.template.json deployment.json
sed -i '' -e 's/KBSUB/'"$KATECHEO_KB"'/g' deployment.json
sed -i '' -e 's/NERSUB/'"$ARTICLE_ID"'/g' deployment.json
sed -i '' -e 's/NERSUB/'"$ARTICLE_TITLE_KEY"'/g' deployment.json
sed -i '' -e 's/NERSUB/'"$ARTICLE_BODY_KEY"'/g' deployment.json
sed -i '' -e 's/NERSUB/'"$COSINE_SIMILARITY_THRESHOLD"'/g' deployment.json

# deploy model servers
kubectl apply -f deployment.json
