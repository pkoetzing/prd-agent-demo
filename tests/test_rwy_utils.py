import os

import numpy as np
import pandas as pd

from rwy_finder import rwy_utils


def test_load_weather_data():
    path = os.path.join('data', 'weather_history.parquet')
    df = rwy_utils.load_weather_data(path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_load_weights():
    path = os.path.join('data', 'weather_metric_weights.csv')
    df = rwy_utils.load_weights(path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_compute_features():
    df = pd.DataFrame(np.random.rand(9000, 3), columns=['a', 'b', 'c'])
    features = rwy_utils.compute_features(df)
    assert features.shape[0] == (9000 - 8760) // 24 + 1


def test_standardize_features():
    features = pd.DataFrame(np.random.rand(10, 6))
    std = rwy_utils.standardize_features(features)
    np.testing.assert_allclose(std.mean(), 0, atol=1)


def test_apply_weights():
    features = pd.DataFrame(np.random.rand(5, 3), columns=['a', 'b', 'c'])
    weights = pd.DataFrame({'a': [1], 'b': [2], 'c': [3]})
    weighted = rwy_utils.apply_weights(features, weights)
    assert weighted.shape == features.shape


def test_perform_pca():
    features = pd.DataFrame(np.random.rand(20, 5))
    result = rwy_utils.perform_pca(features)
    assert 'X_pca' in result
    assert result['X_pca'].shape[0] == 20


def test_compute_distances():
    features = pd.DataFrame(np.random.rand(20, 5))
    pca_result = rwy_utils.perform_pca(features)
    distances = rwy_utils.compute_distances(pca_result)
    assert set(
        ['euclidean', 'mahalanobis', 'cosine']
        ).issubset(distances.columns)
