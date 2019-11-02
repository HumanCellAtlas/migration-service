from packaging import version


class SchemaReference:

    def __init__(self, schema_url):
        self.schema_url = schema_url
        self.base_url, self.high_level_entity, self.domain_entity, self.version, self.module = schema_url.rsplit('/', 4)

    def __eq__(self, other):
        self._validate(other)
        version.parse(other.version) == version.parse(self.version)

    def __ne__(self, other):
        self._validate(other)
        version.parse(other.version) != version.parse(self.version)

    def __gt__(self, other):
        self._validate(other)
        return version.parse(other.version) > version.parse(self.version)

    def __ge__(self, other):
        self._validate(other)
        return version.parse(other.version) >= version.parse(self.version)

    def __lt__(self, other):
        self._validate(other)
        return version.parse(other.version) < version.parse(self.version)

    def __le__(self, other):
        self._validate(other)
        return version.parse(other.version) <= version.parse(self.version)

    def _validate(self, other):
        if not all([
            self.base_url == other.base_url,
            self.high_level_entity == other.high_level_entity,
            self.domain_entity == other.domain_entity,
            self.module == other.module
        ]):
            raise Exception("These versions are non-comparable!")
