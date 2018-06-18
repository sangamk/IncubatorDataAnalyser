import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import pydot
import glob

apps = []


def read_graph_file():
    (graph,) = pydot.graph_from_dot_file("graph.dot")
    edges = graph.obj_dict['edges']

    headers = ["package", "target", "source", "methode"]
    content = []

    for key, (value,) in edges.items():
        package = "package"
        source = key[0].strip('\"')
        target = key[1].strip('\"')
        method = value["attributes"]["label"]
        content.append([package, source, target, method])

    write_to_csv(headers, content, "graph.csv")


def write_to_csv(headers, content, file_name):
    my_file = Path(file_name)
    has_header = my_file.exists()
    with open(file_name, 'a', newline='') as out_csv:
        writer = csv.writer(out_csv)
        if not has_header:
            writer.writerow(headers)
        writer.writerows(l for l in content)


def read_xml_graph_file():
    e = ET.parse('thefile.xml').getroot()
    for atype in e.findall('type'):
        print(atype.get('foobar'))


def run():
    file = Path("./data/apps.txt")
    with open(file) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    apps = [x.strip() for x in content]
    for app in apps:
        read_csv_methods(app)


def read_csv_methods(app):
    path = "D:/thesis/instrumentedapps/test/graphs/" + app + "-methods.csv"
    file = Path(path)
    methods = {}
    if file.exists():
        print("Found " + path)
        random_coverage = glob.glob("D:/thesis/instrumentedapps/test/random/" + app + "*/coverage/coverage.xml")
        systematic_coverage = glob.glob("D:/thesis/instrumentedapps/test/systematic/" + app + "*/coverage/coverage.xml")

        if len(random_coverage) == 1:
            read_xml_coverage(random_coverage[0])

        if len(systematic_coverage) == 1:
            read_xml_coverage(systematic_coverage[0])

        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Skip the header.
            # Unpack the row directly in the head of the for loop.
            # for class_name, method in reader:
            #     print("")
                # print(class_name + " method " + method)
                # methods[class_name] = (method)


def read_xml_coverage(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)


# read_graph_file()

run()


class Class:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class App:
    def __init__(self, package_name, classes):
        self.package_name = package_name
        self.classes = classes
