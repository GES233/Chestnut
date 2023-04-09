from pathlib import Path
import pytest
from pyinstrument.profiler import Profiler


@pytest.fixture(autouse=True)
def auto_profile(request):
    PROFILE_ROOT = Path.cwd() / "tests/.profiles"
    # Turn profiling on
    profiler = Profiler()
    profiler.start()

    yield  # Run test

    profiler.stop()
    PROFILE_ROOT.mkdir(exist_ok=True)
    results_file = PROFILE_ROOT / f"{request.node.name}.html"
    with open(results_file, "w", encoding="utf-8") as f_html:
        f_html.write(profiler.output_html())
