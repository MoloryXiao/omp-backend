from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models


class OmpUserManager(BaseUserManager):
    def create_user(self, email, name, user_type=1, password=None,):
        """
        创建用户
        """
        if not email:
            raise ValueError('邮箱地址必填！')

        if user_type == 0:
            introduction = "超级用户"
        else:
            introduction = "普通用户"

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            user_type=user_type,
            avatar='https://img.zcool.cn/community/018e8d59bf1eaca801207534bcab6e.jpg@1280w_1l_2o_100sh.jpg',
            introduction=introduction,
            status=1
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        创建超级用户
        """
        user = self.create_user(
            email=email,
            name=name,
            user_type=0,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class OmpUser(AbstractBaseUser):
    """
    OMP用户拓展
    """
    email = models.CharField(db_column='FstrEmail', verbose_name='登录邮箱', max_length=256, null=False, unique=True)
    name = models.CharField(db_column='FstrName', verbose_name='姓名', max_length=256, null=True, blank=True)
    password = models.CharField(db_column='FstrPassword', verbose_name='密码', max_length=256, null=False)
    introduction = models.CharField(db_column='FstrIntroduction', verbose_name='用户描述', max_length=256, default='')
    user_type = models.SmallIntegerField(db_column='FuiUserType', verbose_name='用户类型 0:超级用户,1:普通用户', default=1, null=False)
    avatar = models.TextField(db_column='FstrAvatar', verbose_name='头像地址', null=True, blank=True)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态 0:草稿,1:生效,2:失效', default=0)
    # editor = models.CharField(db_column='FstrEditor', verbose_name='最后修改人', max_length=200, default='', null=False)
    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', auto_now=True)

    objects = OmpUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 't_omp_user_permission'

    def __str__(self):
        return self.email
