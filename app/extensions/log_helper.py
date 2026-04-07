# app/extensions/log_helper.py
import os
import inspect
from datetime import datetime

# ── ANSI codes ────────────────────────────────────────────────────────────────
class _C:
    """
    ANSI escape code constants for terminal text styling.

    Used internally by the log helper to apply colors and formatting
    to log output. Not intended for direct use outside this module.
    """
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

# ── Palette ───────────────────────────────────────────────────────────────────
_PALETTE = {
    "QUERY":   (_C.MAGENTA, "🔍"),
    "PARAMS":  (_C.MAGENTA, "📎"),
    "INFO":    (_C.BLUE,    "ℹ️ "),
    "SUCCESS": (_C.GREEN,   "✅"),
    "WARNING": (_C.YELLOW,  "⚠️ "),
    "ERROR":   (_C.RED,     "❌"),
    "DB":      (_C.CYAN,    "🔌"),
    "REQUEST": (_C.WHITE,   "🌐"),
    "AUTH":    (_C.YELLOW,  "🔐"),
    "CACHE":   (_C.CYAN,    "⚡"),
    "TASK":    (_C.BLUE,    "📋"),  # for background tasks etc.
}

# ── Environment guard ─────────────────────────────────────────────────────────
# Levels that are silenced in production
_PROD_SILENT = {"QUERY", "PARAMS", "DB"}

def _is_production() -> bool:
    """
    Determine whether the application is running in production mode.

    Checks Flask's DEBUG setting first. Falls back to the FLASK_ENV
    environment variable if Flask settings are unavailable (e.g. during
    early startup or in standalone scripts).

    Returns:
        bool: True if running in production (DEBUG=False), False otherwise.
    """
    # Defer import to avoid AppRegistryNotReady at module load time
    try:
        from app.config.config import Config
        conf = Config()
        return not conf.DEBUG
    except Exception:
        return os.environ.get("FLASK_ENV", "").lower() == "production"


# ── Core ──────────────────────────────────────────────────────────────────────
def log(level: str, msg: str, *, caller_depth: int = 1) -> None:
    """
    Print a colored, timestamped log message to stdout with caller info.

    The output format is:
        [LEVEL] HH:MM:SS.mmm (filename:function():lineno)  icon  message

    Levels in _PROD_SILENT (QUERY, PARAMS, DB) are suppressed automatically
    when DEBUG=False, so internal noise never leaks into production logs.
    Unknown levels fall back to white text with no icon and do not raise.

    Args:
        level (str):         Log level key. Must match a key in _PALETTE for
                             styled output (e.g. "INFO", "ERROR", "QUERY").
                             Case-insensitive. Custom strings are accepted.
        msg (str):           The message to display.
        caller_depth (int):  Stack frames to walk back when resolving caller
                             info. Default is 1 (direct caller of log()).
                             Pass 2 when wrapping log() in a helper function
                             so the shown caller is your code, not the wrapper.

    Returns:
        None

    Example:
        log("INFO",    "Server started")
        log("SUCCESS", "User created")
        log("WARNING", "Deprecated call used")
        log("ERROR",   "Something broke")
        log("DB",      "Connection opened")
        log("QUERY",   sql_string)
        log("PARAMS",  str(params))
        log("REQUEST", f"{method} {path}")
        log("AUTH",    f"Login attempt: {username}")
        log("CACHE",   f"Cache miss for key: user_{user_id}")
        log("TASK",    "Sending welcome email...")
    """
    level = level.upper()

    # Silence noisy levels in production
    if _is_production() and level in _PROD_SILENT:
        return

    color, icon = _PALETTE.get(level, (_C.WHITE, "  "))

    # ── Caller info ───────────────────────────────────────────────────────────
    try:
        frame      = inspect.stack()[caller_depth]
        filename   = os.path.basename(frame.filename)   # e.g. db_utils.py
        func_name  = frame.function                      # e.g. execute_query
        line_no    = frame.lineno                        # e.g. 42
        caller_str = f"{filename}:{func_name}():{line_no}"
    except Exception:
        caller_str = "unknown"

    # ── Timestamp ─────────────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # 14:32:07.841

    # ── Compose ───────────────────────────────────────────────────────────────
    badge      = f"{color}{_C.BOLD}[{level}]{_C.RESET}"
    time_part  = f"{_C.DIM}{timestamp}{_C.RESET}"
    caller_part = f"{_C.DIM}({caller_str}){_C.RESET}"
    body       = f"{color}{icon}  {msg}{_C.RESET}"

    print(f"{badge} {time_part} {caller_part}  {body}")


# ── Convenience wrappers (optional but nice) ──────────────────────────────────
def log_info(msg: str)    -> None: log("INFO",    msg, caller_depth=2)
def log_success(msg: str) -> None: log("SUCCESS", msg, caller_depth=2)
def log_warning(msg: str) -> None: log("WARNING", msg, caller_depth=2)
def log_error(msg: str)   -> None: log("ERROR",   msg, caller_depth=2)
def log_db(msg: str)      -> None: log("DB",      msg, caller_depth=2)
def log_query(msg: str)   -> None: log("QUERY",   msg, caller_depth=2)
def log_params(msg: str)  -> None: log("PARAMS",  msg, caller_depth=2)
def log_request(msg: str) -> None: log("REQUEST", msg, caller_depth=2)
def log_auth(msg: str)    -> None: log("AUTH",    msg, caller_depth=2)
def log_cache(msg: str)   -> None: log("CACHE",   msg, caller_depth=2)
def log_task(msg: str)    -> None: log("TASK",    msg, caller_depth=2)