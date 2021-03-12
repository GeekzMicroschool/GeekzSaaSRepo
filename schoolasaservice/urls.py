from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

#from  Geekz_Microschool import settings
urlpatterns = [
    path('apply', views.apply, name="apply"),
    path('saasapplication', views.saasapplication, name="saasapplication"),
    path('audition', views.audition, name="audition"),
    path('saasaudition', views.saasaudition, name="saasaudition"),
    path("student_profileEdit",views.student_profileEdit,name="sp"),
    path('schedule_admin', views.schedule_admin, name="schedule_admin"),
    path('profiling', views.profiling, name="profiling"),
    path('saasappointment',views.saasappointment,name="saasappointment"),
    path('ajax/load_slots/', views.load_slots, name='ajax_load_slots'), # AJAX
    path('web_form',views.web_form,name='web_form'),
    path('rough',views.rough,name="rough"),
    path('webpage_creation',views.webpage_creation,name='webpage_creation'),
    path('webpage',views.webpage,name='webpage'),
    path('microschool/<LOCALITY>',views.webpage, name='webpage'),
    path('deletevent',views.deletevent,name="delete"),
    path('superAdmin_dashboard',views.superAdmin_dashboard,name="superAdmin_dashboard"),
    path('individualAdmin_dashboard',views.individualAdmin_dashboard,name="individualAdmin_dashboard"),
    path('bs-basic-table',views.basictables,name="bs-basic-table"),
    path('bs-basicApprovel',views.individualAdmin_approvels,name="individualAdmin_approvels"),
    path('inquiryApprove/<uid>',views.inquiryApprove,name="inquiryApprove"),
    path('invoice',views.GeneratePdf,name="generatepdf"),
    path('create_pdf',views.create_pdf,name="create_pdf"),
    path('index1',views.index1,name="index1"),
    path('geekzmicro',views.school_template,name="geekzmicro"),
    path('web1',views.web1,name="web1"),
    path('rough2',views.rough2,name="rough2"),
    path('IndividualFeedetails',views.IndividualFeedetails,name="IndividualFeedetails"),
    path('bulk_load',views.bulk_load,name="bulk_load"),
    #path('drag_load',views.drag_load,name="drag_load"),
    path('clear',views.clear_database,name="clear"),
    path('affliateslist',views.affliateslist,name="affliateslist"),
    path('affliates_List',views.affliates_List,name="affliates_List"),
    path('notify',views.notify,name="notify"),
    path('affliates_form',views.affliates_form,name="affliatesform"),
    path('feedback_form',views.feedback_form,name="feedback_users"),
    path('student_apply/<SCHOOL_NAME>',views.student_apply,name="student_apply"),
    path('student_profiling',views.student_profiling,name="student_profiling"),
    path('studentdeletevent',views.studentdeletevent,name="studentdeletevent"),
    path('individualAdminSlots',views.individualAdminSlots,name="individualAdminSlots"),
    path('ajax/individual_load_slots/', views.individual_load_slots, name='ajax_individual_load_slots'), # AJAX
    path('invoicees',views.invoice,name="invoice"),
    #path('invoice_pdf/<student_id>',views.invoice_pdf,name="invoice_pdf"),
    path('Invoice_requests',views.Invoice_requests,name="invoice_requests"),
    path('bs-basicInvoice',views.bsbasicInvoice,name="bs-basicInvoice"),
    path('transcriptsApprove',views.transcriptsApprove,name="transcriptsApprove"),
    #path('Transcript_PDF/<student_id>',views.Transcript_PDF,name="transcript_PDF"),
    path('transcripts_request',views.transcripts_request,name="transcripts_request"),
    path('newApplications',views.newApplications,name="newApplications"),
    path('IndividualApproveProfiling',views.IndividualApproveProfiling,name="IndividualApproveProfiling"),
    path('complete_profiling/<student_id>',views.complete_profiling,name="complete_profiling"),
    path('approve_profiling/<student_id>',views.approve_profiling,name="approve_profiling"),
    path('reject_profiling/<student_id>',views.reject_profiling,name="reject_profiling"),
    path('studentedit_admin/<student_id>',views.studentedit_admin,name="studentedit_admin"),
    path('auditionApprove',views.auditionApprove,name="auditionApprove"),
    path('audition_accept/<uid>',views.audition_accept,name="audition_accept"),
    path('Affliatestracker',views.Affliatestracker,name="Affliatestracker"),
    path('Profiling_saas',views.Profiling_saas,name="Profiling_saas"),
    path('Profiling_accept/<uid>',views.Profiling_accept,name="Profiling_accept"),
    path('webpage_Approve',views.webpage_Approve,name="webpage_Approve"),
    path('viewbanners/<uid>',views.viewbanners,name="viewbanners"),
    path('adminprofileEdit/<uid>',views.adminprofileEdit,name="adminprofileEdit"),
    path('individualAdminSlotsView',views.individualAdminSlotsView,name="individualAdminSlotsView"),
    path('edit_time_slot/<pk>',views.edit_time_slot,name="edit_time_slot"),
    path('superAdmin_slots',views.superAdmin_slots,name="superAdmin_slots"),
    path('SuperAdminSlotsView',views.SuperAdminSlotsView,name="SuperAdminSlotsView"),
    path('superedit_time_slot/<pk>',views.superedit_time_slot,name="superedit_time_slot"),
    path('feedetailsreview/<uid>',views.feedetailsreview,name="feedetailsreview"),
    path('feeSplit/<uid>',views.feeSplit,name="feeSplit"),
    path('INDIVIDUAL_WEBPAGESSApprove/<uid>',views.INDIVIDUAL_WEBPAGESSApprove,name="INDIVIDUAL_WEBPAGESSApprove"),
    path('INDIVIDUAL_WEBPAGESSReject/<uid>',views.INDIVIDUAL_WEBPAGESSReject,name="INDIVIDUAL_WEBPAGESSReject"),
    path('addAcademicYear',views.addAcademicYear,name="addAcademicYear"),
    path('studentApplications',views.studentApplicationsview,name="studentApplicationsview"),
    #path('enrolledStudents/<student_id>',views.enrolledStudents,name="enrolledStudents"),
    path('studentsdata',views.studentsdata,name="studentsdata"),
    path('feepayTerm1/<student_id>',views.feepayTerm1,name="feepayTerm1"),
    path('feepayTerm2/<student_id>',views.feepayTerm2,name="feepayTerm2"),
    path('feepayTerm3/<student_id>',views.feepayTerm3,name="feepayTerm3"),
    path('Removestudent/<student_id>',views.Removestudent,name="Removestudent"),
    path('individualstudent',views.individualstudent,name="individualstudent"),
    path('IndividualAlumni',views.IndividualAlumni,name="IndividualAlumni"),
    path('notifyUsers',views.notifyUsers,name="notifyUsers"),
    path('superAdminAlumni',views.superAdminAlumni,name="superAdminAlumni"),
    path('newenrollments',views.newenrollments,name="newenrollments"),
    path('enrollment/<student_id>',views.enrollment,name="enrollment"),
    path('WebpageTracker',views.WebpageTracker,name="WebpageTracker"),
    path('studentDashboard',views.studentDashboard,name="studentDashboard"),
    path('studentfeestatus',views.studentfeestatus,name="studentfeestatus"),
    path('invoice_pdf',views.invoice_pdf,name="invoice_pdf"),
    path('studentinvoice_pdf/<student_id>',views.studentinvoice_pdf,name="studentinvoice_pdf"),
    #path('newenrollments',views.newenrollments,name="newenrollments"),
    path('Transcript_pdf',views.Transcript_pdf,name="Transcript_pdf"),
    path('studentTranscript_pdf/<student_id>',views.studentTranscript_pdf,name="studentTranscript_PDF"),
    path('studentprofileEdit/<student_id>',views.studentprofileEdit,name="studentprofileEdit"),
    path('invoiceConfig',views.invoiceConfig,name="invoiceConfig"),
    path('Enableinvoice/<school>',views.Enableinvoice,name="Enableinvoice"),
    path('Disableinvoice/<school>',views.Disableinvoice,name="Disableinvoice"),
    path('duedatesADD',views.duedatesADD,name="duedatesADD"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
