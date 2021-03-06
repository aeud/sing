from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.http import Http404, HttpResponse
from apps.jobs.models import Job, JobRequest
from apps.dashboards.models import Dashboard
from apps.accounts.models import User, Account
from apps.schedules.models import Schedule
from apps.anonymous.models import SharedDashboard, SharedVisualization
from premailer import transform

def index(request):
    query = """
select
    i::date date,
    count(distinct j.id) jobs,
    count(distinct r.id) job_requests,
    count(distinct e.id) exports,
    count(distinct er.id) export_requests
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i
    left join pilot.jobs_job j on (date(i) = date(j.completed_at))
    left join pilot.jobs_jobrequest r on (j.id = r.job_id)
    left join pilot.jobs_jobexport e on (j.id = e.job_id)
    left join pilot.jobs_jobexportrequest er on (e.id = er.export_id)
group by i
order by i asc;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    jobs = cursor.fetchall()
    query = """
select
    i::date date,
    sum(case when v.is_active is not null then 1 else 0 end) new_visualizations
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i left join pilot.visualizations_visualization v on (date(i) = date(v.created_at))
group by i
order by i asc;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    visualizations = cursor.fetchall()
    query = """
select
    u.email email,
    count(distinct jr.id) requests
from
    pilot.accounts_user u
    left join pilot.jobs_jobrequest jr on u.id = jr.created_by_id
where date(jr.created_at) = CURRENT_DATE - INTERVAL '1 day'
group by 1
order by 2 desc
limit 10;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    yesterday_top_users = cursor.fetchall()
    query = """
select
    u.email email,
    count(distinct jr.id) requests
from
    pilot.accounts_user u
    left join pilot.jobs_jobrequest jr on u.id = jr.created_by_id
where date(jr.created_at) = CURRENT_DATE
group by 1
order by 2 desc
limit 10;
        """
    cursor = connection.cursor()
    cursor.execute(query)
    today_top_users = cursor.fetchall()
    return render(request, 'admin/index.html', dict(jobs=jobs,
                                                    visualizations=visualizations,
                                                    yesterday_top_users=yesterday_top_users,
                                                    today_top_users=today_top_users))

def users(request):
    users = User.objects.all().annotate(requests_count=Count('jobrequest__id', distinct=True)).order_by('email')
    return render(request, 'admin/users/index.html', dict(users=users))

def user_show(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    query = """
select
    i::date date,
    count(distinct r.id) job_requests
from
    generate_series(
        CURRENT_DATE - '1 month'::interval + '1 day'::interval, CURRENT_DATE, '1 day'::interval
    ) i
    left join pilot.jobs_jobrequest r on (date(i), %s) = (date(r.created_at), r.created_by_id)
group by i
order by i asc;
        """
    cursor = connection.cursor()
    cursor.execute(query, [user.id])
    last_requests = cursor.fetchall()
    best_dashboards = Dashboard.objects.values('name', 'id', 'slug').filter(dashboardrequest__created_by=user).annotate(requests_count=Count('dashboardrequest__id', distinct=True)).order_by('-requests_count')[:10]
    starred_dashboards = Dashboard.objects.filter(star_users=user).order_by('name')
    accounts = Account.objects.all()
    return render(request, 'admin/users/show.html', dict(user=user,
                                                         last_requests=last_requests,
                                                         best_dashboards=best_dashboards,
                                                         starred_dashboards=starred_dashboards,
                                                         accounts=accounts))

def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'admin/users/edit.html', dict(user=user))

def user_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.can_schedule = request.POST.get('can_schedule', 'no') == 'yes'
    user.can_invite = request.POST.get('can_invite', 'no') == 'yes'
    user.can_share = request.POST.get('can_share', 'no') == 'yes'
    if user != request.user:
        user.is_admin = request.POST.get('is_admin', 'no') == 'yes'
    user.is_staff = request.POST.get('is_staff', 'no') == 'yes'
    user.save()
    return redirect(user_show, user_id=user.id)

def user_change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'admin/users/change-password.html', dict(user=user))

def user_change_password_post(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.set_password(request.POST.get('password'))
    user.save()
    return redirect(users)

def user_quick_update_account(request, user_id, account_id):
    user = get_object_or_404(User, pk=user_id)
    account = get_object_or_404(Account, pk=account_id)
    user.account = account
    user.save()
    return redirect(user_show, user_id=user.id)

def user_quick_remove_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.account = None
    user.save()
    return redirect(user_show, user_id=user.id)

def user_remove(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return redirect(user_show, user_id=user.id)

def user_active(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    return redirect(user_show, user_id=user.id)

def user_make_staff(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = True
    user.save()
    return redirect(user_show, user_id=user.id)

def user_remove_staff(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = False
    user.save()
    return redirect(user_show, user_id=user.id)

def user_make_admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_admin = True
    user.save()
    return redirect(user_show, user_id=user.id)

def user_remove_admin(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_admin = False
    user.save()
    return redirect(user_show, user_id=user.id)

def user_send_invitation(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    subject = 'Welcome to a colorful world!'
    body = transform(loader.render_to_string('emails/invite.html', dict(user=user)))
    email_message = EmailMultiAlternatives(subject, body, 'Master Yoda <colors@luxola.com>', [user.email])
    html_email = transform(loader.render_to_string('emails/invite.html', dict(user=user, me=request.user)))
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
    return redirect(user_show, user_id=user.id)

def auth_invite(request, user_id):
    user = get_object_or_404(User, pk=user_id, account=request.user.account)
    user.can_invite = True
    user.save()
    return redirect(users)

def unauth_invite(request, user_id):
    user = get_object_or_404(User, pk=user_id, account=request.user.account)
    user.can_invite = False
    user.save()
    return redirect(users)

def last_jobs(request):
    last_jobs = Job.objects.values('id', 'created_by__email', 'completed_at', 'query__visualization__name').all().order_by('-completed_at')[:20]
    last_job_requests = JobRequest.objects.values('id', 'created_by__email', 'created_at', 'job__query__visualization__name').all().order_by('-created_at')[:20]
    return render(request, 'admin/last-jobs.html', dict(last_jobs=last_jobs,
                                                        last_job_requests=last_job_requests,))

def schedules(request):
    schedules = Schedule.objects.filter(is_active=True).order_by('visualization__name')
    return render(request, 'admin/schedules.html', dict(schedules=schedules))

def schedule_remove(request, schedule_id):
    schedule = get_object_or_404(Schedule, pk=schedule_id)
    schedule.is_active = False
    schedule.save()
    return HttpResponse(schedule.id, 'application.json')

def shared_links(request):
    shared_dashboards = SharedDashboard.objects.filter(is_active=True)
    return render(request, 'admin/shared_links.html', dict(shared_dashboards=shared_dashboards))

def shared_dashboard_remove(request, shared_dashboard_id):
    shared_dashboard = get_object_or_404(SharedDashboard, pk=shared_dashboard_id)
    shared_dashboard.is_active = False
    shared_dashboard.save()
    return HttpResponse(shared_dashboard.id, 'application.json')



    