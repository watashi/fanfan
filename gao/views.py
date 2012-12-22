# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from gao.models import Account, Good, Record
from decimal import Decimal
from datetime import datetime, timedelta

def index(request):
    return render_to_response('index.html', {
                              'good_list': Good.objects.all(),
                              }, context_instance=RequestContext(request))

def list(request, good_name):
    good = get_object_or_404(Good, name=good_name)
    return render_to_response('list.html', {
                              'good': good,
                              'account_list': good.account_set.all(),
                              }, context_instance=RequestContext(request))

def register(request):
    logout(request)
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    if len(password) > 0 and password == password2:
        try:
            user = User(username=username)
            user.set_password(password)
            user.save()
            account = Account(name=username)
            account.save()
            # Record(account_from=Account.objects.get(name='god'), account_to=account, amount=128, comment=u'魔法少女启动资金').save()
            return HttpResponse('<font color="green">注册成功！</font><br/><a href="/">回到首页</a>')
        except:
            pass
    return HttpResponse('<font color="red">注册失败！</font><br/><a href="/">回到首页</a>')

def login_(request):
    username = request.POST['username']
    password = request.POST['password']
    auth = authenticate(username=username, password=password)
    if auth is not None:
        login(request, auth)
        return HttpResponseRedirect('/pia/fanfan/gao/profile/')
    else:
        return HttpResponse('<font color="red">用户名或密码错误！</font><br/><a href="/">回到首页</a>')

def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def profile(request):
    user = request.user
    account = get_object_or_404(Account, name=user.username)
    balance = account.balance()
    good_list = []
    for good in Good.objects.all():
        good_list.append((good, len(account.good_set.filter(id=good.id)) > 0))
    return render_to_response('profile.html', {
                              'account': account,
                              'balance': balance,
                              'good_list': good_list,
                              'receive_list': account.receive_records.all(),
                              'send_list': account.send_records.all(),
                              }, context_instance=RequestContext(request))

@login_required
def book(request):
    user = request.user
    account = get_object_or_404(Account, name=user.username)
    good = get_object_or_404(Good, name=request.POST['good'])
    if account.good_set.filter(id=good.id):
        return HttpResponse('<font color="red">你已经订购，不能重复订购！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    elif datetime.now() > good.deadline:
        return HttpResponse('<font color="red">订购时间已过，订购在截至时间后（当天10点）关闭！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
#    elif account.balance() < good.price:
#        return HttpResponse('<font color="red">余额不足，订购失败！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    else:
        account.good_set.add(good)
        r = Record(account_from=account,
                   account_to=Account.objects.get(name='admin'),
                   amount=good.price,
                   comment=('book: %s' % good))
        r.save()
    return HttpResponseRedirect('/pia/fanfan/gao/profile/')

@login_required
def unbook(request):
    user = request.user
    account = get_object_or_404(Account, name=user.username)
    good = get_object_or_404(Good, name=request.POST['good'])
    if not account.good_set.filter(id=good.id):
        return HttpResponse('<font color="red">你尚未订购，不能退订！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    elif datetime.now() > good.deadline - timedelta(0, 3600, 0):
        return HttpResponse('<font color="red">退订时间已过，退订在截止时间前1小时（当天9点）关闭！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    else:
        account.good_set.remove(good)
        r = Record(account_from=Account.objects.get(name='admin'),
                   account_to=account,
                   amount=good.price,
                   comment=('unbook: %s' % good))
        r.save()
    return HttpResponseRedirect('/pia/fanfan/gao/profile/')

@login_required
def transfer(request):
    if not request.user.check_password(request.POST['password']):
        return HttpResponse('<font color="red">密码验证失败，此行为已被记录！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    account_from = request.user.username
    account_to = request.POST['to']
    amount = request.POST['amount']
    comment = request.POST['comment']
    if not Account.objects.filter(name=account_to):
        return HttpResponse('<font color="red">用户不存在！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    if account_from == account_to:
        return HttpResponse('<font color="red">不能自己转给自己！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    account_from = get_object_or_404(Account, name=account_from)
    account_to = get_object_or_404(Account, name=account_to)
    try:
        amount = Decimal(amount)
    except:
        return HttpResponse('<font color="red">金额格式错误！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    if amount < 0.01:
        return HttpResponse('<font color="red">金额必须为正数！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    if account_from.balance() < amount:
        return HttpResponse('<font color="red">余额不足，转账失败！</font><br/><a href="/pia/fanfan/gao/profile/">返回控制面板</a>')
    Record(account_from=account_from, account_to=account_to, amount=amount, comment=comment).save()
    return HttpResponseRedirect('/pia/fanfan/gao/profile/')

