"""The SkyPilot package."""
import os
import subprocess
from typing import Optional
import urllib.request

# Replaced with the current commit when building the wheels.
_SKYPILOT_COMMIT_SHA = '{{SKYPILOT_COMMIT_SHA}}'


def _get_git_commit():
    if 'SKYPILOT_COMMIT_SHA' not in _SKYPILOT_COMMIT_SHA:
        # This is a release build, so we don't need to get the commit hash from
        # git, as it's already been set.
        return _SKYPILOT_COMMIT_SHA

    # This is a development build (pip install -e .), so we need to get the
    # commit hash from git.
    try:
        cwd = os.path.dirname(__file__)
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            cwd=cwd,
            universal_newlines=True,
            stderr=subprocess.DEVNULL).strip()
        changes = subprocess.check_output(['git', 'status', '--porcelain'],
                                          cwd=cwd,
                                          universal_newlines=True,
                                          stderr=subprocess.DEVNULL).strip()
        if changes:
            commit_hash += '-dirty'
        return commit_hash
    except Exception:  # pylint: disable=broad-except
        return _SKYPILOT_COMMIT_SHA


__commit__ = _get_git_commit()
__version__ = '0.8.0'
__root_dir__ = os.path.dirname(os.path.abspath(__file__))


# ---------------------- Proxy Configuration ---------------------- #
def _set_http_proxy_env_vars() -> None:
    urllib_proxies = dict(urllib.request.getproxies())

    def set_proxy_env_var(proxy_var: str, urllib_var: Optional[str]):
        """Sets proxy env vars in os.environ, consulting urllib if needed.

        Logic:
        - If either PROXY_VAR or proxy_var is set in os.environ, set both to the
          same value in os.environ.
        - Else, if urllib_var is set in urllib.request.getproxies(), use that
          value to set PROXY_VAR and proxy_var in os.environ.

        Although many of our underlying libraries are case-insensitive when it
        comes to proxy environment variables, some are not. This has happened to
        GCP's SDK not respecting certain VPN-related proxy env vars.

        This function ensures that both the upper and lower case versions of the
        proxy environment variables are set if either is set to ensure maximum
        compatibility.
        """
        # Check for the uppercase version first
        proxy = os.getenv(proxy_var.upper(), os.getenv(proxy_var.lower()))
        if proxy is None and urllib_var is not None:
            proxy = urllib_proxies.get(urllib_var)

        if proxy is not None:
            os.environ[proxy_var.lower()] = proxy
            os.environ[proxy_var.upper()] = proxy

    set_proxy_env_var('http_proxy', 'http')
    set_proxy_env_var('https_proxy', 'https')
    set_proxy_env_var('all_proxy', None)


_set_http_proxy_env_vars()
# ----------------------------------------------------------------- #

# Keep this order to avoid cyclic imports
# pylint: disable=wrong-import-position
from sky import backends
from sky import benchmark
from sky import clouds
from sky.admin_policy import AdminPolicy
from sky.admin_policy import MutatedUserRequest
from sky.admin_policy import UserRequest
from sky.clouds.service_catalog import list_accelerators
from sky.core import autostop
from sky.core import cancel
from sky.core import cost_report
from sky.core import down
from sky.core import download_logs
from sky.core import job_status
from sky.core import queue
from sky.core import start
from sky.core import status
from sky.core import stop
from sky.core import storage_delete
from sky.core import storage_ls
from sky.core import tail_logs
from sky.dag import Dag
from sky.data import Storage
from sky.data import StorageMode
from sky.data import StoreType
from sky.execution import exec  # pylint: disable=redefined-builtin
from sky.execution import launch
from sky.jobs import ManagedJobStatus
from sky.optimizer import Optimizer
from sky.optimizer import OptimizeTarget
from sky.resources import Resources
from sky.skylet.job_lib import JobStatus
from sky.skypilot_config import Config
from sky.status_lib import ClusterStatus
from sky.task import Task

# Aliases.
IBM = clouds.IBM
AWS = clouds.AWS
Azure = clouds.Azure
Cudo = clouds.Cudo
GCP = clouds.GCP
Lambda = clouds.Lambda
SCP = clouds.SCP
Kubernetes = clouds.Kubernetes
K8s = Kubernetes
OCI = clouds.OCI
Paperspace = clouds.Paperspace
RunPod = clouds.RunPod
Vast = clouds.Vast
Vsphere = clouds.Vsphere
Fluidstack = clouds.Fluidstack
optimize = Optimizer.optimize

__all__ = [
    '__version__',
    'AWS',
    'Azure',
    'Cudo',
    'GCP',
    'IBM',
    'Kubernetes',
    'K8s',
    'Lambda',
    'OCI',
    'Paperspace',
    'RunPod',
    'Vast',
    'SCP',
    'Vsphere',
    'Fluidstack',
    'Optimizer',
    'OptimizeTarget',
    'backends',
    'benchmark',
    'list_accelerators',
    '__root_dir__',
    'Storage',
    'StorageMode',
    'StoreType',
    'ClusterStatus',
    'JobStatus',
    'ManagedJobStatus',
    # APIs
    'Dag',
    'Task',
    'Resources',
    # execution APIs
    'launch',
    'exec',
    # core APIs
    'status',
    'start',
    'stop',
    'down',
    'autostop',
    'cost_report',
    # core APIs Job Management
    'queue',
    'cancel',
    'tail_logs',
    'download_logs',
    'job_status',
    # core APIs Storage Management
    'storage_ls',
    'storage_delete',
    # Admin Policy
    'UserRequest',
    'MutatedUserRequest',
    'AdminPolicy',
    'Config',
]
