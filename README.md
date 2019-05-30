[![](https://readthedocs.org/projects/biobb-analysis/badge/?version=latest)](https://biobb-analysis.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](https://anaconda.org/bioconda/biobb_analysis)
[![](https://quay.io/repository/biocontainers/biobb_io/status)](https://hub.docker.com/r/mmbirb/biobb_analysis)
[![](https://www.singularity-hub.org/static/img/hosted-singularity--hub-%23e32929.svg)](https://singularity-hub.org/collections/2423)
[![](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# biobb_analysis

### Introduction
Biobb_analysis is the Biobb module collection to perform analysis of molecular dynamics simulations.
Biobb (BioExcel building blocks) packages are Python building blocks that
create new layer of compatibility and interoperability over popular
bioinformatics tools.
The latest documentation of this package can be found in our readthedocs site:
[latest API documentation](http://biobb_analysis.readthedocs.io/en/latest/).

### Version
v1.0.5 May 2019 Release

### Installation
Using PIP:
* Installation:


        pip install "biobb_analysis>=1.0.5"


* Usage: [Python API documentation](https://biobb-analysis.readthedocs.io/en/latest/modules.html)

Using ANACONDA:

* Installation:


        conda install -c bioconda "biobb_analysis>=1.0.5"


* Usage: With conda installation BioBBs can be used with the [Python API documentation](https://biobb-analysis.readthedocs.io/en/latest/modules.html) and the [Command Line documentation](https://biobb-analysis.readthedocs.io/en/latest/command_line.html)

Using DOCKER:

* Installation:


        docker pull mmbirb/biobb_analysis:latest


* Usage:


        docker run mmbirb/biobb_analysis:latest <command>


Using SINGULARITY:

* Installation:


        singularity pull shub://bioexcel/biobb_analysis


* Usage:


        singularity exec bioexcel-biobb_analysis-master-latest.simg <command>


The command list and specification can be found at the [Command Line documentation](https://biobb-analysis.readthedocs.io/en/latest/command_line.html).


### Copyright & Licensing
This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2019 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2019 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2015/12/Bioexcell_logo_1080px_transp.png "Bioexcel")
