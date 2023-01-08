from __future__ import annotations
# Our systems produce various types of logs. The objective of this task is to write a simple parser
# Part 1
# 	•	Take a look at sample.log file and its structure
#
# Part 2
# 	•	Design and write LogEntry class which will represent one log entry
# 	•	Log entry is represented in a form of structured data: timestamp, severity, logger name, message - datová struktrua, repezentace dat se kterými budu fungovat
#
# Part 3
# 	•	Write LogEntryProcessor class, which will be able to keep internally list of log entries(LogEntry)
# 	•	Expected methods:
# 	◦	Constructor should accept name of log file
# 	◦	parse() method; it will "transform" the log file into the list of LogEntry instances (kept inside the LogEntryProcessor instance)
# 	◦	get_entries() - returns the list of LogEntry instances. Should indicate error in case parse() was not performed yet.
# Part 4
# 	•	Extending abilities of  LogEntryProcessor by adding methods providing "filtering" functionality (i.e. to return subset of LogEntry list based on specified criteria):
# 	◦	method to return all LogEntry for specified severity ('DEBUG','INFO',..)
# 	◦	method to return all LogEntry for specified logger name ('mf', ...)
# 	◦	method to return all LogEntry containing substring in message
# 	◦	method to return all LogEntry newer than specified timestamp

# log level je to samé jako severity

from enum import Enum, auto
from datetime import datetime
from pprint import pprint

class SeverityEnum(Enum):
    INFO = 'info'
    DEBUG = 'debug'
    WARNING = 'warning'
    ERROR = 'error'


class LogEntry:
    def __init__(self, timestamp: datetime, severity: SeverityEnum, logger_name: str, message: str):
        self.timestamp = timestamp
        self.severity = severity
        self.logger_name = logger_name
        self.message = message

    def __repr__(self):
        return f'{self.timestamp} - {self.severity.value} - {self.logger_name} - {self.message}'


class LogEntryList(list):
    # def get_entries(self) -> list:
    #     if self.log_entries_list is None:
    #         raise RuntimeError('Please call parse method first.')
    #     return self.log_entries_list.copy()

    def filter_according_logger_name(self, logger_name: str) -> LogEntryList:
        filter_logger_name_list = LogEntryList()
        for log_entry in self:
            if log_entry.logger_name == logger_name:
                filter_logger_name_list.append(log_entry)
        return filter_logger_name_list

    def filter_according_severity(self, severity_info: SeverityEnum) -> LogEntryList:
        filter_severity_list = LogEntryList()
        for log_entry in self:
            if log_entry.severity.value == severity_info:
                filter_severity_list.append(log_entry)
        return filter_severity_list

    def filter_newer_entries(self, timestamp_info: datetime) -> LogEntryList:
        filter_timestamp_list = LogEntryList()
        for log_entry in self:
            if log_entry.timestamp > timestamp_info:
                filter_timestamp_list.append(log_entry)
        return filter_timestamp_list

    def filter_containing_substring(self, substring_info: str) -> LogEntryList:
        filter_substring_list = LogEntryList()
        for log_entry in self:
            if substring_info in log_entry.message:
                filter_substring_list.append(log_entry)
        return filter_substring_list


def parse(file_name: str) -> LogEntryList:
    log_entries_list = LogEntryList()
    with open(file=file_name, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            split_line = line.split(' - ', maxsplit=3) #regulární výrazy robustnější řešení
            if len(split_line) != 4:
                raise ValueError(f'Line was split different times than 3 times. Line {split_line}.')
            timestamp = (datetime.strptime(split_line[0], '%Y-%m-%d %H:%M:%S,%f'))
            severity = (SeverityEnum[split_line[2]])
            logger_name = (split_line[1])
            message = split_line[3]

            instance_of_log_entry = LogEntry(timestamp=timestamp, severity=severity, logger_name=logger_name, message=message)
            log_entries_list.append(instance_of_log_entry)
    return log_entries_list

timestamp = datetime(2022, 10, 27, 13, 26, 19)
a = parse('makefile.log')
#pprint(a.get_entries())
pprint(a.filter_according_logger_name('mf').filter_newer_entries(timestamp).filter_according_severity('debug'))
#pprint(a.filter_according_severity('info'))

#pprint(a.filter_newer_entries(timestamp))
#pprint(a.filter_containing_substring('-'))
#
# import re
#
# text = '2022-10-27 11:14:08,757 - mf - INFO - Using configuration DefaultConfig'
#
# a = (re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} - [a-zA-Z]*? - [a-zA-Z]*? - .*?', text))
# print(a.group())


