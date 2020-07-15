from pm4py.algo.discovery.heuristics import factory as heuristics_miner
from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.visualization.petrinet import factory as pn_vis_factory
from pm4py.visualization.heuristics_net import factory as hn_vis_factory
from pm4py.util import constants
import os
os.environ["PATH"] += os.pathsep + 'C:/Archivos de Programa/GraphViz/bin/'

dataframe = csv_import_adapter.import_dataframe_from_path(
    'cursos.csv', sep=",")
log = conversion_factory.apply(dataframe, parameters={constants.PARAMETER_CONSTANT_CASEID_KEY: "case:concept:name",
                                                      constants.PARAMETER_CONSTANT_ACTIVITY_KEY: "concept:name",
                                                      constants.PARAMETER_CONSTANT_TIMESTAMP_KEY: "time:timestamp"})


net = heuristics_miner.apply_heu(
    log, parameters={"dependency_thresh": 0.99})
gviz = hn_vis_factory.apply(net)
hn_vis_factory.view(gviz)
