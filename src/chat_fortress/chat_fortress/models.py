from abc import ABC
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BaseModel(ABC, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatFortressUser(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Chat Fortress User")
        verbose_name_plural = _("Chat Fortress User")


class PublicKey(BaseModel):
    creator = models.ForeignKey(ChatFortressUser, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        verbose_name = _("GPG Public Key")
        verbose_name_plural = _("GPG PublicKeys")


class PrivateKey(BaseModel):
    owner = models.ForeignKey(ChatFortressUser, on_delete=models.CASCADE)
    content = models.TextField()
    password = models.CharField(blank=True, null=True)

    class Meta:
        verbose_name = _("GPG Private Key")
        verbose_name_plural = _("GPG Private Keys")


class Membership(BaseModel):
    user = models.ForeignKey(
        ChatFortressUser, on_delete=models.CASCADE, related_name="encryption_group_memberships",
    )
    encryption_group = models.ForeignKey(
        "EncryptionGroup",
        on_delete=models.CASCADE,
        related_name="encryption_group_memberships",
    )
    is_manager = models.BooleanField(_("Is Group Manager"), default=False)

    class Meta:
        verbose_name = _("Membership")
        verbose_name_plural = _("Memberships")
        unique_together = ("user", "encryption_group")


class EncryptionGroup(BaseModel):
    users = models.ManyToManyField(
        ChatFortressUser, through=Membership, related_name="encryption_groups"
    )
    public_keys = models.ManyToManyField(PublicKey)

    class Meta:
        verbose_name = _("Encryption Group")
        verbose_name_plural = _("Encryption Groups")
