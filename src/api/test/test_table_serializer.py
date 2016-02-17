from mock import patch, MagicMock

from django.test import TestCase

from psycopg2 import ProgrammingError
from ..serializer import TableSerializer


class TableSerializerTests(TestCase):
    """Test RepoSerializer methods"""

    def setUp(self):
        self.username = "delete_me_username"
        self.repo_base = "delete_me_repo_base"
        self.password = "delete_me_password"

        self.mock_manager = self.create_patch(
            'api.serializer.DataHubManager')
        self.serializer = TableSerializer(
            username=self.username, repo_base=self.repo_base)

    def create_patch(self, name):
        # helper method for creating patches
        patcher = patch(name)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def test_create_table_happy_path(self):
        mock_manager_create_table = self.mock_manager.return_value.create_table

        table = 'table_name'
        repo = 'repo_name'
        params = [
            {'column_name': 'id', 'data_type': 'integer'},
            {'column_name': 'words', 'data_type': 'text'}
            ]

        success = self.serializer.create_table(repo, table, params)

        self.assertTrue(mock_manager_create_table.called)
        self.assertTrue(success)

    def test_create_table_sad_path(self):
        mock_manager_create_table = self.mock_manager.return_value.create_table
        mock_manager_create_table.side_effect = ProgrammingError

        table = 'table_name'
        repo = 'repo_name'
        params = [
            {'column_name': 'id', 'data_type': 'integer'},
            {'column_name': 'words', 'data_type': 'text'}
            ]
        success = self.serializer.create_table(repo, table, params)

        self.assertTrue(mock_manager_create_table.called)
        self.assertFalse(success)

    def test_list_tables(self):
        mock_manager_list_tables = self.mock_manager.return_value.list_tables
        mock_manager_list_tables.return_value = ['table1', 'table2']

        repo = 'repo_name'

        tables = self.serializer.list_tables(repo)

        self.assertTrue(mock_manager_list_tables.called)
        self.assertEqual(tables, ['table1', 'table2'])

    def test_describe_table_no_detail(self):
        mock_mngr_desc_table = self.mock_manager.return_value.describe_table
        mock_mngr_desc_table.return_value = [(u'id', u'integer'),
                                             (u'words', u'text')]
        repo = 'repo_name'
        table = 'table_name'
        expected_description = [{"data_type": "integer", "column_name": "id"},
                                {"data_type": "text", "column_name": "words"}]
        description = self.serializer.describe_table(repo, table)

        self.assertTrue(mock_mngr_desc_table.called)
        self.assertEqual(description, expected_description)
