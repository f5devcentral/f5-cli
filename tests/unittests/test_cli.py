import json

import click
from click.testing import CliRunner
import sys

from f5cloudcli.constants import F5_CONFIG_FILE

# Module under test
from f5cloudcli.cli import PASS_CONTEXT, AliasedGroup
from f5cloudcli import cli


class TestContext(object):
    """ Test Class: Context"""
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.context = cli.Context()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """
        pass

    @staticmethod
    def format_output_side_effect(data):
        return data

    def test_log_message_no_argument_with_environment_variable(self, mocker):
        """ Log a message, no argument
        Given
        - Environment variable of output format JSON exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """
        mock_output_format_env = mocker.patch("f5cloudcli.cli.os.environ.get")
        mock_output_format_env.return_value = "json"
        mock_format_output = mocker.patch("f5cloudcli.cli.format_output")
        mock_format_output.side_effect = TestContext.format_output_side_effect
        mock_click_echo = mocker.patch("f5cloudcli.cli.click.echo")
        self.context.log("Test message")
        mock_click_echo.assert_called_once_with('Test message', file=sys.stderr)

    def test_log_message_argument_with_environment_variable(self, mocker):
        """ Log a message, with argument
        Given
        - Environment variable of output format JSON exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """
        mock_output_format_env = mocker.patch("f5cloudcli.cli.os.environ.get")
        mock_output_format_env.return_value = "json"
        mock_format_output = mocker.patch("f5cloudcli.cli.format_output")
        mock_format_output.side_effect = TestContext.format_output_side_effect
        mock_click_echo = mocker.patch("f5cloudcli.cli.click.echo")
        self.context.log("Test message with argument: %s", "fake value")
        mock_click_echo.assert_called_once_with('Test message with argument: fake value', file=sys.stderr)

    def test_log_message_no_argument_no_environment_variable_with_config_file(self, mocker):
        """ Log a message, no argument, no output format env variable, config file exists
        Given
        - Environment variable of output format JSON does not exist
        - F5_CONFIG_FILE exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """
        mock_output_format_env = mocker.patch("f5cloudcli.utils.core.os.environ.get")
        mock_output_format_env.return_value = None
        mock_os_path_isfile = mocker.patch("f5cloudcli.utils.core.os.path.isfile")
        mock_os_path_isfile.return_value = True
        mock_open_config_file = mocker.patch("f5cloudcli.utils.core.open", mocker.mock_open(read_data='json'))
        mock_json_load = mocker.patch("f5cloudcli.utils.core.json.load")
        mock_json_load.return_value = {"output": "json"}

        mock_format_output = mocker.patch("f5cloudcli.utils.core.format_output")
        mock_format_output.side_effect = TestContext.format_output_side_effect
        mock_click_echo = mocker.patch("f5cloudcli.cli.click.echo")
        self.context.log("Test message")
        mock_click_echo.assert_called_once_with(
            '{\n    "message": "Test message"\n}', file=sys.stderr
        )
        mock_open_config_file.assert_called_once_with(F5_CONFIG_FILE, 'r')
        mock_json_load.assert_called_once_with(mock_open_config_file.return_value)

    def test_log_message_no_argument_with_environment_variable_no_config_file(self, mocker):
        """ Log a message, no argument, no output format env variable, config file does not exists
        Given
        - Environment variable of output format JSON does not exist
        - F5_CONFIG_FILE does not exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """
        mock_output_format_env = mocker.patch("f5cloudcli.cli.os.environ.get")
        mock_output_format_env.return_value = "-1"
        mock_os_path_isfile = mocker.patch("f5cloudcli.cli.os.path.isfile")
        mock_os_path_isfile.return_value = False
        mocker.patch("f5cloudcli.cli.open", mocker.mock_open(read_data='json'))

        mock_format_output = mocker.patch("f5cloudcli.cli.format_output")
        mock_format_output.side_effect = TestContext.format_output_side_effect
        mock_click_echo = mocker.patch("f5cloudcli.cli.click.echo")
        self.context.log("Test message")
        mock_click_echo.assert_called_once_with('Test message', file=sys.stderr)

    def test_vlog_message_no_argument_with_environment_variable_no_config_file(self, mocker):
        """ Verbose log a message, no argument, no output format env variable, config file does not exists
        Given
        - Environment variable of output format JSON does not exist
        - F5_CONFIG_FILE does not exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """
        mock_output_format_env = mocker.patch("f5cloudcli.cli.os.environ.get")
        mock_output_format_env.return_value = "-1"
        mock_os_path_isfile = mocker.patch("f5cloudcli.cli.os.path.isfile")
        mock_os_path_isfile.return_value = False
        mocker.patch("f5cloudcli.cli.open", mocker.mock_open(read_data='json'))

        mock_format_output = mocker.patch("f5cloudcli.cli.format_output")
        mock_format_output.side_effect = TestContext.format_output_side_effect
        mock_click_echo = mocker.patch("f5cloudcli.cli.click.echo")
        self.context.verbose = True
        self.context.vlog("Test message")
        mock_click_echo.assert_called_once_with('Test message', file=sys.stderr)


class TestAliasedGroup(object):
    """ Test Class: Aliased Group """
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """
        pass

    def test_get_existed_command(self):
        """
        Given
        - foo command log a message

        When
        - invoke foo command

        Then
        - output of foo command is logged

        """
        @click.group('test_alias_group',
             cls=AliasedGroup)
        def cli():
            """ test aliased group """
            pass

        @cli.command('foo')
        @PASS_CONTEXT
        def foo(ctx):
            ctx.log("Test foo command")
        result = self.runner.invoke(cli, 'foo')
        assert not result.exception
        assert result.output == json.dumps(
            {'message': 'Test foo command'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_get_non_existed_command(self):
        """
        Given
        - foo command log a message

        When
        - invoke bar command

        Then
        - bar not exists message is logged

        """
        @click.group('test_alias_group',
             cls=AliasedGroup)
        def cli():
            """ test aliased group """
            pass

        @cli.command('foo')
        @PASS_CONTEXT
        def foo(ctx):
            ctx.log("Test aliased group")
        result = self.runner.invoke(cli, 'bar')
        assert result.exception
        assert "Error: No such command \"bar\"" in result.output

    def test_get_single_matched_command(self):
        """
        Given
        - foot command log a message

        When
        - invoke  foo command

        Then
        - output of foot command is logged

        """
        @click.group('test_alias_group',
             cls=AliasedGroup)
        def cli():
            """ test aliased group """
            pass

        @cli.command('foot')
        @PASS_CONTEXT
        def foot(ctx):
            ctx.log("Test foot command")
        result = self.runner.invoke(cli, 'foo')
        assert not result.exception
        assert result.output == json.dumps(
            {'message': 'Test foot command'},
            indent=4,
            sort_keys=True
        ) + '\n'

    def test_get_multiple_matched_commands(self):
        """
        Given
        - foot command log a message
        - food command log a message

        When
        - invoke  foo command

        Then
        - error is logged

        """
        @click.group('test_alias_group',
             cls=AliasedGroup)
        def cli():
            """ test aliased group """
            pass

        @cli.command('foot')
        @PASS_CONTEXT
        def foot(ctx):
            ctx.log("Test foot command")

        @cli.command('food')
        @PASS_CONTEXT
        def food(ctx):
            ctx.log("Test food command")

        result = self.runner.invoke(cli, 'foo')
        assert result.exception
        assert "Error: Too many matches: food, foot" in result.output
