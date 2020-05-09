from django.db import models

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'uploaded_imgs_for_recognition' + '/' + filename

def user_directory_path1(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.user.id, filename)
    return 'class_of_predicted_images' + '/' + '{0}/{1}'.format(instance.p_name,filename)

class Recognize_Image(models.Model):
	img = models.FileField(upload_to=user_directory_path)

	def __str__(self):
		return f'{self.id}_'+'img'

class Predicted_Class(models.Model):
	img_predicted = models.FileField(upload_to = user_directory_path1)
	p_name = models.CharField(max_length=20,null=False,blank=False)

	def __str__(self):
		return f' {self.p_name}_{self.id}' + 'img'

