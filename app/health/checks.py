# -*- coding: utf-8 -*-
import platform
import multiprocessing
import sys
import os


def get_cores():
    result = multiprocessing.cpu_count()
    return result


def check_platform() -> dict:
    os = platform.platform()
    processor = platform.processor()
    node = platform.node()
    system = platform.system()
    cpu_count = multiprocessing.cpu_count()
    memory_use = sys.getsizeof({})
    result = {
        "os": os,
        "system": system,
        "node": node,
        "processor": processor,
        "cpu_count": cpu_count,
        "memory_use": memory_use,
    }
    return result


def check_app_information() -> dict:
    """
    get information about the application.

    Returns:
        dict -- [python version and module information]
    """
    app_modules = sys.modules.keys()
    python_version = sys.version
    mod_result = []
    for m in app_modules:
        mod_result.append(m)

    mod_result.sort()
    result = {"python_version": python_version, "app_modules": mod_result}

    return result
