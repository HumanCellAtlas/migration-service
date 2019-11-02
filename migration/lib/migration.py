import json
from enum import Enum


class Migration():
    """
    Class encapsulating information about all potential migrations that may occur as enumerated by a migrations.json
    file.
    """

    class Strategy(Enum):
        EXACT = 1
        BEST_EFFORT = 2

    def __init__(self, migrations_file_path):
        with open(migrations_file_path, 'r') as migrations_file:
            migrations = json.load(migrations_file)
        self.migrations = [self.MigrationDescriptor(migration) for migration in migrations]

    class MigrationDescriptor():
        def __init__(self, dictionary_representation):
            self.source_metadata_schema = dictionary_representation.get("source_ref")
            self.target_metadata_schema = dictionary_representation.get("target_ref")

            self.task_groups = []
            for task_group in dictionary_representation.get("task_groups"):
                task_list = []
                for task in task_group.get("tasks"):
                    task_list.append(self.Task(task))

        class Task():
            """
            A small object encapsulating a function and parameters to be run in order to perform one migration task.
            """

            def __init__(self, dictionary_representation):
                self.function = dictionary_representation.get("function")
                self.parameters = dictionary_representation.get("parameters")

            def run_task(self, object_upon_which_to_perform_task):
                pass
