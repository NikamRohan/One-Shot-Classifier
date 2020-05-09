from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'unaligned_images' + '/' + '{0}/{1}'.format(instance.person.name,filename)


class Person(models.Model):
	name = models.CharField(max_length=20,null=False,blank = False)

	def __str__(self):
		return f'{self.name}'

class Image(models.Model):
	img = models.FileField(upload_to=user_directory_path)
	person = models.ForeignKey(Person, on_delete=models.PROTECT)

	def __str__(self):
		return f' {self.person.name }_{self.id}'+'img'

