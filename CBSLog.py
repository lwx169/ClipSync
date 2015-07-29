#!/usr/bin/env python

import logging

CBS_LOG_TAG = "ClipSync"

def initLog():
    logger     = logging.getLogger(CBS_LOG_TAG)
    console    = logging.StreamHandler()
    formatter  = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(logging.INFO)


def CBS_LOG_INFO(logStr):
    logger = logging.getLogger(CBS_LOG_TAG)
    logger.info(logStr)


def CBS_LOG_DEBUG(logStr):
    logger = logging.getLogger(CBS_LOG_TAG)
    logger.debug(logStr)


def CBS_LOG_ERROR(logStr):
    logger = logging.getLogger(CBS_LOG_TAG)
    logger.error(logStr)
