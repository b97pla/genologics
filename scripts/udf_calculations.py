#!/usr/bin/env python
"""EPP script to perform basic calculations on UDF:s in Clarity LIMS
Command to trigger this script:
bash -c "PATH/TO/INSTALLED/SCRIPT
--pid {processLuid} 
--log {compoundOutputFileLuidN}"
--output_files {outputFileLuids}
--udf1 NameOfUDF 1
--operator Mathematical operator
--udf2 NameOfUDF 2
--result_udf NameOfUDF to store result in
"

Johannes Alneberg, Science for Life Laboratory, Stockholm, Sweden
""" 
from argparse import ArgumentParser

from genologics.lims import Lims
from genologics.entities import Artifact, Process
from genologics.epp import configure_logging,setup_standard_parser
from genologics.config import BASEURI,USERNAME,PASSWORD

def apply_calculations(lims,artifact,udf1,op,udf2,result_udf):
    print 'result_udf: {0}, udf1: {1}, operator: {2}, udf2: {3}'.format(
        result_udf,udf1,op,udf2)
    for artifact in input_artifacts:
        print 'Updating: Artifact id: {0}, result_udf: {1}, udf1: {2}, operator: {3}, udf2: {4}'.format(
            artifact.id, artifact.udf[result_udf],artifact.udf[udf1],op,artifact.udf[udf2])
        artifact.udf[result_udf] = eval('{0}{1}{2}'.format(artifact.udf[udf1],op,artifact.udf[udf2]))
        artifact.put()
        print 'Updated {0} to {1}.'.format(result_udf,artifact.udf[result_udf])

def main(lims,args):
    p = Process(lims,id = args.pid)
    inputs = p.all_inputs(unique=True)

    apply_calculations(lims,inputs,args.udf1,args.operator,args.udf2,args.result_udf)


if __name__ == "__main__":
    # Initialize parser with standard arguments and description
    desc = """EPP script to perform basic calculations on UDF:s in Clarity LIMS.
    result_udf=udf1 *operator* udf2"""
    parser = ArgumentParser(description=desc)

    parser.add_argument('--pid',
                        help='Lims id for current Process')
    parser.add_argument('--log',
                        help='Log file')
    parser.add_argument('--output_files',nargs='*',
                        help='Lims unique ids for each output file artifact')
    parser.add_argument('--udf1',
                        help='The first udf in the formula')
    parser.add_argument('--operator', choices =['+','-','*'],
                        help='operator to apply')
    parser.add_argument('--udf2',
                        help='The second udf in the formula')
    parser.add_argument('--result_udf',
                        help='Udf to store the result')
    args = parser.parse_args()

    # Start logging
    if args.log:
        configure_logging(args.log)
    lims = Lims(BASEURI,USERNAME,PASSWORD)
    lims.check_version()

    main(lims, args)

