#!/bin/bash
case $SSH_ORIGINAL_COMMAND in
 'bash'*)
    $SSH_ORIGINAL_COMMAND
    ;;
 *)
    echo "ACCESS DENIED."
    bash
    ;;
esac
