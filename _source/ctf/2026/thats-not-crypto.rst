.. meta::
   :description: راهنمای حل چالش مهندسی معکوس that's-not-crypto از مسابقات justCTF.
   :keywords: ctf, reversing, python, pyc, uncompyle6, writeup

that's-not-crypto
========================================================================

سناریوی چالش
------------------------------------------------------------------------

در یکی از روزهای کاری توسعه دهندگان دیتائیست، یک فایل مرموز با پسوند ``.pyc`` به دست تیم رسیده است. فرستنده ناشناس ادعا می‌کند که این فایل حاوی یک سیستم احراز هویت است که از محاسبات پیچیده ریاضی برای بررسی پرچم (Flag) استفاده می‌کند. تیم تحلیل امنیت متوجه شده که فایل اصلی کد منبع در دسترس نیست و تنها بایت‌کد کامپایل شده آن باقی مانده است. ماموریت شما این است که با مهندسی معکوس این فایل، منطق بررسی پرچم را کشف کنید. آیا می‌توانید پرچم مخفی شده در لایه‌های پنهان این محاسبات را استخراج کنید؟

دریافت فایل چالش: شما می‌توانید فایل مورد نیاز برای حل این سناریو را از لینک زیر دانلود کنید:
   :download:`دانلود فایل checker.pyc <Original-Files/checker.7z>`

.. note::

   هشدار امنیتی: پیش از اجرای هرگونه فایل مشکوک، حتماً آن را با آنتی‌ویروس اسکن کنید. برای این منظور می‌توانید از ابزار ClamAV استفاده کنید.

   **نصب ClamAV (در لینوکس):**

   .. code-block:: bash

      sudo apt update
      sudo apt install clamav

   **استفاده از ClamAV برای اسکن فایل:**

   .. code-block:: bash

      clamscan -r file_name
حل چالش (Write-up)
------------------------------------------------------------------------

گام اول: دیکامپایل کردن
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

از آنجایی که فایل یک بایت‌کد پایتون است، اولین قدم استفاده از ابزار ``uncompyle6`` برای بازگرداندن آن به کد قابل فهم پایتون است:

.. code-block:: bash

   uncompyle6 checker.pyc

خروجی دیکامپایل شده کدی شبیه به زیر است:

.. code-block:: python

   uncompyle6 checker.pyc 
   # uncompyle6 version 3.7.4
   # Python bytecode 3.6 (3379)
   # Decompiled from: Python 3.8.6 (default, Sep 25 2020, 09:36:53) 
   # [GCC 10.2.0]
   # Embedded file name: checker.py
   # Compiled at: 2021-01-30 10:41:40
   # Size of source mod 2**32: 50109 bytes
   from random import randint

   def make_correct_array(s):
       from itertools import accumulate
       s = map(ord, s)
       s = accumulate(s)
       return [x * 69684751861829721459380039 for x in s]

   def validate(a, xs):
       def poly(a, x):
           value = 0
           for ai in a:
               value *= x
               value += ai
           return value

       if len(a) != len(xs) + 1:
           return False
       else:
           for x in xs:
               value = poly(a, x)
               if value != 24196561:
                   return False
       return True

   if __name__ == '__main__':
       a = [...]
       a = [ai * 4919 for ai in a]
       flag_str = input('flag: ').strip()
       flag = make_correct_array(flag_str)
       if validate(a, flag):
           print('Yes, this is the flag!')
           print(flag_str)
       else:
           print('Incorrect, sorry. :(')
   # okay decompiling checker.pyc

گام دوم: تحلیل منطق محاسباتی
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

با بررسی کد، متوجه می‌شویم که برنامه ورودی ما را دریافت کرده و پس از تبدیل کاراکترها به اعداد (ASCII) و عملیات تجمعی (Accumulate)، آن‌ها را در یک عدد بسیار بزرگ ضرب می‌کند. در نهایت، تابع ``validate`` با استفاده از یک تابع چندجمله‌ای، درستی آن را چک می‌کند.

گام سوم: استراتژی حل (Semi-Brute Force)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

با توجه به اینکه طول آرایه ``a`` برابر با ۵۸ است، متوجه می‌شویم طول پرچم باید ۵۷ کاراکتر باشد. از آنجایی که می‌دانیم فرمت پرچم با ``justCTF{`` شروع می‌شود، بهترین راه استفاده از یک اسکریپت پایتونی برای بروت‌فورس کاراکتر به کاراکتر است.

کد زیر برای یافتن کاراکترهای پرچم به کار گرفته شد:

.. code-block:: python

   from random import randint

   def make_correct_array(s):
       from itertools import accumulate
       s = map(ord, s)
       s = accumulate(s)
       return [x * 69684751861829721459380039 for x in s]

   def validate(a, xs):
       def poly(a, x):
           value = 0
           for ai in a:
               value *= x
               value += ai
           return value

       for x in xs:
           value = poly(a, x)
           if value != 24196561:
               return False
       return True

   if __name__ == '__main__':
       a = [...]
       a = [ai * 4919 for ai in a]

       flag_str = "justCTF{"

       while len(flag_str) < 57:
           i = 32
           while i < 127:
               print(flag_str + chr(i))
               flag = make_correct_array(flag_str + chr(i))
               if (validate(a, flag)):
                   print("correct:     " + chr(i))
                   flag_str += chr(i)
               i += 1

       print(flag_str)

نتیجه‌گیری
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

پس از اجرای اسکریپت و بررسی تمام حالات ممکن برای هر کاراکتر بر اساس معادله موجود، برنامه پرچم نهایی را استخراج کرد:

.. code-block:: text

   justCTF{this_is_very_simple_flag_afer_so_big_polynomails}

.. note::
   این چالش به خوبی نشان می‌دهد که حتی وقتی با معادلات پیچیده ریاضی مواجه هستید، ابزارهای مهندسی معکوس و منطق بروت‌فورس هوشمند می‌توانند به راحتی پرچم را آشکار کنند.
