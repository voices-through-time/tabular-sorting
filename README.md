# tabular-sorting
Script to sort out aggregated texts with high and low volumes of consensus

Create a config using the ‘workflows.csv’ file, with the appropriate workflow name.
(This will create an extractor file)

eg: `panoptes_aggregation config workflows-08-02-2021.csv 17009 -v 406`

Extract the transcriptions using the ‘classifications.csv’ file, and the relevant extractor .yaml file

eg: `panoptes_aggregation extract vtt-c-28-03-21.csv Extractor_config_workflow_17717_V114.240.yaml`

Reduce the extracted transcriptions, with the generated file, and the reducer config YAML file.

`panoptes_aggregation reduce text_extractor_feb-08.csv Reducer_config_workflow_17009_V405.565_text_extractor.yaml -o feb-08`

THEN run your own script, on the ‘text_reducer_text’ to get all the individual files

`python separate.py text_extractor_feb-08`

This will separate the extracted text, and place them in a 'transcribed' folder, separated into folders according to how high the consensus was.
