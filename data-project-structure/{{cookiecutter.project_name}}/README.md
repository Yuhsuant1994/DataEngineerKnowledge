{{cookiecutter.project_name}}
Author: {{cookiecutter.author}}

Project Structure:


├── Makefile                     <- Makefile with commands like `make data` or `make train`
├── README.md                    <- The top-level README for developers using this project.
├── data
│   ├── interim                  <- Intermediate data that has been transformed.
│   ├── processed                <- The final, canonical data sets for modeling.
│   └── raw                      <- The original, immutable data dump.
│
├── docs                         <- A default Sphinx project; see sphinx-doc.org for details
│
├── models                       <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks                    <- Jupyter notebooks. Naming convention is a number (for ordering),
│                                   the creator's initials, and a short `-` delimited description, e.g.
│                                   `1.0-jqp-initial-data-exploration`.
│
├── requirements.txt             <- The requirements file for reproducing the analysis environment, e.g.
│                                   generated with `pip freeze > requirements.txt`
│
├── run.py                       <- Automation tool will look for this file to execute command line
|                                   statements
├── setup.py                     <- Make this project pip installable with `pip install -e`
├── setup.cfg                    <- Contains configuration for setup
├── src                          <- Source code for use in this project.
│   ├── __init__.py              <- Makes src a Python module
|
├── .pre-commit-config.yaml      <- Configuration file for pre-commit. Generally includes congigurations
|                                   for flake8 and black
└── .gitignore                   <- Git ignores file extensions and folders mentioned here
                                    e.g. *.pyc, *.csv