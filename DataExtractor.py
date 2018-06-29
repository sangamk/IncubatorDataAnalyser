import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import pydot
import glob
import re
import logging
import sys

apps = []


def setupConfig():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    logging.basicConfig(filename='DataExtractor.log', level=logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


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
        logging.info(atype.get('foobar'))


def run():
    file = Path("./data/apps.txt")
    with open(file) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    apps = [x.strip() for x in content]
    for app in apps:
        read_xml_coverage(app, "systematic")
        read_xml_coverage(app, "random")


def read_xml_coverage(app, strategy):
    logging.info("------------------------- Read coverage for " + app)
    logging.info("Startegy " + strategy)
    random_coverage = glob.glob("F:/thesis/instrumentedapps/*/" + strategy + "/" + app + ".apk*/coverage/coverage.xml")
    headers = ["package", "class", "method", "strategy", "coverage_type", "coverage_percentage", "covered_lines",
               "total_lines"]
    content = []
    if len(random_coverage) != 1:
        logging.error("Invalid number of coverage files:")
        logging.error(len(random_coverage))
        logging.error("**** Skip + " + app)
        return

    tree = ET.parse(random_coverage[0])
    root = tree.getroot()
    for package in root.iter("package"):
        package_name = package.attrib['name']
        for class_ in package.iter("class"):
            class_name = package_name + "." + class_.attrib["name"]
            for method in class_.iter("method"):
                method_name = method.attrib["name"]
                for coverage in method:
                    coverage_type = coverage.attrib["type"][:-3]
                    raw_value = coverage.attrib["value"]
                    formatted_value = re.findall(r'\d+', raw_value)
                    # logging.debug(
                    #     class_name + " __ " + method_name + " __ " + strategy + "___ " + coverage_type + " __ " +
                    #     formatted_value[0] + "% " + formatted_value[1] + "/" + formatted_value[2])
                    content.append([package_name, class_name, method_name, strategy, coverage_type] + formatted_value)
    logging.info("------------------------- Finished coverage for " + app)
    write_to_csv(headers, content, "./data/" + app + "-coverage.csv")


# read_graph_file()
# read_xml_coverage("")

setupConfig()
run()


class Class:
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class App:
    def __init__(self, package_name, classes):
        self.package_name = package_name
        self.classes = classes
