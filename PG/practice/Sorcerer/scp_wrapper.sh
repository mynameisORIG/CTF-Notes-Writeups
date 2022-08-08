#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'bash'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "Let's figure it out"
    bash
    ;;
esac
