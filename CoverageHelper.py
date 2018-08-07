import pandas as pd


def filter(type: str, strategy: str, df: pd.DataFrame):
    return df[(df.coverage_type == type) & (df.strategy == strategy)]


def widget_counter(df: pd.DataFrame):
    # unique_widgets_per_app = df.widget.value_counts(dropna=False).to_frame(
    unique_widgets_per_app = df.widget.value_counts(dropna=False).to_frame(
        name="widget_count")
    unique_widgets_per_app['percentage'] = unique_widgets_per_app.apply(lambda x: 100 * x / x.sum())
    return unique_widgets_per_app.reset_index()


def diff_screens(full_graph: pd.DataFrame, found_graph: pd.DataFrame):
    # First find all edges that are not in found_graph
    keys = list(["source", "target", "app"])
    i1 = full_graph.set_index(keys).index
    i2 = found_graph.set_index(keys).index
    not_found_edges = full_graph[~i1.isin(i2)]

    # Filter edges that can be reached by one of the sources
    edges_from_source = not_found_edges.merge(found_graph[["app", "source"]].drop_duplicates())

    # Filter edges that can be reached by one of the targets (as source)
    edges_from_target = not_found_edges.merge(
        found_graph[["app", "target"]].drop_duplicates().rename(index=str, columns={"target": "source"}))

    # Combine all edges not reached from the current set of edges found
    direct_edges_not_found = edges_from_target.append(edges_from_source)
    return direct_edges_not_found.drop_duplicates()
