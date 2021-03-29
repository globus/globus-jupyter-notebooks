# globus-jupyter-notebooks

## Install

These notebooks require Python 3.6+. See
http://docs.python-guide.org/en/latest/starting/installation/
for easy Python installation instructions.

You may need to install pip and virtualenv first.  For example, on macOS:

    sudo easy_install pip
    sudo pip install virtualenv

Clone the globus-jupyter-notebooks git reporsitory:

    git clone https://github.com/globus/globus-jupyter-notebooks.git

Create a virtualenv:

    cd globus-jupyter-notebooks
    virtualenv venv
    . ./venv/bin/activate

Install the notebook requirements using pip:

    pip install -r requirements.txt

## Run

To open a browser window with the Jupyter notebook interface:

    jupyter-notebook Platform_Introduction_Native_App_Auth.ipynb

If running remotely, for example, in a tutorial EC2 instance:

    jupyter notebook --ip="*" --no-browser

## Links

* Globus SDK Documentation http://globus.github.io/globus-sdk-python/
* Globus SDK Source: https://github.com/globus/globus-sdk-python
* Globus CLI Source: https://github.com/globus/globus-cli

## Troubleshooting

### pip install fails with message about Python.h

If `pip install -r requirements.txt` fails with a message including

    Python.h: No such file or directory

it likely means that you don't have the python development headers installed.

Getting the headers is platform dependent.

On macOS this issue should not occur.

On Ubuntu:

    sudo apt-get install python-dev

On RHEL and CentOS:

    sudo yum install python-devel
