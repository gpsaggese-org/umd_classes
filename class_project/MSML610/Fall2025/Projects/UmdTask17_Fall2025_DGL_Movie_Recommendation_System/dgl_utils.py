# dgl_utils.py
from typing import Tuple, Dict, Optional, List, Iterable
import os
import re
from collections import defaultdict

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import dgl
from dgl.nn import SAGEConv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from tqdm import tqdm


# =============================================================================
# Data loading & ID mapping
# =============================================================================

def load_movielens(
    ratings_path: str,
    movies_path: Optional[str] = None,
) -> Dict[str, pd.DataFrame]:
    """
    Load MovieLens CSVs (ratings required, movies optional).

    :param ratings_path: Path to ratings.csv (userId,movieId,rating,timestamp).
    :param movies_path: Optional path to movies.csv (movieId,title,genres).
    :return: dict with keys 'ratings' and optionally 'movies'.
    """
    ratings = pd.read_csv(ratings_path)
    out = {"ratings": ratings}
    if movies_path and os.path.exists(movies_path):
        movies = pd.read_csv(movies_path)
        out["movies"] = movies
    return out


def remap_ids(
    df: pd.DataFrame,
    user_col: str = "userId",
    item_col: str = "movieId",
) -> Tuple[pd.DataFrame, Dict[str, np.ndarray]]:
    """
    Remap raw user/movie ids to contiguous [0..U-1] and [0..M-1].

    :return: (df_with_u_v, {'user_map': np.ndarray, 'item_map': np.ndarray})
    """
    user_ids = df[user_col].unique()
    item_ids = df[item_col].unique()
    uid_map = {u: i for i, u in enumerate(user_ids)}
    iid_map = {m: i for i, m in enumerate(item_ids)}
    df2 = df.copy()
    df2["u"] = df2[user_col].map(uid_map)
    df2["v"] = df2[item_col].map(iid_map)
    return df2, {"user_map": user_ids, "item_map": item_ids}


# =============================================================================
# Node features (genres) for movies
# =============================================================================

_GENRE_SPLIT = re.compile(r"[|]")


def build_movie_genre_onehot(
    movies_df: pd.DataFrame,
    item_map: np.ndarray,
) -> Tuple[torch.Tensor, List[str]]:
    """
    Build a movie-genre one-hot matrix aligned to contiguous movie indices.

    :param movies_df: movies.csv with columns (movieId,title,genres).
    :param item_map: np.ndarray where position i holds original movieId for index i.
    :return: (tensor shape [num_movies, num_genres], list of genre names in order)
    """
    # Build vocabulary.
    vocab = []
    seen = set()
    for g in movies_df["genres"].fillna("(no genres listed)"):
        for token in _GENRE_SPLIT.split(g):
            token = token.strip()
            if token and token not in seen:
                seen.add(token)
                vocab.append(token)
    vocab_index = {g: i for i, g in enumerate(vocab)}
    # One-hot per movie (aligned to contiguous index).
    num_movies = len(item_map)
    mat = np.zeros((num_movies, len(vocab)), dtype=np.float32)
    mid_to_row = {int(mid): i for i, mid in enumerate(item_map)}
    for _, row in movies_df.iterrows():
        mid = int(row["movieId"])
        if mid not in mid_to_row:
            continue
        r = mid_to_row[mid]
        for token in _GENRE_SPLIT.split(str(row.get("genres", ""))):
            token = token.strip()
            if token in vocab_index:
                mat[r, vocab_index[token]] = 1.0
    return torch.tensor(mat, dtype=torch.float32), vocab


# =============================================================================
# Graph building & edge splits
# =============================================================================

def build_bipartite_graph(
    df_edges: pd.DataFrame,
    num_users: int,
    num_items: int,
    rating_col: str = "rating",
) -> dgl.DGLHeteroGraph:
    """
    Build heterograph: user --rates--> movie (+ reverse), with edge features.
    """
    src = df_edges["u"].to_numpy()
    dst = df_edges["v"].to_numpy()
    g = dgl.heterograph(
        {
            ("user", "rates", "movie"): (src, dst),
            ("movie", "rated_by", "user"): (dst, src),
        },
        num_nodes_dict={"user": num_users, "movie": num_items},
    )
    g.edges["rates"].data["rating"] = torch.tensor(
        df_edges[rating_col].to_numpy(), dtype=torch.float32
    )
    if "timestamp" in df_edges.columns:
        g.edges["rates"].data["ts"] = torch.tensor(
            df_edges["timestamp"].to_numpy(), dtype=torch.int64
        )
    return g


def make_edge_splits(
    g: dgl.DGLHeteroGraph,
    etype=("user", "rates", "movie"),
    test_size: float = 0.1,
    val_size: float = 0.1,
    seed: int = 42,
) -> Dict[str, torch.Tensor]:
    """
    Random split of edges by EID into train/val/test.
    """
    rng = np.random.RandomState(seed)
    eids = np.arange(g.num_edges(etype=etype))
    rng.shuffle(eids)
    n = len(eids)
    n_test = int(n * test_size)
    n_val = int(n * val_size)
    test_eids = eids[:n_test]
    val_eids = eids[n_test : n_test + n_val]
    train_eids = eids[n_test + n_val :]
    return {
        "train_eids": torch.tensor(train_eids, dtype=torch.int64),
        "val_eids": torch.tensor(val_eids, dtype=torch.int64),
        "test_eids": torch.tensor(test_eids, dtype=torch.int64),
    }


def eids_to_pairs(
    g: dgl.DGLHeteroGraph,
    eids: Iterable[int],
    etype=("user", "rates", "movie"),
) -> List[Tuple[int, int]]:
    """
    Convert edge IDs to (u,v) pairs for a given etype.
    """
    u, v = g.find_edges(torch.tensor(list(eids)), etype=etype)
    return list(zip(u.tolist(), v.tolist()))


# =============================================================================
# Models
# =============================================================================

class GraphSAGEModel(nn.Module):
    """
    Homogeneous GraphSAGE encoder (didactic). For hetero graphs, keep using
    a homogeneous view or switch to type-specific modules.
    """
    def __init__(self, in_feats: int, hidden_feats: int = 64, out_feats: int = 64, num_layers: int = 2):
        super().__init__()
        dims = [in_feats] + [hidden_feats]*(num_layers-1) + [out_feats]
        self.layers = nn.ModuleList([SAGEConv(dims[i], dims[i+1], aggregator_type="mean") for i in range(num_layers)])
        self.act = nn.ReLU()

    def forward(self, g, x):
        h = x
        for i, layer in enumerate(self.layers):
            h = layer(g, h)
            if i < len(self.layers)-1:
                h = self.act(h)
        return h


class LinkPredictorDot(nn.Module):
    """Dot-product scorer for link prediction."""
    def forward(self, user_emb: torch.Tensor, movie_emb: torch.Tensor) -> torch.Tensor:
        return (user_emb * movie_emb).sum(dim=-1)


class LinkPredictorMLP(nn.Module):
    """
    Small MLP scorer useful for rating regression (optional).
    """
    def __init__(self, dim: int):
        super().__init__()
        self.mlp = nn.Sequential(
            nn.Linear(2*dim, 2*dim),
            nn.ReLU(),
            nn.Linear(2*dim, 1),
        )

    def forward(self, user_emb: torch.Tensor, movie_emb: torch.Tensor) -> torch.Tensor:
        x = torch.cat([user_emb, movie_emb], dim=-1)
        return self.mlp(x).squeeze(-1)  # shape [B]


# =============================================================================
# Training & evaluation
# =============================================================================

def negative_sampling_uniform(
    g: dgl.DGLHeteroGraph,
    pos_eids: torch.Tensor,
    num_neg: int = 1,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Uniform negative sampling on items for each positive edge.
    """
    num_items = g.num_nodes("movie")
    u_pos, _ = g.find_edges(pos_eids, etype=("user", "rates", "movie"))
    neg_users = u_pos.repeat_interleave(num_neg)
    neg_items = torch.randint(0, num_items, (pos_eids.shape[0]*num_neg,), device=neg_users.device)
    return neg_users, neg_items


@torch.no_grad()
def evaluate_precision_recall_at_k(
    user_emb: torch.Tensor,
    movie_emb: torch.Tensor,
    test_pairs: List[Tuple[int, int]],
    k: int = 10,
) -> Dict[str, float]:
    """
    Brute-force Precision@K/Recall@K using dot-product scores.
    """
    gt = defaultdict(set)
    for u, v in test_pairs:
        gt[int(u)].add(int(v))

    precisions, recalls = [], []
    for u in gt.keys():
        scores = (movie_emb @ user_emb[u].unsqueeze(1)).squeeze(1)  # [num_movies]
        topk = torch.topk(scores, k=k).indices.cpu().tolist()
        hits = sum(1 for m in topk if m in gt[u])
        precisions.append(hits / k)
        recalls.append(hits / max(1, len(gt[u])))

    return {
        "precision@k": float(np.mean(precisions)) if precisions else 0.0,
        "recall@k": float(np.mean(recalls)) if recalls else 0.0,
    }


def train_link_prediction(
    g: dgl.DGLHeteroGraph,
    splits: Dict[str, torch.Tensor],
    embed_dim: int = 64,
    epochs: int = 3,
    lr: float = 1e-3,
    device: str = "cpu",
    movie_feat_tensor: Optional[torch.Tensor] = None,
) -> Dict[str, torch.Tensor]:
    """
    Didactic end-to-end training:
    - Random trainable embeddings per node type.
    - Optional fusion of static movie features via a learnable projector.
    - GraphSAGE encoder (homogeneous view).
    - Dot-product link prediction with BCE on pos/neg pairs.

    :return: dict with 'user_emb', 'movie_emb' (CPU tensors).
    """
    dev = torch.device(device)
    uN, mN = g.num_nodes("user"), g.num_nodes("movie")

    u_table = nn.Embedding(uN, embed_dim).to(dev)
    m_table = nn.Embedding(mN, embed_dim).to(dev)

    hg = dgl.to_homogeneous(g)
    encoder = GraphSAGEModel(embed_dim, embed_dim, embed_dim, num_layers=2).to(dev)
    scorer = LinkPredictorDot().to(dev)

    # Optional feature projector for movie static features.
    proj = None
    if movie_feat_tensor is not None:
        proj = nn.Linear(movie_feat_tensor.shape[1], embed_dim).to(dev)

    params = list(encoder.parameters()) + list(scorer.parameters()) + list(u_table.parameters()) + list(m_table.parameters())
    if proj is not None:
        params += list(proj.parameters())
    opt = torch.optim.Adam(params, lr=lr)
    bce = nn.BCEWithLogitsLoss()

    train_eids = splits["train_eids"].to(dev)

    for ep in range(epochs):
        # Build homogeneous input features.
        x = torch.empty((uN + mN, embed_dim), device=dev)
        x[:uN] = u_table.weight
        x[uN:] = m_table.weight
        if proj is not None:
            x[uN:] = x[uN:] + proj(movie_feat_tensor.to(dev))

        z = encoder(hg, x)
        z_user, z_movie = z[:uN], z[uN:]

        # Positives.
        u_pos, v_pos = g.find_edges(train_eids, etype=("user", "rates", "movie"))
        u_pos, v_pos = u_pos.to(dev), v_pos.to(dev)
        pos_scores = scorer(z_user[u_pos], z_movie[v_pos])
        pos_labels = torch.ones_like(pos_scores)

        # Negatives.
        neg_u, neg_v = negative_sampling_uniform(g, train_eids, num_neg=1)
        neg_scores = scorer(z_user[neg_u], z_movie[neg_v])
        neg_labels = torch.zeros_like(neg_scores)

        loss = bce(torch.cat([pos_scores, neg_scores]), torch.cat([pos_labels, neg_labels]))
        opt.zero_grad(); loss.backward(); opt.step()

        tqdm.write(f"Epoch {ep+1}/{epochs} | loss={loss.item():.4f}")

    return {"user_emb": z_user.detach().cpu(), "movie_emb": z_movie.detach().cpu()}


# =============================================================================
# RMSE via fast edge regressor (frozen embeddings)
# =============================================================================

def fit_edge_regressor_ridge(
    user_emb: torch.Tensor,
    movie_emb: torch.Tensor,
    pairs: List[Tuple[int, int]],
    ratings: Iterable[float],
    alpha: float = 1.0,
):
    """
    Fit a fast linear regressor on frozen embeddings to predict ratings.

    :return: trained sklearn Ridge model.
    """
    X = []
    for u, v in pairs:
        X.append(np.concatenate([user_emb[u].numpy(), movie_emb[v].numpy()], axis=0))
    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(list(ratings), dtype=np.float32)
    model = Ridge(alpha=alpha)
    model.fit(X, y)
    return model


def rmse_from_regressor(
    model,
    user_emb: torch.Tensor,
    movie_emb: torch.Tensor,
    pairs: List[Tuple[int, int]],
    ratings: Iterable[float],
) -> float:
    """
    Compute RMSE of a fitted regressor on edge pairs.
    """
    X = []
    for u, v in pairs:
        X.append(np.concatenate([user_emb[u].numpy(), movie_emb[v].numpy()], axis=0))
    X = np.asarray(X, dtype=np.float32)
    y_true = np.asarray(list(ratings), dtype=np.float32)
    y_pred = model.predict(X)
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


# =============================================================================
# Recommendation helpers
# =============================================================================

def build_user_seen_map(
    g: dgl.DGLHeteroGraph,
    eids: Iterable[int],
    etype=("user", "rates", "movie"),
) -> Dict[int, set]:
    """
    Map user -> set(items) for edges in the given EIDs (e.g., training set).
    """
    u, v = g.find_edges(torch.tensor(list(eids)), etype=etype)
    out: Dict[int, set] = defaultdict(set)
    for uu, vv in zip(u.tolist(), v.tolist()):
        out[uu].add(vv)
    return out


def recommend_topk_for_user(
    user_id: int,
    user_emb: torch.Tensor,
    movie_emb: torch.Tensor,
    seen_items: Optional[set] = None,
    k: int = 10,
) -> List[int]:
    """
    Recommend top-K movie indices for a user, optionally excluding seen items.
    """
    scores = (movie_emb @ user_emb[user_id].unsqueeze(1)).squeeze(1)  # [num_movies]
    ranked = torch.topk(scores, k=scores.shape[0]).indices.cpu().tolist()
    if seen_items:
        ranked = [m for m in ranked if m not in seen_items]
    return ranked[:k]


def id_maps_to_title_lookup(
    movies_df: Optional[pd.DataFrame],
    item_map: Optional[np.ndarray],
) -> Dict[int, str]:
    """
    Build int-index -> movie title mapping using contiguous item_map ordering.
    """
    if movies_df is None or item_map is None:
        return {}
    mid_to_row = {int(mid): i for i, mid in enumerate(item_map)}
    title_by_idx = {}
    for _, row in movies_df.iterrows():
        mid = int(row["movieId"])
        if mid in mid_to_row:
            title_by_idx[mid_to_row[mid]] = str(row.get("title", f"movie_{mid}"))
    return title_by_idx
