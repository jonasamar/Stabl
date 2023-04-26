from StrokePipeline import stroke_pipeline
                    
for cellpop in ['NKT', 'pDC',
                    'Th1mem', 'Th1naive', 'Tregmem', 'Tregnaive']:
    stroke_pipeline('P1', cellpop)
        