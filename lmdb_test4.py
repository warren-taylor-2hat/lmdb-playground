#!/usr/bin/python2
"""
LMDB test 3.
Two processes accessing shared memory.
"""
import argparse
import lmdb
import logging
import psutil
import random
import string
import uuid

logger = logging.getLogger(__name__)


DATAPATH = 'test_data'
NUM_OF_WRITES = 100


def commandLineArgs():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--reader", action="store_true", help="Run as the reader process.")
    group.add_argument("-w", "--writer", action="store_true", help="Run as the writer process.")
    return parser.parse_args()


def hit_enter():
    try:
        dummy = input('-- hit Enter to continue --')
    except:
        pass #ignore all.


def random_string(string_length=128):
    """
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(string_length))


def the_writer():
    """
    """
    logger.debug('lmdb begin Write test.')
    logger.debug('random_string: %s', random_string())
    # map_size=10485760
    # writemap=True
    env_write = lmdb.open(DATAPATH, readonly=False, max_dbs=2)
    with env_write.begin(write=True, buffers=True) as txn:
        txn.put('somename', 'somedata')
        txn.put('mykey',    'myvalue')

        for index in range(NUM_OF_WRITES):
            txn.put(str(uuid.uuid4()), random_string())
        #
        logger.info('memory:\n%s', psutil.virtual_memory())
        hit_enter()


def the_reader():
    """
    """
    logger.debug('lmdb begin Get test.')
    env_read = lmdb.open(DATAPATH, readonly=True)
    with env_read.begin(write=False, buffers=True) as txn:
        key = 'somename'
        logger.info('key=%s, value=%s', key, txn.get(key))
        key = 'nada'
        logger.info('key=%s, value=%s', key, txn.get(key))

    logger.debug('lmdb begin Cursor test.')
    env_read = lmdb.open(DATAPATH, readonly=True)
    with env_read.begin(write=False, buffers=True) as txn:
        cursor = txn.cursor()
        counter = 0
        for key, value in cursor:
            logger.debug('key=%s, value=%s', key, value)
            counter += 1
        #
        logger.info('%d values.', counter)
        logger.info('memory:\n%s', psutil.virtual_memory())
        hit_enter()


def main(args):
    """
    """
    logger.info('lmdb test3.')
    logger.info('lmdb version %s', lmdb.version())

    if args.writer:
        the_writer()

    if args.reader:
        the_reader()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    args = commandLineArgs()
    main(args)
