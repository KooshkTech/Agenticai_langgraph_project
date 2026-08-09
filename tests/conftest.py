import sys
import os
from unittest.mock import MagicMock

# Ensure the project root is on sys.path so that `src.langgraphagenticai`
# imports resolve correctly when running pytest from the project root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Workaround: On some Windows environments, the zstandard C extension DLL
# is blocked by Windows security policy, causing langsmith (a transitive
# dependency of langchain) to fail on import.  We inject a lightweight
# mock so that the import chain succeeds during testing.
# This does NOT affect production behaviour — it only applies to the
# pytest process.
try:
    import zstandard  # noqa: F401
except ImportError:
    sys.modules["zstandard"] = MagicMock()
