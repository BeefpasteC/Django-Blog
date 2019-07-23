from django.db import models

# Create your models here.

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    def __str__(self):
        return self.name


from ckeditor.fields import RichTextField
class Blog(models.Model): #定义数据表 类名是表名的一部分
    title = models.CharField(max_length=32) #char(32)
    date = models.DateField(auto_now=True) #date
    content = RichTextField()
    description = RichTextField()
    picture = models.ImageField(upload_to='images')
    # upload_to 将图片上传到static文件下的images

    author = models.ForeignKey(to=Author,on_delete = models.SET_DEFAULT,default=1)
        #models.CASCADE 级联删除，主键删除外键对应数据删除
        #models.SET_NULL 主键删除，外键设置为空，需要外键设置可以为空 null = True
        #models.SET_DEFAULT 主键删除之后，外键采用默认值，需要设置默认值 default=""
    type = models.ManyToManyField(to=Type)

    def __str__(self):
        return self.title
    #django 默认创建id字段，主键，自增长
    #django 所有字段默认不可以为空
# Create your models here.
class SignData(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)