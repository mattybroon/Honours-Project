from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import ContextMixin
from .models import Module, Student, StudentMark


class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = 'modules/module_home.html'
    context_object_name = 'modules'


class ModuleDetailView(LoginRequiredMixin, DetailView, ContextMixin):
    context_object_name = 'module-details'
    template_name = 'modules/module_detail.html'
    queryset = Module.objects.all()

    def post(self, request, *args, **kwargs):
        module_code = self.kwargs.get('pk')
        year = request.POST.get('year')
        return HttpResponseRedirect(reverse('results-home', kwargs={'module_code': module_code, 'year': year}))


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    fields = ['module_code', 'module_name', 'module_coordinator', 'semester', 'occurrence', 'module_credits', 'module_SCQF', 'number_of_checkpoints', 'checkpoint_weight', 'assignment_mark_total', 'assignment_weight', 'exam_mark_total', 'exam_weight']


class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    fields = ['module_code', 'module_name', 'module_coordinator', 'semester', 'occurrence', 'module_credits', 'module_SCQF', 'number_of_checkpoints', 'checkpoint_weight', 'assignment_mark_total', 'assignment_weight', 'exam_mark_total', 'exam_weight']


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'modules/student_home.html'
    context_object_name = 'students'


class StudentDetailView(LoginRequiredMixin, DetailView, ContextMixin):
    context_object_name = 'student-details'
    template_name = 'modules/student_detail.html'
    queryset = Student.objects.all()


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    fields = ['student_ID', 'student_forename', 'student_surname']


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    fields = ['student_ID', 'student_forename', 'student_surname']


class StudentMarkListView(LoginRequiredMixin, ListView):
    model = StudentMark
    template_name = 'modules/results_home.html'
    context_object_name = 'marks'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentMarkListView, self).get_context_data(**kwargs)
        context['module_code'] = self.kwargs.get('module_code')
        context['year'] = self.kwargs.get('year')
        context['marks'] = StudentMark.objects.filter(module_code=context['module_code'], year=context['year'])
        return context


class StudentMarkDetailView(LoginRequiredMixin, DetailView, ContextMixin):
    context_object_name = 'marks'
    template_name = 'modules/results_detail.html'
    queryset = StudentMark.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentMarkDetailView, self).get_context_data(**kwargs)
        context['module_code'] = self.kwargs.get('module_code')
        context['year'] = self.kwargs.get('year')
        context['student_id'] = self.kwargs.get('student_id')
        context['pk'] = self.kwargs.get('pk')
        context['marks'] = StudentMark.objects.filter(module_code=context['module_code'], year=context['year'], student_ID=context['student_id'])
        return context


class StudentMarkCreateView(LoginRequiredMixin, CreateView):
    model = StudentMark
    template_name = 'modules/results_form.html'
    fields = ['student_ID', 'checkpoints_complete', 'assignment_mark_results', 'exam_mark_results', 'comment']

    def form_valid(self, form):
        form.instance.module_code = Module.objects.get(module_code=self.kwargs.get('module_code'))
        form.instance.year = self.kwargs.get('year')
        return super().form_valid(form)


class StudentMarkUpdateView(LoginRequiredMixin, UpdateView):
    model = StudentMark
    template_name = 'modules/results_form.html'
    fields = ['checkpoints_complete', 'assignment_mark_results', 'exam_mark_results', 'comment']

    def form_valid(self, form):
        form.instance.module_code = Module.objects.get(module_code=self.kwargs.get('module_code'))
        form.instance.year = self.kwargs.get('year')
        form.instance.student_ID = Student.objects.get(student_ID=self.kwargs.get('student_id'))
        return super().form_valid(form)


class StudentMarkDeleteView(LoginRequiredMixin, DeleteView, ContextMixin):
    context_object_name = 'marks'
    template_name = 'modules/results_confirm_delete.html'
    queryset = StudentMark.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentMarkDeleteView, self).get_context_data(**kwargs)
        context['module_code'] = self.kwargs.get('module_code')
        context['year'] = self.kwargs.get('year')
        context['student_id'] = self.kwargs.get('student_id')
        context['pk'] = self.kwargs.get('pk')
        context['marks'] = StudentMark.objects.filter(module_code=context['module_code'], year=context['year'], student_ID=context['student_id'])
        return context

    def get_success_url(self):
        return reverse('results-home', kwargs={'module_code': self.kwargs.get('module_code'), 'year': self.kwargs.get('year')})