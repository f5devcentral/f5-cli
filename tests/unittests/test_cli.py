""" Test CLI """

import sys
import json

import click

import f5cli
from f5cli.constants import FORMATS, ENV_VARS
from f5cli.cli import PASS_CONTEXT, AliasedGroup
from f5cli.cli import cli as basecli

from ..global_test_imports import pytest, Mock, PropertyMock, CliRunner


class TestBaseCli(object):
    """ Test Class: Base CLI """

    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    def test_cli_sends_telemetry_first_run(self, mocker):
        """ Test CLI sends telemetry

        Given
        - CLI has not been run before

        When
        - User attempts to use the CLI

        Then
        - CLI should exit successfully
        - Telemetry data should be sent
        - First run complete key should be set to True in file
        """

        mocker.patch("os.path.exists").return_value = True
        mocker.patch("os.path.isfile").return_value = True
        mocker.patch(
            'f5cli.config.core.open',
            mocker.mock_open(read_data='')
        )
        mock_yaml_dump = mocker.patch("yaml.safe_dump")
        mock_request = mocker.patch('requests.request')
        mock_request.return_value.json = Mock(return_value={})
        type(mock_request.return_value).status_code = PropertyMock(return_value=200)

        result = self.runner.invoke(basecli, ['config', 'list-defaults'])

        # validate successful exit code
        assert result.exit_code == 0, result.exc_info
        # validate telemetry data was sent
        args, kwargs = mock_request.call_args
        assert '/ee/v1/telemetry' in args[1]
        assert json.loads(kwargs['data'])['telemetryRecords'][0]['installed']
        # validate firstRunComplete is set to true
        args, kwargs = mock_yaml_dump.call_args
        assert args[0] == {'firstRunComplete': True}

    def test_cli_does_not_send_telemetry_on_second_run(self, mocker):
        """ Test CLI does NOT send telemetry on second run

        Given
        - CLI has been run before

        When
        - User attempts to use the CLI

        Then
        - CLI should exit successfully
        - Telemetry data should NOT be sent
        """

        mocker.patch("os.path.exists").return_value = True
        mocker.patch("os.path.isfile").return_value = True
        mocker.patch(
            'f5cli.config.core.open',
            mocker.mock_open(read_data='firstRunComplete: true')
        )
        mock_request = mocker.patch('requests.request')

        result = self.runner.invoke(basecli, ['config', 'list-defaults'])

        # validate successful exit code
        assert result.exit_code == 0, result.exception
        # validate telemetry data was NOT sent
        assert not mock_request.called

    def test_cli_does_not_fail_on_telemetry_failure(self, mocker):
        """ Test CLI does not fail when telemetry failure occurs

        Given
        - CLI has not been run before

        When
        - User attempts to use the CLI
        - Telemetry is unable to be sent successfully

        Then
        - CLI should exit successfully
        """

        mock_request = mocker.patch('requests.request')
        mock_request.return_value.json = Mock(return_value={})
        type(mock_request.return_value).status_code = PropertyMock(return_value=500)

        result = self.runner.invoke(basecli, ['config', 'list-defaults'])

        # validate successful exit code
        assert result.exit_code == 0, result.exception

    def test_cli_does_not_send_telemetry_on_help(self, mocker):
        """ Test CLI does not send telemetry on help

        Given
        - CLI has not been run before

        When
        - User attempts to use the CLI --help

        Then
        - CLI should exit successfully
        - Telemetry should NOT be set
        """

        mock_request = mocker.patch('requests.request')

        result = self.runner.invoke(basecli, ['--help'])

        # validate successful exit code
        assert result.exit_code == 0, result.exception
        # validate telemetry data was NOT sent
        assert not mock_request.called

    def test_cli_does_not_send_telemetry_on_env_var_set_to_false(self, mocker):
        """ Test CLI does not send telemetry when allow analytics environment
        variable is set to false

        Given
        - CLI has not been run before

        When
        - User attempts to disable telemetry prior to use

        Then
        - CLI should exit successfully
        - Telemetry should NOT be set
        """

        mocker.patch.dict(
            "os.environ",
            {
                ENV_VARS['ALLOW_TELEMETRY']: 'false'
            }
        )
        mock_request = mocker.patch('requests.request')

        result = self.runner.invoke(
            basecli,
            ['config', 'set-defaults', '--allow-telemetry', 'false']
        )

        # validate successful exit code
        assert result.exit_code == 0, result.exception
        # validate telemetry data was NOT sent
        assert not mock_request.called

    def disabled_test_cli_does_not_send_telemetry_on_disable_telemetry_command(self, mocker):
        """ Test CLI does not send telemetry on command to disable telemetry

        Note: Disabled, unsure this is the right UX

        Given
        - CLI has not been run before

        When
        - User attempts to disable telemetry prior to use

        Then
        - CLI should exit successfully
        - Telemetry should NOT be set
        """

        mocker.patch("os.path.exists").return_value = True
        mocker.patch("os.path.isfile").return_value = True
        mocker.patch(
            'f5cli.config.core.open',
            mocker.mock_open(read_data='firstRunComplete: false')
        )
        mock_request = mocker.patch('requests.request')

        result = self.runner.invoke(
            basecli,
            ['config', 'set-defaults', '--allow-telemetry', 'false']
        )

        # validate successful exit code
        assert result.exit_code == 0, result.exception
        # validate telemetry data was NOT sent
        assert not mock_request.called


class TestContext(object):
    """ Test Class: Context"""
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.context = f5cli.cli.Context()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    @staticmethod
    @pytest.fixture
    def click_echo_fixture(mocker):
        """Test fixture """

        mocker.patch.dict(
            "os.environ",
            {
                ENV_VARS['OUTPUT_FORMAT']: FORMATS['JSON']
            }
        )
        mocker.patch(
            "f5cli.cli.format_output",
            side_effect=TestContext.format_output_side_effect
        )
        return mocker.patch("f5cli.cli.click.echo")

    @staticmethod
    def format_output_side_effect(data):
        """ Format output side effect """
        return data

    def test_log_message_no_argument_with_environment_variable(self, click_echo_fixture):
        """ Log a message, no argument
        Given
        - Environment variable of output format JSON exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """

        self.context.log("Test message")
        click_echo_fixture.assert_called_once_with('Test message', file=sys.stderr)

    def test_log_message_argument_with_environment_variable(self, click_echo_fixture):
        """ Log a message, with argument
        Given
        - Environment variable of output format JSON exists

        When
        - User attempts to log a message

        Then
        - Message is logged in specific format
        """

        self.context.log("Test message with argument: %s", "fake value")
        click_echo_fixture.assert_called_once_with(
            'Test message with argument: fake value', file=sys.stderr)

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

        mocker.patch("os.environ.get").return_value = None
        mocker.patch("os.path.exists").return_value = True
        mocker.patch("os.path.isfile").return_value = True
        mock_open = mocker.patch(
            'f5cli.config.core.open',
            mocker.mock_open(read_data='output: json')
        )
        mock_click_echo = mocker.patch("f5cli.cli.click.echo")

        self.context.log("Test message")

        mock_click_echo.assert_called_once_with(
            '{\n    "message": "Test message"\n}', file=sys.stderr
        )
        assert mock_open.called

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
        mocker.patch("f5cli.cli.os.environ.get").return_value = None
        mocker.patch("f5cli.cli.os.path.isfile").return_value = False
        mocker.patch("f5cli.cli.open", mocker.mock_open(read_data='json'))

        mocker.patch(
            "f5cli.cli.format_output",
            side_effect=TestContext.format_output_side_effect
        )
        mock_click_echo = mocker.patch("f5cli.cli.click.echo")

        self.context.log("Test message")

        mock_click_echo.assert_called_once_with('Test message', file=sys.stderr)

    def test_vlog_message(self, click_echo_fixture):
        """ Vlog a message
        Given
        - Environment variable of output format JSON exists

        When
        - User attempts to log a message

        Then
        - Verbose message is logged
        """

        self.context.verbose = True
        self.context.vlog("Test message")
        click_echo_fixture.assert_called_once_with('Test message', file=sys.stderr)

    def test_vlog_message_verbose_false(self, click_echo_fixture):
        """ Vlog a message
        Given
        - Environment variable of output format JSON exists
        - context.verbose is set to 'False'

        When
        - User attempts to log a message

        Then
        - Verbose message is NOT logged
        """

        self.context.verbose = False
        self.context.vlog("Test message")
        assert click_echo_fixture.called == 0


class TestAliasedGroup(object):
    """ Test Class: Aliased Group """

    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    def test_get_existed_command(self):
        """
        Given
        - foo command log a message

        When
        - invoke foo command

        Then
        - output of foo command is logged

        """
        @click.group('test_alias_group', cls=AliasedGroup)
        def mockcli():
            """ test aliased group """

        @mockcli.command('mockcommand')
        @PASS_CONTEXT
        def mockcommand(ctx):  # pylint: disable=unused-variable
            ctx.log("Test mock command")
        result = self.runner.invoke(mockcli, 'mockcommand')
        assert not result.exception
        assert result.output == json.dumps(
            {'message': 'Test mock command'},
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
        @click.group('test_alias_group', cls=AliasedGroup)
        def mockcli():
            """ test aliased group """

        @mockcli.command('mockcommand')
        @PASS_CONTEXT
        def mockcommand(ctx):  # pylint: disable=unused-variable
            ctx.log("Test aliased group")
        result = self.runner.invoke(mockcli, 'bar')
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
        @click.group('test_alias_group', cls=AliasedGroup)
        def mockcli():
            """ test aliased group """

        @mockcli.command('foot')
        @PASS_CONTEXT
        def foot(ctx):  # pylint: disable=unused-variable
            ctx.log("Test foot command")
        result = self.runner.invoke(mockcli, 'foo')

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
        def mockcli():
            """ test aliased group """

        @mockcli.command('foot')
        @PASS_CONTEXT
        def foot(ctx):  # pylint: disable=unused-variable
            ctx.log("Test foot command")

        @mockcli.command('food')
        @PASS_CONTEXT
        def food(ctx):  # pylint: disable=unused-variable
            ctx.log("Test food command")

        result = self.runner.invoke(mockcli, 'foo')
        assert result.exception
        assert "Error: Too many matches: food, foot" in result.output
