#!/bin/sh

task='create'
platforms='tiktok linkedin instagram facebook twitter'

for platform in $platforms; do
    /home/fasih/k_cluster_smar/venv/bin/python \
        scripts/admin/${task}_topic.py -t "${platform}_posts,${platform}_post_tasks,${platform}_post_task_finished,${platform}_comments,${platform}_comment_tasks,${platform}_comment_tasks_finished"
done
