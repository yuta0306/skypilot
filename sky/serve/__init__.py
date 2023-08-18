"""Modules for SkyServe services."""
from sky.serve.constants import CONTROLLER_PORT
from sky.serve.constants import CONTROLLER_PREFIX
from sky.serve.constants import CONTROLLER_RESOURCES
from sky.serve.constants import CONTROLLER_TEMPLATE
from sky.serve.serve_utils import generate_controller_cluster_name
from sky.serve.serve_utils import generate_controller_yaml_file_name
from sky.serve.serve_utils import generate_remote_task_yaml_file_name
from sky.serve.serve_utils import load_latest_info
from sky.serve.serve_utils import load_reload_replica_result
from sky.serve.serve_utils import load_terminate_service_result
from sky.serve.serve_utils import SERVE_PREHOOK_COMMANDS
from sky.serve.serve_utils import ServeCodeGen
from sky.serve.serve_utils import ServiceHandle
from sky.serve.service_spec import SkyServiceSpec
