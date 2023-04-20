import warnings
warnings.filterwarnings('ignore')

# Libaries

from sklearn.linear_model import Lasso, ElasticNet
from sklearn.base import clone

from stabl.synthetic_utils import synthetic_benchmark_regression
# Base models

lasso = Lasso(max_iter=int(1e6))
# Hyperparameters
base_estimator = clone(lasso)
lambda_name = 'alpha'
n_informative_list = [10, 25, 50] # Number of artificial f
n_features_list = [1000] 
#n_features_list = [100, 500, 1000, 2500, 5000, 7500, 10000]
n_samples_list = [30, 40, 50, 75, 100, 150, 250, 350, 500, 750, 1000]
artificial_type = "random_permutation"
n_experiments = 50
result_folder_title = "test synthetic"
synthetic_benchmark_regression(
    base_estimator=base_estimator,
    lambda_name=lambda_name,
    n_features_list=n_features_list,
    n_informative_list=n_informative_list,
    n_samples_list=n_samples_list,
    n_experiments=n_experiments,
    artificial_type=artificial_type,
    result_folder_title=result_folder_title
)