<div align="center">
<img src="https://raw.githubusercontent.com/jakebrehm/referral-network/master/img/logo.png" alt="Referral Network Logo"/>
</div>

<h4 align="center">Can we visualize the bottlenecks that occur in the specialty referral network so that opportunities for improvement can be further explored?</h4>

<hr>

## Table of contents

* [Introduction](#introduction)
* [Getting set up](#getting-set-up)
    * [Required dependencies](#required-dependencies)
    * [Installing the dependencies](#installing-the-dependencies)
* [Starting the web application](#starting-the-web-application)
* [Debug mode](#debug-mode)
* [Formatting the input data](#formatting-the-input-data)
* [About the visualization](#about-the-visualization)
    * [Node color](#node-color)
    * [Node sizing](#node-sizing)
    * [Edge color](#edge-color)
* [Filtering the visualization](#filtering-the-visualization)
    * [By minimum referrals](#by-minimum-referrals)
    * [By department](#by-department)
    * [By node pair efficiency](#by-node-pair-efficiency)
* [Flask app demo](#flask-app-demo)
* [Future improvements](#future-improvements)
* [Contributors](#contributors)
* [Acknowledgements](#acknowledgements)

<hr>

## Introduction

At the University of Rochester Medical Center (UR Medicine), referrals typically originate in primary care and are sent out to the appropriate internal and external specialty practices. Ideally, these referrals are sent out upon request and processed immediately, without too much hassle for the medical staff or the patient. Unfortunately, it is not uncommon for bottlenecks to occur in the referral pipeline, leading to extra work for the medical team and added uncertainty for the patient. In this project, our goal is to be able to identify where these bottlenecks are occurring—i.e., which departments and specialties are least efficient, and if there are any referral pathways that are convoluted in particular.

## Getting set up

The source code can be viewed on GitHub [here](https://github.com/jakebrehm/referral-network).

### Required dependencies

This project currently requires a minimum of *Python 3.10*.

Dependencies are handled by the `poetry` package, primarily meant to allow for easy dependency management, but the noteable dependencies are:

- [pandas](https://github.com/pandas-dev/pandas)
- [networkx](https://github.com/networkx/networkx)
- [plotly](https://github.com/plotly/plotly.py)
- [Flask](https://github.com/pallets/flask)

### Installing the dependencies

The first step to setting up this project is to clone this repository. To do this, open a command line instance and change your working directory to the directory you'd like to clone the repository to.

```
cd path/to/clone/repository/to
```

Then, use the following command to clone the repository.

```
git clone https://github.com/jakebrehm/referral-network.git
```

Assuming Python is already installed, make sure that the `poetry` package is installed as well. This package is primarily for easily managing dependencies.

```
pip install poetry
```

Use `pip3` instead of `pip` if you also have Python 2 installed on your machine (this is typically the case by default for certain operating systems like MacOS).

Once `poetry` has been installed, use the following command to install the project dependencies in a virtual environment.

```
poetry install
```

This virtual environment will be stored in an out-of-the-way location. If you'd prefer to store it directly in the project directory, use the following command.

```
poetry config virtualenvs.in-project true
```

## Starting the web application

To activate the virtual environment that was initialized in [Installing the dependencies](#installing-the-dependencies), use the following command.

```
poetry shell
```

Once the virtual environment has been activated, you can start the Flask application by running `app.py`, which is located in the `referral_network` directory.

```
python referral_network/app.py
```

To deactivate the virtual environment and exit the shell at any point, type `exit`. To deactivate the virtual environment without leaving the shell, type `deactivate`, although this usage is much less common.

## Debug mode

To run the Flask application in debug mode, which is recommended if not being used in a production environment until the project is in a more stable state, use the `-d` or `--debug` command line argument.

```
python referral_network/app.py -d
```

This option will display a page that allows the user to determine where the error is occurring. It will also send all logging messages to the console instead of to a file that is stored on disk.

## Formatting the input data

The input data must be in *CSV* format with a header, and include the columns that match the schema shown in the table below.

| Column Name | Date Type | Description |
| ----------- | --------- | ----------- |
| Referred From | integer | Anonymized ID of referring department |
| Referred To | integer | Anonymized ID of department being referred to |
| Days to Schedule | integer | Number of days to schedule the referral |

## About the visualization

Certain aesthetic choices were made when creating the visualization in order to provide a more intuitive and meaningful experience; the subsections below describe these choices.

Note that hovering over nodes and edges will provide more information about that node or edge.

### Node color

The color of each node in the graph is meant to show at a glance in which direction referrals are flowing.

| Node color | Meaning |
| - | - |
| Brown | Only makes referrals |
| Yellow | Only receives referrals |
| Cyan | Makes and receives referrals |

These colors were specifically selected to take into account potential color blind users.

### Node sizing

Node size is determined by the degree of the node; in this case, this means the number of referrals that are associated with a node.

Nodes that have a non-zero in-degree and a zero out-degree, i.e., only *makes* referrals, will be sized according to the in-degree value.

Nodes that have a zero in-degree and a non-zero out-degree, i.e., only *receive* referrals, will be sized according to the out-degree value.

Nodes that have non-zero in-degrees and out-degrees will be sized according to the sum of these values.

Essentially, node sizing is meant to work in conjunction with node coloring to illustrate how important and central a node is in the network.

### Edge color

The color of an edge is meant to depict how long it takes to schedule a referral between two nodes. In this case, *median* is the aggregation statistic that is used.

| Edge color | Median days to schedule |
| - | - |
| Green | < 15 |
| Orange | 16 - 50 |
| Red | > 51 |

Essentially, the darker an edge is, the longer it takes for referrals to be scheduled between those two nodes.

Currently, we are restricting the tooltip values to only nodes where the number of referrals is above a certain dynamically-calculated threshold.

## Filtering the visualization

The following subsections describe the features of the visualization the can be customized (i.e., that controls appear in the sidebar to manipulate).

### By minimum referrals

*Minimum referrals* is the minimum number of referrals made between two nodes for it to appear in the visualization.

### By department

It is possible to filter the visualization by department, i.e., only referrals that are related to the specified department will be considered.

### By node pair efficiency

*Node pair efficiency* is a measure of how efficient a node pair is in processing referrals. It is calculated by dividing the total number of referrals made between two nodes by the total number of days needed to schedule those referrals. Then, once all node pair efficiencies have been calculated, min-max normalization is applied; thus, an efficiency of 0 represents the least efficient node in terms of processing referrals, where 1 indicates the opposite.

## Future improvements

The following potential improvements are listed in no particular order.

- Allow support for uploading Excel spreadsheets in addition to CSV files
- Add tooltips to UI items such as the customizability controls
- Implement a memory of the visualization settings between sessions
- Added more customizability to the visualization via the sidebar
- Should check if CSV file is formatted correctly, and return an error if not
- Need to sanitize input, e.g., negative minimum referral values should be prohibited

<hr>

## Contributors

- **Jake Brehm** - [Email](mailto:mail@jakebrehm.com) | [LinkedIn](http://linkedin.com/in/jacobbrehm) | [Github](http://github.com/jakebrehm)
- **Sayan Swar** - [Email](mailto:sayankrswar@hotmail.com) | [LinkedIn](http://linkedin.com/in/sayankrswar) | [Github](http://github.com/skswar)

## Acknowledgements

We thank [Dr. Kathleen Fear](https://www.linkedin.com/in/kathleen-fear/) (UR Medicine) and [Dr. Justin Zelenka](https://www.urmc.rochester.edu/people/29494170-justin-zelenka) (UR Medicine) for providing the opportunity to conduct research on this subject, providing data, and regularly engaging with us in helpful discussions.
