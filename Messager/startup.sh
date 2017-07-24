#!/usr/bin/env bash

export YHD_USERNAME='username'
export YHD_PASSWORD='pwd'
export YHD_ADV_MESSAGE='msg'
export YHD_OUTPUT_DIR='output_folder_path'
export YHD_WEBDRIVER_PATH='phantomjs driver path'

python ADMain.py -d $YHD_OUTPUT_DIR -wp $YHD_WEBDRIVER_PATH -u $YHD_USERNAME -p $YHD_PASSWORD -m "$YHD_ADV_MESSAGE"

