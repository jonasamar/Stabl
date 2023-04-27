from StrokePipeline import stroke_pipeline
                    
for cellpop in ['CD41hiCD61hiPLT', 'CD4Tcm',
                    'CD4Tem', 'CD4Tnaive', 'CD4Trm', 'CD56brightCD16nNKcells']:
    stroke_pipeline('P2', cellpop)
        