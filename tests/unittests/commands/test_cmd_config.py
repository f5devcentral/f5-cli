""" Test Config command """

from f5cli.commands.cmd_config import cli

from ...global_test_imports import CliRunner


class TestCommandConfig(object):
    """ Test Class: command config """
    @classmethod
    def setup_class(cls):
        """ Setup func """
        cls.runner = CliRunner()

    @classmethod
    def teardown_class(cls):
        """ Teardown func """

    def test_cmd_configure_output_format_cli_dir_not_exist(self, mocker):
        """ Configure output format
        Given
        - BIG IP is up
        - F5_CLI_DIR not exists

        When
        - User attempts to configure output format as JSON_FORMAT

        Then
        - F5_CLI_DIR is created
        - JSON_FORMAT is written into F5_CONFIG_FILE
        """
        mock_path_exist = mocker.patch("os.path.exists")
        mock_path_exist.return_value = False
        mock_make_dir = mocker.patch("os.makedirs")
        mocker.patch("f5cli.cli.Context.log")
        with mocker.patch('f5cli.commands.cmd_config.open', new_callable=mocker.mock_open()):
            mock_json_dump = mocker.patch("json.dump")
            self.runner.invoke(cli, ['output-format', '--output', 'json'])
            mock_json_dump.assert_called_once()
            mock_make_dir.assert_called_once()

    def test_cmd_configure_output_format_cli_dir_exist(self, mocker):
        """ Configure output format
        Given
        - BIG IP is up
        - F5_CLI_DIR exists

        When
        - User attempts to configure output format as JSON_FORMAT

        Then
        - JSON_FORMAT is written into F5_CONFIG_FILE
        """
        mock_path_exist = mocker.patch("os.path.exists")
        mock_path_exist.return_value = True
        mocker.patch("f5cli.cli.Context.log")
        with mocker.patch('f5cli.commands.cmd_config.open', new_callable=mocker.mock_open()):
            mock_json_dump = mocker.patch("json.dump")
            self.runner.invoke(cli, ['output-format', '--output', 'json'])
            mock_json_dump.assert_called_once()
