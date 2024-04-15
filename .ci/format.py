#!/usr/bin/env python3

import os
import subprocess
import argparse

py_sub_folders = [".ci", "bv", "tools", "tutorial"]


def error(msg=""):
  print("error: %s" % msg)
  exit(1)


def check_yapf():
  # check yapf exist
  os.system("yapf --version") == 0 or os.system(
    "pip install yapf"
  ) == 0 or error(
    "error: fail to use yapf, maybe you can try install by command: pip install yapf --user"
  )


def get_root_path(anchor=".style.cfg"):
  path = os.path.abspath(__file__)
  while True:
    path = os.path.dirname(path)
    if (os.path.exists(path + "/" + anchor)):
      return path
    if (path == "/"):
      error("%s not found" % anchor)


def _run_py(sub_folders, file_types=["*.py"], format_file=".style.cfg"):
  check_yapf()
  assert isinstance(file_types, list)
  assert format_file.strip()
  root = get_root_path(format_file)
  print("check in [%s] with [%s]" %
        (", ".join(sub_folders), ", ".join(file_types)))
  for folder in sub_folders:
    for file_type in file_types:
      cmd = "yapf --style %s/%s -i -r %s/%s %s" % (root, format_file, root,
                                                   folder, file_type)
      os.system(cmd)


def run():
  _run_py(py_sub_folders)


def _check_py(sub_folders, file_types=["*.py"], format_file=".style.cfg"):
  check_yapf()
  assert isinstance(file_types, list)
  assert format_file.strip()
  root = get_root_path(format_file)
  print("check in [%s] with [%s]" %
        (", ".join(sub_folders), ", ".join(file_types)))
  for folder in sub_folders:
    for file_type in file_types:
      try:
        cmd = "yapf --style %s/%s -d -r %s/%s '%s'" % (root, format_file, root,
                                                       folder, file_type)
        result = subprocess.check_output(cmd, shell=True)
      except subprocess.CalledProcessError as e:
        error("not all %s in %s/%s is formatted" % (file_type, root, folder))


def check():
  _check_py(py_sub_folders)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("action",
                      choices=["check", "run"],
                      nargs="?",
                      default="run",
                      help="The actions")
  args = parser.parse_args()
  if (args.action == "run"):
    run()
  elif (args.action == "check"):
    check()

  exit(0)
