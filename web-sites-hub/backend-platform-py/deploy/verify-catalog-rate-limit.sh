#!/usr/bin/env bash
# Burst-test GET catalog rate limit (poems / snippets).
#
# Usage:
#   ./deploy/verify-catalog-rate-limit.sh
#   ./deploy/verify-catalog-rate-limit.sh --url https://showcase.joketop.com/api/v1/poems/meta/wordcloud
#   ./deploy/verify-catalog-rate-limit.sh --burst 130 --expect-limit 120
#
# Exit 0 if at least one HTTP 429 observed when burst > expect-limit; 1 otherwise.

set -euo pipefail

URL="${URL:-https://showcase.joketop.com/api/v1/poems/meta/wordcloud}"
BURST="${BURST:-130}"
EXPECT_LIMIT="${EXPECT_LIMIT:-120}"
CONNECT_TIMEOUT=8
MAX_TIME=20

usage() {
    sed -n '2,9p' "$0" | sed 's/^# \?//'
}

while [ $# -gt 0 ]; do
    case "$1" in
        --url)
            URL="${2:?missing value for --url}"
            shift 2
            ;;
        --burst)
            BURST="${2:?missing value for --burst}"
            shift 2
            ;;
        --expect-limit)
            EXPECT_LIMIT="${2:?missing value for --expect-limit}"
            shift 2
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

if ! [[ "$BURST" =~ ^[0-9]+$ ]] || [ "$BURST" -lt 1 ]; then
    echo "Invalid --burst: $BURST" >&2
    exit 2
fi

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN} Catalog rate-limit probe${NC}"
echo -e "${CYAN}========================================${NC}"
echo "URL:          $URL"
echo "Burst:        $BURST requests (sequential)"
echo "Expect limit: ~${EXPECT_LIMIT}/60s per IP (env CATALOG_RATE_LIMIT_MAX_REQUESTS)"
echo ""

count_200=0
count_429=0
count_other=0
first_429_at=0

i=1
while [ "$i" -le "$BURST" ]; do
    code="$(
        curl -sS -o /dev/null -w '%{http_code}' \
            --connect-timeout "$CONNECT_TIMEOUT" \
            --max-time "$MAX_TIME" \
            "$URL" || echo "000"
    )"
    case "$code" in
        200) count_200=$((count_200 + 1)) ;;
        429)
            count_429=$((count_429 + 1))
            if [ "$first_429_at" -eq 0 ]; then
                first_429_at=$i
            fi
            ;;
        *) count_other=$((count_other + 1)) ;;
    esac
    i=$((i + 1))
done

echo -e "${CYAN}--- Results ---${NC}"
echo "HTTP 200: $count_200"
echo "HTTP 429: $count_429"
echo "Other:    $count_other (incl. network errors as 000)"
if [ "$first_429_at" -gt 0 ]; then
    echo "First 429 at request #: $first_429_at"
fi
echo ""

if [ "$count_200" -gt 0 ]; then
    echo -e "${GREEN}Sample OK:${NC} endpoint reachable (got $count_200 x 200)"
fi

if [ "$count_429" -gt 0 ]; then
    echo -e "${GREEN}[PASS]${NC} Rate limiting active ($count_429/$BURST returned 429)"
    if [ "$first_429_at" -gt 0 ] && [ "$first_429_at" -le $((EXPECT_LIMIT + 5)) ]; then
        echo -e "${GREEN}       ${NC} First 429 near expected quota (~$EXPECT_LIMIT) — looks correct"
    elif [ "$first_429_at" -gt $((EXPECT_LIMIT + 5)) ]; then
        echo -e "${YELLOW}[NOTE]${NC} First 429 at #$first_429_at (expected around #$((EXPECT_LIMIT + 1)))"
    fi
    exit 0
fi

if [ "$BURST" -le "$EXPECT_LIMIT" ]; then
    echo -e "${YELLOW}[SKIP]${NC} Burst ($BURST) <= expect-limit ($EXPECT_LIMIT); increase --burst to trigger 429"
    exit 2
fi

echo -e "${RED}[FAIL]${NC} No 429 after $BURST requests — catalog rate limit may be off or quota very high"
exit 1
