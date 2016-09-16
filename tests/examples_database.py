import sqlite3
from contextlib import contextmanager

from concurrent.futures import Future

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from threading import Thread

import binascii
from hypothesis.database import SQLiteExampleDatabase
from hypothesis.internal.compat import b64decode, b64encode
from concurrent.futures import ThreadPoolExecutor

# Object used by _background_consumer to signal the source is exhausted
# to the main thread.
_sentinel = object()


class _background_consumer(Thread):
    """Will fill the queue with content of the source in a separate thread.

    >>> import Queue
    >>> q = Queue.Queue()
    >>> c = _background_consumer(q, range(3))
    >>> c.start()
    >>> q.get(True, 1)
    0
    >>> q.get(True, 1)
    1
    >>> q.get(True, 1)
    2
    >>> q.get(True, 1) is _sentinel
    True
    """

    def __init__(self, queue, source):
        Thread.__init__(self)

        self._queue = queue
        self._source = source

    def run(self):
        for item in self._source:
            self._queue.put(item)

        # Signal the consumer we are done.
        self._queue.put(_sentinel)


class ibuffer(object):
    """Buffers content of an iterator polling the contents of the given
    iterator in a separate thread.
    When the consumer is faster than many producers, this kind of
    concurrency and buffering makes sense.

    The size parameter is the number of elements to buffer.

    The source must be threadsafe.

    Next is a slow task:
    >>> from itertools import chain
    >>> import time
    >>> def slow_source():
    ...     for i in range(10):
    ...         time.sleep(0.1)
    ...         yield i
    ...
    >>>
    >>> t0 = time.time()
    >>> max(chain(*( slow_source() for _ in range(10) )))
    9
    >>> int(time.time() - t0)
    10

    Now with the ibuffer:
    >>> t0 = time.time()
    >>> max(chain(*( ibuffer(5, slow_source()) for _ in range(10) )))
    9
    >>> int(time.time() - t0)
    4

    60% FASTER!!!!!11
    """

    def __init__(self, source, maxsize=0):
        self._queue = Queue(maxsize)

        self._poller = _background_consumer(self._queue, source)
        self._poller.daemon = True
        self._poller.start()

    def __iter__(self):
        return self

    def next(self):
        item = self._queue.get(True)
        if item is _sentinel:
            raise StopIteration()
        return item


class ThreadedSQLiteExampleDatabase(SQLiteExampleDatabase):
    def __init__(self, path=u':memory:', max_workers=2):
        self.path = path
        self.db_created = False
        self.pool = ThreadPoolExecutor(max_workers)
        self.current_connection = self._establish_connection()

    def _establish_connection(self):
        return self.pool.submit(sqlite3.connect, self.path, check_same_thread=False)

    def connection(self):
        if isinstance(self.current_connection, Future):
            self.current_connection = self.current_connection.result()
        return self.current_connection

    def close(self):
        if self.current_connection:
            try:
                self.pool.shutdown()
                self.connection().close()
            finally:
                del self.current_connection

    def __repr__(self):
        return u'%s(%s)' % (self.__class__.__name__, self.path)

    @contextmanager
    def cursor(self):
        conn = self.connection()
        cursor = conn.cursor()
        try:
            try:
                yield cursor
            finally:
                cursor.close()
        except:
            self.pool.submit(conn.rollback)
            raise
        else:
            self.pool.submit(conn.commit)

    def save(self, key, value):
        def _save_internal(cursor):
            try:
                cursor.execute("""
                    insert into hypothesis_data_mapping(key, value)
                    values(?, ?)
                """, (b64encode(key), b64encode(value)))
            except sqlite3.IntegrityError:
                pass

        self.create_db_if_needed()
        with self.cursor() as cursor:
            self.pool.submit(_save_internal, cursor)

    def delete(self, key, value):
        def _delete_internal(cursor):
            cursor.execute("""
                            delete from hypothesis_data_mapping
                            where key = ? and value = ?
                        """, (b64encode(key), b64encode(value)))

        self.create_db_if_needed()
        with self.cursor() as cursor:
            self.pool.submit(_delete_internal, cursor)

    def fetch(self, key):
        self.create_db_if_needed()
        with self.cursor() as cursor:
            cursor.execute("""
                select value from hypothesis_data_mapping
                where key = ?
            """, (b64encode(key),))
            for (value,) in ibuffer(cursor):
                try:
                    yield b64decode(value)
                except (binascii.Error, TypeError):
                    pass

    def create_db_if_needed(self):
        if self.db_created:
            return
        with self.cursor() as cursor:
            cursor.execute("""
                create table if not exists hypothesis_data_mapping(
                    key text,
                    value text,
                    unique(key, value)
                )
            """)
        self.db_created = True
