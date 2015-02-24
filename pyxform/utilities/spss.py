'''
Created on Jan 21, 2015

@author: esmail
'''


from __future__ import absolute_import
from __future__ import unicode_literals
from collections import OrderedDict

import odk_to_spss_syntax
from odk_to_spss_syntax import get_spss_variable_name
from odk_to_spss_syntax import get_spss_variable_label
from odk_to_spss_syntax import get_spss_value_label

from .. import constants
from .get_label_mappings import get_label_mappings
from ..utilities import get_questions
from ..survey import Survey


VARIABLE_LABELS_DICT_KEY, VALUE_LABELS_DICT_KEY= 'variable_labels_dict', 'value_labels_dict'


def question_to_spss_variable_name(question, group_delimiter=None):
    group_prefix= ''
    if group_delimiter is not None:
        # If the question's full path is desired, find it.
        parent= question.get(constants.PARENT, Survey())
        while not isinstance(parent, Survey):
            group_prefix= parent.name + group_delimiter + group_prefix
            parent= parent.get(constants.PARENT, Survey())

    if question.is_multi_select():
        # FIXME: This kind of overloading is dangerous; find a better interface.
        # Actually return a list of the names of the SPSS variables this multi-select will be disaggregated into.
        base_variable_name= group_prefix + question.name
        spss_variable_name= [get_spss_variable_name(base_variable_name)]

        for option in question.options:
            disaggregated_variable_name= get_spss_variable_name(base_variable_name + option.name)
            spss_variable_name.append(disaggregated_variable_name)
    else:
        spss_variable_name= get_spss_variable_name(group_prefix + question.name)

    return spss_variable_name


def get_per_language_labels(survey, path_prefixes=True, question_name_transform=None):

    question_label_mappings, option_label_mappings, label_languages= get_label_mappings(survey, path_prefixes=path_prefixes)
    per_language_labels= dict()

    for question_name, question_labels in question_label_mappings.iteritems():

        if question_name_transform:
            final_question_name= question_name_transform(question_name)
        else:
            final_question_name= question_name
        question_options= option_label_mappings.get(question_name, dict())

        for language in label_languages:
            if language in question_labels:
                per_language_labels.setdefault(language, dict()).setdefault(VARIABLE_LABELS_DICT_KEY, OrderedDict())[final_question_name]= question_labels[language]

            for option_name, option_labels in question_options.iteritems():
                if language in option_labels:
                    per_language_labels.setdefault(language, dict()).setdefault(VALUE_LABELS_DICT_KEY, OrderedDict()).setdefault(final_question_name, OrderedDict())[option_name]= option_labels[language]

    return per_language_labels


def survey_to_spss_label_syntax(survey):

    exportable_label_mappings= get_per_language_labels(survey)

    syntaxes= dict()
    for language in exportable_label_mappings.keys():
        variable_labels_dict= exportable_label_mappings.get(language, dict()).get(VARIABLE_LABELS_DICT_KEY)
        value_labels_dict= exportable_label_mappings.get(language, dict()).get(VALUE_LABELS_DICT_KEY)

        spss_label_syntax_string= odk_to_spss_syntax.from_dicts(variable_labels_dict, value_labels_dict)
        syntaxes[language]= spss_label_syntax_string

    return syntaxes


if __name__ == '__main__':
    from .. import survey_from
    s= survey_from.xls('/home/esmail/Downloads/uga_14_v6 (1).xls')
    syntaxes= survey_to_spss_label_syntax(s)
    for language in syntaxes:
        with open('/home/esmail/Downloads/uga_14_v6' + '_' + language + '_labels.sps', 'w') as f:
            f.write(syntaxes['default'].encode('UTF-8'))
