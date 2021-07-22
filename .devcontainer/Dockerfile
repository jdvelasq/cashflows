# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
ARG VARIANT="3.9"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN apt-get update \
    && apt-get -yq --no-install-recommends install  pandoc  make \
    && apt-get clean \
    && apt-get autoremove -yq \
    && rm -rf /var/lib/apt/lists/* 

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    bandit \
    black \
    flake8 \
    isort \
    jedi \
    mypy \
    nose \
    poetry \
    prospector \
    pycodestyle \
    pylama \
    pylint \
    pytest \
    rope \
    yapf

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    twine \
    setuptools \
    wheel 

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    nbsphinx \
    sphinx-rtd-theme \ 
    sphinx_copybutton \    
    pygments     

RUN pip3 --disable-pip-version-check --no-cache-dir install \
    numpy \
    matplotlib \
    graphviz \
    ipykernel \
    pandas

RUN apt update \
    && apt -yq --no-install-recommends install  graphviz \
    && apt clean \
    && apt autoremove -yq \
    && rm -rf /var/lib/apt/lists/* 


# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1