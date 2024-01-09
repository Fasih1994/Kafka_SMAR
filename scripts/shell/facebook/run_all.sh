#!/bin/bash
ROOT_DIR=$(dirname "$0")

sh $ROOT_DIR/run_update_post_tasks.sh &
sh $ROOT_DIR/run_check_post_tasks.sh &
sh $ROOT_DIR/run_get_post_tasks.sh &
sh $ROOT_DIR/run_update_comment_tasks.sh &
sh $ROOT_DIR/run_check_comment_tasks.sh &
sh $ROOT_DIR/run_get_comments_data.sh