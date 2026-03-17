from django.db import models

class HeartUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # hashed ONLY
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.username



class Writing(models.Model):

    user = models.ForeignKey(HeartUser, on_delete=models.CASCADE)

    tool = models.CharField(max_length=50)
    icon = models.CharField(max_length=5)

    nameInput = models.TextField()
    descInput = models.TextField()
    depthInput = models.CharField(max_length=20)

    output = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    