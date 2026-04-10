# Will Borrelli Teiko Technical 

## Instructions
The Makefile has several options:
- setup: install the necessary requirements from requirements.txt
- pipeline: run the full analysis pipeline
    - creates: 
        - boxplots.png: box and whisker plots for cell type frequency statistics
        - bar_charts.png: bar charts of subject counts
        - results.txt: grid formatted summary statistics table for each sample and p-value statistics for cell type frequencies
    - additionally, the box plots bar charts will be printed to the screen
- dashboard: starts the interactive web dashboard (http://localhost:8501)
- clean: cleans up created files

## Data Schema
The data schema used has the following form:
(project TEXT, subject TEXT, condition TEXT, age INTEGER, sex TEXT, treatment TEXT, response TEXT, sample TEXT, sample_type TEXT, time_from_treatment_start INTEGER, b_cell INTEGER, cd8_t_cell INTEGER, cd4_t_cell INTEGER, nk_cell INTEGER, monocyte INTEGER)
This schema loads the necessary fields in a very straightforward way. Given that sample statistics 

