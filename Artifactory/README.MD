### Description
The script ***cleanup_old_docker_images_manual.py*** is used for controlled one-time cleaning of repositories. The script ***cleanup_old_docker_images_automate.py*** will be executed as a cronjob in k8s.


#### cleanup_old_docker_images_manual.py script:

1. Constructs an AQL query to search only by the artifact's creation time.
2. Executes the query and outputs the found artifacts.
3. Deletes the artifacts if the --dry-run parameter is not specified.
4. The tag "latest" is not included in the deletion filter.
5. 5 last unique tags always remains.
6. All deleted artifacts can be restored from the Trash can.


#### cleanup_old_docker_images_automate.py script:

Does all the same for all artifacts in repositories that fall under the *-docker-snapshots filter

### Execution examples:

##### Output example:
```bash
2024-06-21 16:52:25,217 - INFO - {
    "repo": "docker-test-local",
    "path": "position-keeping/2023-01-19-05-11-release-st-f65bd37b5",
    "name": "manifest.json",
    "created": "2023-01-19T05:12:53.797Z"
}
2024-06-21 16:52:25,218 - INFO - [DRY RUN] Will be deleted: https://artifactory.example.com/artifactory/docker-test-local/position-keeping/2023-01-19-05-11-release-st-f65bd37b5
2024-06-21 16:52:25,218 - INFO - {
    "repo": "docker-test-local",
    "path": "position-keeping/2023-02-10-06-46-develop-52f503e0c",
    "name": "manifest.json",
    "created": "2023-02-10T06:49:08.096Z"
}
2024-06-21 16:52:25,219 - INFO - [DRY RUN] Will be deleted: https://artifactory.example.com/artifactory/docker-test-local/position-keeping/2023-02-10-06-46-develop-52f503e0c
```

#### cleanup_old_docker_images_manual.py
##### Dry-run output example:
```bash
# python3 cleanup_old_docker_images_manual.py --repo-name docker-test-local --created 1y --dry-run

2024-06-21 13:11:59,809 - INFO - {
    "repo": "docker-test-local",
    "path": "psd2-ccc/2019-10-02_10-snapshot-fcc731b",
    "name": "manifest.json",
    "created": "2019-10-02T10:52:13.247Z"
}
2024-06-21 13:12:01,141 - INFO - Deleted: https://artifactory.example.com/artifactory/docker-test-local/psd2-ccc/2019-10-02_10-snapshot-fcc731b
2024-06-21 13:12:01,142 - INFO - {
    "repo": "docker-test-local",
    "path": "bridge-id/2019-08-14_12-master-22f96f9",
    "name": "manifest.json",
    "created": "2019-08-14T12:06:34.727Z"
}
2024-06-21 13:12:01,988 - INFO - Deleted: https://artifactory.example.com/artifactory/docker-test-local/bridge-id/2019-08-14_12-master-22f96f9
```

#### cleanup_old_docker_images_automate.py
##### Output example:
```bash
# python3 cleanup_old_docker_images_automate.py --created 1m
2024-07-24 13:02:59,645 - INFO - Cleaning up repository: hello-docker-releases
2024-07-24 13:03:00,134 - INFO - Nothing to clean up in repository: hello-docker-releases
2024-07-24 13:03:00,135 - INFO - Cleaning up repository: hello-docker-snapshots
2024-07-24 13:03:00,614 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.23-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:51.218Z"
}
2024-07-24 13:03:01,542 - INFO - Deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.23-perl
----------------------------------
2024-07-24 13:03:01,544 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.24-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:29.876Z"
}
2024-07-24 13:03:02,296 - INFO - Deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.24-perl
----------------------------------
2024-07-24 13:03:02,298 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.25-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:09.242Z"
}
2024-07-24 13:03:03,113 - INFO - Deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.25-perl
```

##### Dry-run output example:
```bash
# python3 cleanup_old_docker_images_automate.py --created 1m --dry-run
2024-07-24 12:58:25,307 - INFO - Cleaning up repository: hello-docker-releases
2024-07-24 12:58:25,792 - INFO - Nothing to clean up in repository: hello-docker-releases
2024-07-24 12:58:25,793 - INFO - Cleaning up repository: hello-docker-snapshots
2024-07-24 12:58:26,272 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.23-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:51.218Z"
}
2024-07-24 12:58:26,272 - INFO - [DRY RUN] Will be deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.23-perl
----------------------------------
2024-07-24 12:58:26,273 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.24-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:29.876Z"
}
2024-07-24 12:58:26,273 - INFO - [DRY RUN] Will be deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.24-perl
----------------------------------
2024-07-24 12:58:26,274 - INFO - {
    "repo": "hello-docker-snapshots",
    "path": "nginx/1.25-perl",
    "name": "manifest.json",
    "created": "2024-07-24T10:48:09.242Z"
}
2024-07-24 12:58:26,274 - INFO - [DRY RUN] Will be deleted: https://artifactory.example.com/artifactory/hello-docker-snapshots/nginx/1.25-perl
```
