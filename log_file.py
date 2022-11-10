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


# parse() method; it will "transform" the log file into the list of LogEntry instances (kept inside
# the LogEntryProcessor instance)
# get_entries() - returns the list of LogEntry instances. Should indicate error in case parse() was not performed yet.
#

class LogEntryProcess:
    def __init__(self, file_name):
        self.file_name = file_name
        self.log_entries_list = []

    def parse(self):
        with open(file=self.file_name, mode='r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                split_line = line.split(' - ', maxsplit=3) #regulární výrazy robustnější řešení
                if len(split_line) > 4:
                    raise ValueError('Line was split more than 3 times.')
                timestamp = datetime.strptime(split_line[0], '%Y-%m-%d %H:%M:%S,%f')
                severity = SeverityEnum[split_line[2]]
                if isinstance(severity, SeverityEnum) is False:
                    raise ValueError('Expected type in SeverityEnum')
                logger_name = split_line[1]
                message = split_line[3]

                LogEntry(timestamp=timestamp, severity=severity, logger_name=logger_name, message=message)

                #print(timestamp, severity, logger_name, message)



a = LogEntryProcess('makefile.log')
a.parse()



    #
    #
    # def get_entries(self) -> list:
    #     # TODO Should indicate error in case parse() was not performed yet.
    #     return self.log_entries_list
    #
    #
    #
    # def filter_according_severity(self):
    #
    #
    #
    # def filter_according_logger_name(self):
    #
    #
    # def filer_containing_substring(self):
    #
    #
    # def filer_according_timestamp(self):
    #



