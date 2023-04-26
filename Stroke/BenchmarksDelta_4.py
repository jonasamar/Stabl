from StrokePipeline import stroke_pipeline

# NKT          
for cellpop in ['pDC',
                    'Th1mem', 'Th1naive', 'Tregmem', 'Tregnaive']:
    stroke_pipeline('Delta', cellpop)
        