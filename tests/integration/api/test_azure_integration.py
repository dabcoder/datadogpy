from datadog import api as dog
from datadog import initialize
from tests.integration.api.constants import API_KEY, APP_KEY, API_HOST


class TestAzureIntegration:

    test_tenant_name = "testc44-1234-5678-9101-cc00736ftest"
    test_client_id = "testc7f6-1234-5678-9101-3fcbf464test"
    test_client_secret = "testingx./Sw*g/Y33t..R1cH+hScMDt"
    test_new_tenant_name = "1234abcd-1234-5678-9101-abcd1234abcd"
    test_new_client_id = "abcd1234-5678-1234-5678-1234abcd5678"
    not_yet_installed_error = 'Azure Integration not yet installed.'

    @classmethod
    def setup_class(cls):
        initialize(api_key=API_KEY, app_key=APP_KEY, api_host=API_HOST)

    def test_azure_crud(self):
        # Test Create
        create_output = dog.AzureIntegration.create(
            tenant_name=self.test_tenant_name,
            host_filters="api:test",
            client_id=self.test_client_id,
            client_secret=self.test_client_secret
        )
        assert create_output == {}
        # Test List
        list_tests_pass = False
        for i in dog.AzureIntegration.list():
            if (i['tenant_name'] == self.test_tenant_name and
                    i['host_filters'] == 'api:test'):
                list_tests_pass = True
        assert list_tests_pass
        # Test Update Host Filters
        dog.AzureIntegration.update_host_filters(
            tenant_name=self.test_tenant_name,
            host_filters='api:test2',
            client_id=self.test_client_id
        )
        update_host_filters_tests_pass = False
        for i in dog.AzureIntegration.list():
            if i['host_filters'] == 'api:test2':
                update_host_filters_tests_pass = True
        assert update_host_filters_tests_pass
        # Test Update
        dog.AzureIntegration.update(
            tenant_name=self.test_tenant_name,
            new_tenant_name=self.test_new_tenant_name,
            host_filters="api:test3",
            client_id=self.test_client_id,
            new_client_id=self.test_new_client_id,
            client_secret=self.test_client_secret
        )
        update_tests_pass = False
        for i in dog.AzureIntegration.list():
            if (i['tenant_name'] == self.test_new_tenant_name and
                    i['host_filters'] == 'api:test3'):
                update_tests_pass = True
        assert update_tests_pass
        # Test Delete
        dog.AzureIntegration.delete(
            tenant_name=self.test_new_tenant_name,
            client_id=self.test_new_client_id
        )
        delete_tests_pass = True
        list_output = dog.AzureIntegration.list()
        if type(list_output) == list:
            for i in dog.AzureIntegration.list():
                if i['tenant_name'] == self.test_new_tenant_name:
                    delete_tests_pass = False
        elif self.not_yet_installed_error in list_output['errors'][0]:
            pass
        assert delete_tests_pass
