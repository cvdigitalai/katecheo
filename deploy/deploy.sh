#!/bin/bash

# Set env vars
KATECHEO_NER=$(python deploy.py ner)
KATECHEO_KB=$(python deploy.py kb)

# Substitute the values in the deployment files
mkdir deployments
cp ../comprehension/deployment.json deployments/reading_comp.json
cp ../kb-search/deployment.json deployments/kb_search.json
cp ../question-detector/deployment.json deployments/question_detector.json
cp ../target-classifier/deployment.json deployments/target_classifier.json
sed -i -e 's/NERSUB/'"$KATECHEO_NER"'/g' deployments/target_classifier.json
sed -i -e 's/KBSUB/'"$KATECHEO_KB"'/g' deployments/kb_search.json

# clean up
#rm -rf deployments
