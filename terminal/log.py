# -*- coding: utf-8 -*-
import sys
import copy


class Logger(object):
    """
    The Logger interface.

    :param verbose: control if the log to show verbose log
    :param quiet: control if the log to show debug and info log
    :param indent: control the indent level, default is zero

    Play with :class:`Logger`, it supports nested logging::

        log = Logger()
        log.info('play with log')

        log.start('start a indent level')
        log.info('this log will indent two spaces')
        log.end('close a indent level')
    """

    def __init__(self, **kwargs):
        self.config(**kwargs)

    def config(self, **kwargs):
        """
        Config the behavior of :class:`Logger`.

        Control the output to show :class:`Logger.verbose` log::

            log.config(verbose=True)

        Control the output to show only the :class:`Logger.warn` and
        :class:`Logger.error` log::

            log.config(quiet=True)

        """

        self._is_verbose = False
        self._indent = kwargs.get('indent', 0)
        self._enable_verbose = kwargs.get('verbose', False)
        self._enable_quiet = kwargs.get('quiet', False)

    def message(self, level, *args):
        """
        Format the message of the logger.

        You can rewrite this method to format your own message::

            class MyLogger(Logger):

                def message(self, level, *args):
                    msg = ' '.join(args)

                    if level == 'error':
                        return terminal.red(msg)
                    return msg
        """

        from . import color
        msg = ' '.join(args)
        if level == 'start':
            return color.magenta('=> ') + msg
        if level == 'end':
            return color.magenta('* ') + msg
        m = {
            'debug': 'gray',
            'info': 'green',
            'warn': 'yellow',
            'error': 'red'
        }
        if level in m:
            fn = getattr(color, m[level])
            return '%s: %s' % (fn(level), msg)
        return msg

    def writeln(self, level='info', *args):
        if not self._enable_verbose and self._is_verbose:
            return self
        msg = self.message(level, *args)
        if self._indent:
            msg = '  ' * self._indent + msg
        if level == 'error':
            sys.stderr.write(msg + '\n')
        else:
            sys.stdout.write(msg + '\n')
        return self

    @property
    def verbose(self):
        """
        Make it the verbose log.

        A verbose log can be only shown when user want to see more logs.
        It works as::

            log.verbose.warn('this is a verbose warn')
            log.verbose.info('this is a verbose info')
        """

        log = copy.copy(self)
        log._is_verbose = True
        return log

    def start(self, *args):
        """
        Start a nested log.
        """

        self.writeln('start', *args)
        self._indent += 1
        return self

    def end(self, *args):
        """
        End a nested log.
        """

        self._indent -= 1
        return self.writeln('end', *args)

    def debug(self, *args):
        """
        The debug level log.
        """

        if self._enable_quiet:
            return self
        return self.writeln('debug', *args)

    def info(self, *args):
        """
        The info level log.
        """

        if self._enable_quiet:
            return self
        return self.writeln('info', *args)

    def warn(self, *args):
        """
        The warn level log.
        """

        return self.writeln('warn', *args)

    def error(self, *args):
        """
        The error level log.
        """

        return self.writeln('error', *args)
