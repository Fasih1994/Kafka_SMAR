#!/bin/sh

task='create'
platforms='tiktok linkedin instagram facebook twitter'
working_dir=$(pwd)

for platform in $platforms; do
    "${working_dir}/venv/bin/python" \
        scripts/admin/${task}_topic.py -t "${platform}_posts,${platform}_post_tasks,${platform}_post_task_finished,${platform}_comments,${platform}_comment_tasks,${platform}_comment_tasks_finished"
done
