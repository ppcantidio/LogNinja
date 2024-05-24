# This file contains code derived from the structlog project,
# available at https://github.com/hynek/structlog. Changes were made starting from May 24th, 2024.
# The original code is licensed under the MIT License or Apache-2.0.

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from traceback import walk_tb
from types import TracebackType
from typing import Any, Optional, Tuple, Type, Union

ExcInfo = Tuple[Type[BaseException], BaseException, Optional[TracebackType]]


SHOW_LOCALS = True
LOCALS_MAX_STRING = 80
MAX_FRAMES = 50

OptExcInfo = Union[ExcInfo, Tuple[None, None, None]]


@dataclass
class Frame:
    """
    Represents a single stack frame.
    """

    filename: str
    lineno: int
    name: str
    line: str = ""
    locals: dict[str, str] | None = None


@dataclass
class SyntaxError_:
    """
    Contains detailed information about :exc:`SyntaxError` exceptions.
    """

    offset: int
    filename: str
    line: str
    lineno: int
    msg: str


@dataclass
class Stack:
    """
    Represents an exception and a list of stack frames.
    """

    exc_type: str
    exc_value: str
    syntax_error: SyntaxError_ | None = None
    is_cause: bool = False
    frames: list[Frame] = field(default_factory=list)


@dataclass
class Trace:
    """
    Container for a list of stack traces.
    """

    stacks: list[Stack]


def safe_str(_object: Any) -> str:
    """Don't allow exceptions from __str__ to propegate."""
    try:
        return str(_object)
    except Exception as error:
        return f"<str-error {str(error)!r}>"


def to_repr(obj: Any, max_string: int | None = None) -> str:
    """Get repr string for an object, but catch errors."""
    if isinstance(obj, str):
        obj_repr = obj
    else:
        try:
            obj_repr = repr(obj)
        except Exception as error:
            obj_repr = f"<repr-error {str(error)!r}>"

    if max_string is not None and len(obj_repr) > max_string:
        truncated = len(obj_repr) - max_string
        obj_repr = f"{obj_repr[:max_string]!r}+{truncated}"

    return obj_repr


def extract(
    exc_type: type[BaseException],
    exc_value: BaseException,
    traceback: TracebackType | None,
    *,
    show_locals: bool = False,
    locals_max_string: int = LOCALS_MAX_STRING,
) -> Trace:
    """
    Extract traceback information.

    Args:
        exc_type: Exception type.

        exc_value: Exception value.

        traceback: Python Traceback object.

        show_locals: Enable display of local variables. Defaults to False.

        locals_max_string:
            Maximum length of string before truncating, or ``None`` to disable.

        max_frames: Maximum number of frames in each stack

    Returns:
        A Trace instance with structured information about all exceptions.

    .. versionadded:: 22.1.0
    """

    stacks: list[Stack] = []
    is_cause = False

    while True:
        stack = Stack(
            exc_type=safe_str(exc_type.__name__),
            exc_value=safe_str(exc_value),
            is_cause=is_cause,
        )

        if isinstance(exc_value, SyntaxError):
            stack.syntax_error = SyntaxError_(
                offset=exc_value.offset or 0,
                filename=exc_value.filename or "?",
                lineno=exc_value.lineno or 0,
                line=exc_value.text or "",
                msg=exc_value.msg,
            )

        stacks.append(stack)
        append = stack.frames.append

        for frame_summary, line_no in walk_tb(traceback):
            filename = frame_summary.f_code.co_filename
            if filename and not filename.startswith("<"):
                filename = os.path.abspath(filename)
            frame = Frame(
                filename=filename or "?",
                lineno=line_no,
                name=frame_summary.f_code.co_name,
                locals=(
                    {
                        key: to_repr(value, max_string=locals_max_string)
                        for key, value in frame_summary.f_locals.items()
                    }
                    if show_locals
                    else None
                ),
            )
            append(frame)

        cause = getattr(exc_value, "__cause__", None)
        if cause and cause.__traceback__:
            exc_type = cause.__class__
            exc_value = cause
            traceback = cause.__traceback__
            is_cause = True
            continue

        cause = exc_value.__context__
        if (
            cause
            and cause.__traceback__
            and not getattr(exc_value, "__suppress_context__", False)
        ):
            exc_type = cause.__class__
            exc_value = cause
            traceback = cause.__traceback__
            is_cause = False
            continue

        break

    return Trace(stacks=stacks)


def format_exception(
    exc_info: ExcInfo,
    locals_max_string: int = LOCALS_MAX_STRING,
    max_frames: int = MAX_FRAMES,
    show_locals: bool = SHOW_LOCALS,
) -> list[dict[str, Any]]:
    trace = extract(
        *exc_info,
        show_locals=show_locals,
        locals_max_string=locals_max_string,
    )

    for stack in trace.stacks:
        if len(stack.frames) <= max_frames:
            continue

        half = max_frames // 2  # Force int division to handle odd numbers correctly
        fake_frame = Frame(
            filename="",
            lineno=-1,
            name=f"Skipped frames: {len(stack.frames) - (2 * half)}",
        )
        stack.frames[:] = [
            *stack.frames[:half],
            fake_frame,
            *stack.frames[-half:],
        ]

    return [asdict(stack) for stack in trace.stacks]
