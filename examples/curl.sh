#!/usr/bin/env bash
# 爱奇艺 API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the iQIYI API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search 纪录片
#   bash examples/curl.sh video "<video url>" # search 结果里 v_ 开头的 url / a v_ url from a search result
#   bash examples/curl.sh album 苍兰诀
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|video|album> <value>"}
value=${2:?"value: a keyword or a video url"}

case "$action" in
  search | album) params="{\"keyword\":\"$value\"}" ;;
  video)          params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, video or album)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"iqiyi\",\"action\":\"$action\",\"params\":$params}"
echo
