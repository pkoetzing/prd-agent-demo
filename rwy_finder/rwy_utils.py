from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from factor_analyzer import Rotator
from sklearn.decomposition import PCA


def load_weather_data(path: str) -> pd.DataFrame:
    """Load weather data from a Parquet file."""
    return pd.read_parquet(path)


def load_weights(path: str) -> pd.DataFrame:
    """Load metric weights from a CSV file."""
    return pd.read_csv(path, index_col=0)


def compute_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute mean and std for each 8760-hour window."""
    window_size = 8760
    step = 24
    features = []
    starts = []
    for start in range(0, len(df) - window_size + 1, step):
        window = df.iloc[start:start + window_size]
        mu = window.mean()
        sigma = window.std()
        mu.index = [f'{col}_mean' for col in mu.index]
        sigma.index = [f'{col}_std' for col in sigma.index]
        feat = pd.concat([mu, sigma])
        features.append(feat)
        starts.append(df.index[start])
    features_df = pd.DataFrame(features, index=starts)
    return features_df


def standardize_features(features: pd.DataFrame) -> pd.DataFrame:
    """Z-score standardization across all windows."""
    return (features - features.mean()) / features.std()


def apply_weights(
        features: pd.DataFrame,
        weights: pd.DataFrame
        ) -> pd.DataFrame:
    """Apply technology weights to features."""
    weighted = features.copy()
    for col in features.columns:
        tech = col.split('_')[0]
        if tech in weights.columns:
            weighted[col] = features[col] * weights[tech].values[0]
    return weighted


def perform_pca(features: pd.DataFrame) -> dict[str, Any]:
    """Perform PCA, retain PCs explaining >=95% variance."""
    pca = PCA()
    X = features.values
    pca.fit(X)
    explained = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.searchsorted(explained, 0.95) + 1
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    # Add loadings to the PCA result
    feature_names = [
        col.replace('load_factor_', '') for col in features.columns]
    loadings = pd.DataFrame(
       pca.components_.T,  # shape e.g. 24 rows 6 columns
       index=feature_names,
       columns=[f"PC{i + 1}" for i in range(n_components)])
    # Turn raw loadings into interpretable contributions
    contrib = (loadings ** 2)
    contrib = contrib.div(contrib.sum(axis=0), axis=1) * 100
    # Give each PC a one-line human label
    labels = []
    for pc in contrib.columns:
        top = contrib[pc].nlargest(3)
        desc = " + ".join(
            [f"{name} ({pct:.0f}%)" for name, pct in top.items()])
        labels.append(f"{pc}: {desc}")

    # Apply a Varimax rotation for even cleaner interpretation
    rot = Rotator(method="varimax")
    load_rot = pd.DataFrame(
        rot.fit_transform(loadings.values),
        index=feature_names,
        columns=[f"RPC{i + 1}" for i in range(n_components)])
    contrib_rot = (load_rot**2)
    contrib_rot = contrib_rot.div(contrib_rot.sum(axis=0), axis=1) * 100

    labels_rot = []
    for pc in contrib_rot.columns:
        top = contrib_rot[pc].nlargest(3)
        desc = " + ".join(
            [f"{name} ({pct:.0f}%)" for name, pct in top.items()])
        labels_rot.append(f"{pc}: {desc}")

    return {
        'pca': pca,
        'X_pca': X_pca,
        'explained_variance': pca.explained_variance_ratio_,
        'components': pca.components_,
        'mean': X_pca.mean(axis=0),
        'window_idx': features.index,
        'loadings': loadings,
        'labels': labels_rot,
        'loadings_rot': load_rot,
        'contrib_rot': contrib_rot
    }


def compute_distances(pca_result: dict[str, Any]) -> pd.DataFrame:
    """Compute Euclidean, Mahalanobis, and cosine distances in PC space."""
    X = pca_result['X_pca']
    mean = pca_result['mean']
    euclid = np.linalg.norm(X - mean, axis=1)
    lambdas = pca_result['pca'].explained_variance_
    maha = np.sqrt(((X ** 2) / lambdas).sum(axis=1))
    dot = (X * mean).sum(axis=1)
    norm_x = np.linalg.norm(X, axis=1)
    norm_mean = np.linalg.norm(mean)
    cosine = 1 - (dot / (norm_x * norm_mean))
    return pd.DataFrame({
        'euclidean': euclid,
        'mahalanobis': maha,
        'cosine': cosine
    }, index=pca_result['window_idx'])


def plot_pca_explained_variance(pca_result, output_path):
    """Plot explained variance waterfall and cumulative line for PCA.
    Show top 3 features per PC in a textbox.
    """
    explained = pca_result['explained_variance']
    loadings = pca_result['loadings']
    pcs = [f'PC{i + 1}' for i in range(len(explained))]
    _fig, ax = plt.subplots(figsize=(7, 5))
    prev = 0
    for i, val in enumerate(explained):
        ax.bar(i, val * 100, bottom=prev, color='C0')
        prev += val * 100
    # Add cumulative numbers as percentage
    cumvals = np.cumsum(explained) * 100
    for x, y in zip(range(len(explained)), cumvals, strict=False):
        ax.text(x, y, f'{y:.1f}%', va='bottom', ha='center', fontsize=8)
    ax.set_xticks(range(len(pcs)))
    ax.set_xticklabels(pcs)
    ax.set_ylabel('Explained Variance (%)')
    ax.set_title('PCA Waterfall Chart')
    ax.grid(axis='y')
    plt.xlabel('Principal Components')
    label_lines = []
    for pc in loadings.columns:
        top3 = loadings[pc].abs().nlargest(3)
        label = f"{pc}: " + ", ".join([f"{name}" for name in top3.index])
        label_lines.append(label)
    textstr = "\n".join(label_lines)
    ax.text(
        0.95, 0.05, textstr,
        transform=ax.transAxes,
        fontsize=9,
        va='bottom', ha='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=0.5)
    )
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def export_outputs(
        weather_df: pd.DataFrame,
        features: pd.DataFrame,
        features_weighted: pd.DataFrame,
        pca_result: dict[str, Any],
        distances: pd.DataFrame,
        data_path: str,
        output_dir: str
        ) -> None:
    """Export all required artefacts to output_dir."""
    output_path = Path(output_dir)
    window_starts = list(features.index)
    features_weighted.to_parquet(output_path / 'features.parquet')
    pd.DataFrame(pca_result['components']).to_parquet(
        output_path / 'pca_components.parquet')

    # Explained variance plot with waterfall diagram
    plot_pca_explained_variance(
        pca_result,
        output_path / 'pca_explained_variance.png')

    # Print the labels to a markdown file
    with (output_path / 'pca_loadings.md').open('w') as f:
        for label in pca_result['labels']:
            f.write(f"{label}\n")

    distances.to_parquet(output_path / 'distance_series.parquet')
    candidates_df = _make_candidates_df(distances)
    candidates_df.to_parquet(output_path / 'rwy_candidates.parquet')
    plot_rwy_candidates_euclidean(
        candidates_df, output_path / 'rwy_candidates.png')

    # Write top10 markdowns for full and recent decade
    top10_full_md = _make_top10_md(distances)
    with (output_path / 'rwy_top10_full.md').open('w') as f:
        f.write(top10_full_md)
    recent_start = pd.Timestamp('2013-01-01 00:00:00')
    mask = [s >= recent_start for s in window_starts]
    if any(mask):
        distances_recent = distances[mask]
        top10_recent_md = _make_top10_md(distances_recent)
        with (output_path / 'rwy_top10_recent.md').open('w') as f:
            f.write(top10_recent_md)
    _export_best_windows(weather_df, window_starts, distances, output_dir)

    # Plot Sankey diagram for rotated loadings
    plot_sankey_rotated_loadings(
        pca_result['contrib_rot'],
        output_path / 'pca_sankey.html'
    )


def _make_candidates_df(distances: pd.DataFrame) -> pd.DataFrame:
    """Create DataFrame for all candidates by adding an 'End' column.
    Rename the index to 'Start' and capitalize the column names.
    """
    df = distances.copy()
    df.insert(0, 'End', (df.index + pd.Timedelta(hours=8759)).date)
    df = df.rename(columns={
        'euclidean': 'Euclidean',
        'mahalanobis': 'Mahalanobis',
        'cosine': 'Cosine'
        })
    df.index.name = 'Start'
    return df


def plot_rwy_candidates_euclidean(df_candidates, output_path):
    # Use the columns as produced by _make_candidates_df
    DATE_MARKS = {
        '2013-10-01': 'Legacy',
        '2017-07-01': 'Initial',
        '1981-09-05': 'Full Horizon',
        '2013-09-18': 'Last Decade'
        }
    plt.figure(figsize=(10, 4))
    plt.plot(df_candidates.index, df_candidates['Euclidean'], linestyle='-')
    # Add red markers for each date in DATE_MARKS
    for date_str, label in DATE_MARKS.items():
        date = pd.to_datetime(date_str)
        if date in df_candidates.index:
            y = df_candidates.loc[date, 'Euclidean']
            plt.plot(date, y, 'ro')
            plt.text(date, y, f' {label}', color='red', va='bottom')
    plt.xlabel('Window Start Date')
    plt.ylabel('Euclidean Distance')
    plt.title('RWY Candidates: Euclidean Distance vs. Start Date')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def _make_top10_md(distances: pd.DataFrame) -> str:
    """Create markdown table for top 10 windows."""
    top10 = distances.nsmallest(10, 'euclidean')
    lines = [
        '| Rank | Start | End | Euclidean | Mahalanobis | Cosine |',
        '|---|---|---|---|---|---|'
    ]
    for rank, row in enumerate(top10.itertuples(index=True), 1):
        start = row.Index.date()
        end = (row.Index + pd.Timedelta(hours=8759)).date()
        lines.append(
            f'| {rank} | {start} | {end} | {row.euclidean:.3f} | '
            f'{row.mahalanobis:.3f} | {row.cosine:.3f} |'
        )
    return '\n'.join(lines)


def _export_best_windows(
        weather_df: pd.DataFrame,
        window_starts: list[pd.Timestamp],
        distances: pd.DataFrame,
        output_dir: str
        ) -> None:
    """
    Export best full and recent decade windows as Parquet, reordered to
    start Jan 1.
    """
    output_path = Path(output_dir)
    idx_best = distances['euclidean'].idxmin()
    # Convert idx_best (Timestamp) to integer position
    pos_best = weather_df.index.get_loc(idx_best)
    best_window = weather_df.iloc[pos_best:pos_best + 8760].copy()
    best_window = _rotate_to_jan1(best_window)
    best_window.to_parquet(
        output_path / 'rwy_best_full.parquet', index=True)
    recent_start = pd.Timestamp('2013-01-01 00:00:00')
    mask = [s >= recent_start for s in window_starts]
    if any(mask):
        idx_recent = distances[mask]['euclidean'].idxmin()
        # Convert idx_recent (Timestamp) to integer position
        pos_recent = weather_df.index.get_loc(idx_recent)
        best_recent = weather_df.iloc[pos_recent:pos_recent + 8760].copy()
        best_recent = _rotate_to_jan1(best_recent)
        best_recent.to_parquet(
            output_path / 'rwy_best_recent.parquet', index=True)


def _rotate_to_jan1(df: pd.DataFrame) -> pd.DataFrame:
    """Rotate DataFrame so it starts on Jan 1 00:00."""
    idx_jan1 = df.index.get_loc(df.index[df.index.month == 1][0])
    return pd.concat([df.iloc[idx_jan1:], df.iloc[:idx_jan1]])


def plot_sankey_rotated_loadings(contrib_rot: pd.DataFrame, output_path):
    """
    Plot a Sankey diagram from the Varimax-rotated squared-loading matrix.
    Only show links with ≥2% contribution.
    """
    sources = []
    targets = []
    values = []
    feature_names = list(contrib_rot.index)
    pc_names = list(contrib_rot.columns)
    node_labels = feature_names + pc_names

    for i, _feat in enumerate(feature_names):
        for j, _pc in enumerate(pc_names):
            val = contrib_rot.iloc[i, j]
            if val >= 2:
                sources.append(i)
                targets.append(len(feature_names) + j)
                values.append(val)

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=node_labels
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    ))
    fig.update_layout(
        title_text="Sankey Diagram of Varimax-Rotated Feature Contributions",
        font_size=10
    )
    fig.write_html(str(output_path))
