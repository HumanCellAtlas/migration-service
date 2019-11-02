import unittest

from migration.lib.metadata_transformation_functions import move_property, delete_property


class TestMetadataTransformationFunctions(unittest.TestCase):

    def test__move_property__same_nesting(self):
        metadata_dict = {"salutations": {"greetings": {"hi": 1234, "hello": 2345, "hiya": 3456}}}
        source_property = "salutations.greetings.hi"
        target_property = "salutations.greetings.yo"

        actual_transformed_metadata_dict = move_property(metadata_dict, source_property, target_property)

        expected_transformed_metadata_dict = {"salutations": {"greetings": {"yo": 1234, "hello": 2345, "hiya": 3456}}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)

    def test__move_property__different_nesting(self):
        metadata_dict = {"salutations": {"greetings": {"hi": 1234, "hello": 2345, "hiya": 3456}}}
        source_property = "salutations.greetings.hi"
        target_property = "salutations.goodbyes"

        actual_transformed_metadata_dict = move_property(metadata_dict, source_property, target_property)

        expected_transformed_metadata_dict = {
            "salutations": {"goodbyes": 1234, "greetings": {"hello": 2345, "hiya": 3456}}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)

    def test__move_property__same_nesting_multiple_new_keys(self):
        metadata_dict = {"salutations": {"greetings": {"hi": 1234, "hello": 2345, "hiya": 3456}}}
        source_property = "salutations.greetings.hi"
        target_property = "salutations.goodbyes.bye"

        actual_transformed_metadata_dict = move_property(metadata_dict, source_property, target_property)

        expected_transformed_metadata_dict = {
            "salutations": {"goodbyes": {"bye": 1234}, "greetings": {"hello": 2345, "hiya": 3456}}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)

    def test__move_property__multiple_objects(self):
        metadata_dict = {
            "salutations": {"greetings": [{"approach": "hi"}, {"approach": "hello"}, {"approach": "hiya"}]}}
        source_property = "salutations.greetings.approach"
        target_property = "salutations.greetings.spoken"

        actual_transformed_metadata_dict = move_property(metadata_dict, source_property, target_property)

        expected_transformed_metadata_dict = {
            "salutations": {"greetings": [{"spoken": "hi"}, {"spoken": "hello"}, {"spoken": "hiya"}]}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)

    def test__move_property__multiple_objects_different_nesting_fails(self):
        metadata_dict = {
            "salutations": {"greetings": [{"approach": "hi"}, {"approach": "hello"}, {"approach": "hiya"}]}}
        source_property = "salutations.greetings.approach"
        target_property = "salutations.spoken"

        with self.assertRaises(Exception) as expected_exception:
            move_property(metadata_dict, source_property, target_property)
        self.assertIn("Cannot migration a multivalue object at one nested level to a different nested level",
                      str(expected_exception.exception))

    def test__move_property__multiple_objects_mismatch_hierarchy_fails(self):
        metadata_dict = {
            "salutations": {"greetings": [{"approach": "hi"}, {"approach": "hello"}, {"approach": "hiya"}]}}
        source_property = "salutations.greetings.approach"
        target_property = "salutations.goodbyes.spoken"

        with self.assertRaises(Exception) as expected_exception:
            move_property(metadata_dict, source_property, target_property)
        self.assertIn("Cannot migration a multivalue object at one nested level to a different nested level",
                      str(expected_exception.exception))

    def test__delete_property__leaf_property(self):
        metadata_dict = {"salutations": {"greetings": {"hi": 1234, "hello": 2345, "hiya": 3456}}}
        property_to_delete = "salutations.greetings.hi"

        actual_transformed_metadata_dict = delete_property(metadata_dict, property_to_delete)

        expected_transformed_metadata_dict = {"salutations": {"greetings": {"hello": 2345, "hiya": 3456}}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)

    def test__delete_property__non_leaf_property(self):
        metadata_dict = {"salutations": {"greetings": {"hi": 1234, "hello": 2345, "hiya": 3456}}}
        property_to_delete = "salutations.greetings"

        actual_transformed_metadata_dict = delete_property(metadata_dict, property_to_delete)

        expected_transformed_metadata_dict = {"salutations": {}}
        self.assertEqual(expected_transformed_metadata_dict, actual_transformed_metadata_dict)
