#!/usr/bin/env python

from optparse import OptionParser
import commands
import logging
import os
import sys
import time
import yaml

from fsevents import Observer, Stream

"""
https://developer.apple.com/library/mac/#documentation/Darwin/Reference/FSEvents_Ref/Reference/reference.html#//apple_ref/doc/c_ref/kFSEventStreamEventFlagNone
"""
# FSEventStreamEventFlags
NONE                = kFSEventStreamEventFlagNone               = 0x00000
MUST_SCAN_SUB_DIRS  = kFSEventStreamEventFlagMustScanSubDirs    = 0x00001
USER_DROPPED        = kFSEventStreamEventFlagUserDropped        = 0x00002
KERNEl_DROPPED      = kFSEventStreamEventFlagKernelDropped      = 0x00004
EVENT_IDS_WRAPPED   = kFSEventStreamEventFlagEventIdsWrapped    = 0x00008
HISTORY_DONE        = kFSEventStreamEventFlagHistoryDone        = 0x00010
ROOT_CHANGED        = kFSEventStreamEventFlagRootChanged        = 0x00020
MOUNT               = kFSEventStreamEventFlagMount              = 0x00040
UNMOUNT             = kFSEventStreamEventFlagUnmount            = 0x00080 # These flags are only set if you specified the FileEvents
# flags when creating the stream.
CREATED             = kFSEventStreamEventFlagItemcreated        = 0x00100
REMOVED             = kFSEventStreamEventFlagItemremoved        = 0x00200
INODEMETAMOD        = kFSEventStreamEventFlagIteminodemetamod   = 0x00400
RENAMED             = kFSEventStreamEventFlagItemrenamed        = 0x00800
MODIFIED            = kFSEventStreamEventFlagItemmodified       = 0x01000
FINDERINFOMOD       = kFSEventStreamEventFlagItemfinderinfomod  = 0x02000
CHANGEOWNER         = kFSEventStreamEventFlagItemchangeowner    = 0x04000
XATTRMOD            = kFSEventStreamEventFlagItemxattrmod       = 0x08000
ISFILE              = kFSEventStreamEventFlagItemisfile         = 0x10000
ISDIR               = kFSEventStreamEventFlagItemisdir          = 0x20000
ISSYMLINK           = kFSEventStreamEventFlagItemissymlink      = 0x40000

FSEventStreamEventMap = {
  NONE               : "NONE",
  MUST_SCAN_SUB_DIRS : "MUST_SCAN_SUB_DIRS",
  USER_DROPPED       : "USER_DROPPED",
  KERNEl_DROPPED     : "KERNEl_DROPPED",
  EVENT_IDS_WRAPPED  : "EVENT_IDS_WRAPPED",
  HISTORY_DONE       : "HISTORY_DONE",
  ROOT_CHANGED       : "ROOT_CHANGED",
  MOUNT              : "MOUNT",
  UNMOUNT            : "UNMOUNT",
  CREATED            : "CREATED",
  REMOVED            : "REMOVED",
  INODEMETAMOD       : "INODEMETAMOD",
  RENAMED            : "RENAMED",
  MODIFIED           : "MODIFIED",
  FINDERINFOMOD      : "FINDERINFOMOD",
  CHANGEOWNER        : "CHANGEOWNER",
  XATTRMOD           : "XATTRMOD",
  ISFILE             : "ISFILE",
  ISDIR              : "ISDIR",
  ISSYMLINK          : "ISSYMLINK",
}

BUILD_CMD = dict()
CONFIG_PATH = None
WATCH_EVENTS = (USER_DROPPED, UNMOUNT, CREATED, REMOVED, RENAMED, MODIFIED)
WATCH_EXTENSIONS = tuple()

def is_watch_event(file_event):
  return file_event.mask in WATCH_EVENTS

def set_watch_extension(arg):
  global WATCH_EXTENSIONS
  WATCH_EXTENSIONS = arg

def is_watch_extension(file_event):
  return os.path.splitext(file_event.name)[1] in WATCH_EXTENSIONS

def set_build_cmd(arg):
  global BUILD_CMD
  BUILD_CMD = arg

def callback(file_event):
  logging.debug("%s, %s, %s" % (FSEventStreamEventMap[file_event.mask], file_event.cookie, file_event.name))
  if file_event.name == CONFIG_PATH:
    load_config()
    return
  cmd = BUILD_CMD.get(os.path.splitext(file_event.name)[1].lstrip("."), "make")
  if is_watch_event(file_event) and is_watch_extension(file_event):
    logging.info(cmd)
    logging.info(commands.getoutput(cmd))

def parse_options():
  parser = OptionParser()
  parser.add_option("-c", "--config", dest="config", default=".watchlion.yaml", help="path to config FILE", metavar="FILE")
  (options, _args) = parser.parse_args()
  global CONFIG_PATH
  CONFIG_PATH = os.path.abspath(options.config)
  logging.debug("parse_options: %s" % options)
  return options

def load_config(options=[0]):
  if CONFIG_PATH is None:
    options[0] = parse_options()
  logging.info("load_config: loading %s" % options[0].config)
  try:
    config = yaml.load(open(options[0].config).read())
  except Exception, e:
    logging.error("%s: %s" % (e.__class__.__name__, e))
    if not WATCH_EXTENSIONS:
      sys.exit(1)
  else:
    logging.debug("load_config: loaded %s" % config)
    set_watch_extension([".%s" % i for i in config["build"].keys()])
    set_build_cmd(config["build"])
    logging.getLogger().setLevel(config["loglevel"].upper())

def main():
  logging.basicConfig(level=logging.INFO)
  load_config()
  observer = Observer()
  observer.setDaemon(True)
  observer.start()
  observer.schedule(Stream(callback, ".", file_events=True))
  try:
    while True:
      time.sleep(10)
  except KeyboardInterrupt:
    pass
  finally:
    observer.stop()
    print("")

if __name__ == "__main__":
  main()
