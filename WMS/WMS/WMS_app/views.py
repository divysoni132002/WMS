from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from fuzzywuzzy import fuzz
import json

from .models import Task, TechLog, Vendor, DependencyResolution, EmailLog

def login(request):
    print('login called')
    return render(request, 'login.html')

def counter(request):
    print('counter called')
    return render(request, 'counter.html')

def work_management(request):
    print('work management called')
    username = request.session.get('username')
    print(f'username is {username}')
    
    if username:
        hours_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
        vendors = Vendor.objects.all()  # Fetch all vendors from the database
        context = {
            'username': username,
            'hours_list': hours_list,
            'vendors': vendors
        }
        return render(request, 'work_management.html', context)
    else:
        # User is not authenticated
        return redirect('login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        
        try:
            vendor = Vendor.objects.get(username=username)
            if password == vendor.password:
                # Authentication successful
                request.session['username'] = username
                print(username)
                return redirect('work_management')
            else:
                # Authentication failed
                error_message = 'Invalid password.'
        except Vendor.DoesNotExist:
            # Authentication failed
            error_message = 'Invalid username.'
        
        return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

@csrf_exempt
def submit_task(request):
    if request.method == 'POST':
        username = request.session.get('username')
        if username:
            # Calculate the number of task rows based on the task input names
            num_rows = sum(1 for key in request.POST.keys() if key.startswith('task-'))
            
            for i in range(num_rows):
                date = request.POST.get(f'date-{i}')
                time = request.POST.get(f'time-{i}')
                task = request.POST.get(f'task-{i}')
                hours = float(request.POST.get(f'hours-{i}', 0))
                status = request.POST.get(f'status-{i}')
                dependency = request.POST.get(f'dependency-{i}')
                communication_of_change = request.POST.get(f'communicative-changes-{i}')
                
                # Create a new Task object for each row
                Task.objects.create(
                    username=username,
                    date=date,
                    time=time,
                    task=task,
                    hours=hours,
                    status=status,
                    dependency=dependency,
                    communication_of_change=communication_of_change,
                    submission_time=timezone.now()
                )

                if communication_of_change and communication_of_change.strip() != 'None':                    
                    change_type = communication_of_change
                    tech_log = TechLog(
                        username=username,
                        date=date,
                        time=time,
                        change_type=communication_of_change
                    )
                    tech_log.save()

                    subject = f"Communicative Change: {communication_of_change}"
                    message = f"{username} has logged a change that may need your attention.\n\nChange Type: {change_type}\nTask Details: {task}\n\nPlease review the task details for more information or contact {username}."

                    if communication_of_change in ["Payload change by frontend", "Look UI change"]:
                        recipient_list = list(Vendor.objects.filter(username__in=["Darwin", "Rohit", "Vaishnawi"]).values_list('email', flat=True))
                    elif communication_of_change in ["Request param change", "Logic change in API", "Response change from backend", "Endpoint name change", "Table structure change", "Table data change"]:
                        recipient_list = list(Vendor.objects.filter(username__in=["Rohit","Sourabh", "Raj", "Nancy_ad", "Pandi_web", "Anant", "Bala"]).values_list('email', flat=True))
                    else:
                        recipient_list = list(Vendor.objects.filter(username__in=["Sourabh","Sandhya", "Bala", "Rohit"]).values_list('email', flat=True))

                    try:
                        send_mail(subject, message, 'cosmicwisdomyt@gmail.com', recipient_list)
                    except (BadHeaderError, Exception) as e:
                        return HttpResponse(f'An error occurred while sending the email: {str(e)}')

            total_hours = sum(float(request.POST.get(f'hours-{i}', 0)) for i in range(num_rows))
            print(f'total hours are {total_hours}')

            if total_hours < 8:
                subject = f"Less than 8 hours input by {username}"
                message = f"{username} has logged total work that is less than 8 hours for the {date}."
                vendor_email = Vendor.objects.filter(username=username).values_list('email', flat=True).first()
                recipient_list = ["rohit@unboxai.in"]
                if vendor_email:
                    recipient_list.append(vendor_email)
                
                try:
                    send_mail(subject, message, 'cosmicwisdomyt@gmail.com', recipient_list)
                except (BadHeaderError, Exception) as e:
                    return HttpResponse(f'An error occurred while sending the email: {str(e)}')

            # Check if any task has a status of "Stuck because of dependency"
            has_stuck_tasks = Task.objects.filter(username=username, status="Stuck because of dependency").exists()
            
            return redirect('stuck_tasks' if has_stuck_tasks else 'task_success')
        else:
            return redirect('login')
    
    return render(request, 'submit_task.html')

def task_success(request):
    return render(request, 'task_success.html')

def stuck_tasks(request):
    username = request.session.get('username')
    if username:
        stuck_tasks = Task.objects.filter(status='Stuck because of dependency')
        context = {
            'username': username,
            'stuck_tasks': stuck_tasks
        }
        return render(request, 'stuck_tasks.html', context)
    else:
        return redirect('login')

def resolve_dependency(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)        
        username = request.session.get('username')

        if task.status == 'Stuck because of dependency':
            task.status = 'Dependency Resolved'
            task.save()
            
            DependencyResolution.objects.create(
                task=task,
                resolved_by=username,
                resolved_date=timezone.now()
            )
        
        return redirect('stuck_tasks')
    else:
        return redirect('stuck_tasks')

@csrf_exempt
def send_email_view(request):
    if request.method == 'POST':
        current_datetime = timezone.now()
        date = current_datetime.strftime("%Y-%m-%d")
        time = current_datetime.strftime("%H:%M:%S")
        
        json_data = json.loads(request.body)
        event = json_data.get('event')
        user_id = json_data.get('user_id')
        username = json_data.get('username')
        phone = json_data.get('phone')

        # Configure email subject and message based on event
        if event == 'User registered':
            subject = f'New User Registration - {user_id}'
            message = f'A new user with user id {user_id} and username {username} has registered on the platform on {date} at {time}.'
        else:
            return HttpResponse('Invalid event')

        # Save email log
        email_log = EmailLog(
            event=event,
            subject=subject,
            message=message,
            email_status='Not sent yet',
            phone=phone,
            user_id=user_id,
            username=username
        )
        email_log.save()

        # Send email
        recipient_list = ['rohit@unboxai.in']
        try:
            send_mail(subject, message, 'cosmicwisdomyt@gmail.com', recipient_list)
            email_log.email_status = 'Sent'
            email_log.save()
            return HttpResponse('Email sent successfully')
        except (BadHeaderError, Exception) as e:
            email_log.email_status = 'Not Sent'
            email_log.save()
            return HttpResponse(f'An error occurred while sending the email: {str(e)}')

    return HttpResponse('Invalid request method')

@csrf_exempt
def email_confirmation(request):
    print('API Called for email confirmation.')
    if request.method == 'POST':
        data = json.loads(request.body)
        to_mailaddress = data.get('to_mailaddress')
        subject = data.get('subject')
        message = data.get('message')
        otp = data.get('otp')
        
        if to_mailaddress and subject and message:
            try:
                email_message = f"{message}\n\nOTP: {otp}"
                send_mail(subject, email_message, 'cosmicwisdomyt@gmail.com', [to_mailaddress])
                return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def check_vendor_entries(request):
    print('Automatic cron-based API called to check vendor work.')
    today = timezone.now().date()
    day_of_week = today.strftime('%A')
    exempt_vendors = ["Bala", "Rohit", "Aazeema", "Tanzeela"]

    if day_of_week == "Sunday":
        return HttpResponse("Today is Sunday. No emails need to be sent.")

    all_vendors = Vendor.objects.all()
    
    for vendor in all_vendors:
        if vendor.username in exempt_vendors:
            continue
        
        if not Task.objects.filter(username=vendor.username, submission_time__date=today).exists():
            subject = f"{vendor.username} Looks like you forgot to update your work for yesterday on {today}."
            message = "It looks like you forgot to fill up the web app today. Please ensure that it is updated. Please ignore if this has been sent by mistake."
            recipient_list = [vendor.email, "rohit@unboxai.in", "srconsultant@unboxai.in"]
            
            try:
                send_mail(subject, message, 'cosmicwisdomyt@gmail.com', recipient_list)
            except Exception as e:
                print(f"An error occurred while sending the email: {str(e)}")
    
    return HttpResponse("Vendor entry check completed.")