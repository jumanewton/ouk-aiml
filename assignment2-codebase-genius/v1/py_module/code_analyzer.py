"""Lightweight facade for code analysis helpers used by Jac walkers.

This module intentionally re-exports only the helpers that already exist in
the Python implementation. It keeps the Jac imports satisfied without
recreating the entire Jac-based orchestration layer.
"""

from py_modules import ccg


def build_ccg(targets):
	return ccg.build_ccg(targets)


def summarize_module(module_path, symbols, code_snippet=""):
	return ccg.summarize_module(module_path, symbols, code_snippet)
