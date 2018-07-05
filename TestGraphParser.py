import csv
import xml.etree.ElementTree as ET
from pathlib import Path
import pydot
import glob
import re
import logging
import sys

apps = []
base_path = "F:/thesis/instrumentedapps"


def setupConfig():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    logging.basicConfig(filename='TestGraphExtractor.log', level=logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def write_to_csv(headers, content, file_name):
    my_file = Path(file_name)
    has_header = my_file.exists()
    with open(file_name, 'a', newline='') as out_csv:
        writer = csv.writer(out_csv)
        if not has_header:
            writer.writerow(headers)
        writer.writerows(l for l in content)


def run():
    file = Path("./data/apps.txt")
    with open(file) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    apps = [x.strip() for x in content]
    for app in apps:
        read_xml_graph(app, "systematic")
        read_xml_graph(app, "random")


def read_xml_graph(app, strategy):
    logging.info("------------------------- Read graph for " + app)
    logging.info("Startegy " + strategy)
    graph_Path = glob.glob(base_path + "/*/" + strategy + "/" + app + ".apk*/model/graph.xml")
    headers = ["source", "target", "action", "widget_id", "widget", "strategy"]
    content = []
    if len(graph_Path) != 1:
        logging.error("Invalid number of graph files:")
        logging.error(len(graph_Path))
        logging.error("**** Skip + " + app)
        return

    tree = ET.parse(graph_Path[0])
    root = tree.getroot()
    # for report in root.iter("report"):

    if len(list(root.iter("activity"))):
        print("everything found")
        for activities in root.iter("activity"):

            for xml_source in activities.findall("source"):
                source = xml_source.text
            for xml_target in activities.findall("target"):
                target = xml_target.text
            for xml_widgets in activities.iter("ev"):
                action = xml_widgets.attrib["in"]

                if len(list(xml_widgets)):
                    for xml_widgetInfo in xml_widgets.iter("w"):
                        id = xml_widgetInfo.attrib["id"]
                        widget_class = xml_widgetInfo.attrib["cl"]
                        content.append([source, target, action, id, widget_class, strategy])
                else:
                    content.append([source, target, action, "", "", strategy])

        write_to_csv(headers, content, "./data/" + app + "-test-graph.csv")
    else:
        print("nothing found")
        read_cml_logs(app, strategy)




def read_cml_logs(app, strategy):
    graph_Path = glob.glob(base_path + "/*/" + strategy + "/" + app + ".apk*/model/log_*.xml")
    headers = ["source", "target", "action", "widget_id", "widget", "strategy"]
    content = []
    actvities = set()
    if len(graph_Path) == 0:
        logging.error("Invalid number of log files:")
        logging.error(len(graph_Path))
        logging.error("**** Skip + " + app)
        return

    for file in graph_Path:
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for activity in root.findall("a"):
                actvities.add(activity.attrib["cl"])
        except ET.ParseError:
            print("invalid log continue...")

    if len(actvities) != 1:
        logging.error("invalid number of activities found for a class without a graph")
        logging.error("**** Skip + " + app)
        return

    write_to_csv(headers, [[list(actvities)[0], "", "", "", "", strategy]], "./data/" + app + "-test-graph.csv")


run()
