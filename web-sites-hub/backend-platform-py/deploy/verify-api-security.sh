#!/usr/bin/env bash
# Verify known API security posture for backend-platform-py.
#
# Usage:
#   ./deploy/verify-api-security.sh
#   ./deploy/verify-api-security.sh --base https://joketop.com
#   ./deploy/verify-api-security.sh --base http://127.0.0.1:8300
#   ./deploy/verify-api-security.sh --include-write   # mutating probes (register write test)
#   ./deploy/verify-api-security.sh --rate-limit-burst 15
#
# Exit code: 0 if no VULNERABLE findings; 1 otherwise.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BASE_URL="${BASE_URL:-https://joketop.com}"
INCLUDE_WRITE=0
RATE_LIMIT_BURST=0
CURL_CONNECT_TIMEOUT=8
CURL_MAX_TIME=20

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VULN=0
WARN=0
PASS=0
SKIP=0

usage() {
    sed -n '2,12p' "$0" | sed 's/^# \?//'
}

while [ $# -gt 0 ]; do
    case "$1" in
        --base)
            BASE_URL="${2:?missing value for --base}"
            shift 2
            ;;
        --include-write)
            INCLUDE_WRITE=1
            shift
            ;;
        --rate-limit-burst)
            RATE_LIMIT_BURST="${2:?missing value for --rate-limit-burst}"
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

BASE_URL="${BASE_URL%/}"
API="${BASE_URL}/api/v1"

print_header() {
    echo
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN} API security verification${NC}"
    echo -e "${CYAN} Target: ${BASE_URL}${NC}"
    echo -e "${CYAN}========================================${NC}"
}

# http_request METHOD URL [curl-extra-args...]
# Sets globals: HTTP_CODE, RESP_BODY
http_request() {
    local method="$1"
    local url="$2"
    shift 2

    local tmp
    tmp="$(mktemp)"
    HTTP_CODE="$(
        curl -sS \
            --connect-timeout "${CURL_CONNECT_TIMEOUT}" \
            --max-time "${CURL_MAX_TIME}" \
            -X "${method}" \
            -w '%{http_code}' \
            -o "${tmp}" \
            "$@" \
            "${url}" || echo "000"
    )"
    RESP_BODY="$(cat "${tmp}")"
    rm -f "${tmp}"
}

json_field() {
    local expr="$1"
    python3 -c "
import json, sys
try:
    obj = json.loads(sys.stdin.read() or '{}')
except json.JSONDecodeError:
    print('')
    raise SystemExit(0)
def pick(o, path):
    cur = o
    for part in path.split('.'):
        if part.endswith(']'):
            name, idx = part[:-1].split('[', 1)
            cur = cur.get(name, [])
            cur = cur[int(idx)] if isinstance(cur, list) and len(cur) > int(idx) else None
        else:
            cur = cur.get(part) if isinstance(cur, dict) else None
        if cur is None:
            return None
    return cur
val = pick(obj, '''${expr}''')
if val is None:
    print('')
elif isinstance(val, bool):
    print('true' if val else 'false')
elif isinstance(val, (dict, list)):
    import json as j
    print(j.dumps(val, ensure_ascii=False))
else:
    print(val)
" <<<"${RESP_BODY}" 2>/dev/null || true
}

redact_body() {
    python3 -c "
import json, re, sys
raw = sys.stdin.read()
try:
    obj = json.loads(raw)
except json.JSONDecodeError:
    print(raw[:400])
    raise SystemExit(0)

def scrub(o):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if k in {'key', 'access_token', 'refresh_token', 'password'}:
                out[k] = '<redacted>'
            else:
                out[k] = scrub(v)
        return out
    if isinstance(o, list):
        return [scrub(x) for x in o]
    return o

print(json.dumps(scrub(obj), ensure_ascii=False, indent=2)[:1200])
" <<<"${RESP_BODY}" 2>/dev/null || printf '%s' "${RESP_BODY:0:400}"
}

record() {
    local status="$1"
    local id="$2"
    local detail="$3"
    case "${status}" in
        PASS)
            PASS=$((PASS + 1))
            echo -e "${GREEN}[PASS]${NC} ${id}: ${detail}"
            ;;
        VULN)
            VULN=$((VULN + 1))
            echo -e "${RED}[VULN]${NC} ${id}: ${detail}"
            ;;
        WARN)
            WARN=$((WARN + 1))
            echo -e "${YELLOW}[WARN]${NC} ${id}: ${detail}"
            ;;
        SKIP)
            SKIP=$((SKIP + 1))
            echo -e "${YELLOW}[SKIP]${NC} ${id}: ${detail}"
            ;;
    esac
}

run_case() {
    local id="$1"
    local method="$2"
    local path="$3"
    local expect="$4"
    local note="$5"
    shift 5

    local url="${API}${path}"
    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "${method} ${url}"
    echo "Expect: ${expect} | ${note}"

    http_request "${method}" "${url}" "$@"
    echo "HTTP ${HTTP_CODE}"
    echo "Body (redacted):"
    redact_body
    echo

    local success code
    success="$(json_field success)"
    code="$(json_field code)"

    case "${expect}" in
        protected)
            if [[ "${HTTP_CODE}" == "401" || "${HTTP_CODE}" == "403" ]]; then
                record PASS "${id}" "requires auth (${HTTP_CODE})"
            elif [[ "${success}" == "false" && "${code}" =~ ^(UNAUTHORIZED|FORBIDDEN|INVALID_CREDENTIALS)$ ]]; then
                record PASS "${id}" "rejected without credentials (${code})"
            elif [[ "${success}" == "true" && "${HTTP_CODE}" == "200" ]]; then
                record VULN "${id}" "unauthenticated access succeeded"
            else
                record WARN "${id}" "inconclusive HTTP=${HTTP_CODE} code=${code:-n/a}"
            fi
            ;;
        protected_no_keys)
            if [[ "${HTTP_CODE}" == "401" || "${HTTP_CODE}" == "403" ]]; then
                record PASS "${id}" "requires auth (${HTTP_CODE})"
            elif [[ "${success}" == "true" && "${RESP_BODY}" == *'"key"'* ]]; then
                record VULN "${id}" "returns invite keys without auth"
            elif [[ "${success}" == "true" ]]; then
                record VULN "${id}" "unauthenticated access succeeded"
            else
                record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
            fi
            ;;
        public_ok)
            if [[ "${HTTP_CODE}" == "200" && "${success}" == "true" ]]; then
                record PASS "${id}" "public read OK"
            elif [[ "${HTTP_CODE}" == "200" ]]; then
                record PASS "${id}" "reachable (HTTP 200)"
            else
                record WARN "${id}" "unexpected HTTP=${HTTP_CODE} success=${success:-n/a}"
            fi
            ;;
        reject_write)
            if [[ "${HTTP_CODE}" == "401" || "${HTTP_CODE}" == "403" ]]; then
                record PASS "${id}" "write blocked (${HTTP_CODE})"
            elif [[ "${success}" == "true" && "${HTTP_CODE}" == "200" ]]; then
                record VULN "${id}" "unauthenticated write succeeded"
            else
                record WARN "${id}" "inconclusive HTTP=${HTTP_CODE} code=${code:-n/a}"
            fi
            ;;
        reject_or_invalid)
            if [[ "${HTTP_CODE}" == "429" ]]; then
                record PASS "${id}" "rate limited (${HTTP_CODE})"
            elif [[ "${success}" == "false" ]]; then
                record WARN "${id}" "no rate limit yet; got business error ${code:-n/a}"
            else
                record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
            fi
            ;;
    esac
}

test_auth_rate_limit() {
    local burst="$1"
    local id="auth.login-rate-limit"
    local url="${API}/auth/login"
    local got_429=0
    local got_401=0
    local i

    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "POST ${url} x${burst} (wrong password, no Authorization)"
    echo "Expect: at least one HTTP 429 if brute-force protection exists"

    for i in $(seq 1 "${burst}"); do
        http_request POST "${url}" \
            -H "Content-Type: application/json" \
            -d '{"username":"__security_probe__","password":"wrong-password"}'
        if [[ "${HTTP_CODE}" == "429" ]]; then
            got_429=$((got_429 + 1))
        elif [[ "${HTTP_CODE}" == "401" ]]; then
            got_401=$((got_401 + 1))
        fi
    done

    echo "Results: 401=${got_401}, 429=${got_429} / ${burst} attempts"
    if [ "${got_429}" -gt 0 ]; then
        record PASS "${id}" "rate limiting active (${got_429}/${burst} got 429)"
    else
        record VULN "${id}" "no 429 observed after ${burst} failed login attempts"
    fi
}

test_open_register() {
    local id="auth.open-register"
    local url="${API}/auth/register"

    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "POST ${url} (invalid payload: username too short — no account created)"
    echo "Expect: WARN if registration endpoint is publicly reachable"

    http_request POST "${url}" \
        -H "Content-Type: application/json" \
        -d '{"username":"ab","password":"probe123456"}'

    echo "HTTP ${HTTP_CODE}"
    redact_body
    echo

    if [[ "${HTTP_CODE}" == "422" ]]; then
        record WARN "${id}" "registration endpoint is public (validation reached; no user created)"
    elif [[ "${HTTP_CODE}" == "403" || "${HTTP_CODE}" == "429" ]]; then
        record PASS "${id}" "registration restricted (${HTTP_CODE})"
    else
        record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
    fi
}

test_open_register_write() {
    local id="auth.open-register-write"
    local url="${API}/auth/register"
    local username="sec_probe_$(date +%s)_$RANDOM"

    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "POST ${url} (creates a throwaway user — use only on test/staging)"
    echo "Expect: WARN if self-registration returns tokens"

    http_request POST "${url}" \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"${username}\",\"password\":\"probe123456\",\"nickname\":\"audit\"}"

    echo "HTTP ${HTTP_CODE}"
    redact_body
    echo

    local success
    success="$(json_field success)"
    if [[ "${success}" == "true" && "${HTTP_CODE}" == "200" && "${RESP_BODY}" == *'"access_token"'* ]]; then
        record WARN "${id}" "open self-registration returns token pair (review if intentional)"
    elif [[ "${HTTP_CODE}" == "403" || "${HTTP_CODE}" == "429" ]]; then
        record PASS "${id}" "registration restricted (${HTTP_CODE})"
    else
        record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
    fi
}

test_admin_surface() {
    local id="admin.remote-surface"
    local url="${BASE_URL}/admin/"

    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "GET ${url}"
    echo "Expect: WARN if admin UI reachable remotely without extra gate"

    http_request GET "${url}"
    echo "HTTP ${HTTP_CODE}"
    printf '%s\n' "${RESP_BODY:0:200}"
    echo

    if [[ "${HTTP_CODE}" == "403" && "${RESP_BODY}" == *"localhost"* ]]; then
        record PASS "${id}" "admin blocked for non-localhost (${HTTP_CODE})"
    elif [[ "${HTTP_CODE}" == "200" || "${HTTP_CODE}" == "302" ]]; then
        record WARN "${id}" "admin UI reachable at ${url} (ensure strong ADMIN_PASSWORD + rate limit)"
    else
        record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
    fi
}

test_jwt_ignored_on_protected_route() {
    local id="auth.fake-bearer-ignored"
    local url="${API}/invite/list"

    echo
    echo -e "${CYAN}--- ${id} ---${NC}"
    echo "GET ${url} with fake Authorization header"
    echo "Expect: still blocked after fix; currently may ignore invalid bearer on open routes"

    http_request GET "${url}" -H "Authorization: Bearer fake-token-for-audit"
    echo "HTTP ${HTTP_CODE}"
    redact_body
    echo

    if [[ "${HTTP_CODE}" == "401" || "${HTTP_CODE}" == "403" ]]; then
        record PASS "${id}" "fake bearer rejected (${HTTP_CODE})"
    elif [[ "${HTTP_CODE}" == "200" && "${RESP_BODY}" == *'"key"'* ]]; then
        record VULN "${id}" "endpoint ignores auth; still exposes keys with fake bearer"
    else
        record WARN "${id}" "inconclusive HTTP=${HTTP_CODE}"
    fi
}

print_header

echo "Read-only probes (default). Mutating probes: INCLUDE_WRITE=${INCLUDE_WRITE}"

# --- P0: invite management (should be protected) ---
run_case "invite.list" GET "/invite/list" protected_no_keys \
    "invite key enumeration must not be public"
run_case "invite.stats" GET "/invite/stats" protected \
    "pool statistics must not be public"

run_case "invite.generate" POST "/invite/generate" reject_write \
    "key generation must require admin auth (POST without key; no side effect on 403)" \
    -H "Content-Type: application/json" -d '{}'

run_case "invite.verify" POST "/invite/verify" reject_or_invalid \
    "verify should fail on bad key; ideally rate-limited" \
    -H "Content-Type: application/json" -d '{"key":"00000000000000000000000000000000"}'

# --- Should be protected: JWT user routes ---
run_case "users.me" GET "/users/me" protected \
    "profile requires Bearer access token"
run_case "poems.favorites" GET "/poems/favorites" protected \
    "favorites require Bearer access token"

# --- Public by design (200 is OK) ---
run_case "system.health" GET "/system/health" public_ok "health probe"
run_case "system.info" GET "/system/info" public_ok "service metadata"
run_case "snippets.list" GET "/snippets?page=1&page_size=3" public_ok "public catalog"
run_case "poems.list" GET "/poems?page=1&page_size=3" public_ok "public catalog"
run_case "content.items" GET "/content/items" public_ok "public content"
run_case "fund.list" GET "/fund/list" public_ok "public fund list (review if needed)"
run_case "market.gold.quote" GET "/market/gold/quote" public_ok "public quote (upstream throttled server-side)"
run_case "resume.status" GET "/resume/status" public_ok "session status for resume page"

# --- Sensitive read surfaces (informational) ---
run_case "fund.download" GET "/fund/download" public_ok \
    "CSV export is public today — review if this should require auth"

# --- Auth surface ---
run_case "auth.login-invalid" POST "/auth/login" reject_or_invalid \
    "invalid login should fail (429 if rate limit exists)" \
    -H "Content-Type: application/json" \
    -d '{"username":"nobody","password":"wrong"}'

test_open_register
if [ "${INCLUDE_WRITE}" -eq 1 ]; then
    test_open_register_write
fi
test_jwt_ignored_on_protected_route
test_admin_surface

if [ "${RATE_LIMIT_BURST}" -gt 0 ]; then
    test_auth_rate_limit "${RATE_LIMIT_BURST}"
else
    record SKIP "auth.login-rate-limit" "skipped (use --rate-limit-burst 15)"
fi

echo
echo -e "${CYAN}========================================${NC}"
echo -e "Summary for ${BASE_URL}"
echo -e "  ${GREEN}PASS${NC}: ${PASS}"
echo -e "  ${RED}VULN${NC}: ${VULN}"
echo -e "  ${YELLOW}WARN${NC}: ${WARN}"
echo -e "  ${YELLOW}SKIP${NC}: ${SKIP}"
echo -e "${CYAN}========================================${NC}"

if [ "${VULN}" -gt 0 ]; then
    echo -e "${RED}Findings require attention.${NC}"
    exit 1
fi

if [ "${WARN}" -gt 0 ]; then
    echo -e "${YELLOW}No critical VULN, but review WARN items.${NC}"
fi

echo -e "${GREEN}No VULN findings.${NC}"
exit 0
