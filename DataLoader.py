import pandas as pd
import glob


def load_csv_graphs():
    csv_graph_files = {x.strip(): 'F:/thesis/instrumentedapps/batch1/graphs/' + x.strip() + ".csv" for x in apps}

    # for app,f in csv_graph_files.items():
    df_from_each_file = (pd.read_csv(f).assign(app=app) for app, f in csv_graph_files.items())
    actual_graph_df = pd.concat(df_from_each_file, ignore_index=True)
    print("Total graphs:")
    print(len(actual_graph_df))

    return actual_graph_df


def load_csv_methods():
    csv_methods_files = {x.strip(): 'F:/thesis/instrumentedapps/batch1/graphs/' + x.strip() + "-methods.csv" for x in
                         apps}

    df_from_each_file = (pd.read_csv(f).assign(app=app) for app, f in csv_methods_files.items())
    methods_df = pd.concat(df_from_each_file, ignore_index=True)

    print("Total methods:")
    print(len(methods_df))

    return methods_df


def load_csv_coverage():
    csv_coverage_files = {x.strip(): glob.glob('F:/thesis/instrumentedapps/*/graphs/' + x.strip() + "-coverage.csv") for
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


with open("./data/apps.txt") as f:
    apps = set(f.readlines())

print("Number of apps: ")
print(len(apps))
