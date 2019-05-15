#!/usr/bin/env python3

"""Module containing the GMX TrjConvStr class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.command_wrapper import cmd_wrapper
from biobb_analysis.gromacs.common import *


class GMXTrjConvStrEns():
    """Wrapper of the GROMACS trjconv (http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-trjconv.html) module.

    Args:
        input_traj_path (str): Path to the GROMACS trajectory file: xtc, trr, cpt, gro, g96, pdb, tng.
        input_top_path (str): Path to the GROMACS input topology file: tpr, gro, g96, pdb, brk, ent.
        output_str_ens_path (str): Path to the output file: zip.
        properties (dic):
            * **selection** (*str*) - ("System") Group where the trjconv will be performed: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
            * **start** (*int*) - (0) Time of first frame to read from trajectory (default unit ps).
            * **end** (*int*) - (0) Time of last frame to read from trajectory (default unit ps).
            * **dt** (*int*) - (0) Only write frame when t MOD dt = first time (ps).
            * **output_name** (*str*) - ("output") File name for ensemble of output files.
            * **output_type** (*str*) - ("pdb") File type for ensemble of output files: gro, g96, pdb.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_traj_path, input_top_path, output_str_ens_path, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_traj_path = input_traj_path
        self.input_top_path = input_top_path
        self.output_str_ens_path = output_str_ens_path

        # Properties specific for BB
        self.properties = properties

        # Properties common in all GROMACS BB
        self.gmx_path = get_binary_path(properties, 'gmx_path')

        # Properties common in all BB
        self.can_write_console_log = properties.get('can_write_console_log', True)
        self.global_log = properties.get('global_log', None)
        self.prefix = properties.get('prefix', None)
        self.step = properties.get('step', None)
        self.path = properties.get('path', '')

    def check_data_params(self):
        """ Checks all the input/output paths and parameters """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)
        self.input_traj_path = check_traj_path(self.input_traj_path, out_log, self.__class__.__name__)
        self.input_top_path = check_input_path(self.input_top_path, out_log, self.__class__.__name__)
        self.output_str_ens_path = check_out_str_ens_path(self.output_str_ens_path, out_log, self.__class__.__name__)
        self.selection = get_selection(self.properties, out_log, self.__class__.__name__)
        self.start = get_start(self.properties, out_log, self.__class__.__name__)
        self.end = get_end(self.properties, out_log, self.__class__.__name__)
        self.dt = get_dt(self.properties, out_log, self.__class__.__name__)
        self.output_name = self.properties.get('output_name', 'output')
        self.output_type = get_ot_str_ens(self.properties, out_log, self.__class__.__name__)

    def launch(self):
        """Launches the execution of the GROMACS rgyr module."""
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        # check input/output paths and parameters
        self.check_data_params()

        # create temporary folder
        self.tmp_folder = fu.create_unique_dir()
        fu.log('Creating %s temporary folder' % self.tmp_folder, out_log)

        cmd = ['echo', '\"'+self.selection+'\"', '|',
               self.gmx_path, 'trjconv',
               '-f', self.input_traj_path,
               '-s', self.input_top_path,
               '-b', self.start,
               '-e', self.end,
               '-dt', self.dt,
               '-sep',
               '-o', self.output_name + '.' + self.output_type]

        # change execution directory to temporary folder
        cwd = os.getcwd()
        os.chdir(self.tmp_folder)

        # execute cmd
        returncode = cmd_wrapper.CmdWrapper(cmd, out_log, err_log, self.global_log).launch()
        # move files to output_str_ens_path and removes temporary folder
        os.chdir(cwd)
        process_output_trjconv_str_ens(self.tmp_folder, self.output_str_ens_path, out_log)
        return returncode

def main():
    parser = argparse.ArgumentParser(description="Wrapper of the GROMACS trjconv module.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_traj_path', required=True, help='Path to the GROMACS trajectory file: xtc, trr, cpt, gro, g96, pdb, tng.')
    required_args.add_argument('--input_top_path', required=True, help='Path to the GROMACS input topology file: tpr, gro, g96, pdb, brk, ent.')
    required_args.add_argument('--output_str_ens_path', required=True, help='Path to the output file: gro, g96, pdb.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    GMXTrjConvStrEns(input_traj_path=args.input_traj_path, input_top_path=args.input_top_path, output_str_ens_path=args.output_str_ens_path, properties=properties).launch()

if __name__ == '__main__':
    main()