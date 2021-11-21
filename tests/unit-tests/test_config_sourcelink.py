# -*- coding: utf-8 -*-
"""
:copyright: Copyright 2021 Sphinx Confluence Builder Contributors (AUTHORS)
:license: BSD-2-Clause (LICENSE)
"""

from tests.lib import build_sphinx
from tests.lib import parse
from tests.lib import prepare_conf
import os
import unittest


class TestConfluenceConfigSourceLink(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = prepare_conf()
        test_dir = os.path.dirname(os.path.realpath(__file__))
        cls.dataset = os.path.join(test_dir, 'datasets', 'minimal')

    def test_storage_sourcelink_custom_text(self):
        """validate sourcelink can handle custom options (storage)"""
        #
        # Ensures the URL format string can be customizable by a user, if they
        # want to provide other options to help format the source URL.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'text': 'custom text',
            'url': 'dummy',
        }

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            text = a_tag.find(string=True, recursive=False)
            self.assertEqual(text, 'custom text')

    def test_storage_sourcelink_custom_url(self):
        """validate sourcelink can handle custom options (storage)"""
        #
        # Ensures the URL format string can be customizable by a user, if they
        # want to provide other options to help format the source URL.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'mypath': 'test-docs',
            'url': 'ftp://example.com/{mypath}/{version}',
            'version': 'v8',
        }

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], 'ftp://example.com/test-docs/v8')

    def test_storage_sourcelink_docvalues(self):
        """validate sourcelink is given page/suffix values (storage)"""
        #
        # Ensures the URL format string is provided individual document names
        # and their suffixes when generating a link.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'url': '{page}{suffix}',
        }

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], 'index.rst')

    def test_storage_sourcelink_simple(self):
        """validate sourcelink can accept a simple url value (storage)"""
        #
        # Ensures the URL string can be a non-special format string, applying
        # the contents directly into the href value.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'url': 'https://git.example.net/mydocs',
        }

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], 'https://git.example.net/mydocs')

    def test_storage_sourcelink_template_bitbucket_default(self):
        """validate sourcelink bitbucket default options (storage)"""
        #
        # Ensures the a Bitbucket configured source link generated an expected
        # Bitbucket.com reference.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'subfolder/',
            'owner': 'example-owner',
            'repo': 'example-prj',
            'type': 'bitbucket',
            'version': 'v1.0',
        }

        expected = 'https://bitbucket.org/example-owner/example-prj/src/v1.0/subfolder/index.rst?mode=view'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_bitbucket_edit_mode(self):
        """validate sourcelink bitbucket edit-mode (storage)"""
        #
        # Ensures the a Bitbucket configured source link generated an expected
        # Bitbucket.com reference with an edit mode.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'doc/',
            'owner': 'example-owner',
            'repo': 'example-prj2',
            'type': 'bitbucket',
            'version': 'main',
            'view': 'edit',
        }

        expected = 'https://bitbucket.org/example-owner/example-prj2/src/main/doc/index.rst?mode=edit'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_bitbucket_host_protocol(self):
        """validate sourcelink bitbucket custom host (storage)"""
        #
        # Ensures the a Bitbucket configured source link generated with a custom
        # hostname and protocol, but still with the expected Bitbucket path.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'host': 'example.com',
            'owner': 'owner',
            'protocol': 'http',
            'repo': 'prj-q',
            'type': 'bitbucket',
            'version': 'feature-one',
        }

        expected = 'http://example.com/owner/prj-q/src/feature-one/index.rst?mode=view'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_github_default(self):
        """validate sourcelink github default options (storage)"""
        #
        # Ensures the a GitHub configured source link generated an expected
        # GitHub.com reference.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'Documentation/',
            'owner': 'example-owner',
            'repo': 'example-prj',
            'type': 'github',
            'version': 'v1.0',
        }

        expected = 'https://github.com/example-owner/example-prj/blob/v1.0/Documentation/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_github_edit_mode(self):
        """validate sourcelink github edit-mode (storage)"""
        #
        # Ensures the a GitHub configured source link generated an expected
        # GitHub.com reference with an edit mode.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'doc/',
            'owner': 'example-owner',
            'repo': 'example-prj2',
            'type': 'github',
            'version': 'main',
            'view': 'edit',
        }

        expected = 'https://github.com/example-owner/example-prj2/edit/main/doc/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_github_host_protocol(self):
        """validate sourcelink github custom host (storage)"""
        #
        # Ensures the a GitHub configured source link generated with a custom
        # hostname and protocol, but still with the expected GitHub path.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'docs/',
            'host': 'example.com',
            'owner': 'owner',
            'protocol': 'http',
            'repo': 'prj',
            'type': 'github',
            'version': 'bugfix/alpha',
        }

        expected = 'http://example.com/owner/prj/blob/bugfix/alpha/docs/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_gitlab_default(self):
        """validate sourcelink gitlab default options (storage)"""
        #
        # Ensures the a GitLab configured source link generated an expected
        # GitLab.com reference.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'Documentation/',
            'owner': 'example-owner',
            'repo': 'prj3',
            'type': 'gitlab',
            'version': '2-7',
        }

        expected = 'https://gitlab.com/example-owner/prj3/blob/2-7/Documentation/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_gitlab_edit_mode(self):
        """validate sourcelink gitlab edit-mode (storage)"""
        #
        # Ensures the a GitLab configured source link generated an expected
        # GitLab.com reference with an edit mode.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'owner': 'my-owner',
            'repo': 'my-project',
            'type': 'gitlab',
            'version': 'master',
            'view': 'edit',
        }

        expected = 'https://gitlab.com/my-owner/my-project/edit/master/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)

    def test_storage_sourcelink_template_gitlab_host_protocol(self):
        """validate sourcelink gitlab custom host (storage)"""
        #
        # Ensures the a GitLab configured source link generated with a custom
        # hostname and protocol, but still with the expected GitLab path.

        config = dict(self.config)
        config['confluence_sourcelink'] = {
            'container': 'docs/',
            'host': 'example.net',
            'owner': 'owner4',
            'protocol': 'http',
            'repo': 'prj',
            'type': 'gitlab',
            'version': 'bugfix/beta',
        }

        expected = 'http://example.net/owner4/prj/blob/bugfix/beta/docs/index.rst'

        out_dir = build_sphinx(self.dataset, config=config)

        with parse('index', out_dir) as data:
            a_tag = data.find('a')
            self.assertTrue(a_tag.has_attr('href'))
            self.assertEqual(a_tag['href'], expected)