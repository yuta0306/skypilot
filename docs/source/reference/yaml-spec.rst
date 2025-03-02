.. _yaml-spec:

SkyPilot YAML
=============

SkyPilot provides an intuitive YAML interface to specify clusters, jobs, or
services (resource requirements, setup commands, run commands, file mounts,
storage mounts, and so on).

YAMLs can be used with the :ref:`CLI <cli>`, or the programmatic API (e.g., :meth:`sky.Task.from_yaml`).

Available fields:

.. code-block:: yaml

    # Task name (optional), used for display purposes.
    name: my-task

    # Working directory (optional), synced to ~/sky_workdir on the remote cluster
    # each time launch or exec is run with the yaml file.
    #
    # Commands in "setup" and "run" will be executed under it.
    #
    # If a relative path is used, it's evaluated relative to the location from
    # which `sky` is called.
    #
    # To exclude files from syncing, see
    # https://docs.skypilot.co/en/latest/examples/syncing-code-artifacts.html#exclude-uploading-files
    workdir: ~/my-task-code

    # Number of nodes (optional; defaults to 1) to launch including the head node.
    #
    # A task can set this to a smaller value than the size of a cluster.
    num_nodes: 4

    # Per-node resource requirements (optional).
    resources:
      cloud: aws  # The cloud to use (optional).

      # The region to use (optional). Auto-failover will be disabled
      # if this is specified.
      region: us-east-1

      # The zone to use (optional). Auto-failover will be disabled
      # if this is specified.
      zone: us-east-1a

      # Accelerator name and count per node (optional).
      #
      # Use `sky show-gpus` to view available accelerator configurations.
      #
      # The following three ways are valid for specifying accelerators for a cluster:
      #
      #   To specify a single type of accelerator:
      #     Format: <name>:<count> (or simply <name>, short for a count of 1).
      #     accelerators: H100:4
      #
      #   To specify an ordered list of accelerators (try the accelerators in
      #   the specified order):
      #     Format: [<name>:<count>, ...]
      #     accelerators: ['L4:1', 'H100:1', 'A100:1']
      #
      #   To specify an unordered set of accelerators (optimize all specified
      #   accelerators together, and try accelerator with lowest cost first):
      #     Format: {<name>:<count>, ...}
      #     accelerators: {'L4:1', 'H100:1', 'A100:1'}
      accelerators: H100:8

      # Number of vCPUs per node (optional).
      #
      # Format:
      #   <count>: exactly <count> vCPUs
      #   <count>+: at least <count> vCPUs
      #
      # E.g., 4+ means first try to find an instance type with >= 4 vCPUs. If
      # not found, use the next cheapest instance with more than 4 vCPUs.
      cpus: 4+

      # Memory in GiB per node (optional).
      #
      # Format:
      #  <num>: exactly <num> GiB
      #  <num>+: at least <num> GiB
      #
      # E.g., 32+ means first try to find an instance type with >= 32 GiB. If
      # not found, use the next cheapest instance with more than 32 GiB.
      memory: 32+

      # Instance type to use (optional). If 'accelerators' is specified,
      # the corresponding instance type is automatically inferred.
      instance_type: p3.8xlarge

      # Whether the cluster should use spot instances (optional).
      # If unspecified, defaults to False (on-demand instances).
      use_spot: False

      # The recovery strategy for managed jobs (optional).
      #
      # In effect for managed jobs. Possible values are `FAILOVER` and `EAGER_NEXT_REGION`.
      #
      # If `FAILOVER` is specified, the job will be restarted in the same region
      # if the node fails, and go to the next region if no available resources
      # are found in the same region.
      #
      # If `EAGER_NEXT_REGION` is specified, the job will go to the next region
      # directly if the node fails. This is useful for spot instances, as in
      # practice, preemptions in a region usually indicate a shortage of resources
      # in that region.
      #
      # default: EAGER_NEXT_REGION
      job_recovery: none
      # Or, to allow up to 3 restarts (default: 0) on user code errors:
      # job_recovery:
      #   strategy: EAGER_NEXT_REGION
      #   max_restarts_on_errors: 3

      # Disk size in GB to allocate for OS (mounted at /). Increase this if you
      # have a large working directory or tasks that write out large outputs.
      disk_size: 256

      # Disk tier to use for OS (optional).
      # Could be one of 'low', 'medium', 'high', 'ultra' or 'best' (default: 'medium').
      # if 'best' is specified, use the best disk tier enabled.
      # Rough performance estimate:
      #   low: 1000 IOPS; read 90 MB/s; write 90 MB/s
      #   medium: 3000 IOPS; read 220 MB/s; write 220 MB/s
      #   high: 6000 IOPS; read 400 MB/s; write 400 MB/s
      #   ultra: 60000 IOPS;  read 4000 MB/s; write 3000 MB/s
      # Measured by examples/perf/storage_rawperf.yaml
      disk_tier: medium

      # Ports to expose (optional).
      #
      # All ports specified here will be exposed to the public Internet. Under
      # the hood, a firewall rule / inbound rule is automatically added to allow
      # inbound traffic to these ports. Applies to all VMs of a cluster created
      # with this field set.
      #
      # Currently only TCP protocol is supported.
      #
      # Ports Lifecycle:
      # A cluster's ports will be updated whenever `sky launch` is executed.
      # When launching an existing cluster, any new ports specified will be
      # opened for the cluster, and the firewall rules for old ports will never
      # be removed until the cluster is terminated.
      #
      # Could be an integer, a range, or a list of integers and ranges:
      #   To specify a single port:
      #     ports: 8081
      #   To specify a port range:
      #     ports: 10052-10100
      #   To specify multiple ports / port ranges:
      #     ports:
      #       - 8080
      #       - 10022-10040
      ports: 8081

      # Additional accelerator metadata (optional); only used for TPU node
      # and TPU VM.
      # Example usage:
      #
      #   To request a TPU VM:
      #     accelerator_args:
      #       tpu_vm: True (optional, default: True)
      #
      #   To request a TPU node:
      #     accelerator_args:
      #       tpu_name: ...
      #       tpu_vm: False
      #
      # By default, the value for "runtime_version" is decided based on which is
      # requested and should work for either case. If passing in an incompatible
      # version, GCP will throw an error during provisioning.
      accelerator_args:
        # Default is "tpu-vm-base" for TPU VM and "2.12.0" for TPU node.
        runtime_version: tpu-vm-base
      # tpu_name: mytpu
      # tpu_vm: True  # True to use TPU VM (the default); False to use TPU node.

      # Custom image id (optional, advanced). The image id used to boot the
      # instances. Only supported for AWS, GCP, OCI and IBM (for non-docker image).
      # If not specified, SkyPilot will use the default debian-based image
      # suitable for machine learning tasks.
      #
      # Docker support
      # You can specify docker image to use by setting the image_id to
      # `docker:<image name>` for Azure, AWS and GCP. For example,
      #   image_id: docker:ubuntu:latest
      # Currently, only debian and ubuntu images are supported.
      # If you want to use a docker image in a private registry, you can specify your
      # username, password, and registry server as task environment variable. For
      # details, please refer to the `envs` section below.
      #
      # AWS
      # To find AWS AMI ids: https://leaherb.com/how-to-find-an-aws-marketplace-ami-image-id
      # You can also change the default OS version by choosing from the
      # following image tags provided by SkyPilot:
      #   image_id: skypilot:gpu-ubuntu-2004
      #   image_id: skypilot:k80-ubuntu-2004
      #   image_id: skypilot:gpu-ubuntu-1804
      #   image_id: skypilot:k80-ubuntu-1804
      #
      # It is also possible to specify a per-region image id (failover will only
      # go through the regions specified as keys; useful when you have the
      # custom images in multiple regions):
      #   image_id:
      #     us-east-1: ami-0729d913a335efca7
      #     us-west-2: ami-050814f384259894c
      #
      # GCP
      # To find GCP images: https://cloud.google.com/compute/docs/images
      # image_id: projects/deeplearning-platform-release/global/images/common-cpu-v20230615-debian-11-py310
      # Or machine image: https://cloud.google.com/compute/docs/machine-images
      # image_id: projects/my-project/global/machineImages/my-machine-image
      #
      # Azure
      # To find Azure images: https://docs.microsoft.com/en-us/azure/virtual-machines/linux/cli-ps-findimage
      # image_id: microsoft-dsvm:ubuntu-2004:2004:21.11.04
      #
      # OCI
      # To find OCI images: https://docs.oracle.com/en-us/iaas/images
      # You can choose the image with OS version from the following image tags
      # provided by SkyPilot:
      #   image_id: skypilot:gpu-ubuntu-2204
      #   image_id: skypilot:gpu-ubuntu-2004
      #   image_id: skypilot:gpu-oraclelinux9
      #   image_id: skypilot:gpu-oraclelinux8
      #   image_id: skypilot:cpu-ubuntu-2204
      #   image_id: skypilot:cpu-ubuntu-2004
      #   image_id: skypilot:cpu-oraclelinux9
      #   image_id: skypilot:cpu-oraclelinux8
      #
      # It is also possible to specify your custom image's OCID with OS type,
      # for example:
      #   image_id: ocid1.image.oc1.us-sanjose-1.aaaaaaaaywwfvy67wwe7f24juvjwhyjn3u7g7s3wzkhduxcbewzaeki2nt5q:oraclelinux
      #   image_id: ocid1.image.oc1.us-sanjose-1.aaaaaaaa5tnuiqevhoyfnaa5pqeiwjv6w5vf6w4q2hpj3atyvu3yd6rhlhyq:ubuntu
      #
      # IBM
      # Create a private VPC image and paste its ID in the following format:
      # image_id: <unique_image_id>
      # To create an image manually:
      # https://cloud.ibm.com/docs/vpc?topic=vpc-creating-and-using-an-image-from-volume.
      # To use an official VPC image creation tool:
      # https://www.ibm.com/cloud/blog/use-ibm-packer-plugin-to-create-custom-images-on-ibm-cloud-vpc-infrastructure
      # To use a more limited but easier to manage tool:
      # https://github.com/IBM/vpc-img-inst
      image_id: ami-0868a20f5a3bf9702

      # Labels to apply to the instances (optional).
      #
      # If specified, these labels will be applied to the VMs or pods created
      # by SkyPilot. These are useful for assigning metadata that may be
      # used by external tools. Implementation depends on the chosen cloud -
      # On AWS, labels map to instance tags. On GCP, labels map to instance
      # labels. On Kubernetes, labels map to pod labels. On other clouds,
      # labels are not supported and will be ignored.
      #
      # Note: Labels are applied only on the first launch of the cluster. They
      # are not updated on subsequent launches.
      labels:
        my-label: my-value

      # Candidate resources (optional). If specified, SkyPilot will only use
      # these candidate resources to launch the cluster. The fields specified
      # outside of `any_of`, `ordered` will be used as the default values for
      # all candidate resources, and any duplicate fields specified inside
      # `any_of`, `ordered` will override the default values.
      # `any_of:` means that SkyPilot will try to find a resource that matches
      # any of the candidate resources, i.e. the failover order will be decided
      # by the optimizer.
      # `ordered:` means that SkyPilot will failover through the candidate
      # resources with the specified order.
      # Note: accelerators under `any_of` and `ordered` cannot be a list or set.
      any_of:
        - cloud: aws
          region: us-west-2
          accelerators: H100
        - cloud: gcp
          accelerators: H100


    # Environment variables (optional). These values can be accessed in the
    # `file_mounts`, `setup`, and `run` sections below.
    #
    # Values set here can be overridden by a CLI flag:
    # `sky launch/exec --env ENV=val` (if ENV is present).
    #
    # If you want to use a docker image as runtime environment in a private
    # registry, you can specify your username, password, and registry server as
    # task environment variable.  For example:
    #   envs:
    #     SKYPILOT_DOCKER_USERNAME: <username>
    #     SKYPILOT_DOCKER_PASSWORD: <password>
    #     SKYPILOT_DOCKER_SERVER: <registry server>
    #
    # SkyPilot will execute `docker login --username <username> --password
    # <password> <registry server>` before pulling the docker image. For `docker
    # login`, see https://docs.docker.com/engine/reference/commandline/login/
    #
    # You could also specify any of them through the CLI flag if you don't want
    # to store them in your yaml file or if you want to generate them for
    # constantly changing password. For example:
    #   sky launch --env SKYPILOT_DOCKER_PASSWORD=$(aws ecr get-login-password --region us-east-1).
    #
    # For more information about docker support in SkyPilot, please refer to the `image_id` section above.
    envs:
      MY_BUCKET: skypilot-temp-gcs-test
      MY_LOCAL_PATH: tmp-workdir
      MODEL_SIZE: 13b

    file_mounts:
      # Uses rsync to sync local files/directories to all nodes of the cluster.
      #
      # If a relative path is used, it's evaluated relative to the location from
      # which `sky` is called.
      #
      # If symlinks are present, they are copied as symlinks, and their targets
      # must also be synced using file_mounts to ensure correctness.
      /remote/dir1/file: /local/dir1/file
      /remote/dir2: /local/dir2

      # Create a S3 bucket named sky-dataset, uploads the contents of
      # /local/path/datasets to the bucket, and marks the bucket as persistent
      # (it will not be deleted after the completion of this task).
      # Symlinks and their contents are NOT copied.
      #
      # Mounts the bucket at /datasets-storage on every node of the cluster.
      /datasets-storage:
        name: sky-dataset  # Name of storage, optional when source is bucket URI
        source: /local/path/datasets  # Source path, can be local or bucket URI. Optional, do not specify to create an empty bucket.
        store: s3  # Could be either 's3', 'gcs', 'azure', 'r2', 'oci', or 'ibm'; default: None. Optional.
        persistent: True  # Defaults to True; can be set to false to delete bucket after cluster is downed. Optional.
        mode: MOUNT  # Either MOUNT or COPY. Defaults to MOUNT. Optional.

      # Copies a cloud object store URI to the cluster. Can be private buckets.
      /datasets-s3: s3://my-awesome-dataset

      # Demoing env var usage.
      /checkpoint/${MODEL_SIZE}: ~/${MY_LOCAL_PATH}
      /mydir:
        name: ${MY_BUCKET}  # Name of the bucket.
        mode: MOUNT

    # Setup script (optional) to execute on every `sky launch`.
    # This is executed before the 'run' commands.
    #
    # The '|' separator indicates a multiline string. To specify a single command:
    #   setup: pip install -r requirements.txt
    setup: |
      echo "Begin setup."
      pip install -r requirements.txt
      echo "Setup complete."

    # Main program (optional, but recommended) to run on every node of the cluster.
    run: |
      echo "Beginning task."
      python train.py

      # Demoing env var usage.
      echo Env var MODEL_SIZE has value: ${MODEL_SIZE}


.. _task-yaml-experimental:

Experimental configurations
---------------------------

.. note::

  Experimental features and APIs may be changed or removed without any notice.

In additional to the above fields, SkyPilot also supports the following experimental fields in the task YAML:

.. code-block:: yaml

  experimental:
    # Override the configs in ~/.sky/config.yaml from a task level.
    #
    # The following fields can be overridden. Please refer to docs of Advanced
    # Configuration for more details of those fields:
    # https://docs.skypilot.co/en/latest/reference/config.html
    config_overrides:
        docker:
            run_options: ...
        kubernetes:
            pod_config: ...
            provision_timeout: ...
        gcp:
            managed_instance_group: ...
        nvidia_gpus:
            disable_ecc: ...



.. _service-yaml-spec:

SkyServe services
=================

To define a YAML for use for :ref:`services <sky-serve>`, use previously
mentioned fields to describe each replica, then add a ``service`` section to
describe the entire service.

.. code-block:: yaml

    service:

      # Readiness probe (required). Used by SkyServe to check if your service
      # replicas are ready for accepting traffic. If the readiness probe returns
      # a 200, SkyServe will start routing traffic to that replica.
      readiness_probe:
        # Path to probe (required).
        path: /v1/models
        # Post data (optional). If this is specified, the readiness probe will use
        # POST instead of GET, and the post data will be sent as the request body.
        post_data: {'model_name': 'model'}
        # Initial delay in seconds (optional). Defaults to 1200 seconds (20 minutes).
        # Any readiness probe failures during this period will be ignored. This is
        # highly related to your service, so it is recommended to set this value
        # based on your service's startup time.
        initial_delay_seconds: 1200
        # The Timeout in seconds for a readiness probe request (optional).
        # Defaults to 15 seconds. If the readiness probe takes longer than this
        # time to respond, the probe will be considered as failed. This is
        # useful when your service is slow to respond to readiness probe
        # requests. Note, having a too high timeout will delay the detection
        # of a real failure of your service replica.
        timeout_seconds: 15

      # Simplified version of readiness probe that only contains the readiness
      # probe path. If you want to use GET method for readiness probe and the
      # default initial delay, you can use the following syntax:
      readiness_probe: /v1/models

      # One of the two following fields (replica_policy or replicas) is required.

      # Replica autoscaling policy. This describes how SkyServe autoscales
      # your service based on the QPS (queries per second) of your service.
      replica_policy:
        # Minimum number of replicas (required).
        min_replicas: 1
        # Maximum number of replicas (optional). If not specified, SkyServe will
        # use a fixed number of replicas (the same as min_replicas) and ignore
        # any QPS threshold specified below.
        max_replicas: 3
        # Following specs describe the autoscaling policy.
        # Target query per second per replica (optional). SkyServe will scale your
        # service so that, ultimately, each replica manages approximately
        # target_qps_per_replica queries per second. **Autoscaling will only be
        # enabled if this value is specified.**
        target_qps_per_replica: 5
        # Upscale and downscale delay in seconds (optional). Defaults to 300 seconds
        # (5 minutes) and 1200 seconds (20 minutes) respectively. To avoid aggressive
        # autoscaling, SkyServe will only upscale or downscale your service if the
        # QPS of your service is higher or lower than the target QPS for a period
        # of time. This period of time is controlled by upscale_delay_seconds and
        # downscale_delay_seconds. The default values should work in most cases.
        # If you want to scale your service more aggressively, you can set
        # these values to a smaller number.
        upscale_delay_seconds: 300
        downscale_delay_seconds: 1200
      # Simplified version of replica policy that uses a fixed number of
      # replicas:
      replicas: 2

    ##### Fields below describe each replica #####

    # Besides the `service` section, the rest is a regular SkyPilot task YAML.

    resources:
      # Port to run your service on each replica (required). This port will be
      # automatically exposed to the public internet by SkyServe.
      ports: 8080
      # Other resources config...

    # Other fields of your SkyPilot task YAML...

