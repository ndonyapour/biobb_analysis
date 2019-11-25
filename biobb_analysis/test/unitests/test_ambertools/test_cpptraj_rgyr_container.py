from biobb_common.tools import test_fixtures as fx
from biobb_analysis.ambertools.cpptraj_rgyr import Rgyr


class TestCpptrajRgyrDocker():
    def setUp(self):
        fx.test_setup(self,'cpptraj_rgyr_docker')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_rgyr_docker(self):
        Rgyr(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpptraj_path'])
        assert fx.equal(self.paths['output_cpptraj_path'], self.paths['ref_output_cpptraj_path'])

class TestCpptrajRgyrSingularity():
    def setUp(self):
        fx.test_setup(self,'cpptraj_rgyr_singularity')

    def tearDown(self):
        fx.test_teardown(self)
        pass

    def test_rgyr_singularity(self):
        Rgyr(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_cpptraj_path'])
        assert fx.equal(self.paths['output_cpptraj_path'], self.paths['ref_output_cpptraj_path'])