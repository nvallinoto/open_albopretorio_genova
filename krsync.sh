#!/bin/bash
#
# https://serverfault.com/questions/741670/rsync-files-to-a-kubernetes-pod
#
# krsync.sh -av --progress --stats src-dir/ pod:/dest-dir
#
# krsync.sh -av --progress --stats src-dir/ pod@namespace:/dest-dir
#
# NB: the pod must have the rsync executable installed for this to work.
#

if [ -z "$KRSYNC_STARTED" ]; then
    export KRSYNC_STARTED=true
    exec rsync --blocking-io --rsh "$0" $@
fi

# Running as --rsh
namespace=''
pod=$1
shift

# If user uses pod@namespace, rsync passes args as: {us} -l pod namespace ...
if [ "X$pod" = "X-l" ]; then
    pod=$1
    shift
    namespace="-n $1"
    shift
fi

exec kubectl $namespace exec -i $pod -- "$@"

