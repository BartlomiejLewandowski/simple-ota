set -o allexport
source ../.env
set +o allexport
../bin/upload.sh "stg" "f.txt"
