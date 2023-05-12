def preprocessing(fpy):
    fpy.write("\n")
    fpy.write("preprocessing = Pipeline(\n\tsteps=[\n\t\t('lif', LowInfoFilter(0.2)),\n\t\t('variance', VarianceThreshold(0.01)),\n\t\t('impute', SimpleImputer(strategy='median')),\n\t\t('std', StandardScaler())\n\t])\n")
    fpy.write("\n")
    fpy.write("X_STD = pd.DataFrame(\n\tdata=preprocessing.fit_transform(X),\n\tindex=X.index,\n\tcolumns=preprocessing.get_feature_names_out()\n)\n")
    