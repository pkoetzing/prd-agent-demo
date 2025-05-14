import logging
import os

import rwy_finder.rwy_utils as utils


def run_rwy_pipeline(data_path: str, output_dir: str) -> None:
    """Run the full RWY pipeline from data loading to output export."""
    logging.info('Loading weather data...')
    weather_df = utils.load_weather_data(
        os.path.join(data_path, 'weather_history.parquet'))
    weights_df = utils.load_weights(
        os.path.join(data_path, 'weather_metric_weights.csv'))
    logging.info('Computing features...')
    features = utils.compute_features(weather_df)
    logging.info('Standardizing features...')
    features_std = utils.standardize_features(features)
    logging.info('Applying weights...')
    features_weighted = utils.apply_weights(features_std, weights_df)
    logging.info('Performing PCA...')
    pca_result = utils.perform_pca(features_weighted)
    logging.info('Computing distances...')
    distances = utils.compute_distances(pca_result)
    logging.info('Exporting outputs...')
    utils.export_outputs(
        weather_df, features, features_weighted, pca_result, distances,
        data_path, output_dir
    )
    logging.info('Pipeline complete.')
