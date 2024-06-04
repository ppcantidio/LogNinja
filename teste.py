from rich.console import Console

from logninja.ninja_rich_console import NinjaRichConsole

console = Console(record=True, no_color=True)
console.print("""
[2024-06-01 19:52:07][DEBUG   ] Console logging setup complete              (logninja) __init__.py:27
[2024-06-01 19:52:07][DEBUG   ] File logging setup complete                 (logninja) __init__.py:32
[2024-06-01 19:52:07][DEBUG   ] Logging setup complete                      (logninja) __init__.py:36  [users=adfdfs][2024-06-01 19:52:07][DEBUG   ] Starting execution of function 'run'        (logninja) decorators.py:39
[params={'args': [], 'kwargs': {'logger': <Logger logninja (DEBUG)>}}]
[2024-06-01 19:52:07][INFO    ] Hello, world!                               (logninja) run_logs.py:8
[X-Trace-Id=adfdfs, x-user=admin]
[2024-06-01 19:52:07][DEBUG   ] Loading configuration file /adasd/asdasd... (logninja) run_logs.py:9
[2024-06-01 19:52:07][ERROR   ] Unable to find 'pomelo' in database!        (logninja) run_logs.py:12
[2024-06-01 19:52:07][INFO    ] POST /jsonrpc/ 200 65532                    (logninja) run_logs.py:13
[2024-06-01 19:52:07][INFO    ] POST /admin/ 401 42234                      (logninja) run_logs.py:14
[2024-06-01 19:52:07][WARNING ] password was rejected for admin site.       (logninja) run_logs.py:15
[2024-06-01 19:52:07][CRITICAL] Out of memory!                              (logninja) run_logs.py:16
[2024-06-01 19:52:07][INFO    ] Server exited with code=-1                  (logninja) run_logs.py:17
[2024-06-01 19:52:07][DEBUG   ] in divide                                   (logninja) run_logs.py:21
[2024-06-01 19:52:07][ERROR   ] An error occurred while executing 'run'     (logninja) decorators.py:50
""")

console.save_svg("docs/assets/table.svg", title="example.py")
