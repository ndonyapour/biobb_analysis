#!/usr/bin/env python3

"""Module containing the GMX TrjConvStr class and the command line interface."""
import argparse
from biobb_common.configuration import  settings
from biobb_common.tools import file_utils as fu
from biobb_common.tools.file_utils import launchlogger
from biobb_common.command_wrapper import cmd_wrapper
from biobb_analysis.gromacs.common import *


class GMXTrjConvStrEns():
    """Extracts an ensemble of frames containing a selection of atoms from GROMACS compatible trajectory files.
    Wrapper of the GROMACS trjconv (http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-trjconv.html) module.

    Args:
        input_traj_path (str): Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.
        input_top_path (str): Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.
        input_index_path (str): Path to the GROMACS index file. Accepted formats: ndx.
        output_str_ens_path (str): Path to the output file. Accepted formats: zip.
        properties (dic):
            * **selection** (*str*) - ("System") Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values, if not, values: System, Protein, Protein-H, C-alpha, Backbone, MainChain, MainChain+Cb, MainChain+H, SideChain, SideChain-H, Prot-Masses, non-Protein, Water, SOL, non-Water, Ion, NA, CL, Water_and_ions.
            * **start** (*int*) - (0) Time of first frame to read from trajectory (default unit ps).
            * **end** (*int*) - (0) Time of last frame to read from trajectory (default unit ps).
            * **dt** (*int*) - (0) Only write frame when t MOD dt = first time (ps).
            * **output_name** (*str*) - ("output") File name for ensemble of output files.
            * **output_type** (*str*) - ("pdb") File type for ensemble of output files. Values: gro, g96, pdb.
            * **gmx_path** (*str*) - ("gmx") Path to the GROMACS executable binary.
    """

    def __init__(self, input_traj_path, input_top_path, output_str_ens_path, input_index_path=None, properties=None, **kwargs):
        properties = properties or {}

        # Input/Output files
        self.input_traj_path = input_traj_path
        self.input_top_path = input_top_path
        self.input_index_path = input_index_path
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
        self.remove_tmp = properties.get('remove_tmp', True)
        self.restart = properties.get('restart', False)

        # check input/output paths and parameters
        self.check_data_params()

        # Check the properties
        fu.check_properties(self, properties)

    def check_data_params(self):
        """ Checks all the input/output paths and parameters """
        out_log, err_log = fu.get_logs(path=self.path, prefix=self.prefix, step=self.step, can_write_console=self.can_write_console_log)

        self.input_traj_path = check_traj_path(self.input_traj_path, out_log, self.__class__.__name__)
        self.input_top_path = check_input_path(self.input_top_path, out_log, self.__class__.__name__)
        self.input_index_path = check_index_path(self.input_index_path, out_log, self.__class__.__name__)
        self.output_str_ens_path = check_out_str_ens_path(self.output_str_ens_path, out_log, self.__class__.__name__)
        if not self.input_index_path:
            self.selection = get_selection(self.properties, out_log, self.__class__.__name__)
        else:
            self.selection = get_selection_index_file(self.properties, self.input_index_path, 'selection', out_log, self.__class__.__name__)
        self.start = get_start(self.properties, out_log, self.__class__.__name__)
        self.end = get_end(self.properties, out_log, self.__class__.__name__)
        self.dt = get_dt(self.properties, out_log, self.__class__.__name__)
        self.output_name = self.properties.get('output_name', 'output')
        self.output_type = get_ot_str_ens(self.properties, out_log, self.__class__.__name__)

        handlers = out_log.handlers[:]
        for handler in handlers:
            handler.close()
            out_log.removeHandler(handler)
        handlers = err_log.handlers[:] # Create a copy [:] of the handler list to be able to modify it while we are iterating
        for handler in handlers:
            handler.close()
            err_log.removeHandler(handler)

    @launchlogger
    def launch(self):
        """Launches the execution of the GROMACS rgyr module."""
        tmp_files = []

        # Get local loggers from launchlogger decorator
        out_log = getattr(self, 'out_log', None)
        err_log = getattr(self, 'err_log', None)

        #Restart
        if self.restart:
            output_file_list = [self.output_str_ens_path]
            if fu.check_complete_files(output_file_list):
                fu.log('Restart is enabled, this step: %s will the skipped' % self.step, out_log, self.global_log)
                return 0

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

        if self.remove_tmp:
            fu.rm_file_list(tmp_files)

        return returncode

def main():
    parser = argparse.ArgumentParser(description="Extracts an ensemble of frames containing a selection of atoms from GROMACS compatible trajectory files.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')
    parser.add_argument('--system', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")
    parser.add_argument('--step', required=False, help="Check 'https://biobb-common.readthedocs.io/en/latest/system_step.html' for help")

    #Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_traj_path', required=True, help='Path to the GROMACS trajectory file. Accepted formats: xtc, trr, cpt, gro, g96, pdb, tng.')
    required_args.add_argument('--input_top_path', required=True, help='Path to the GROMACS input topology file. Accepted formats: tpr, gro, g96, pdb, brk, ent.')
    parser.add_argument('--input_index_path', required=False, help="Path to the GROMACS index file. Accepted formats: ndx.")
    required_args.add_argument('--output_str_ens_path', required=True, help='Path to the output file. Accepted formats: zip.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config, system=args.system).get_prop_dic()
    if args.step:
        properties = properties[args.step]

    #Specific call of each building block
    GMXTrjConvStrEns(input_traj_path=args.input_traj_path, input_top_path=args.input_top_path, output_str_ens_path=args.output_str_ens_path, input_index_path=args.input_index_path, properties=properties).launch()

if __name__ == '__main__':
    main()
