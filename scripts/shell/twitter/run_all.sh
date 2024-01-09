ROOT_DIR=$(dirname "$0")

sh $ROOT_DIR/run_update_post_tasks_twitter.sh &
sh $ROOT_DIR/run_check_post_tasks_twitter.sh &
sh $ROOT_DIR/run_get_post_tasks_twitter.sh &
sh $ROOT_DIR/run_update_comment_tasks_twitter.sh &
sh $ROOT_DIR/run_check_comment_tasks_twitter.sh &
sh $ROOT_DIR/run_get_comments_data_twitter.sh