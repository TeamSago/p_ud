from django.db import models

# Create your models here.
# verbose_name은 라벨이라고 생각하면 된다.
class User(models.Model):
    user_id = models.CharField(max_length=32, unique=True, verbose_name="User ID")
    user_pw = models.CharField(max_length=128, verbose_name="user password")
    user_name = models.CharField(max_length=16, unique=True, verbose_name="User Name")
    user_email = models.CharField(
        max_length=128, unique=True, verbose_name="User Email"
    )
    user_register_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name="Account Created Datetime"
    )

    # 생성된 객체의 이름을 저장하는 메서드로, str타입을 리턴한다.
    # 이것이 없으면, User 클래스로 생성된 object를 불러왔을 때 User object (1), User object (2)와 같은 이름으로 표시된다.
    # user_name을 리턴하도록 등록했으니, object를 불러로면 object의 user_name 값이 표시된다.₩
    def __str__(self):
        return self.user_name

    # class Meta는 DB의 테이블 명을 지정해주는 옵션이다.
    # db_table은 테이블명, verbose_name은 테이블의 닉네임, verbose_name_plural은 등록하지 않으면 users처럼 복수형으로 표시될 때가 있으니 verbose_name과 동일하게 설정.
    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "user"
