# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from django.contrib.auth.models import Permission, Group, GroupManager
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from systems.models import *
from common.models import BaseModel

menu_type = {
    1: '模塊',
    2: '菜單',
    3: '操作',
}

operate_type = {
    'none': '無',
    'add': '新增',
    'del': '刪除',
    'update': '編輯',
    'view': '查看',
}


class Menu(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='父級菜單')
    name = models.CharField(max_length=32, verbose_name='菜單名稱')
    code = models.CharField(max_length=32, verbose_name='菜單代碼')
    curl = models.CharField(max_length=101, verbose_name='菜單URL')
    icon = models.CharField(max_length=32, blank=True, verbose_name='菜單圖標')
    hidden = models.BooleanField(default=False, verbose_name='菜單是否隱藏')
    no_cache = models.BooleanField(default=True, verbose_name='菜單是否緩存')
    active_menu = models.CharField(max_length=32, blank=True, verbose_name='激活菜單')
    sequence = models.SmallIntegerField(default=0, verbose_name='排序值')
    type = models.CharField(max_length=1, choices=tuple(menu_type.items()), default=2, verbose_name='菜單類型')
    status = models.BooleanField(default=True, verbose_name='狀態')
    operate = models.CharField(max_length=11, choices=tuple(operate_type.items()), default='none', verbose_name='操作類型')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        ordering = ['id', ]
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Role(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='父級角色')
    name = models.CharField(max_length=32, unique=True, verbose_name='名稱')
    code = models.CharField(max_length=32, unique=True, verbose_name='代碼')
    sequence = models.SmallIntegerField(default=0, verbose_name='排序值')
    menus = models.ManyToManyField(Menu, blank=True, verbose_name='菜單')
    model_perms = models.ManyToManyField(Permission, blank=True, verbose_name='model權限')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Group(BaseModel, Group):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='父級角色')
    code = models.CharField(max_length=32, unique=True, verbose_name='代碼')
    sequence = models.SmallIntegerField(default=0, verbose_name='排序值')
    roles = models.ManyToManyField(Role, verbose_name='roles', blank=True, )

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = '分組'
        verbose_name_plural = verbose_name

    objects = GroupManager()  # 創建用戶


class PermissionsMixin(models.Model):
    group = models.ForeignKey(
        Group,
        verbose_name='group',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user_set",
        related_query_name="user",
    )
    roles = models.ManyToManyField(
        Role,
        verbose_name='roles',
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )
    model_perms = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        username 是唯一標識，沒有會報錯
        """

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )
        user.set_password(password)  # 檢測密碼合理性
        user.save(using=self._db)  # 保存密碼
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username,
                                password=password,
                                )
        user.is_admin = True  # 比創建用戶多的一個字段
        user.save(using=self._db)
        return user


class User(BaseModel, PermissionsMixin, AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, db_index=True)
    realname = models.CharField(max_length=32, default="圖書館管理員", blank=True, verbose_name='真實名字')
    email = models.EmailField(blank=True, default="itimor@126.com", verbose_name='郵箱')
    avatar = models.CharField(max_length=255, default='http://m.imeitou.com/uploads/allimg/2017110610/b3c433vwhsk.jpg')
    status = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'  # 必須有一個唯一標識--USERNAME_FIELD

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用戶'
        verbose_name_plural = '用戶'

    objects = UserManager()  # 創建用戶
