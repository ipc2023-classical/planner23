#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from lab.environments import LocalEnvironment
from lab.reports import Attribute, arithmetic_mean, geometric_mean
from downward.reports.absolute import AbsoluteReport
from downward.reports.compare import ComparativeReport
# from downward.reports.scatter import ScatterPlotReport
from lab import tools

from common_setup import IssueConfig, IssueExperiment, DEFAULT_SATISFICING_SUITE



REVISION = 'ipc2023-classical'


def main(revisions=None):
    benchmarks_dir = os.environ["DOWNWARD_BENCHMARKS"]
    suite = ["agricola-sat18-strips", "airport", "barman-sat11-strips", "barman-sat14-strips", "blocks", "childsnack-sat14-strips", "data-network-sat18-strips", "depot", "driverlog", "elevators-sat08-strips", "elevators-sat11-strips", "floortile-sat11-strips", "floortile-sat14-strips", "freecell", "ged-sat14-strips", "grid", "gripper", "hiking-sat14-strips", "logistics00", "logistics98", "miconic", "movie", "mprime", "mystery", "nomystery-sat11-strips", "openstacks-sat08-strips", "openstacks-sat11-strips", "openstacks-sat14-strips", "openstacks-strips", "organic-synthesis-sat18-strips", "organic-synthesis-split-sat18-strips", "parcprinter-08-strips", "parcprinter-sat11-strips", "parking-sat11-strips", "parking-sat14-strips", "pathways", "pegsol-08-strips", "pegsol-sat11-strips", "pipesworld-notankage", "pipesworld-tankage", "psr-small", "rovers", "satellite", "scanalyzer-08-strips", "scanalyzer-sat11-strips", "snake-sat18-strips", "sokoban-sat08-strips", "sokoban-sat11-strips", "spider-sat18-strips", "storage", "termes-sat18-strips", "tetris-sat14-strips", "thoughtful-sat14-strips", "tidybot-sat11-strips", "tpp", "transport-sat08-strips", "transport-sat11-strips", "transport-sat14-strips", "trucks-strips", "visitall-sat11-strips", "visitall-sat14-strips", "woodworking-sat08-strips", "woodworking-sat11-strips", "zenotravel"]
    environment = LocalEnvironment(processes=48)


    suite = DEFAULT_SATISFICING_SUITE
    suite = ["barman-sat11-strips", "cavediving-14-adl", "citycar-sat14-adl"]
    BUILD_OPTIONS = []
    configs = set()

    configs.add(IssueConfig('tftm-argmax', [],build_options=BUILD_OPTIONS, driver_options=["--alias", "seq-sat-cerberus-novelops-argmax", "--overall-time-limit", "30m", "--overall-memory-limit", "3584M"])) 
    configs.add(IssueConfig('tftm-co1', [],build_options=BUILD_OPTIONS, driver_options=["--alias", "seq-sat-cerberus-novelops-co1", "--overall-time-limit", "30m", "--overall-memory-limit", "3584M"]))

    exp = IssueExperiment(
        revisions=revisions,
        configs=configs,
        environment=environment,
    )

    exp.add_suite(benchmarks_dir, suite)

    autoscale_benchmarks_dir = "/data/software/autoscale/benchmarks/2022-03-03-sat"
    autoscale_suite = ["agricola", "airport", "barman", "blocksworld", "childsnack", "data-network", "depots", "driverlog", "elevators", "floortile", "freecell", "ged", "grid", "gripper", "hiking", "logistics", "miconic", "mprime", "nomystery", "openstacks", "organic-synthesis-split", "parcprinter", "parking", "pathways", "pegsol", "pipesworld-notankage", "pipesworld-tankage", "rovers", "satellite", "scanalyzer", "snake", "sokoban", "storage", "termes", "tetris", "thoughtful", "tidybot", "tpp", "transport", "visitall", "woodworking", "zenotravel"]
    autoscale_suite = ["agricola", "data-network"]

    exp.add_suite(autoscale_benchmarks_dir, autoscale_suite)
    exp.add_parser(exp.EXITCODE_PARSER)
    exp.add_parser(exp.PLANNER_PARSER)
    exp.add_parser(exp.SINGLE_SEARCH_PARSER)
    exp.add_parser('red-black-parser.py')

    REDBLACK_ATTRIBUTES = ["rb_invertible_variables", "rb_black_variables", "rb_black_root_variables", "rb_all_variables", "rb_variables_dtg_complete", "rb_variables_all_values_connected_to_goal", "rb_black_variables_only_strongly_connected_parents", "rb_max_side_effects_of_black_variables"]

    attributes = exp.DEFAULT_TABLE_ATTRIBUTES + ["plan_length"] + REDBLACK_ATTRIBUTES

    exp.add_step('build', exp.build)
    exp.add_step('start', exp.start_runs)
    exp.add_fetcher(name='fetch')


    # def rename_algorithms(run):
    #     name = run["algorithm"]
    #     paper_names = {
    #         '{}-{}'.format(REVISION, 'cerberus'): "cerberus-2018",
    #         '{}-{}'.format(REVISION, 'cerberus-new'): "cerberus-2022"}
        
    #     run["algorithm"] = paper_names.get(name, name)
    #     return run
    # algs = ["cerberus-2018", "cerberus-2022"]

    # exp.add_absolute_report_step(attributes=attributes, filter=rename_algorithms, filter_algorithm=algs)
    exp.add_absolute_report_step(attributes=attributes)

    # pairs = [ ("cerberus-2018", "cerberus-2022")]
    # exp.add_report(
    #     ComparativeReport(filter=rename_algorithms, 
    #         algorithm_pairs=pairs,
    #         attributes=attributes,
    #     ),
    #     outfile=os.path.join(exp.eval_dir, 'a' + exp.name + '-compare.html'),
    # )

    exp.run_steps()

main(revisions=[REVISION])
