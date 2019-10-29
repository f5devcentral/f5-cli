import click
from ...global_test_imports import pytest

# Module under test
from f5cloudcli.utils import clients


class TestUtilsClients(object):
    """ Test Utils clients"""
    @classmethod
    def setup_class(cls):
        """ Setup func """
        pass

    @classmethod
    def teardown_class(cls):
        """ Teardown func """
        pass

    def test_get_non_exist_environment_variables(self, mocker):
        """ Retrieve a non existed environment variable
        Given
        - Environment variable FOO does not exist
        - Environment variable BAR exists

        When
        - Multiple environment variables including FOO are requested

        Then
        - Exception is thrown
        """
        mocker.patch.dict("f5cloudcli.utils.clients.os.environ",
                          {
                              "BAR": "bar_value",
                              "TENANT_ID": "tenant_id_value",
                              "CLIENT_ID": "client_id_value"
                          })
        with pytest.raises(click.exceptions.ClickException) as e:
            clients.get_env_vars(["FOO", "BAR", "CLIENT_ID"])
        assert e.value.args[0] == "Environment variables must exist: ['FOO', 'BAR', 'CLIENT_ID']"

    def test_get_existed_environment_variables(self, mocker):
        """ Retrieve multiple existed environment variable
        Given
        - Environment variables FOO and BAR exist

        When
        - FOO and BAR are requested

        Then
        - Values for FOO and BAR are returned
        """
        mocker.patch.dict("f5cloudcli.utils.clients.os.environ",
                          {"FOO": "foo_value", "BAR": "bar_value", "CLIENT_ID": "test_client_id"})
        results = clients.get_env_vars(["FOO", "BAR"])
        assert results == ["foo_value", "bar_value"]

    def test_get_unsupported_provider(self, mocker):
        """ Retrieve a unsupported cloud provider
        Given
        - 'alibaba' cloud is not supported

        When
        - 'alibaba' cloud is requested

        Then
        - exception is thrown
        """
        with pytest.raises(click.exceptions.ClickException) as e:
            clients.get_provider_client('alibaba')
        assert e.value.args[0] == "Provider alibaba not implemented"

    def test_get_azure_provider(self, mocker):
        """ Retrieve azure cloud provider
        Given
        - 'azure' cloud is supported

        When
        - 'azure' cloud is requested

        Then
        - azure provider client is returned
        """
        mocker.patch.dict("f5cloudcli.utils.clients.os.environ",
                          {
                              'F5_CLI_PROVIDER_TENANT_ID': '1',
                              'F5_CLI_PROVIDER_CLIENT_ID': '2',
                              'F5_CLI_PROVIDER_SECRET': '3',
                              'F5_CLI_PROVIDER_SUBSCRIPTION_ID': '4'
                          })
        mock_azure_client = mocker.patch("f5cloudcli.utils.clients.provider.azure.ProviderClient")
        clients.get_provider_client('azure')
        mock_azure_client.assert_called_once_with(tenant_id='1',
                                                  client_id='2',
                                                  secret='3',
                                                  subscription_id='4')

    def test_get_aws_provider(self, mocker):
        """ Retrieve aws cloud provider
        Given
        - 'aws' cloud is supported

        When
        - 'aws' cloud provider is requested

        Then
        - aws provider client is returned
        """
        mocker.patch.dict("f5cloudcli.utils.clients.os.environ",
                          {
                              'F5_CLI_PROVIDER_ACCESS_KEY': '1',
                              'F5_CLI_PROVIDER_SECRET_KEY': '2',
                              'F5_CLI_PROVIDER_REGION_NAME': '3'
                          })
        mock_aws_client = mocker.patch("f5cloudcli.utils.clients.provider.aws.ProviderClient")
        clients.get_provider_client('aws')
        mock_aws_client.assert_called_once_with(access_key='1',
                                                secret_key='2',
                                                region_name='3')
