#!/bin/bash

# Set env vars
KATECHEO_NER=$(python deploy.py ner)
KATECHEO_KB=$(python deploy.py kb)

# Substitute the values in the deployment files
cp deployment.template.json deployment.json
sed -i '' -e 's/NERSUB/'"$KATECHEO_NER"'/g' deployment.json && sed -i '' -e 's/KBSUB/'"$KATECHEO_KB"'/g' deployment.json

# deploy model servers
# kubectl apply -f deployment.json
