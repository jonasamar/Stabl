from StrokePipeline import stroke_pipeline

# error : 'CD41hiCD61hiPLT', (no values...)
                    
for cellpop in [ 'CD4Tcm',
                    'CD4Tem', 'CD4Tnaive', 'CD4Trm', 'CD56brightCD16nNKcells']:
    stroke_pipeline('P3', cellpop)
        