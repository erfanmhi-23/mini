```

1.ثبت کابر:
url:http://127.0.0.1:8000/api/users/register/
body requirements:username, email, password
post method
---
2.دریافت jwt:
url:http://127.0.0.1:8000/api/users/token/
body requirements:username, password
post method
---
3.ایجاد اشتراک:
url:http://127.0.0.1:8000/api/users/subscription/
body requirements:user id , plan
post method
---
4.ایجاد ادمین :
python manage.py createsuperuser
---
5.ایجاد ویدیو یا token ادمین:
url:http://127.0.0.1:8000/api/videos/create/
body requirements:title, description, file_url , duration, active
"file_url": "https://example.com/video.mp4"
post method
---
6.دیدن لیست ویدیو:
url:http://127.0.0.1:8000/api/videos/
body requirements:{}
get method
---
7.ثبت تماشا:
url:http://127.0.0.1:8000/api/history/create/
body requirements:user, video, progress
post method
---
8.مشاهده تاریخچه تماشا:
url:http://127.0.0.1:8000/api/history/my/
body requirements:{}
get method
---
9.ثبت کامنت :
url:http://127.0.0.1:8000/api/interactions/comment/
body requirements:user, video, content
post method
---
10.دیدن کامنت های ویدیو :
url:http://127.0.0.1:8000/api/interactions/comment/(videoid)/
body requirements:{}
get method
---
11.ثبت امتیاز:
url:http://127.0.0.1:8000/api/interactions/rating/
body requirements:user, video, score
post method
---
12.ثبت پرداخت :
url:http://127.0.0.1:8000/api/payments/create/
body requirements:user, subscription= pk = 1,2,3,4
post method
---
13.لیست پرداخت:
url:http://127.0.0.1:8000/api/payments/my/
body requirements:{}
get method
---
14.وب سوکت:
daphne -p 8080 video_subscription.asgi:application
url:ws://127.0.0.1:8080/ws/videos/(videoid)/
---

15.وضعیت اشتراک
url:http://127.0.0.1:8000/api/users/subscription/status/

---
16.تمدید اشتراک
http://127.0.0.1:8000/api/users/subscription/renew/
---
17.کنسل کردن اشتراک
http://127.0.0.1:8000/api/users/subscription/cancel/


```
