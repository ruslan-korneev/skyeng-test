#!/bin/bash

skyeng collectstatic --noinput
skyeng migrate
"$@"