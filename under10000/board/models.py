from django.db import models
import os
from django.conf import settings

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=64, verbose_name="title")
    contents = models.TextField(verbose_name="contents")
    writer = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="writer"
    )
    write_dttm = models.DateTimeField(auto_now_add=True, verbose_name="upload Date")

    board_name = models.CharField(
        max_length=32, default="Python", verbose_name="board category"
    )
    update_dttm = models.DateTimeField(auto_now=True, verbose_name="lastest updated")
    hits = models.PositiveIntegerField(default=0, verbose_name="hits")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "board"
        verbose_name = "board"
        verbose_name_plural = "board"
