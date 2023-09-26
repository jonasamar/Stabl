import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_selection import SelectorMixin
from sklearn.utils.validation import check_is_fitted


def remove_low_info_samples(X, threshold=1.0):
    """Removes low info samples

    A sample is considered to have sufficient info if the nan fraction is below the
    input hard_threshold.
    
    Parameters
    ----------
    X : {array-like, sparse matrix}, or DataFrame, shape (n_repeats, n_features)
        Data from which to compute NaN proportion, where `n_repeats` is
        the number of samples and `n_features` is the number of features.

    threshold : float, default=1.0
        Samples with a proportion of NaN greater than this value will be removed.
    
    Returns
    -------
    X_reduced : array, shape(n_samples_out, n_features)
        The reduced array of siwe n_samples_out, n_features
    """
    if not isinstance(threshold, float) or (threshold < 0. or threshold > 1.):
        raise ValueError(f"Nan fraction must be between 0 and 1 Got: {threshold}")

    if isinstance(X, pd.DataFrame):
        nan_fraction = X.isnull().sum() / X.shape[0]
        mask = nan_fraction < threshold
        return X.loc[:, mask]
    elif isinstance(X, np.array):
        nan_fraction = np.isnan(X).sum(1) / X.shape[1]
        mask = nan_fraction < threshold
        return X[mask]
    
class Winsorizer(BaseEstimator, TransformerMixin):
    """
    Winsorizer: A feature preprocessing technique that performs winsorization on the input features (X).

    Winsorization is used to handle extreme values (outliers) in each feature column by capping them
    at specified percentiles, thereby minimizing the impact of outliers without removing them entirely.
    This technique is suitable for unsupervised learning tasks, where the focus is on feature transformation
    without considering the output labels (y).

    Parameters
    ----------
    winsor_percentile : float, default=5
        Features with extreme values beyond this percentile will be capped during winsorization.
        The extreme values will be replaced with the values at this percentile.

    Attributes
    ----------
    winsor_low_ : dict
        A dictionary that stores the winsor low values for each individual feature.
        The winsor low value is the threshold below which extreme values in the feature will be capped during winsorization.

    winsor_high_ : dict
        A dictionary that stores the winsor high values for each individual feature.
        The winsor high value is the threshold above which extreme values in the feature will be capped during winsorization.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during the fit. Defined only when X has feature names that are all strings.

    Example Usage
    -------------
    # Instantiate the Winsorizer with a winsorization percentile of 5
    winsorizer = Winsorizer(winsor_percentile=5)

    # Fit and transform the Winsorizer to the training data
    X_train_winsorized = winsorizer.fit_transform(X_train)

    # Apply the same Winsorizer to the testing data
    X_test_winsorized = winsorizer.transform(X_test)
    """
    
    def __init__(self, winsor_percentile=5):
        self.winsor_percentile = winsor_percentile
        self.winsor_low_ = None
        self.winsor_high_ = None

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            X_data = X
            self.feature_names_in_ = X.columns
        else:
            X_data = pd.DataFrame(X)
            self.feature_names_in_ = None

        self.winsor_low_ = {}
        self.winsor_high_ = {}
        for col in X_data.columns:
            winsor_low = np.percentile(X_data[col], self.winsor_percentile)
            winsor_high = np.percentile(X_data[col], 100 - self.winsor_percentile)
            self.winsor_low_[col] = winsor_low
            self.winsor_high_[col] = winsor_high

        self.n_features_in_ = X_data.shape[1]
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            X_data = X.copy()
        else:
            X_data = pd.DataFrame(X)

        for col in X_data.columns:
            X_data[col] = np.clip(X_data[col], self.winsor_low_[col], self.winsor_high_[col])

        return X_data.values if self.feature_names_in_ is None else X_data

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)


class LowInfoFilter(SelectorMixin, BaseEstimator):
    """Feature selector that removes all low-variance features.

    This feature selection algorithm looks only at the features (X), not the
    desired outputs (y), and can thus be used for unsupervised learning.

    A feature is considered to be a low info one if the proportion of nan
    values is above a given hard_threshold set by the user.

    Parameters
    ----------
    max_nan_fraction : float, default=0.2
        Features with a proportion of nan values greater than this hard_threshold will
        be removed. By default, the proportion is set to 0.2.

    Attributes
    ----------
    nan_counts_ : array, shape (n_features,)
        Count of nan values for each individual feature.

    n_features_in_ : int
        Number of features seen during fit.

    feature_names_in_ : ndarray of shape (n_features_in_,)
        Names of features seen during the fit. Defined only when X
        has feature names that are all strings.

    Notes
    -----
    Allows NaN in the input.
    Raises ValueError if no feature in X meets the low info hard_threshold.
    """

    def __init__(self, max_nan_fraction=0.2):
        self.max_nan_fraction = max_nan_fraction
        self.n_samples = None
        self.nan_counts_ = None

    def fit(self, X, y=None):
        """Learn empirical Nan proportion in X.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape (n_repeats, n_features)
            Data from which to compute NaN proportion, where `n_repeats` is
            the number of samples and `n_features` is the number of features.

        y : any, default=None
            Ignored. This parameter exists only for compatibility with
            sklearn.pipeline.Pipeline.

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        X = self._validate_data(
            X,
            accept_sparse=("csr", "csc"),
            dtype=np.float64,
            force_all_finite="allow-nan",
        )

        if self.max_nan_fraction > 1 or self.max_nan_fraction < 0:
            raise ValueError(
                f"Nan fraction must be between 0 and 1 Got: {self.max_nan_fraction}")

        n_samples = X.shape[0]
        self.n_samples = n_samples
        self.nan_counts_ = np.isnan(np.array(X)).sum(0)

        if np.all(~np.isfinite(self.nan_counts_) | (
                self.nan_counts_ > self.max_nan_fraction * self.n_samples)):
            msg = "No feature in X meets the low info hard_threshold {0:.5f}"
            if n_samples == 1:
                msg += " (X contains only one sample)"
            raise ValueError(msg.format(self.max_nan_fraction))

        return self

    def _get_support_mask(self):
        """Get a mask, or integer index, of the features selected
            
        Returns
        -------
        support : array
            An index that selects the retained features from a feature vector.
            This is a boolean array of shape
            [# input features], in which an element is True iff its
            corresponding feature is selected for retention. 
        """
        check_is_fitted(self)

        return self.nan_counts_ <= self.max_nan_fraction * self.n_samples

    def _more_tags(self):
        # Useful to allow the use of nan values
        # For the transform function ;)
        return {"allow_nan": True}
