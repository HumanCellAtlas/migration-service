import json

from .schema_reference import SchemaReference


class MetadataView(dict):
    """
    A view representing the data that exists in a metadata file. The contents are stored as a dictionary with a
    specific pointer to the metadata schema that was responsible for generating the view of the data as it is currently.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def from_file(path_to_metadata_json_file: str):
        with open(path_to_metadata_json_file, 'r') as metadata_file:
            metadata_dict = json.load(metadata_file)
        return MetadataView(**metadata_dict)

    @property
    def schema_reference(self) -> SchemaReference:
        return SchemaReference(self['describedBy'])
