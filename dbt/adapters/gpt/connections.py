from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional
from dbt.exceptions import (
    FailedToConnectError,
    DbtRuntimeError
)
from dbt.contracts.connection import ConnectionState
from dbt.adapters.base import Credentials
from dbt.adapters.base import BaseConnectionManager as connection_cls

from dbt.logger import GLOBAL_LOGGER as logger
import openai

@dataclass
class GptCredentials(Credentials):
    """
    Defines database specific credentials that get added to
    profiles.yml to connect to new adapter
    """

    api_key: str
    model: str
    organization: Optional[str] = None

    _ALIASES = {}

    @property
    def type(self):
        """Return name of adapter."""
        return "gpt"

    @property
    def unique_field(self):
        """
        Hashed and included in anonymous telemetry to track adapter adoption.
        Pick a field that can uniquely identify one team/organization building with this adapter
        """
        return self.organization

    def _connection_keys(self):
        """
        List of keys to display in the `dbt debug` output.
        """
        return ("organization","model",openai.Model.retrieve(connection.credentials.model))

class GptConnectionManager(connection_cls):
    TYPE = "gpt"


    @contextmanager
    def exception_handler(self, sql: str):
        """
        Returns a context manager, that will handle exceptions raised
        from queries, catch, log, and raise dbt exceptions it knows how to handle.
        """
        # ## Example ##
        try:
            yield

        except Exception as exc:
            logger.debug("Error running chat prompt: {}".format(sql))
            raise DbtRuntimeError(str(exc))


    @classmethod
    def open(cls, connection):
        """
        Receives a connection object and a Credentials object
        and moves it to the "open" state.
        """
        if connection.state == "open":
            logger.debug("Connection is already open, skipping open.")
            return connection

        credentials = connection.credentials

        try:
            openai.api_key = credentials.api_key
            openai.organization = credentials.organization
            test = openai.Model.retrieve(credentials.model)
            handle = openai

        except Exception as e:
            logger.debug(
                "Got an error when attempting to create an openai " "connection: '{}'".format(e)
            )

            connection.handle = None
            connection.state = "fail"

            raise FailedToConnectError(str(e))

        connection.handle = handle
        connection.state = "open"
        return connection

    def execute(self, connection):
        credentials = connection.credentials

        response = openai.ChatCompletion.create(
            model=credentials.model,
            messages=[
                {"role": "user", "content": "Hello!"}
            ]
        )
        return response

    @classmethod
    def close(self, connection):
        connection.state = ConnectionState.CLOSED

        return connection