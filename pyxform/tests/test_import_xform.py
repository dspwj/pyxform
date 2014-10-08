'''
Tests importing of XForms. XForm importing is also tested in 
'test_survey_to_xlsform' to a degree.

.. module:: test_import_xform
    :Date: 2014/09/15
    
.. codeauthor:: Esmail Fadae <esmail.fadae@kobotoolbox.org>
'''


import unittest
import os.path

from pyxform import survey_from


class Test_ImportXForm(unittest.TestCase):
    test_directory_path= os.path.dirname(__file__)

    def test_single_select_one_survey(self):
        '''
        Test that an XForm with a single "Select One" question is imported \
        correctly.
        '''
        
        xform_file_path= os.path.join(self.test_directory_path,\
                                  'example_xforms/single_select_one_survey.xml')
        
        survey= survey_from.xform(xform_file_path)
        self.assertEqual(survey['title'], 'Single "select one" survey')
        self.assertEqual(survey['name'], 'single_select_one_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 1)
                
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select one" question')
        self.assertEqual(question_1['name'], 'Select_one_question')
        self.assertEqual(question_1['type'], 'select one')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


    def test_single_select_many_survey(self):
        '''
        Test that an XForm with a single "Select Many" question is imported \
        correctly.
        '''
        
        xform_file_path= os.path.join(self.test_directory_path,\
                                  'example_xforms/single_select_many_survey.xml')
        
        survey= survey_from.xform(xform_file_path)
        self.assertEqual(survey['title'], 'Single "Select Many" Survey')
        self.assertEqual(survey['name'], 'single_select_many_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 1)
                
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select Many" question.')
        self.assertEqual(question_1['name'], 'Select_Many_question')
        self.assertEqual(question_1['type'], 'select all that apply')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


    def test_multiple_select_question_survey(self):
        '''
        Test that an XForm with a "Select One" and a "Select Many" question is \
        imported correctly.
        '''
        
        xform_file_path= os.path.join(self.test_directory_path,\
                            'example_xforms/multiple_select_question_survey.xml')
        
        survey= survey_from.xform(xform_file_path)
        self.assertEqual(survey['title'], 'Multiple "Select" Question Survey.')
        self.assertEqual(survey['name'], 'multiple_select_question_survey')
        
        questions= survey['children']
        self.assertEqual(len(questions), 2)
        
        question_1= questions[0]
        self.assertEqual(question_1['label'], '"Select One" question.')
        self.assertEqual(question_1['name'], 'Select_One_question')
        self.assertEqual(question_1['type'], 'select one')
        
        options= question_1['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))

        question_2= questions[1]
        self.assertEqual(question_2['label'], '"Select Many" question.')
        self.assertEqual(question_2['name'], 'Select_Many_question')
        self.assertEqual(question_2['type'], 'select all that apply')
        
        options= question_2['children']
        self.assertEqual(len(options), 2)
        
        for o_num, o in enumerate(options, 1):
            self.assertEqual(o['label'], 'Option {}'.format(o_num))
            self.assertEqual(o['name'], 'option_{}'.format(o_num))


    def test_import_from_file_obj(self):
        '''
        Test the interface for importing XForms from an already-opened file 
        object.
        '''
        
        xform_file_path= os.path.join(self.test_directory_path, \
          'example_xforms/all_question_types_survey_kf1.xml')
        
        survey_from_path= survey_from.xform(path=xform_file_path)
        
        with open(xform_file_path) as f:
            survey_from_file_obj= survey_from.xform(filelike_obj=f)
        
        self.assertEqual(survey_from_file_obj, survey_from_path)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()