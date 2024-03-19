#!/bin/bash
cd /Users/user/nwd_ig_crawler/sdc

# Updated LOG_PATH to include the YYYYMMDD format
DATE=$(date +%Y%m%d) # Changed to match the YYYYMMDD format
LOG_PATH="/Users/user/nwd_ig_crawler/scheduler/logs/${DATE}"

# Create the log directory if it doesn't exist
mkdir -p "$LOG_PATH"


TOPIC='DC'

run_command_with_retries() {
    local command=$1
    local log_file=$2
    local max_attempts=10
    local attempt=1
    local exit_status

    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt for $command" >> "${LOG_PATH}/${DATE}${log_file}.log"
        /usr/bin/python3 /Users/user/nwd_ig_crawler/sdc/ro.py $command >> "${LOG_PATH}/${DATE}${log_file}.log" 2>&1
        exit_status=$?
        if [ $exit_status -eq 0 ]; then
            echo "$command completed successfully on attempt $attempt." >> "${LOG_PATH}/${DATE}${log_file}.log"
            return 0
        else
            echo "$command failed with exit status $exit_status on attempt $attempt." >> "${LOG_PATH}/${DATE}${log_file}.log"
        fi
        attempt=$((attempt + 1))
    done

    /usr/bin/python3 /Users/user/nwd_ig_crawler/scheduler/send_email.py --topic "error" --subtopic "${TOPIC}-$command"
    return $exit_status
}

main_retry_limit=3
main_attempt=0

while [ $main_attempt -lt $main_retry_limit ]; do
    main_attempt=$((main_attempt + 1))
    echo "Main attempt $main_attempt of $main_retry_limit"
    
    # Run each command with retries in the background
    run_command_with_retries "dc_crawl hashtag" "dc_hashtag" &
    PID1=$!
    run_command_with_retries "dc_crawl location" "dc_location" &
    PID2=$!
    run_command_with_retries "dc_crawl user" "dc_user" &
    PID3=$!

    # Wait for all commands to complete
    wait $PID1
    STATUS1=$?
    wait $PID2
    STATUS2=$?
    wait $PID3
    STATUS3=$?

    # Only check if all commands succeeded on the final attempt
    if [ $main_attempt -eq $main_retry_limit ]; then
        all_success=true  # Assume success, then check each status
        if [ $STATUS1 -ne 0 ] || [ $STATUS2 -ne 0 ] || [ $STATUS3 -ne 0 ]; then
            all_success=false  # Set to false if any command failed
            break  # No need to loop again if we're on the last attempt
        fi
    fi
done

# If all commands succeeded, run the final command and send a success email
if $all_success; then
    if /usr/bin/python3 /Users/user/nwd_ig_crawler/sdc/ro.py dc_upload >> "${LOG_PATH}/${DATE}dc_upload.log" 2>&1; then
        /usr/bin/python3 /Users/user/nwd_ig_crawler/scheduler/send_email.py --topic "${TOPIC}" --subtopic "success"
    else
        echo "dc_upload failed. Check ${LOG_PATH}/${DATE}dc_upload.log for details." >> "${LOG_PATH}/${DATE}dc_upload.log"
        /usr/bin/python3 /Users/user/nwd_ig_crawler/scheduler/send_email.py --topic "error" --subtopic "${TOPIC}-upload"
    fi
else
    echo "Not all commands succeeded after $main_retry_limit attempts. Check logs for details."
    # Optionally, handle the case where not all commands succeeded after retries.
fi
