"""
sentry_sprintly.plugin
~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""

from django import forms
from django.utils import simplejson as json
from django.utils.translation import ugettext_lazy as _
from sentry.plugins.bases import issue

import sentry_sprintly
import urllib
import urllib2
import base64


class SprintlyOptionsForm(forms.Form):
    email = forms.CharField(label=_('Email'),
        help_text=_('Enter your Sprint.ly account email address.'))
    api_key = forms.CharField(label=_('API Key'),
        help_text=_('Enter your Sprint.ly API key.'))
    product_id = forms.CharField(label=_('Product id'),
        help_text=_('Enter your Sprint.ly product id.'))


class SprintlyNewIssueForm(issue.NewIssueForm):
    SCORE_CHOICES = (
        ('~', '---'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )
    tags = forms.CharField(label=_('Tags'), required=False,
        widget=forms.TextInput(attrs={'class': 'span3', 'placeholder': 'e.g. sentry, exception'}),
        help_text=_('Enter comma separated list of tags. (optional)'))
    score = forms.CharField(label=_('Score'),
        widget=forms.Select(choices=SCORE_CHOICES),
        help_text=_('(optional)'))


class SprintlyPlugin(issue.IssuePlugin):
    author = 'Matt Robenolt'
    author_url = 'https://github.com/mattrobenolt'
    version = sentry_sprintly.VERSION
    description = 'Turn Sentry exceptions into new Sprint.ly defects.'
    resource_links = (
        ('Bug Tracker', 'http://github.com/mattrobenolt/sentry-sprintly/issues'),
        ('Source', 'http://github.com/mattrobenolt/sentry-sprintly'),
    )

    slug = 'sprintly'
    title = _('Sprint.ly')
    conf_title = title
    conf_key = 'sprintly'
    project_conf_form = SprintlyOptionsForm
    new_issue_form = SprintlyNewIssueForm

    def is_configured(self, request, project, **kwargs):
        return all([self.get_option(o, project) for o in ('email', 'api_key', 'product_id')])

    def get_new_issue_title(self, **kwargs):
        return 'Create Sprint.ly Defect'

    def create_issue(self, request, group, form_data, **kwargs):
        email = self.get_option('email', group.project)
        api_key = self.get_option('api_key', group.project)
        product_id = self.get_option('product_id', group.project)

        url = 'https://sprint.ly/api/products/{0}/items.json'.format(product_id)

        data = urllib.urlencode({
            'type': 'defect',
            'title': form_data['title'],
            'description': form_data['description'],
            'status': 'backlog',
            'tags': form_data['tags'],
            'score': form_data['score'],
        })

        # Authorization base64
        auth = '{0}:{1}'.format(email, api_key)
        auth = base64.b64encode(auth)

        req = urllib2.Request(url)
        req.add_header('User-Agent', 'sentry-sprintly/{0}'.format(self.version))
        req.add_header('Authorization', 'Basic {0}'.format(auth))

        try:
            resp = urllib2.urlopen(req, data)
        except Exception as e:
            if isinstance(e, urllib2.HTTPError):
                if e.code == 404:
                    raise forms.ValidationError(_('Sprint.ly product not found: {0}'.format(product_id)))

                msg = e.read()
                try:
                    msg = json.loads(msg)
                    msg = msg['message']
                except Exception:
                    pass
            else:
                msg = unicode(e)
            raise forms.ValidationError(_('Error from Sprint.ly: {0}'.format(msg)))

        try:
            data = json.load(resp)
        except Exception as e:
            raise forms.ValidationError(_('Error decoding response from Sprint.ly: {0}'.format(e)))

        return data['number']


    def get_issue_label(self, group, issue_id, **kwargs):
        return 'Sprint.ly #{0}'.format(issue_id)

    def get_issue_url(self, group, issue_id, **kwargs):
        product_id = self.get_option('product_id', group.project)

        return 'https://sprint.ly/product/{0}/item/{1}'.format(product_id, issue_id)
