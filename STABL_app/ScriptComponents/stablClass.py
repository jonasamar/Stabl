#------------------------------------------------------------------------------------------------------------------------------
#
# Function : stabl_class
#
# Description :
#       - arguments : fpy (python file), parameters linked to the stabl model the user wants to build
#       - effect : Add lines of code to the python script so that the stabl model is initialized with the desired parameters.
#
#------------------------------------------------------------------------------------------------------------------------------

def stabl_class(fpy, l1_ratio, artificial_type, sample_fraction, replace, random_state):
    fpy.write("\n")
    fpy.write(f"logit_en = LogisticRegression(penalty='elasticnet', l1_ratio = {l1_ratio}, max_iter=int(1e6), solver='saga', class_weight='balanced')\n")
    fpy.write("\n")
    fpy.write(f"stabl = Stabl(base_estimator=clone(logit_en),\n\tlambda_name='C',\n\tlambda_grid=list(np.linspace(0.01, 1, 30)),\n\tn_bootstraps=1000,\n\tartificial_type='{artificial_type}',\n\tartificial_proportion=1.,\n\tsample_fraction={sample_fraction},\n\treplace={replace},\n\tfdr_threshold_range=list(np.arange(0., 1., .01)),\n\tsample_weight_bootstrap=None,\n\tbootstrap_threshold=1e-5,\n\tbackend_multi='threading',\n\tverbose=0,\n\tn_jobs=-1,\n\trandom_state={random_state})\n")
    fpy.write("\n")
    fpy.write("stability_selection = clone(stabl).set_params(artificial_type=None, hard_threshold=0.3)\n")