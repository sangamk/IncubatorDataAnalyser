import pandas as pd
import glob
import csv
import os

base_path = "F:/thesis/instrumentedapps"
base_tool_path = "C:/Master/Thesis/IncubatorDataAnalyser"


# load statical graphs
def load_csv_graphs():
    csv_graph_files = {x.strip(): base_path + '/data/' + x.strip() + ".csv" for x in apps}

    # for app,f in csv_graph_files.items():
    df_from_each_file = (pd.read_csv(f).assign(app=app) for app, f in csv_graph_files.items())
    actual_graph_df = pd.concat(df_from_each_file, ignore_index=True)
    print("Total graphs:")
    print(len(actual_graph_df))

    return actual_graph_df


# load statical methods of all screens
def load_csv_methods():
    csv_methods_files = {x.strip(): base_path + '/data/' + x.strip() + "-methods.csv" for x in
                         apps}

    df_from_each_file = (pd.read_csv(f).assign(app=app) for app, f in csv_methods_files.items())
    methods_df = pd.concat(df_from_each_file, ignore_index=True)

    print("Total methods:")
    print(len(methods_df))

    return methods_df


# load coverage from apps
def load_csv_coverage():
    csv_coverage_files = {x.strip(): glob.glob(base_path + '/data/' + x.strip() + "-coverage.csv") for
                          x in
                          apps}

    for k, v in csv_coverage_files.items():
        if len(v) != 1:
            print("Found error ... aborting: " + k)
            print(v)
            return

    df_from_each_file = (pd.read_csv(f[0], encoding='latin-1').assign(app=app) for app, f in csv_coverage_files.items())
    coverage_df = pd.concat(df_from_each_file, ignore_index=True)

    print("Total covered methods:")
    print(len(coverage_df))

    systematic_coverage = coverage_df[coverage_df.coverage_type == "method"]
    random_coverage = coverage_df[coverage_df.coverage_type == "systematic"]

    check_df = systematic_coverage.method.ne(random_coverage.method)

    if len(check_df[check_df != True]) != 0:
        print("Error: unique values found!")
        check_df[check_df != True]
    else:
        print("Everything is good!")

    return coverage_df


# Load csv test result graph
def load_csv_test_graphs():
    # csv_graph_files = {x.strip(): base_path + '/batch1/graphs/' + x.strip() + "-test-graph.csv" for x in apps}
    csv_graph_files = {x.strip(): glob.glob(base_path + '/data/' + x.strip() + "-test-graph.csv") for
                       x in
                       apps}

    for k, v in csv_graph_files.items():
        if len(v) != 1:
            print("Found error ... aborting: " + k)
            print(v)
            return

    # for app,f in csv_graph_files.items():
    graph_from_each_file = (pd.read_csv(f[0]).assign(app=app) for app, f in csv_graph_files.items())
    test_graph_df = pd.concat(graph_from_each_file, ignore_index=True)
    print("Total entries:")
    print(len(test_graph_df))

    return test_graph_df


def load_csv_stat_graph(postfix):
    csv_graph_files = {x.strip(): glob.glob(base_path + '/data/' + x.strip() + postfix + ".csv") for x in apps}

    for k, v in csv_graph_files.items():
        if len(v) != 1:
            print("Found error ... aborting: " + k)
            print(v)
            return

    # for app, f in csv_graph_files.items():
    #     print("safsdf " + app)
    #     pd.read_csv(f[0], encoding='latin-1').assign(app=app)

    df_from_each_file = (pd.read_csv(f[0], encoding='latin-1').assign(app=app) for app, f in csv_graph_files.items())
    stat_graph_df = pd.concat(df_from_each_file, ignore_index=True)

    print("Total entries:")
    print(len(stat_graph_df))
    return stat_graph_df


with open(base_tool_path + "/data/apps.txt") as f:
    apps = set(f.readlines())

print("Number of apps: ")
print(len(apps))

# load_csv_stat_graph("-act-transitive")
# load_csv_test_graphs()
# load_csv_coverage()
