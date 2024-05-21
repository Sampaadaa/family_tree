from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Relationship(models.Model):
    parent = models.ForeignKey(Person, related_name='child_relationships', on_delete=models.CASCADE)
    child = models.ForeignKey(Person, related_name='parent_relationships', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.parent} -> {self.child}"
