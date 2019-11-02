from enum import Enum
from .metadata_view import MetadataView

class MetadataMigrator():
    """
    Given a JSON file containing metadata and a metadata schema version that is appropriate for the metadata file,
    generates a new file that migrates it to the newer version.
    """



    def __init__(self, metadata_json_file, target_schema_version):
        self.metadata_json_file = metadata_json_file
        pass

    def migrate_metadata(self, strategy: Strategy):
        metadata_view = MetadataView.from_file(path_to_metadata_json_file=self.metadata_json_file)