from django.shortcuts import render, redirect
from .models import Uezu_seminar
import datetime
import qrcode
import xlsxwriter
from django.core.signing import TimestampSigner,BadSignature,SignatureExpired
from django.views import View
import random
import string
from datetime import timedelta

# 処理速度計測用
import time

# 出席入力機能

def success(request):
    return render(request, 'attendance/success.html')

def attend(request):
    now_login_student_id = request.user.student_id
    day_of_attendance = datetime.date.today()
    if request.method == 'POST':
        data = Uezu_seminar(student_id=now_login_student_id, attended_day=day_of_attendance)
        data.save()
        return redirect('attendance:success')
    else:
        return render(request, 'attendance/attend_btn.html')


# 時間制限付URL作成（QRコード化まで）
EXPIRED_SECONDS = 30

class For_attendView(View):
    template_name = 'attendance/for_attend.html'
    timestamp_signer = TimestampSigner()

    def get_random_chars(self,char_num=30):
         return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(char_num)])

    def get(self,request,token=None):
        context = {}
        context['expired_seconds'] = EXPIRED_SECONDS

        if token:
            try:
                # 有効なトークン
                unsigned_token = self.timestamp_signer.unsign(
                    token,
                    max_age=timedelta(seconds=EXPIRED_SECONDS)
                )
                return redirect('attendance:attend')
            except SignatureExpired:
                context['message'] = 'このURLは期限切れです。'
            except BadSignature:
                context['message'] = 'URLが正しくありません。もう一度お試しください。'
            return render(request, 'attendance/failure.html', context)

        return render(request, self.template_name, context)


    def post(self,request):
        context = {}
        context['expired_seconds'] = EXPIRED_SECONDS
        token = self.get_random_chars()
        token_signed = self.timestamp_signer.sign(token)
        context['token_signed'] = token_signed
        token_qrcode = 'http://localhost:8000/attendance/test/' + token_signed
        context['token_qrcode'] = token_qrcode
        qr_img = qrcode.make(token_qrcode)
        qr_img.save('static/qrcodes/qrcode.png')

        return render(request, self.template_name, context)


# 出席出力機能

def output_to_excel(request):
    start = time.time()
    db_data = Uezu_seminar.objects.all()
    set_day = set([i.attended_day for i in db_data])
    set_id = set([j.student_id for j in db_data])
    sorted_day = sorted(set_day)
    sorted_id = sorted(set_id)
    lists = [[j,[1 if Uezu_seminar.objects.filter(student_id=j, attended_day=i) else 0 for i in sorted_day]] for j in sorted_id]
    book = xlsxwriter.Workbook('excel/Uezu_seminar.xlsx')
    sheet = book.add_worksheet('NewSheet1')
    c = 1
    for i in sorted_day:
        j = i.strftime('%m/%d')
        sheet.write(0, c, j)
        c += 1
    row = 1
    for list in lists:
        days = list[1]
        column = 0
        sheet.write(row, column, list[0])
        for day in days:
            column += 1
            sheet.write(row, column, day)
        row += 1
    book.close()
    end = time.time()
    kekka = str(end-start)

    return render(request, 'attendance/output_to_excel.html', {'lists': lists, 'kekka': kekka})
