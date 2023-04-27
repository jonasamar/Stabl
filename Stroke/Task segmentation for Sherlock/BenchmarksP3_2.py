from StrokePipeline import stroke_pipeline
                    
for cellpop in ['CD56dimCD16pNKcells', 'CD61pCD41pPLT', 'CD62LnAgedNeutrophils',
                    'CD62LpImmatureNeutrophils', 'CD8Tcm', 'CD8Tem']:
    stroke_pipeline('P3', cellpop)
        