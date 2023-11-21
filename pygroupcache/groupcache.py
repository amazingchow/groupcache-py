# -*- coding: utf-8 -*-
import ctypes
import os
from typing import Union

root_path = os.path.dirname(os.path.abspath(__file__))
lib = ctypes.cdll.LoadLibrary(os.path.join(root_path, "libs/groupcache.so"))

gget = lib.cache_get
gget.argtypes = [ctypes.c_char_p]
gget.restype = ctypes.c_char_p
gset = lib.cache_set
gset.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
gset.restype = ctypes.c_char_p
gsetup = lib.setup
gsetup.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
ginitialized = lib.initialized
ginitialized.restype = ctypes.c_char_p


def get(key: str) -> str:
    """
    Retrieves the value associated with the given key from the cache.

    Args:
        key (str): The key to retrieve the value for.

    Returns:
        str: The value associated with the key, or an empty string if the key is not found.
    """
    r = gget(ctypes.c_char_p(key.encode("utf8")))
    return r.decode("utf8") if isinstance(r, bytes) else ""


def set(key: str, value: Union[str, bytes]) -> str:
    """
    Sets the value for the given key in the cache.

    Args:
        key (str): The key to set the value for.
        value (Union[str, bytes]): The value to set for the key. If it's a string, it will be encoded as UTF-8.

    Returns:
        str: The previous value associated with the key, or an empty string if the key is not found.
    """
    if not isinstance(value, bytes):
        value = value.encode("utf-8")
    r = gset(ctypes.c_char_p(key.encode("utf8")), ctypes.c_char_p(value))
    return r.decode("utf8") if isinstance(r, bytes) else ""


def setup(addr: str, base_url: str):
    """
    Sets up the cache with the given address.

    Args:
        addr (str): The address of the cache.

    Returns:
        None
    """
    gsetup(ctypes.c_char_p(addr.encode("utf8")), ctypes.c_char_p(base_url.encode("utf8")))


def initialized() -> bool:
    """
    Checks if the cache is initialized.

    Returns:
        bool: True if the cache is initialized, False otherwise.
    """
    return ginitialized().decode("utf8") == "1"
