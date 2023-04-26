from StrokePipeline import stroke_pipeline
                    
for cellpop in ['CD8Tnaive',
                'CD8Trm', 'gdTcells', 'intMC', 'mDC', 'MDSC']:
    stroke_pipeline('P3', cellpop)
        