from tortoise import Model, fields


class Sources(Model):
    name = fields.CharField(20, pk=True)

    def __str__(self):
        return f"{self.name}"


class Binaries(Model):
    name = fields.CharField(20, pk=True)

    def __str__(self):
        return f"{self.name}"
